# **disops**: a Python library for Orthogonal Polinomial Sequences of a Discrete Variable

## Installation
For installing **disops** from [Pypi](https://pypi.org/project/disops/) run:
```
pip install disops
```

## Usage

### Constructors
**disops** provides four public classes: `Charlier`, `Meixner`, `Krawtchouk` and `Hahn`. All four are child classes of the abstract class `OrthogonalPolynomialsGenerator`, that you should not instantiate.

The constructors headers are as follows.

#### Charlier
```python
Charlier(mu, x=sympy.Symbol('x'))
```
Attributes:
- `mu`: a positive `float` or a `sympy.Symbol`
- `x`: a `sympy.Symbol` (optional)

Returns: a Charlier polynomials generator of variable `x` and parameter `mu`.

#### Meixner
```python
Meixner(beta, c, x=sympy.Symbol('x'))
```
Attributes:
- `beta`: a positive `float` or a `sympy.Symbol`
- `c`: a `float` in ]0,1[ or a `sympy.Symbol`
- `x`: a `sympy.Symbol` (optional)

Returns: a Meixner polynomials generator of variable `x` and parameters `beta` and `c`.


#### Krawtchouk
```python
Krawtchouk(N, p, x=sympy.Symbol('x'))
```
Attributes:
- `N`: a positive `int`
- `p`: a `float` in ]0,1[ or a `sympy.Symbol`
- `x`: a `sympy.Symbol` (optional)

Returns: a Krawtchouk polynomials generator of variable `x`, size `N` and parameter `p`.

#### Hahn
```python
Hahn(N, alpha, beta, x=sympy.Symbol('x'))
```
Attributes:
- `N`: a positive `int`
- `alpha`: a `float` greater than or equal to `-1` or a `sympy.Symbol`
- `beta`: a `float` greater than or equal to `-1` or a `sympy.Symbol`
- `x`: a `sympy.Symbol` (optional)

Returns: a Hahn polynomials generator of variable `x`, size `N` and parameters `alpha` and `beta`.

### Methods
All four classes have the following public methods:
___
```python
clear()
````
Remove generator cache.

___

```python
gen_poly(n)
```
Generate the polynomial of degree n.

Args:
- `n` (`int`): degree of generated polynomial

Returns: a `sympy.Poly`

___

```python
sgen_poly(n)
```
Generate the polynomial of degree n safely.

Args:
- `n` (`int`): degree of generated polynomial

Returns: a `sympy.Poly`
____

```python
gen_ops(n)
```
Generate the Orthogonal Polynomials Sequence

Args:
- `n` (`int`): maximum degree of generated polynomials

Returns: a `list` of `sympy.Poly`
___

```python
sgen_ops(n)
```
Generate the Orthogonal Polynomials Sequence safely

Args:
- `n` (`int`): maximum degree of generated polynomials

Returns: a `list` of `sympy.Poly`

Note: This method uses only the explicit formula instead of recurrence formula and could be slower.
___

```python
check(pol)
```
Check if a polynomial belongs to the orthogonal sequence.

Args:
- `pol` (`sympy.poly`): a polynomial

Returns: The degree of pol and  its leading coefficient if pol belongs to sequence, `(-1, 0)` otherwise.
___

```python
plot(degrees, xlim=(0, 10))
```
Plot the Charlier polynomials of given degrees

Args:
- `degrees` (`list` of `int`): degrees of plotted polynomials
- `xlim` (two `floats`): left and right limits of X axis

Returns: a `Sympy` plot