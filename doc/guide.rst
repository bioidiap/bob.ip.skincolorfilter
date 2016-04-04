.. py:currentmodule:: bob.ip.skincolorfilter

.. testsetup:: *

   from __future__ import print_function
   import bob.io.base
   import bob.io.base.test_utils
   import bob.io.image
   import bob.ip.facedetect
   from bob.ip.skincolorfilter.skin_color_filter import SkinColorFilter

   import pkg_resources
   face_image = bob.io.base.load(bob.io.base.test_utils.datafile('001.png', 'bob.ip.skincolorfilter'))

=============
 Users Guide
=============

This skin color filter relies on the result of face detection. The skin color values 
are estimated from the center of the detected face area. The probability of a pixel
to be of skin color is modeled as a bivariate gaussian in the normalized rg colorspace 

Skin pixels detection in a single image
---------------------------------------

The function to detect skin pixels will return a mask (logical numpy array of the
same size of the image) where location corresponding to skin color pixels is True.
Hence, to detect skin pixels inside a face image, you should do the following:

.. doctest::

   >>> face_image = bob.io.base.load('001.png') # doctest: +SKIP
   >>> detection = bob.ip.facedetect.detect_single_face(face_image)
   >>> bounding_box, quality = bob.ip.facedetect.detect_single_face(face_image)
   >>> face = face_image[:, bounding_box.top:bounding_box.bottom, bounding_box.left:bounding_box.right]
   >>> skin_filter = SkinColorFilter()
   >>> skin_filter.get_gaussian_parameters(face)
   >>> skin_mask = skin_filter.get_skin_pixels(face_image, 0.5)


.. plot:: plot/detect_skin_pixels.py
   :include-source: False


Skin pixels detection in videos
-------------------------------
To detect skin pixels in video, you don't need to re-init the gaussian parameters at each frame.
However, you can do it if you really want to by calling the appropriate function (i.e. get_gaussian_parameters).

