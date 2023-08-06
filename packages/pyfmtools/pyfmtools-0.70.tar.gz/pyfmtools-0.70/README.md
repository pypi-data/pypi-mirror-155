# Pyfmtools    
Pyfmtools provides various tools for handling fuzzy measures, calculating various indices, Choquet and Sugeno integrals, as well as fitting fuzzy measures to empirical data. This package is designed for Python , but it also includes the C++ source files and a user manual.
Chapter 2 of the user manual provides some background on fuzzy measures. A more detailed overview can be found in [4, 5, 12, 16] and references therein. Chapter 3 of the user manual outlines computational methods used to fit fuzzy measures to empirical data. The description of the programming library pyfmtools is given in Chapter 4. Examples of its usage are provided in Section 4.6.
To cite pyfmtools package, use references [2–6,21–24]. 
### New in version 4
Random generation of fuzzy measures of different types, including k-additive, k-interactive, supermodular and submodular, sparse representation of k- additive fuzzy measures.<br>
### We added in version 3
We added the concept of K-interactive fuzzy measures, and 4 methods of fitting K-interactive fuzzy measures from data based on linear program- ming. K-interactive fuzzy measures significantly reduce the computational complexity. We also added fitting fuzzy measures in marginal contribution representation and using maximal chains method, which fits only the values directly identifiable from the data. This method is useful for small data sets.
Fitting fuzzy measures in marginal contribution representation allows simple sub and supermodularity constraints, which can now be enforced.
See functions fittingKinteractive, fittingKinteractiveAuto, fittingKinter- activeMC, fittingKinteractiveMarginal, fittingKinteractiveMarginalMC.
We added calculation of new non-additivity and bipartition interaction indices. See functions Bipartition, BipartitionBanzhaf, NonadditivityIndex, NonadditivityIndexMob.<br>
### We added in version 2
We added fitting K-maxitive and K-tolerant fuzzy measures, based on linear and mixed integer programming. See functions fittingktolerant and fittingK- maxitive.
We added a method for fitting sub-modular fuzzy measures reported in [3]. Supermodular fuzzy measure can also be fit by using duality: construct dual data set, fit a sub-modular fuzzy measure and then compute its dual. See function FuzzyMeasureFitLP.
We added an extra requirement of preservation of output ordering. See function FuzzyMeasureFitLP.
Fixed many warnings in the lpsolve code.<br>

## Documentation
[User Manual](http://gbfiles.epizy.com/pyfmtools.pdf)

## Installation
To install type:
```python
$ pip install pyfmtools
```
## Usage of the library 


## How to use the library with Python only
```python
import pyfmtools as pyfm
```
Follow these steps in your Python code to use the library:<br>
- Initialize resources<br>
- Use library function(s)<br>
- Free resources<br>
### Example how to initialize resources
```python
n=3<br>
env = pyfm.fm_init( n)<br>
```

### Example how to free resources
```python
pyfm.fm_free( env)<br>
```

### Usage of library functions
To implement a function follow these steps:
1. Initialize input arrays.
2. Initialize input parameters.
3. Call wrapper function.
4. Evaluate output parameters. 
### Example
```python
import pyfmtools as pyfm

n=3
env = pyfm.fm_init( n)

k = 2
Mob =[0.0,0.3,0.5,-0.2,0.4,0.1,-0.2,0.1]
pnm = pyfm.NonmodularityIndexMobkadditive(Mob, k, env)
print( "k: ", k)
print( "Mob: ", Mob)
print( "nonmodularity indices: ", pnm)

pyfm.fm_free( env)
```

### Parameters
#### Input parameters:
See input parameter list in user manual
#### Output parameters:
See output parameter list in user manual

### Test
To unit test type:
```python
$ test/test_wrapper.py
```


## How to use the library utilizing NumPy and CFFI
```python
from _pyfmtools import flib, lib
```
Follow these steps in your Python code to use the library:<br>
- Initialize resources<br>
- Use library function(s)<br>
- Free resources<br>
### Example how to initialize resources
```python
n=3
env=ffi.new( "struct fm_env *")
fm.py_fm_init( n, env)
```

### Example how to free resources
```python
fm.py_fm_free( env)<br>
```

### Usage of library functions
To implement a function follow these steps:
1. Initialise input parameters 
2. Initialise input arrays.
3. Covert input arrays to CFFI.
4. Initialise output arrays.
5. Covert output arrays to CFFI.
4. Call C function.
### Parameters
#### Input parameters:
See input parameter list in user manual
#### Output parameters:
See output parameter list in user manual
### Example
```python
import numpy as np
from  _pyfmtools import ffi,lib as fm

n=4
fm.py_fm_init(n,  env);

ti=1
v = np.zeros(env.m,float);
pv = ffi.cast("double *", v.ctypes.data);
vb = np.zeros(env.m,float);
pvb = ffi.cast("double *", vb.ctypes.data);
size = fm.py_generate_fm_2additive_concave(ti,n,pv)
print( "2-additive concave FM in Mobius and its length (n=4)")
print( v)
print( "has ", size, " nonzero parameters ")

fm.py_fm_free( env);
```


### Test
To unit test type:
```python
$ test/test_no_wrapper.py
```