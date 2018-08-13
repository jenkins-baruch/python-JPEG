

```python
from matplotlib import pyplot
```


```python
import cv2
```


```python
import numpy as np
```


```python
def split(img):
    a, b, c = cv2.split(img)
    zeros = np.zeros_like(a)
    pyplot.imshow(cv2.merge((a, zeros, zeros)))
    pyplot.show()
    pyplot.imshow(cv2.merge((zeros, b, zeros)))
    pyplot.show()
    pyplot.imshow(cv2.merge((zeros, zeros, c)))
    pyplot.show()
```


```python
def split_ycbcr(img):
    a, b, c = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb))
    zeros = np.zeros_like(a)
    pyplot.imshow(cv2.cvtColor(cv2.merge((a, zeros, zeros)), cv2.COLOR_YCrCb2BGR))
    pyplot.show()
    pyplot.imshow(cv2.cvtColor(cv2.merge((zeros, b, zeros)), cv2.COLOR_YCrCb2BGR))
    pyplot.show()
    pyplot.imshow(cv2.cvtColor(cv2.merge((zeros, zeros, c)), cv2.COLOR_YCrCb2BGR))
    pyplot.show()
```


```python
split(cv2.imread("img/colored.bmp"))
```


![png](output_5_0.png)



![png](output_5_1.png)



![png](output_5_2.png)



```python
split(cv2.imread("img/moto.png"))
```


![png](output_6_0.png)



![png](output_6_1.png)



![png](output_6_2.png)



```python
split_ycbcr(cv2.imread("img/colored.bmp"))
```


![png](output_7_0.png)



![png](output_7_1.png)



![png](output_7_2.png)



```python
split_ycbcr(cv2.imread("img/moto.png"))
```


![png](output_8_0.png)



![png](output_8_1.png)



![png](output_8_2.png)

