# The MarINvaders Toolkit

The MarINvaders Toolkit is a Python 3 module to assess the native and alien (non-native) distribution of marine species.

It can be used to find the native and alien distribution of a given species or to get an overview of all alien and native species found in one [marine ecoregion](https://academic.oup.com/bioscience/article/57/7/573/238419). 

To do so, MarINvaders cross-references and harmonizes distribution maps from [several databases](https://marinvaders.gitlab.io/marinvaders/data_background/) to find all occurrences of a given species and to gather information on its native and alien status per location recording. 
You can find [the full documentation here.](https://marinvaders.gitlab.io/marinvaders/)


## Where to get it

The full source code and all required local data is available [at the MarINvaders GitLab repository.](https://gitlab.com/dlab-indecol/marinvaders).

MarINvaders is registered at PyPI and at conda-forge for installation within a conda environment.
To install use

    pip install MarINvaders --upgrade
    
    
and when using conda:

    conda install -c conda-forge MarINvaders

We recommend to install the package in a [virtual environment](https://docs.python.org/3/library/venv.html) or [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). See [here for further information (including how to make the environment discoverable in your JupyterLab.](https://marinvaders.gitlab.io/marinvaders/install/).


## Getting started in five lines

Install the package as explained above and start your preferred Python interpreter

Import the package

``` python
import marinvaders
```

Get the species AphiaID you are interested in from the [WoRMS - marine species database](https://www.marinespecies.org/index.php). Here we use * Amphibalanus amphitrite * (Darwin, 1854), aka the [striped barnacle](https://www.marinespecies.org/aphia.php?p=taxdetails&id=421137) which has the AphiaID 421137.

Now we can get the species data from this barnacle with

``` python
species_data = marinvaders.Species(aphia_id=421137)
```

and list all occurrences 

``` python
species_data.all_occurrences
```

as well as the alien distribution of the barnacle with

``` python
species_data.reported_as_alien
```

These can also be easily plotted with

``` python
species_data.plot()
```

In addition, MarINvaders includes API functions for analyzing all species within an ecoregion.

For a full overview of the capabilities see the [example/tutorial notebook](https://marinvaders.gitlab.io/marinvaders/marinvaders_tutorial/). 
This can also be run in the cloud through [Binder](https://mybinder.org/):

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/marinvaders%2Fmarinvaders/master?filepath=%2Fdocs%2Fmarinvaders_tutorial.ipynb)


## Citations

Releases of MarINvaders are deposited at [the Zenodo research repository](https://zenodo.org/) and can be cited by their DOI: 10.5281/zenodo.4621393

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4621393.svg)](https://doi.org/10.5281/zenodo.4621393)


## Communication, issues, bugs and enhancements

Please use the [issue tracker](https://gitlab.com/marinvaders/marinvaders/-/issues) for documenting bugs, proposing enhancements and all other communication related to marinvaders. 
See [the Contribution section of the docs](https://marinvaders.gitlab.io/marinvaders/contributing/) for further information on code contributions.
 

## License and data terms of use

This project is licensed under The [GNU GPL v3](LICENSE)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This license only applies to the source code, for the licenses of the data processed by the modules see

### Required data sources - terms of use:

- WoRMS/marinespecies: http://marinespecies.org/about.php#terms
- OBIS: https://obis.org/manual/policy/
- NatCon: https://www.conservationgateway.org/ConservationPractices/Marine/Pages/marineinvasives.aspx see https://www.conservationgateway.org/Pages/Terms-of-Use.aspx

### IUCN/optional data - terms of use

This data is not allowed to redistributed and most be downloaded manually. For more information [see the documentation](https://marinvaders.gitlab.io/marinvaders/iucn_data/)

- ICUN GISD: http://www.iucngisd.org/gisd/legal.php
- ICUN Red List: https://www.iucnredlist.org/terms/terms-of-use
