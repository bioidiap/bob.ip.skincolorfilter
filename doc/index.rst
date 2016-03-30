.. vim: set fileencoding=utf-8 :
.. Guillaume HEUSCH <guillaume.heusch@idiap.ch>
.. Wed 30 Mar 15:46:29 CEST 2016
..
.. Copyright (C) 2015 Idiap Research Institute, Martigny, Switzerland

.. _bob.ip.skincolorfilter:


========================
 Bob's Skin Color Filter
========================

This module contains the implementation of the skin color filter described in [taylor-spie-2014]_.
The skin color is modeled as a 2-dimensional gaussian in the normalised rg colorspace. Note that
the estimation of the gaussian parameters should be done using a cropped face image. As a consequence,
this pacakge depends on the Bob's face detection package.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api


References
----------

.. [taylor-spie-2014]  *M.J. Taylor and T. Morris*. **Adaptive skin segmentation via feature-based face detection,** Proc SPIE Photonics Europe, 2014. `pdf <http://www.cs.man.ac.uk/~tmorris/pubs/AdaptSS_SPIE.pdf>`__

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
