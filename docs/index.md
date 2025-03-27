# NextRNGBook: A Python Random Number Generation Package

## Introduction

The **NextRNGBook** package aims to incorporate a variety of high-quality 
random number generators (RNGs) documented in 
*Random Number Generators for Computer Simulation and Cyber Security* [[1]](#references). 
The Python package is **NumPy-compatible**
, making it easy to integrate into existing workflows.

In its current version, the package features the **DX generator**, 
which offers several key advantages:


- **Long period length**: 
Prevents early repetition and is crucial for large-scale simulations.    

- **High-dimensional equidistribution**: 
Ensures that random samples are uniformly distributed across multiple dimensions, 
enhancing simulation accuracy, minimizing errors, and supporting parallel execution.    

- **Parallelizable**: To avoid potential confounding inference, 
it is recommended to use "different" RNGs for parallel computations. 
This package provides over **4,000 distinct DX generators**, 
allowing users to select different generators alongside different starting seeds 
for effective parallelization. 

- **Strong statistical properties**: 
The DX generator successfully passes **110 stringent empirical tests** 
in the TestU01 suite, ensuring high-quality randomness.

These properties make the DX generator an excellent choice for applications 
requiring reliable randomness. 
Future versions of **NextRNGBook** will expand the collection by incorporating 
additional RNGs from the book, 
providing a comprehensive suite of state-of-the-art random number generation techniques. 
For example, the DL, DS, DT, and DW generators will be included. 
For more details on these generators, including the DX generator, 
refer to [Chapter 3 of the RNG book](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3). 
For the motivation behind the proposed generators, 
refer to Sections 3.2 and 3.3. 
[Chapter 9](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_9) 
provides a more detailed description of the DW generator.
Additionally, for information on parallelization, please refer to 
[Chapter 8](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_8).

## Learn More

- **[Quick Start](quick_start.md)** – Learn how to install and use NextRNGBook.
- **[API Reference](reference.md)** – API documentation.
- **[Explanation](team_and_contributor.md)** – Background and design principles. 
*Under construction. Currently, it lists the team members.*


## References

[1] Deng, L.-Y., Kumar, N., Lu, H. H.-S., & Yang, C.-C. (2025). 
*Random Number Generators for Computer Simulation and Cyber Security:
 Design, Search, Theory, and Application* (1st ed.). Springer. 
 [https://doi.org/10.1007/978-3-031-76722-7](https://doi.org/10.1007/978-3-031-76722-7)