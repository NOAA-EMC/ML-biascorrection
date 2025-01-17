# Installing the BUFR decding software

### Get the code:
git clone https://github.com/NCAR/rda-bufr-decode-ADPsfc.git

### Load NCEP BUFRLIB software library, on Hera:

```bash
module use /scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.7.0/envs/gsi-addon-intel/install/modulefiles/Core
module load  bufr
```

Go to the `rda-bufr-decode-ADPsfc/install` directory. You will need to edit `LIB` in `install.sh`, on Hera it is:
```bash
LIB=/scratch1/NCEPDEV/nems/role.epic/spack-stack/spack-stack-1.7.0/envs/gsi-addon-intel/install/intel/2021.5.0/bufr-11.7.0-jz6icbx/lib64/libbufr_d.so
```
And set the `FC` and `CC` compilers. Then run the `install.sh` script. The executables will be created in the `../exe` directory.

### Dataset

The NCEP ADP Global Surface Observational Weather Data can be downloaded from `here <https://rda.ucar.edu/datasets/d461000/>`_

### Usage

```bash
./bufrsurface.x input_file output_file configuration_file
```

For example:
./bufrsurface.x gdas.adpsfc.t00z.20240101.bufr gdas.adpsfc.t00z.20240101.txt ../configs/bufrsurface.config


The bash script `bufr2ascii.sh` is for batch processing.  
