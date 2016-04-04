import sys
import numpy

import bob.io.base
import bob.io.image
import bob.ip.facedetect
from ..skin_color_filter import SkinColorFilter

def show_image(image, title=''):
  """ 
  This function just shows an image with a title (if provided)

  :param image: the image to show
  :param title: the title of the plot
  """
  from matplotlib import pyplot
  # color image
  if len(image.shape) == 3: 
    im = image.transpose(1,2,0)
    pyplot.figure()
    pyplot.imshow(im)
    pyplot.title(title)
    pyplot.show()
  # grayscale
  else:
    pyplot.figure()
    pyplot.imshow(image.astype(numpy.uint8), cmap='gray')
    pyplot.title(title)
    pyplot.show()

def main(user_input=None):

  image = bob.io.base.load('./bob/ip/skincolorfilter/data/001.bmp')
  show_image(image, 'original image')

  detection = bob.ip.facedetect.detect_single_face(image)
  if detection is not None:
    bb, quality = detection
    face = image[:, bb.top:bb.bottom, bb.left:bb.right]
    show_image(face, 'cropped face')
    skin_filter = SkinColorFilter()
    skin_filter.get_gaussian_parameters(face)
    skin_mask = skin_filter.get_skin_pixels(image, 0.5)
    display_skin = numpy.copy(image)
    display_skin[:, numpy.logical_not(skin_mask)] = 0
    show_image(display_skin, 'skin pixels')

  else:
    print "No face detected in the image"
    sys.exit()
