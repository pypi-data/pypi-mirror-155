from setuptools import setup

setup(name='disops',
      version='0.3.2',
      description='Orthogonal Polynomials of a Discrete Variable',
      author='José L. Ruiz',
      packages=['disops'],
      license='GNU GPLv3 ',
      zip_safe=False,
      python_requires=">=3.8",
      install_requires=["sympy>=1.10.1"],
      url='https://gitlab.com/joselruiz/tfg/-/tree/main/disops'
)
