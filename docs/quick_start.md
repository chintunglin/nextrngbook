This section will guide you through the steps to install **NextRandom** and begin 
applying its functionality. If you're new to this package, follow the instructions 
below to get started smoothly.

## Installation

To install NextRandom, you can use the Python package manager `pip` 
in your terminal or command line interface:

```bash
pip install nextrandom

``` 

## Import the package

After installing NextRandom, you can start by importing the package into your 
Python script. You will need to import both NextRandom and NumPy. 
NextRandom is designed to work with the underlying uniform random number generator (RNG), 
while NumPy is used for higher-level operations such as generating random arrays, 
matrices, and distributions.

```python

from nextrandom.dx_generator import create_dx32
from numpy.random import Generator

``` 

## Create DX generators

NextRandom provides the `create_dx32` function to initialize a specific RNG 
from the DX generator family, which includes over 4,000 built-in RNGs. 
By calling this function, you can create an instance of a 32-bit uniform 
DX generator that can be used for further operations.

```python

>>> create_dx32()
_DXGenerator32(bb=32747, pp=4294966997, kk=2, ss=2, log10_period=19.299999237060547)

``` 

`create_dx32(dx32_id, seed)` takes two parameters:

- dx32_id: Selects a specific DX generator from the DX generator family (over 4000 options).
- seed: Sets the RNG state for reproducibility (optional).
This allows you to obtain a specific RNG with a controlled seed.


```python

>>> create_dx32(dx32_id=4000, seed=101)
_DXGenerator32(bb=1046381, pp=2147472413, kk=1301, ss=2, log10_period=12140.7998046875)

``` 

In short, `dx32_id` determines the specific DX generator, 
and `seed` ensures reproducibility.
For more details on potential issues with `dx32_id` values and reproducibility,
refer to the [Reference section](dx_generator.md).


## View DX generator info 

To obtain information about the created DX generator, you can print it out.

```python

dx32_rng = create_dx32(dx32_id=3999)
print(dx32_rng)

``` 

    DX-1301-2 generator
    Multiplier = 1073694173
    Modulus    = 2146412747
    The log₁₀(period) of the PRNG is 12140.6

## Use NumPy's Generator Class with DX generator

After creating a DX generator with create_dx32(), you can easily connect it to 
NumPy's `Generator` class.

```python

>>> dx32 = Generator(dx32_rng)
>>> dx32
Generator(_DXGenerator32) at ...

``` 

## Generate random numbers

Once you have connected the DX generator to NumPy's `Generator` class, 
you can begin generating random numbers. This step enables you to create 
random numbers based on your desired distribution or for various operations. 
To generate random numbers, simply call the appropriate method from 
the Generator class, such as `integers()`, `random()`, or others, 
depending on your specific needs. 
For more information about the available methods, you can consult the 
[NumPy documentation](https://numpy.org/doc/stable/reference/random/generator.html).
Here are some examples of generating random numbers using NumPy’s 
Generator with the DX generator.


```python

# sampling from distributions
print(dx32.normal(0, 1, 20)) # generate twenty N(0, 1) data
print(dx32.uniform(0, 1, 10)) # generate ten U(0, 1) data

# randomly choose
print(dx32.choice(["A", "B", "C", "D", "E"], size=30)) # choose ten elements with replacement

# randomly shuffle
sample_lst = ["A", "B", "C", "D", "E"]
dx32.shuffle(sample_lst)
print(sample_lst)

``` 

    [-0.00213944 -0.16430093  0.31275819  0.46733231 -1.66207846  1.46714534
     -0.26847522 -0.75476158  0.05660134  0.17005816 -1.23263801  1.05619617
      1.58009983  0.35782657 -0.39891161  0.89384609  0.80806737 -1.01287135
     -0.42067584 -0.89925814]
    [0.69362038 0.26363807 0.67196451 0.76542885 0.69339551 0.90578292
     0.32005051 0.60380831 0.01674061 0.94753803]
    ['B' 'E' 'B' 'B' 'D' 'A' 'A' 'A' 'D' 'D' 'C' 'E' 'E' 'B' 'B' 'A' 'D' 'A'
     'B' 'D' 'D' 'C' 'A' 'A' 'E' 'A' 'E' 'E' 'B' 'D']
    ['C', 'A', 'D', 'E', 'B']


## Parallel random number generation

To enable parallel computation, you can create multiple DX generators with 
different dx32_id values. This approach allows for the generation of several 
low-correlation generators, which can be utilized in parallel processes to 
minimize potential dependencies between random sequences.

```python

from nextrandom.dx_generator import create_dx32
from numpy.random import Generator

# Create multiple DX generators with different dx32_id values
generators = [Generator(create_dx32(dx32_id=i)) for i in range(4100, 4108)]

``` 


## Extend usage with other libraries

NumPy’s `Generator`, beyond basic random number generation, can be integrated 
with libraries such as SciPy for scientific computing and SymPy for symbolic 
mathematics. For more information, refer to their respective documentation.
