Pytearcat: PYthon TEnsor AlgebRa calCulATor - A python package for general relativity and tensor calculus
=======================================================================================================

Pytearcat is an open-source Python package created to work with general
tensor operations, either in the field of General Relativity (GR) or
others that need to use tensor calculus. It provides the basic GR
tensors built in the package and uses a standard syntax for the Einstein
notation.

Installation
------------

As a Python package, Pytearcat can be installed through pip using

.. code:: bash

   pip install pytearcat

To use the Giacpy core in Pytearcat, the user must explicitly indicate
during the package installation that the installer must include the
Giacpy module in the process. This is done through

.. code:: bash

   pip install pytearcat[giapy]

File structure summary
----------------------

Inside the Pytearcat package, there are two sub-packages named *gr* and
*tensor*. Inside the first one, there are six modules related to GR
expressions. These libraries allow calculating quantities that are very
common in GR, such as the Christoffel symbols (first and the second
kind, *christoffel.py*), the Ricci tensor and the Ricci scalar
(*ricci.py*), the Riemann tensor (*riemann.py*) and the Einstein tensor
(*einstein.py*). Also, there is a module to define the metric
(*metric.py*) and another to calculate the geodesics (*geodesic.py*).
The second sub-package named *tensor* contains modules that allow to
define tensors and operate with them. The *misc.py* module contains
functions that allow defining symbolic functions, variables, and
constants. It also contains other functions to work with series
expansions and to simplify expressions. The *kdelta.py* and *lcivita.py*
modules contain the data classes which define the Kronecker Delta symbol
and the Levi-Civita symbol, respectively. The *tensor.py* module
contains the code related with the class *tensor* and many functions
that are useful to define a tensor, operate tensors, recognise the
contravariant and covariant indices, lower and raise indices and expand
a tensor like a series up to a specific order. Inside this sub-package,
there is another one named *core* which contains essential information
that the program needs to operate tensors. All the functions required by
the user are located at the top level of the package.

Usage
-----

Pytearcat works using Jupyter Notebooks to give the outputs in
mathematical form. To use the package the user should import Pytearcat
within a Jypyter Notebook

.. code:: python

   import pytearcat as pt

Later, it is possible to access the functions and methods of the package
within the notebook. Different usage examples can be found in the top
directory of the GitHub repository.

How to cite this work
---------------------

To cite this work, please refer to Pytearcat’s release paper `San Martin
& Sureda (2021) <https://doi.org/10.1016/j.ascom.2022.100572>`__ (also
available on `arXiv <https://arxiv.org/abs/2106.15016>`__) and use the
following Bibtex citation:

::

   @article{pytearcat2022,
       abstract = {This paper introduces the first release of Pytearcat, a Python package developed to compute tensor algebra operations in the context of theoretical physics, for instance, in general relativity. Given that working with tensors can become a complex task, people often rely on computational tools to perform tensor calculations. We aim to build a tensor calculator based on Python, which benefits from being free and easy to use. Pytearcat syntax resembles the usual physics notation for tensor calculus, such as the Einstein notation for index contraction. This version allows the user to perform many tensor operations, including derivatives and series expansions, along with routines to obtain the typical General Relativity tensors. A particular concern was put in the execution times, leading to incorporate an alternative core for the symbolic calculations, enabling to reach much faster execution times. The syntax and the versatility of Pytearcat are the most important features of this package, where the latter can be used to extend Pytearcat to other areas of theoretical physics.},
       author = {M. San Mart\'in and J. Sureda},
       doi = {https://doi.org/10.1016/j.ascom.2022.100572},
       issn = {2213-1337},
       journal = {Astronomy and Computing},
       keywords = {Software, Public release, General relativity, Tensor algebra, Computer algebra system},
       pages = {100572},
       title = {Pytearcat: PYthon TEnsor AlgebRa calCulATor A python package for general relativity and tensor calculus},
       url = {https://www.sciencedirect.com/science/article/pii/S221313372200018X},
       year = {2022},
       Bdsk-Url-1 = {https://www.sciencedirect.com/science/article/pii/S221313372200018X},
       Bdsk-Url-2 = {https://doi.org/10.1016/j.ascom.2022.100572}}
