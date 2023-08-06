from .OrthogonalPolynomialsGenerator import OrthogonalPolynomialsGenerator

from sympy import poly, rf, Symbol
from math import factorial
from warnings import warn

class Hahn(OrthogonalPolynomialsGenerator):
    """Hahn Polynomials Generator.

    Attributes:
        x (:obj: `sympy.Symbol`): variable of polynomials
        N (int, or sympy.Symbol): size of Hanh Polynomials Sequence
        alpha (int, float or sympy.Symbol): fist parameter of Hahn polynomials
        beta (int, float or sympy.Symbol): second parameter of Hahn polynomials
    """

    def __init__(self, N, alpha, beta, x=Symbol('x')):
        if not (isinstance(N, int) and N > 0):
            warn("The size N should be an integer positive number (int).")
        if not (isinstance(alpha, Symbol) or (isinstance(alpha, float) and alpha >= -1)):
            warn("The parameter alpha should be a real number greater than or equal to -1 (float) or a sympy.Symbol.")
        if not (isinstance(beta, Symbol) or (isinstance(beta, float) and beta >= -1)):
            warn("The parameter beta should be a real number greater than or equal to -1 (float) or a sympy.Symbol.")
        super().__init__([N, alpha, beta], x)


    def __str__(self):
        return "<Hahn Polynomials Generator of variable "+str(self.x)+", size="+str(self.params[0])+" and parameters alpha="+str(self.params[1])+" and beta="+str(self.params[2])+">"


    def _gen_explicit(self, n):
        return poly(sum([rf(-n,k) * rf(n+self.params[1]+self.params[2]+1,k) * rf(-self.x, k) / (rf(self.params[1]+1,k) * rf(-self.params[0], k) * factorial(k)) for k in range(n+1)]), self.x)


    def _recurrence_coeffs(self, n):
        A = (n+self.params[1]+self.params[2]) * (n+self.params[1]) * (self.params[0]-n+1) / ((2*n+self.params[1]+self.params[2]-1) * (2*n+self.params[1]+self.params[2]))
        C = (n-1) * (n+self.params[1]+self.params[2]+self.params[0]) * (n-1+self.params[2]) / ((2*(n-1)+self.params[1]+self.params[2]) * (2*n+self.params[1]+self.params[2]-1))
        return ((-self.x+A+C)/A, -C/A)