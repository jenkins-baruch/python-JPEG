# JPEG Algorithm with Python

## By [Meny Buganim](todo), [Lital Hayat](todo) and [Baruch Rothkoff](todo)

### Build status:

[![Build Status](http://54.218.224.31:8080/job/python-JPEG/job/master/badge/icon)](http://54.218.224.31:8080/job/python-JPEG/job/master/)

## Flow and explanation of JPEG algorithm

Note that because during the work we compare our results vs [cv2 library (OpenCV for Python)](TODO), who is display color in different order, our colors represented as **BGR** (instead of **RGB**) and **Y'CrCb** (instead of **Y'CbCr**)

### Original Image

<img src="Flowchart/original.png" width="100%">

### Convert to Y'CrCb

Y'CrCb is channels represention as luma component, blue-difference and red-difference ([from wikipedia](https://en.wikipedia.org/wiki/YCbCr)).

We know that __B__GR is  Blue, Green and Red channels, like this:
<img src="Flowchart/channel_b.png" width="30%">
<img src="Flowchart/channel_g.png" width="30%">
<img src="Flowchart/channel_r.png" width="30%">

But Y'CrCb shouls be different division (Without lossing the data!):

<img src="Flowchart/channel_y.png" width="30%">
<img src="Flowchart/channel_cr.png" width="30%">
<img src="Flowchart/channel_cb.png" width="30%">

We do this because the humen eyes are more luma sensitive to red and blue, so

### Downsampling

we can remove data from blue and red, and the impact of whole image will be less than downsapling BGR image, like that:

#### BGR Downsapling

<img src="Flowchart/bgr_downsapling.png" width="1000%">

#### Y'CrCb

<img src="Flowchart/ycrcb_downsapling.png" width="1000%">