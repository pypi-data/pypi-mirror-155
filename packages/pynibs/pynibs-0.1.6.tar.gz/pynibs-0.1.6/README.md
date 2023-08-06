# pyNIBS
Preprocessing, postprocessing, and analyses routines for non-invasive brain stimulation experiments.

[![Latest Release](https://gitlab.gwdg.de/tms-localization/pynibs/-/badges/release.svg)](https://gitlab.gwdg.de/tms-localization/pynibs/-/releases)   

`pyNIBS` provides the necessary tools to allow **cortical mappings** with transcranial magnetic stimulation (TMS) via **functional analysis**. `pyNIBS` is developed to work with [SimNIBS](http://www.simnibs.org), i.e. SimNIBS' meshes and FEM results can directly be used.


See the [documentation](https://pynibs.readthedocs.io/en/latest/) for package details and our [protocol](https://protocolexchange.researchsquare.com/article/pex-1780/v1) publication for an extensive example of the usage.

## Installation
Via pip:

``` bash
pip install pynibs
```

Or clone the source repository and install via `setup.py`:

``` bash
git clone https://gitlab.gwdg.de/tms-localization/pynibs
cd pynibs
python setup.py develop
```

To import CED Signal EMG data use the `export to .mat` feature of Signal. 
To read .cfs files exported with CED Signal you might need to manually compile the libbiosig package:

``` bash
cd pynibs/pckg/biosig
tar -xvf biosig4c++-1.9.5.src_fixed.tar.gz
cd biosig4c++-1.9.5
./configure
make
cd python
python setup.py install
```

Finally, add `~/.local/lib` to your `.bashrc`:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib
```




## Bugs
Yes. Drop us a line if you find any or feel free to file a PR.


## Citation
Please cite _Numssen, O., Zier, A. L., Thielscher, A., Hartwigsen, G., Knösche, T. R., & Weise, K. (2021). Efficient high-resolution TMS mapping of the human motor cortex by nonlinear regression. NeuroImage, 245, 118654. doi:[10.1016/j.neuroimage.2021.118654](https://doi.org/10.1016/j.neuroimage.2021.118654)_ when using this toolbox in your research.


## References
  - Weise, K., Numssen, O., Thielscher, A., Hartwigsen, G., & Knösche, T. R. (2020). A novel approach to localize cortical TMS effects. Neuroimage, 209, 116486. doi: [10.1016/j.neuroimage.2019.116486](https://doi.org/10.1016/j.neuroimage.2019.116486)
  - Numssen, O., Zier, A. L., Thielscher, A., Hartwigsen, G., Knösche, T. R., & Weise, K. (2021). Efficient high-resolution TMS mapping of the human motor cortex by nonlinear regression. NeuroImage, 245, 118654. doi:[10.1016/j.neuroimage.2021.118654](https://doi.org/10.1016/j.neuroimage.2021.118654)
  - Weise, K., Numssen, O., Kalloch, B., Zier, A. L., Thielscher, A., Hartwigsen, G., Knösche, T. R. (2022). Precise transcranial magnetic stimulation motor-mapping. Nature Protocols. (accepted) 
