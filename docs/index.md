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
enhancing simulation accuracy and minimizing errors.    

- **Parallelizable**: To avoid potential confounding inference, 
it is recommended to use "different" RNGs for parallel computations. 
This package provides over **4,000 distinct DX generators**, 
allowing users to select different generators alongside different starting seeds 
for effective parallelization. 

- **Strong statistical properties**: 
The DX generator successfully passes **144 stringent empirical tests** 
in the TestU01 suite, ensuring high-quality randomness.

These properties make the DX generator an excellent choice for applications 
requiring reliable randomness. 
Future versions of **NextRNGBook** will expand the collection by incorporating 
additional RNGs from the book, 
providing a comprehensive suite of state-of-the-art random number generation techniques. 


## Background

This section provides an overview of the **DX generator**, 
focusing on its theoretical properties and mathematical expression. 
The DX generator are a class of **Multiple Recursive Generators (MRGs)** 
designed by Deng and Xu in 2003 to take advantage 
of the desirable theoretical properties of MRGs, 
such as long period lengths and equidistribution properties, 
while maximizing efficiency. 
They achieved this by limiting the number of nonzero coefficients and requiring 
that these coefficients share the same multiplier. 
Their major contribution was extending this idea to maximum-period MRGs of 
larger and larger orders. 
The result was the fast DX generator with both 
excellent theoretical and empirical properties.

### Multiple Recursive Generators

**Multiple Recursive Generators (MRGs)** compute a linear combination of 
the past \( k \) random numbers generated. 
The random numbers are generated sequentially 
using a \( k \)-th order linear recurrence:

$$
X_i = (a_1 X_{i-1} + a_2 X_{i-2} + \dots + a_k X_{i-k}) \mod p, \quad i \geq k \tag{1}
$$

The initial seeds \( X_0, \dots, X_{k-1} \) are integers in \( \mathbb{Z}_p \),
with the condition that not all of them are zero. 
The modulus \( p \) is a large prime number.

To obtain variates \( U_i \) between 0 and 1, 
the generated values \( X_i \) can be transformed using the formula:

\[
U_i = \frac{X_i}{p}
\]

However, to avoid the possibility of obtaining values exactly equal to 0 or 1, 
it is recommended to apply the following transformation instead:

\[
U_i = \frac{X_i + 0.5}{p}
\]


It is well known that the maximum period of the MRG in the recurrence relation (1) 
is \( p^k - 1 \), which is achieved if and only if its characteristic polynomial 

\[
f(x) = x^k - \alpha_1 x^{k-1} - \alpha_2 x^{k-2} - \cdots - \alpha_k 
\]


is a primitive polynomial.

### DX Generator

The **DX-k-s** class of generators improves the efficiency of the MRG 
by restricting the number of nonzero coefficients to \( s \) 
and requiring them all to have the same multiplier \( B \). 
Therefore, the \( k \)-th order linear recurrences for \( s = 1, 2 \) are:

When \( s = 1 \):

  $$
  X_i = (X_{i-1} + B X_{i-k}) \mod p, \quad i \geq k
  $$

When \( s = 2 \):

  $$
  X_i = B(X_{i-1} + X_{i-k}) \mod p, \quad i \geq k
  $$

- \( k \) is the order of the recurrence relation.
- \( s \) specifies the recurrence structure.
- \( B \) is the multiplier.
- \( p \) is the prime modulus.

### Advantages of DX Generator

The **DX generator** offers several key advantages, 
making it an ideal choice for applications that require reliable randomness.

- **Long period length**  

    The **period length** refers to the number of iterations 
    (or random numbers generated) before the sequence of numbers repeats itself. 
    Every RNG will eventually enter a cycle and start producing the same sequence 
    of numbers again after a certain number of steps. 
    A longer period length means that the sequence takes more iterations before repeating, 
    making it more suitable for applications that require generating 
    a large number of random numbers without encountering repetitions. 
    The period length of the DX generator is \( p^k - 1 \). 
    For instance, consider the parameters for the **DX-50873-2** generator:

    - \( k = 50,873 \)
    - \( s = 2 \)
    - \( B = 1,016,882 \)
    - \( p = 2,146,123,787 \)

    The period length for this configuration is approximately 
    \( \mathbf{2^{1,577,017}} \), which is significantly larger than 
    the period of NumPy's default RNG, 
    [`PCG64`](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html) 
    (with a period of \( 2^{128} \)), and 
    [`MT19937`](https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html) 
    (with a period of \( 2^{19,937} \)).    

- **High-dimensional equidistribution**  

    The DX generator ensures high-dimensional equidistribution up to \( k \) dimensions. 
    Specifically, every \( d \)-tuple (where \( 1 \leq d \leq k \)) of integers 
    between 0 and \( p-1 \) appears exactly \( p^{k-d} \) 
    times across the entire period \( p^k - 1 \), 
    except for the all-zero tuple, 
    which appears one less time, i.e., \( p^{k-d} - 1 \). 
    For example, the **DX-50873-2** generator exhibits equidistribution up to 
    **50,873** dimensions.
  
- **Favorable empirical test results**  

    The DX generator consistently passes all the empirical tests in **TestU01 BigCrush**, 
    even while popular RNGs like 
    [`MT19937`](https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html)
    could not.
  
- **Parallelizable**  

    The package offers over **4,000 distinct DX generators** with desirable properties, 
    allowing users to assign different generators to different threads 
    or processors for parallel simulations. 
    This approach is more effective than those used in 
    [NumPy](https://numpy.org/doc/stable/reference/random/parallel.html), 
    such as `jumped` or `spawn`, 
    where a single RNG with different starting seeds may lead to overlaps and high correlations. 
    Different combinations of \( B \), \( p \), \( k \), and \( s \) in the DX generator 
    effectively mitigate these issues, enabling better parallelization.


For more details on the DX generator, 
refer to [Chapter 3 of the RNG book](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3). 
**Section 3.1** discusses the advantage and challenge of large order MRGs, 
and **Section 3.2** provides an explanation of the DX generator. 
Parallelization of the DX generator was introduced in 
[Chapter 8](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_8), 
with the classical method covered in **Section 8.1** 
and the advantage of the proposed method in **Section 8.2.2**.

## NextRNGBook Expansion Plans

Beyond the **DX generator**, 
NextRNGBook is set to expand by including additional RNGs discussed 
in the book [[1]](#references), 
all of which will be available in both 32-bit and 64-bit versions:

- **DL Generator**
- **DS Generator**
- **DT Generator**
- **DW Generator**

The DX generator is a highly efficient MRG recognized 
for its speed and favorable statistical properties. 
However, it has two potential limitations: 
(1) poor initialization behavior, 
where a near-zero state may result in a prolonged sequence of zero values, 
and (2) suboptimal spectral test results in dimensions higher than \( k \). 
These limitations arise from the generator's design, 
which prioritizes efficiency by using a minimal number of non-zero terms 
in the recurrence equation.

To address these issues, 
the **DL**, **DS**, and **DT generators** 
were developed by incorporating additional non-zero terms into the recurrence relation. 
While the DL generator improves initialization behavior, 
its spectral performance in dimensions higher than \( k \) remains somewhat limited. 
The DS and DT generators enhance both initialization behavior 
and spectral properties, offering a more balanced and effective solution. 
Like the DX generator, all three maintain desirable statistical properties. 
For more details on these generators, 
refer to [Chapter 3 of the RNG book](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3), 
where **Section 3.2.5** provides the motivation behind the proposed efficient generators.

The **DW generator** 
was developed to tackle two significant challenges 
faced by MRGs with numerous non-zero terms: (1) computational inefficiency 
due to the large number of multiplications required, 
and (2) difficulties in parallelization, 
particularly with traditional methods such as "jump-ahead parallelization." 
The DW generator addresses these challenges by utilizing a 
Matrix Congruential Generator to efficiently implement 
maximum-period MRGs with a large number of non-zero terms. 
This approach ensures both strong statistical properties 
and efficient parallel execution, 
providing a practical solution for high-order MRGs with numerous non-zero terms.
For more details on the DW generator and its motivation, 
refer to **Section 3.3** of 
[Chapter 3](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3) 
and [Chapter 9](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_9) 
for a more detailed description.


## Learn More

- **[Quick Start](quick_start.md)** – Learn how to install and use NextRNGBook.
- **[API Reference](reference.md)** – API documentation.
- **[Explanation](team_and_contributor.md)** – Background, design principles, and team members. 
  *Under construction. Currently lists team members only.*


## References

[1] Deng, L.-Y., Kumar, N., Lu, H. H.-S., & Yang, C.-C. (2025). 
*Random Number Generators for Computer Simulation and Cyber Security:
 Design, Search, Theory, and Application* (1st ed.). Springer. 
 [https://doi.org/10.1007/978-3-031-76722-7](https://doi.org/10.1007/978-3-031-76722-7)