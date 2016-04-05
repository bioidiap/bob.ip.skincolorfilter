#!/usr/bin/env python
# encoding: utf-8
# Guillaume HEUSCH <guillaume.heusch@idiap.ch>
# Wed 29 Jul 09:27:26 CEST 2015

import sys
import numpy

class SkinColorFilter():
  """
  This class implements a number of functions to perform skin color filtering. It is based on the work published in 
  "Adaptive skin segmentation via feature-based face detection", M.J. Taylor and T. Morris, Proc SPIE Photonics Europe, 2014
  """
  def __init__(self):
    self.mean = numpy.array([0.0, 0.0])
    self.covariance = numpy.zeros((2, 2), 'float64')
    self.covariance_inverse = numpy.zeros((2, 2), 'float64')

  def generate_circular_mask(self, image, radius_ratio=0.4):
    """
    This function will generate a circular mask to be applied to the image. 
    The mask will be true for the pixels contained in a circle centered in the image center,
    and with radius equals to radius_ratio * the image's height.

    :param image: the (face) image to mask
    """
    x_center = image.shape[1] / 2
    y_center = image.shape[2] / 2

    # arrays with the image coordinates
    x = numpy.zeros((image.shape[1], image.shape[2]))
    x[:] = range(0, x.shape[1])
    y = numpy.zeros((image.shape[2], image.shape[1]))
    y[:] = range(0, y.shape[1])
    y = numpy.transpose(y)

    # translate s.t. the center is the origin
    x -= x_center
    y -= y_center

    # condition to be inside of a circle: x^2 + y^2 < r^2
    radius = radius_ratio*image.shape[2]
    self.circular_mask = (x**2 + y**2) < (radius**2)


  def remove_luma(self, image):
    """
    This function remove pixels that are considered as non-skin according to their luma values.
    The luma value for all pixels inside a provided circular mask is calculated. Pixels for which the
    luma value deviates more than 1.5 * standard deviation are pruned. 

    :param image: the (face) image to process
    """
    # compute the mean and std of luma values on non-masked pixels only
    luma = 0.299*image[0, self.circular_mask] + 0.587*image[1, self.circular_mask] + 0.114*image[2, self.circular_mask]
    m = numpy.mean(luma)
    s = numpy.std(luma)

    # apply the filtering to the whole image to get the luma mask
    luma = 0.299*image[0, :, :] + 0.587*image[1, :, :] + 0.114*image[2, :, :]
    self.luma_mask = numpy.logical_and((luma > (m - 1.5*s)), (luma < (m + 1.5*s)))


  def get_gaussian_parameters(self, image):
    """
    This function computes the mean and covariance matrix of the skin pixels in the normalised rg colorspace.
    Note that only the pixels for which both the circular and the luma mask is 'True' are considered. 

    :param image: the (face) image out of which skin color characteristics will be extracted.
    """
    self.generate_circular_mask(image)
    self.remove_luma(image)
    mask = numpy.logical_and(self.luma_mask, self.circular_mask)

    # get the mean
    channel_sum = image[0].astype('float64') + image[1] + image[2]
    nonzero_mask = numpy.logical_or(numpy.logical_or(image[0] > 0, image[1] > 0), image[2] > 0)
    r = numpy.zeros((image.shape[1], image.shape[2]))
    r[nonzero_mask] = image[0, nonzero_mask] / channel_sum[nonzero_mask]
    g = numpy.zeros((image.shape[1], image.shape[2]))
    g[nonzero_mask] = image[1, nonzero_mask] / channel_sum[nonzero_mask]
    self.mean = numpy.array([numpy.mean(r[mask]), numpy.mean(g[mask])])
   
    # get the covariance
    r_minus_mean = r[mask] - self.mean[0]
    g_minus_mean = g[mask] - self.mean[1]
    samples = numpy.vstack((r_minus_mean, g_minus_mean))
    samples = samples.T
    cov = sum([numpy.outer(s,s) for s in samples])
    self.covariance = cov / float(samples.shape[0] - 1) 
    
    # store the inverse covariance matrix (no need to recompute)
    if numpy.linalg.det(self.covariance) != 0:
      self.covariance_inverse = numpy.linalg.inv(self.covariance)
    else:
      self.covariance_inverse = numpy.zeros_like(self.covariance)


  def get_skin_pixels(self, image, threshold):
    """
    This function computes the probability of skin-color for each pixel in the image.
    the distribution of skin color is considered to be gaussian in the rg colorspace.
    
    :param image: the image to process
    :param threshold: the threshold on the probability of a pixel to be of skin color.
    """
    skin_map = numpy.zeros((image.shape[1], image.shape[2]), 'float64')
    
    # get the image in rg colorspace
    channel_sum = image[0].astype('float64') + image[1] + image[2]
    nonzero_mask = numpy.logical_or(numpy.logical_or(image[0] > 0, image[1] > 0), image[2] > 0)
    r = numpy.zeros((image.shape[1], image.shape[2]), 'float64')
    r[nonzero_mask] = image[0, nonzero_mask] / channel_sum[nonzero_mask]
    g = numpy.zeros((image.shape[1], image.shape[2]), 'float64')
    g[nonzero_mask] = image[1, nonzero_mask] / channel_sum[nonzero_mask]
    
    # compute the skin probability map
    r_minus_mean = r - self.mean[0]
    g_minus_mean = g - self.mean[1]
    v = numpy.dstack((r_minus_mean, g_minus_mean))
    v = v.reshape((r.shape[0]*r.shape[1], 2))
    probs = [numpy.dot(k, numpy.dot(self.covariance_inverse, k)) for k in v]
    probs = numpy.array(probs).reshape(r.shape)
    skin_map = numpy.exp(-0.5 * probs)

    return skin_map > threshold
