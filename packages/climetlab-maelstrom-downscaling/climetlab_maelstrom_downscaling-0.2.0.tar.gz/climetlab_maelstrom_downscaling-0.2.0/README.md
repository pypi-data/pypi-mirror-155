
## maelstrom-downscaling-ap5

A <a href="https://climetlab.readthedocs.io">CliMetLab </a> dataset plugin for the dataset maelstrom-downscaling.


Features
--------

This README provides a brief description of how to get the maelstrom-downscaling-ap5 is provided.

## Datasets description

Within the <a href="https://maelstrom-eurohpc.eu/">MAELSTROM</a> project, two-tier datasets are provided. In scope of AP5 which targets a deep-learning (statistical) downscaling system, the tier-1 dataset serves as the starting point and is described in the following. Tier-2 will be published at a later stage and its detailed content is not concrete yet. In addition to more predictors, 
it will also include temporary coherent sequences of data to allow application of recurrent network architectures.

### Tier 1 dataset: 
The dataset contains 2m temperature and surface elevation obtained from the IFS HRES model at its initialization times 00 and 12 UTC between 2016 and 2020.
The data coverage is shrinked on monthly level to the summer half of the year (defined between April and September inclusively). 
Spatially, the data is limited to a domain covering Central Europe including complex topography with 128x96 grid points in zonal and meridional direction.
For convenience, the data has been remapped onto a regular spherical grid with a spacing (dx) of 0.1° for the input and output data.
<br><br>
While the output data constitutes the objective of the DL downscaling approach, namely the `t2m_tar`, and was directly obtained from the remapped IFS HRES analysis, 
the input data has undergone a preprocessing chain which aims to emulate a coarse-grained model similar to [1]:<br>
The first step comprises a conservative remapping onto a coarse grid with dx = 0.8°. This step effectively removes fine-grained information from 
the data. Second, the data is interpolated back (naively) onto the high resolved grid (with dx = 0.1°) via bi-linear interpolation. Note that this step does 
*not* recover the information loss from step 1. Finally, to obtain energetic consistency, all calculation have been performed using the dry static energy 
which is a pure function of the temperature and the elevation.<br><br>

The datset is thereby subdivided into subsets for training, valiadation and testing. The former comprises the data between 2016 and 2019,
while the two latters are made of monthly data from 2020. Note that the netCDF files are splitted in monthly files. 

### Tier 2 dataset
Details still under development.


## Using climetlab to access the data

The climetlab python package allows easy access to the data with a few lines of code. In the following example, 
the training subset is retrieved:
```
!pip install climetlab climetlab_maelstrom_downscaling
import climetlab as cml
ds = cml.load_dataset("maelstrom-downscaling", dataset="training")
ds.to_xarray()
```
However, also customized data retrieval is possible with the help of the `months`-keyword which allows parsing a list of months of interest.<br>
A tutorial is available in form of a <a href="https://git.ecmwf.int/projects/MLFET/repos/maelstrom-downscaling-ap5/browse/notebooks/demo_downscaling_dataset.ipynb">Jupyter Notebook</a>.
