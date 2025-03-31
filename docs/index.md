# NextRNGBook: A Python Random Number Generation Package

## Introduction

The **NextRNGBook** package incorporates a variety of high-quality random number 
generators (RNGs) from 
*Random Number Generators for Computer Simulation and Cyber Security* [[1]](#references). 
Designed for seamless compatibility with **NumPy**, 
this Python package integrates easily into existing workflows, 
offering a selection of state-of-the-art random number generation techniques 
suitable for scientific computing, large-scale simulations, and cryptographic tasks.


## Background and Motivation

This section provides foundational information about RNGs 
and explains the motivation behind both the package and the proposed RNGs.

<!--
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
-->


### Random Number Generators

A general form of an RNG is defined as:

$$
X_i = f(X_{i-1}, X_{i-2}, \dots, X_{i-k}) \mod p, \quad i \geq k \tag{1}
$$

where \( f \) is a function of the most recent \( k \) integers, 
and \( X_{0}, X_{1}, \dots, X_{k-1} \) represent the initial seeds 
taken from \( \mathbb{Z}_p = \{0, 1, \dots, p-1\} \).

To obtain variates \( U_i \) between 0 and 1, 
the generated values \( X_i \) can be transformed using the formula:

$$
U_i = \frac{X_i}{p}
$$

However, to avoid the possibility of obtaining values exactly equal to 0 or 1, 
it is recommended to apply the following transformation instead:

$$
U_i = \frac{X_i + 0.5}{p}
$$


### Desirable Properties

An ideal RNG should meet the **HELP** properties, 
a set of fundamental properties introduced by Deng [[2]](#references)
, ensuring its reliability and suitability for various applications. 
These properties include:

- **H**igh-dimensional equidistribution: 
The RNG should generate uniformly distributed tuples across multiple dimensions, 
which reduces correlation artifacts and improves accuracy in high-dimensional simulations. 


- **E**fficiency: 
The RNG must be computationally efficient, 
producing high-quality random numbers with minimal time and resource consumption, 
crucial for large-scale simulations and real-time applications.

- **L**ong period length: 
The period length refers to the number of iterations 
(or random numbers generated) before the sequence repeats itself. 
Every RNG will eventually enter a cycle and start producing the same sequence 
of numbers again after a certain number of steps.
To avoid premature sequence repetition, 
the RNG should have an extensive period length, 
which is critical for large simulations and cryptographic applications.

- **P**ortability: 
The RNG should be adaptable across different computing environments 
and hardware architectures without compromising statistical properties 
or efficiency, ensuring consistency and reproducibility.


In addition to the HELP properties, 
a random number generator should demonstrate favorable **empirical performance**. 
It should pass empirical tests, such as those in **TestU01**, 
to verify its randomness and reliability.

Another important aspect is the **parallelizability** of the RNG. 
It should support parallel processing, 
enabling the generation of substreams that can be used concurrently 
without significant loss of quality or independence, 
which is critical for large-scale simulations.

Furthermore, the RNG should **ensure security** in cryptographic and 
security-critical applications. 
A secure RNG is designed to generate random numbers that are 
resistant to prediction, manipulation, or reverse engineering. 
These RNGs are essential for applications such as encryption, 
digital signatures, key generation, and other security protocols,
where the unpredictability of random numbers is crucial.


### Linear Congruential Generators

If \( f \) is a linear function with \( k = 1 \), 
the generator in Eq. (1) becomes a **Linear Congruential Generator (LCG)**. 
The sequence is given by:

$$
X_i = (B X_{i-1} + A) \mod p, \quad i \geq 1 \tag{2}
$$

where \( X_i \), \( A \), \( B \), and \( p \) are nonnegative integers, 
and \( X_0 \neq 0 \) is chosen from \( \mathbb{Z}_p \) as a seed. 
If \( A \neq 0 \), it is possible to achieve a full period of \( p \).

On the other hand, when \( A = 0 \), the sequence is described by:

$$
X_i = B X_{i-1} \mod p, \quad i \geq 1 \tag{3}
$$

where \( X_0 \neq 0 \). 
When \( p \) is a prime number and \( B \) is a primitive root modulo \( p \), 
the LCG in Eq. (3) has a period of \( p-1 \).

While LCGs gained popularity for their simplicity, 
efficiency, and well-established theoretical properties, 
they are now considered less ideal. 
This is primarily due to their relatively short periods by modern standards, 
as well as their inability to achieve equidistribution in dimensions greater than one. 
Furthermore, LCGs often show poor empirical performance, 
failing to meet the requirements of rigorous statistical tests.

[PCG64](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html) 
attempts to address this issue by using a 128-bit LCG with \( p = 2^{128} \), 
combined with a special transformation. 
However, the use of 128 bits introduces portability challenges, 
as not all platforms support 128-bit unsigned integers. 
On the other hand, a natural extension of the LCGs that achieves good properties, 
does not require transformations, 
and does not rely on high-bit operations (therefore avoiding portability issues) 
will be introduced in the next subsection.



### Multiple Recursive Generators

The **Multiple Recursive Generator (MRG)**  is a natural extension of the LCG. 
The random numbers are generated sequentially 
using a \( k \)-th order linear recurrence:

$$
X_i = (\alpha_1 X_{i-1} + \alpha_2 X_{i-2} + \dots + \alpha_k X_{i-k}) \mod p, \quad i \geq k \tag{4}
$$

The initial seeds \( X_0, \dots, X_{k-1} \) are integers in \( \mathbb{Z}_p \),
with the condition that not all of them are zero. 
The modulus \( p \) is a large prime number.

It is well known that the maximum period of the MRG in the recurrence relation (4) 
is \( p^k - 1 \), which is achieved if and only if its characteristic polynomial 

$$
f(x) = x^k - \alpha_1 x^{k-1} - \alpha_2 x^{k-2} - \cdots - \alpha_k 
$$


is a primitive polynomial. 
A maximal period MRG also demonstrates equidistribution in spaces up to 
$k$ dimension and shows favorable performance in empirical tests. 
Therefore, a large-order MRG provides improved empirical performance, 
longer periods, and better uniformity across higher dimensions, 
all without the need for additional transformations. 
When \( p \) is 32-bit, there are no portability issues, 
making the RNG more adaptable to different platforms without relying on high-bit operations.
However, when the order \( k \) increases, 
two challenges arise: efficiency issues due to the numerous multiplications involved, 
and the difficulty of finding the right parameters to achieve the maximum period length.
The **DX Generator** was proposed to address these issues.


### DX Generators

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

where 
\( k \) represents the order of the recurrence relation, 
\( s \) specifies the recurrence structure, 
\( B \) is the multiplier, 
and \( p \) is the prime modulus.

The generators are efficient, as they require only a single multiplication and addition. 
Additionally, Deng [[3]](#references) proposed an efficient search algorithm called GMP 
for finding maximal period MRGs of large order. 
With the Algorithm GMP, the maximum period parameters for DX generators can be identified, 
achieving a period length of \( p^k - 1 \), 
\( k \)-dimensional equidistribution, 
and favorable empirical test results.

Deng [[3]](#references) also proposed a method for constructing maximum-period MRGs 
from a single DX generator. 
Using this method, multiple distinct maximal-period MRGs 
can be found and then assigned to different threads or processors for parallel simulations. 
This approach is more effective than traditional methods, 
such as "jump-ahead parallelization."


For more details on the DX generators, 
refer to [Chapter 3](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3)
of the RNG book [[1]](#references). 
**Section 3.1** discusses the advantage and challenge of large order MRGs, 
and **Section 3.2** provides an explanation of the DX generator. 
Parallelization of the DX generator was introduced in 
[Chapter 8](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_8), 
with the classical method covered in **Section 8.1** 
and the advantage of the proposed method in **Section 8.2.2**.


### DL/DS/DT/DW Generators

The **DX generator** is a highly efficient MRG recognized 
for its speed and favorable statistical properties. 
However, it has two potential limitations: 
(a) poor initialization behavior, 
where a near-zero state may result in a prolonged sequence of zero values, 
and (b) suboptimal spectral test results in dimensions higher than \( k \). 
These limitations arise from the generator's design, 
which prioritizes efficiency by using a minimal number of non-zero terms 
in the recurrence equation (4).

To address these issues while ensuring efficiency, 
the **DL**, **DS**, and **DT generators** 
were developed by incorporating additional non-zero terms in the recurrence relation (4). 
While the DL generator improves initialization behavior, 
its spectral performance in dimensions higher than \( k \) remains somewhat limited. 
The DS and DT generators enhance both initialization behavior 
and spectral properties, offering a more balanced and effective solution. 
Like the DX generator, all three maintain desirable statistical properties. 
For more details on these generators, 
refer to [Chapter 3](https://link.springer.com/chapter/10.1007/978-3-031-76722-7_3)
of the RNG book [[1]](#references), 
where **Section 3.2.5** provides the motivation behind the efficient generators.

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

### Security Consideration

In cryptographic and security-critical applications, 
the RNG should **ensure security**. 
While classical linear generators, such as MRGs, 
exhibit excellent statistical properties and are suitable for statistical simulations, 
they are not appropriate for use as secure RNGs.
Therefore, many secure random number generators 
have been developed to address these security concerns. 
For more details, refer to **Part IV** of the RNG book [[1]](#references).


## Current Features of NextRNGBook

In its current version, the package features the **32-bit DX generator** and 
provides parallelization capabilities. 
Specifically, the package offers over **4,000 distinct DX generators** 
with desirable properties, allowing users to assign different generators to different threads 
or processors for parallel simulations. This approach is more effective than those used in 
[NumPy](https://numpy.org/doc/stable/reference/random/parallel.html), 
such as `jumped` or `spawn`, 
where a single RNG with different starting seeds may lead to overlaps and high correlations. 
Different combinations of \( B \), \( p \), \( k \), and \( s \) in the DX generator 
effectively mitigate these issues, enabling better parallelization.

## NextRNGBook Expansion Plans

NextRNGBook will include the **64-bit DX generator** 
and is set to expand with additional RNGs discussed in the book [[1]](#references).

The package will feature RNGs for **statistical simulations**, 
available in both 32-bit and 64-bit versions, including:

- **DL Generator**
- **DS Generator**
- **DT Generator**
- **DW Generator**

In addition, **secure RNGs** will be introduced, 
designed for cryptographic and security-critical applications, such as:

- **SAFE**
- **eRC**
- **eHC**
- **eChaCha**
- **eRabbit**


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
 
[2] Deng, L.-Y. (2005). 
*Efficient and portable multiple recursive generators of large order*. 
ACM Transactions on Modeling and Computer Simulation, 15(1), 1–13. 
[https://doi.org/10.1145/1044322.1044323](https://doi.org/10.1145/1044322.1044323)

[3] Deng, L. Y. (2004). 
*Generalized Mersenne prime number and its application to random number generation*. 
In Monte Carlo and Quasi-Monte Carlo Methods 2002: 
Proceedings of a Conference held at the National University of Singapore, 
Republic of Singapore, November 25–28, 2002 (pp. 167-180). Springer Berlin Heidelberg.
[https://doi.org/10.1007/978-3-642-18743-8_9](https://doi.org/10.1007/978-3-642-18743-8_9)
