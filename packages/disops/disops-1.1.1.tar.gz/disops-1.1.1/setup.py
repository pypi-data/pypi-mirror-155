from setuptools import setup

setup(name='disops',
      version='1.1.1',
      description='Orthogonal Polynomials of a Discrete Variable',
      author='José L. Ruiz',
      packages=['disops'],
      license='GNU GPLv3 ',
      zip_safe=False,
      python_requires=">=3.8",
      install_requires=["sympy>=1.10.1", "matplotlib>=3.5.1"],
      url='https://gitlab.com/joselruiz/tfg/-/tree/main/disops'
)
