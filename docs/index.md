# NextRNGBook: A Python Random Number Generation Package

**NextRNGBook** is a Python package for high-quality random number generation (RNG), 
implementing the **DX generator**, as introduced in 
*Random Number Generators for Computer Simulation and Cyber Security* [[1]](#references). 
The package is **NumPy-compatible** 
[[NumPy random documentation]](https://numpy.org/doc/stable/reference/random/index.html)
, making it easy to integrate into existing workflows.

## DX Generator

The **DX generator** is designed with the following characteristics:    

- **Mathematical Expression**     

    The DX-k-s generator is defined by the parameters \( k, s, B, p \):  

    When \( s = 1 \), the equation is:
    
      $$
      X_i = (B X_{i-k} + X_{i-1}) \mod p, \quad i \geq k
      $$
    
    When \( s = 2 \), the equation is:
    
      $$
      X_i = B(X_{i-k} + X_{i-1}) \mod p, \quad i \geq k
      $$     
    
    - \( k \): Order of the recurrence relation.
    - \( s \): Recurrence structure.
    - \( B \): Multiplier.
    - \( p \): Prime modulus.


- **Long Period Length**  

    The period length of the DX generator is \( p^k - 1 \). 
    For example, consider the following parameters for **DX-50873-2**:

    - \( k = 50873 \)
    - \( s = 2 \)
    - \( B = 1016882 \)
    - \( p = 2146123787 \)

    The period length for this configuration is approximately \( \mathbf{2^{1577017}} \), 
    which is much larger than the period of NumPy's default RNG, 
    [`MT19937`](https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html)
    (with a period of \( 2^{19937} \)), 
    and [`PCG64`](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html) 
    (with a period of \( 2^{128} \)).



- **High-dimensional Equidistribution**  

    The DX generator has the property of equidistribution up to \( k \) dimensions, 
    ensuring uniformity across multiple dimensions.
    For example, the **DX-50873-2** generator exhibits equidistribution 
    up to **50873** dimensions.


  
- **Favorable Empirical Test Results**  
  
    DX generators are able to pass stringent empirical tests in **TestU01**.


- **Ability to Parallelize**  

    Our package provides over **4,000 DX generators** with desirable properties, 
    allowing users to assign different generators to different threads 
    for parallel simulations. This method is preferable to approaches used in 
    [NumPy](https://numpy.org/doc/stable/reference/random/parallel.html), 
    where a single RNG with different starting seeds (such as `jumped` or `spawn`) is used.
    In such cases, overlaps and high correlations between the sequences may occur. 
    In contrast, using different combinations of
    \( B \), \( p \), \( k \), and \( s \) in DX generators helps mitigate these issues.
    More details on this topic can be found in 
    [Chapter 8 of our RNG book](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_8).

  
Currently, the implementation supports 32-bit DX generators, 
with future plans to add 64-bit support.

## Future Work: Expanding NextRNGBook

Beyond the **DX generator**, we plan to expand **NextRNGBook** 
by including additional RNGs discussed in our book, 
all of which will be available in both 32-bit and 64-bit RNG versions:

- **DL Generator**
- **DS Generator**
- **DT Generator**
- **DW Generator**

The **DX generator** is an efficient Multiple Recursive Generator (MRG) known for its 
high speed and desirable statistical properties. However, it has two potential 
limitations: (1) poor initialization behavior, 
where a near-zero state may result in a long sequence of zero values, 
and (2) suboptimal spectral test results in dimensions higher than \( k \). 
These limitations stem from the generator's design, 
which prioritizes efficiency by using very few non-zero terms in the recurrence equation. 

To address these limitations, the **DL, DS, and DT generators** were developed by 
incorporating additional non-zero terms into the recurrence relation. 
While **DL generator** improves initialization behavior, 
its spectral performance remains somewhat limited. 
**DS and DT generators** further enhance both initialization behavior and spectral properties, 
offering a more balanced and effective solution. 
All three generators, like DX, maintain desirable statistical properties.

The **DW generator** was developed to address two key challenges posed 
by MRGs with numerous non-zero terms: 
(1) computational inefficiency due to the large number of multiplications required, 
and (2) difficulties in parallelization, particularly with traditional methods 
like "jump-ahead parallelization." 
The **DW generator** tackles these challenges by utilizing a Matrix Congruential Generator 
to efficiently implement maximum period MRGs with a large number of non-zero terms. 
This strategy ensures both strong desirable statistical properties 
and efficient parallel execution, offering a practical solution for high-order MRGs.


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