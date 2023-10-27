import torch
import torch.nn as nn
import netCDF4 as nc
import numpy as np
import os
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("mps")

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv3d(1, 64, kernel_size=(3,3,3), padding=(1,1,1)),
            nn.ReLU(True),
            #nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2))
        )
        
        # Bottleneck (no further reduction of dimensions)

        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose3d(64, 1, kernel_size=(3,3,3), padding=(1,1,1)),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# Create your autoencoder model
autoencoder = Autoencoder()
if torch.cuda.device_count() > 1:
    print("Using", torch.cuda.device_count(), "GPUs!")
    autoencoder = nn.DataParallel(autoencoder)


class NetCDFDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.file_list = [f for f in os.listdir(root_dir) if f.endswith('.nc')]

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        file_path = os.path.join(self.root_dir, self.file_list[idx])
        
        # Load NetCDF data
        dataset = nc.Dataset(file_path)
        data = dataset.variables['t2m'][:].astype(np.float32)  # Adjust 'data' to the variable name in your file
        dataset.close()
        
        # Reshape the data to (1, 50, 721, 1440)
        data = data.reshape(1, 50, 721, 1440)
        return torch.tensor(data)

# Define your data directories
gfs_biased_dir = 'GFS/'
era5_unbiased_dir = 'ERA5/'

batch_size = 1  # Adjust batch size as needed
shuffle = False
num_workers = 0  # Adjust the number of workers for data loading
seed = 42  # Your desired seed value
torch.manual_seed(seed)


# Create your autoencoder model
autoencoder = Autoencoder().to(device)

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(autoencoder.parameters(), lr=0.01)

# Create data loaders for GFS (biased) and ERA5 (unbiased) data
gfs_dataset = NetCDFDataset(root_dir=gfs_biased_dir)
era5_dataset = NetCDFDataset(root_dir=era5_unbiased_dir)

gfs_data_loader = DataLoader(gfs_dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
era5_data_loader = DataLoader(era5_dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)

# Training loop with tqdm
num_epochs = 10
for epoch in range(num_epochs):
    autoencoder.train()
    total_loss = 0.0
    
    # Wrap the DataLoader with tqdm for a progress bar
    for gfs_data, era5_data in tqdm(zip(gfs_data_loader, era5_data_loader), desc=f'Epoch [{epoch+1}/{num_epochs}]'):
        optimizer.zero_grad()
        outputs = autoencoder(gfs_data.to(device))
        loss = criterion(outputs, era5_data.to(device))
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    # Calculate and print the average loss for the epoch
    avg_loss = total_loss / len(gfs_data_loader)
    print(f'Epoch [{epoch+1}/{num_epochs}], Average Loss: {avg_loss:.4f}')

# Save the trained model
torch.save(autoencoder.module.state_dict() if isinstance(autoencoder, nn.DataParallel) else autoencoder.state_dict(), 'autoencoder_model.pth')

