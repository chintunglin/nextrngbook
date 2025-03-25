# NextRandom: Next-Generation Random Number Generators  

## Introduction

NextRandom is a random number generator (RNG) package that is compatible with NumPy. 
Its purpose is to introduce various ideas or systems for random number generation 
that are not available in other packages within NumPy's ecosystem, 
including NumPy and RandomGen. 

The first system offered is the parallelization of the DX generator. 
Instead of providing a single specific RNG and methods to spawn or jump from it,
NextRandom offers a family of DX generators. This allows users to utilize 
multi-threading or multi-processing with different RNGs. Each specific DX generator
operates at the same level as a specific RNG in NumPy, such as MT19937 or PCG64.

In the initial version of NextRandom, 
over 4,000 distinct DX generators are available for users to apply.

## Documentation overview

1. [Quick Start](quick_start.md) -
A quick guide to get you started with basic installation and usage.
2. [Reference](dx_generator.md) - 
Detailed reference for functions, classes, and modules in the package.
3. [Explanation (Under Construction)](team_and_contributor.md) - 
This section will provide in-depth explanations about the background, 
objectives, and theory behind the package. Currently, it lists the team members.


## DX generator references

For more information about DX generators and related resources, 
refer to the official 
[DX Random Number Generators](http://web0.cs.memphis.edu/~dengl/dx-rng/) website, 
which includes relevant papers and additional details.


