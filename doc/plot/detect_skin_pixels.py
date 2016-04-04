import sys
import numpy

import bob.io.base
import bob.io.base.test_utils
import bob.io.image
import bob.ip.facedetect
from bob.ip.skincolorfilter.skin_color_filter import SkinColorFilter

face_image = bob.io.base.load(bob.io.base.test_utils.datafile('001.png', 'bob.ip.skincolorfilter'))
detection = bob.ip.facedetect.detect_single_face(face_image)
bounding_box, quality = bob.ip.facedetect.detect_single_face(face_image)
face = face_image[:, bounding_box.top:bounding_box.bottom, bounding_box.left:bounding_box.right]
skin_filter = SkinColorFilter()
skin_filter.get_gaussian_parameters(face)
skin_mask = skin_filter.get_skin_pixels(face_image, 0.5)
skin_image = numpy.copy(face_image)
skin_image[:, numpy.logical_not(skin_mask)] = 0

from matplotlib import pyplot
ax = pyplot.subplot(2, 1, 1)
ax[0].imshow(numpy.rollaxis(numpy.rollaxis(face_image, 2),2))
ax[0].title('Original Image')
ax[1].imshow(numpy.rollaxis(numpy.rollaxis(skin_image, 2),2))
ax[1].title('Detected skin pixels')
