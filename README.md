# JPEG Algorithm with Python

## By [Meny Buganim](todo), [Lital Hayat](todo) and [Baruch Rothkoff](todo)

### Build status

[![Build Status](http://54.218.224.31:8080/job/python-JPEG/job/master/badge/icon)](http://54.218.224.31:8080/job/python-JPEG/job/master/)

## Flow and explanation of JPEG algorithm

Note that because during the work we compare our results vs [cv2 library (OpenCV for Python)](TODO), who is display color in different order, our colors represented as **BGR** (instead of **RGB**) and **Y'CrCb** (instead of **Y'CbCr**)

### Original Image

![Original Image](Flowchart/original.png)

### Convert to Y'CrCb

Y'CrCb is channels represention as luma component, blue-difference and red-difference ([from wikipedia](https://en.wikipedia.org/wiki/YCbCr)).

We know that __B__GR is  Blue, Green and Red channels, like this:

| B | G | R |
|:-: | :-: | :-: |
| ![B](Flowchart/channel_b.png) | ![G](Flowchart/channel_g.png) | ![R](Flowchart/channel_r.png) |

But Y'CrCb shouls be different division (Without lossing the data!):

| Y' | Cr | Cb |
|:-: | :-: | :-: |
| ![Y'](Flowchart/channel_y.png) | ![Cr](Flowchart/channel_cr.png) | ![Cb](Flowchart/channel_cb.png) |

We do this because the humen eyes are more luma sensitive to red and blue, so

### Downsampling

we can remove data from blue and red, and the impact of whole image will be less than downsapling BGR image, like that:

#### BGR Downsapling

![BGR Downsampling](Flowchart/bgr_downsapling.png)

#### Y'CrCb

![Y'CrCb Downsampling](Flowchart/ycrcb_downsapling.png)