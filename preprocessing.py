import os
import boto3
import xarray as xr
import subprocess
import numpy as np
from datetime import datetime, timedelta, date, time
from botocore.config import Config
from botocore import UNSIGNED
import argparse
import fnmatch
import pygrib
import cdsapi

class DataProcessor:
    def __init__(self, start_date, end_date, output_directory=None, download_directory=None, keep_downloaded_data=False):
        self.start_date = start_date
        self.end_date = end_date
        self.output_directory = output_directory
        self.download_directory = download_directory
        self.keep_downloaded_data = keep_downloaded_data
        self.output_gfs = None
        self.output_era5 = None
        
        # Specify the output directory where you want to save the files
        if self.output_directory is None:
            self.output_directory= os.getcwd()
        
        # Initialize the S3 client
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

        # Specify the S3 bucket name and root directory for GFS forecasts
        self.bucket_name = 'noaa-gfs-bdp-pds'
        self.root_directory = 'gfs'

        # Initialize the cdsapi client
        self.cds = cdsapi.Client()


    def gfs_process(self):



    def era5_process(self):




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process GFS and ERA5 data")
    parser.add_argument("start_date", help="Start date in the format 'YYYYMMDD'")
    parser.add_argument("end_date", help="End date in the format 'YYYYMMDD'")
    parser.add_argument("-o", "--output", help="Output directory for processed data")
    parser.add_argument("-d", "--download", help="Download directory for raw data")
    parser.add_argument("-k", "--keep", help="Keep downloaded data (optional)", action="store_true", default=False)
    parser.add_argument("-p", "--process", nargs="*", choices=["gfs", "era5"], help="Specify which process to run")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y%m%d")
    end_date = datetime.strptime(args.end_date, "%Y%m%d")
    output_directory = args.output
    download_directory = args.download
    keep_downloaded_data = args.keep

    data_processor = DataProcessor(start_date, end_date, output_directory, download_directory, keep_downloaded_data)      
    if not args.process or "gfs" in args.process:
        data_processor.gfs_process()
    if not args.process or "era5" in args.process:
        data_processor.era5_process()
