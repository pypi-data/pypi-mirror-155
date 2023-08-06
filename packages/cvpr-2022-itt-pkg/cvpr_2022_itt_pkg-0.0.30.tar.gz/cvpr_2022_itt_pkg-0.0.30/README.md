# CVPR 2022 Tutorial: Imaging Through Turbulence

This repo is a collection of demos and source code for a Python package aimed at
providing some programming-based insight into the CVPR 2022 Tutorial: Imaging Through
Turbulence.

The overall organization of this repo is as follows.

* `cvpr_2022_itt_pkg` contains the source for the package that we use to
    simplify the demos overall. Go here if you are interested in the source code.
    The code itself will not likely be informative outside of the case that you
    are interested in doing something like this yourself. But for the sake of
    completeness we provide it.
    This package can be installed with:
    ```bash
    pip install cvpr_2022_itt_pkg
    ```

* `part1_XXXXXXX.ipynb` will be the demos most relevant to the
    Fourier optics portion of the tutorial. Wave propagation, PSF formation, lenses,
    etc. can be found here.

* `part2_XXXXXXX.ipynb` will be the demos most relevant to the
    split-step portion of the tutorial. Phase screen generation and wave propagation 
    with phase screens are the main focuses here. 

    **Note**: We do not ''fully enable''
    the entire split-step pipeline. To our knowledge, the authors of any split-step
    approach have not actively posted their method publicly. Therefore, this is *our*
    implemenatation of what is outlined in Schmidt's book *Numerical Simulation of 
    Optical Wave Propagation* (see https://schmidtwaveopticsbook.org/). We specifically
    do this for a case of a *single* point source only.

* `part3_XXXXXXX.ipynb` will be the demos most relevant to the
    multi-aperture portion of the tutorial.

    **Note**: This is a simplified version of the ''version 1'' 
    multi-aperture simulation. More info about these simplifications can be
    found within the Python notebook. For later changes,
    integrations with the P2S network, and overall improved usability, see 
    https://github.itap.purdue.edu/StanleyChanGroup/TurbulenceSim_P2S.
    
* A personal note: You might be wondering, what's up with all the clutter? This is my first time using PyPI so I have no idea what I'm really doing, but this managed to make it all work. If it's not broken, don't fix it!


## Lab website and other info
* [Main i2Lab website](https://engineering.purdue.edu/ChanGroup/index.html)
* [i2Lab turbulence page](https://engineering.purdue.edu/ChanGroup/project_turbulence.html)
* [@StanleyChan](https://twitter.com/stanley_h_chan) 
    [@NickChimitt](https://twitter.com/NickChimitt) **Warning:** We don't really
    tweet that often!!!
