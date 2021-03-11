=====================
Welcome to MathCrypto
=====================

MathCrypto is a library of useful funtions used in cryptography. Do not use this library for improving the security of your application, it is not safe or powerful enough to provide that.

Current version is |release|.

.. _GitHub: https://github.com/Czechbol/mathcrypto

Includes
========

- Multiplicative group operations
   - Generating a group from modulus
   - Get inverse element any element of the group
   - Get element order of any element in group
- Math functions
   - Classic number primality check
   - Fermat's primality test
   - Euler's Totient function (Phi)
   - Euclidean algorithm (GCD)
   - Simple number factorization
   - Chinese Remainder Theorem
   - Extended Euclidean Algorithm
- Cryptography algorithms
   - Diffie-Hellman Key exchange generation and cracking
      - Multithreaded Brute-force cracking
      - Baby-step Giant-step algorithm cracking

Installation
============

MathCrypto is avalaible through Python Package Index (`PyPI <https://pypi.python.org/pypi>`_) using `pip <https://pip.pypa.io>`_:

.. code-block:: bash

   $ python3 -m pip install mathcrypto

To uninstall using `pip <https://pip.pypa.io>`_:

.. code-block:: bash

   $ python3 -m pip uninstall mathcrypto

Getting Started
===============

.. code-block:: python

   from mathcrypto import MathFunctions, MultiplicativeGroup

   def main():
       print("Playing with math functions")
       print()
       print("Is 137 prime?")
       print(MathFunctions.is_prime(137))
       print("What are the factors of 134?")
       print(MathFunctions.factorize(134))
       print("What is the greatest common divisor of 135 and 186?")
       print(MathFunctions.euclid_gcd(135, 186))
       print("What is the Euler's Totient function of 65?")
       print(MathFunctions.phi(65))
       print()

       print("Playing with multiplicative groups")
       print()
       group = MultiplicativeGroup(13)

       print("Group modulus:")
       print(group.mod)
       print("Group order:")
       print(group.order)
       print("Group elements:")
       print(group.elements)
       print("Group generators:")  # If there are any
       print(group.generators)
   
   main()

This outputs:

.. code-block:: text

   Playing with math functions
   
   Is 137 prime?
   True
   What are the factors of 134?
   [2, 67]
   What is the greatest common divisor of 135 and 186?
   3
   What is the Euler's Totient function of 65?
   48

   Playing with multiplicative groups

   Group modulus:
   13
   Group order:
   12
   Group elements:
   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
   Group generators:
   [2, 6, 7, 11]



Development
===========
Source code repository is available on `GitHub <https://github.com/Czechbol/mathcrypto>`_. Feel free to contribute. `Bug reports <https://github.com/Czechbol/mathcrypto/issues>`_ and suggestions are welcome.

License
=======

MathCrypto is licensed under the `MIT License <https://github.com/Czechbol/mathcrypto/blob/main/LICENSE>`_.


.. toctree::
   :name: mastertoc
   :maxdepth: 2

   mathcrypto



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
