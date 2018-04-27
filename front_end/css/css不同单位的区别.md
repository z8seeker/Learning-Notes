# css 中的长度单位

有很多 css 属性的属性值为一个长度值，比如: `width`, `margin`, `padding`, `font-size`, `border-width`, 等。

长度的数值和单位之间不能有空格，但如果数值为零时，单位是可以忽略的。对于一些 css 属性，允许有负的长度。

有两种类型的长度单位：

- 绝对长度
- 相对长度

## 绝对长度单位

The absolute length units are _fixed in relation_ to each other and _anchored to some physical measurement_. 

绝对长度单位包括：

- 物理长度单位
  - `cm`，厘米
  - `mm`，毫米
  - `in`，英寸。 `1in = 96px = 2.54cm`
  - `pt`，点。 `1pt = 1/72th of 1in`
  - `pc`，picas。 `1pc = 12pt = 1/6th of 1in`
- 视觉角度单位（visual angle unit）
  - `px`，像素。 `1px = 1/96th of 1in`

所有的绝对长度单位都是互相兼容的，而像素是所有绝对单位的规范单位。

For a CSS device, these dimensions are anchored either：

- by relating the physical units to their physical measurements, or
- by relating the pixel unit to the reference pixel. 

Note: If the anchor unit is the pixel unit, _the physical units might not match their physical measurements_. Alternatively if the anchor unit is a physical unit, the pixel unit might not map to a whole number of device pixels

The _reference pixel_ is the visual angle of one pixel on a device with a pixel density of 96dpi and a distance from the reader of an arm’s length. For a nominal arm’s length of 28 inches, the visual angle is therefore about 0.0213 degrees. For reading at arm’s length, 1px thus corresponds to about 0.26 mm (1/96 inch).

对参考像素点（reference pixel）的理解：

CSS defines the reference pixel, which measures the size of a pixel on a 96 dpi display. On a display that has a dpi _substantially different_ than 96dpi (like Retina displays), the user agent rescales the px unit so that its size matches that of a reference pixel. In other words, this rescaling is exactly why 1 CSS pixel equals 2 physical Retina display pixels.

Historically px units typically represented one device pixel. With devices having higher and higher pixel density this no longer holds for many devices, such as with Apple's Retina Display.

### 理解像素

图片中的像素（Pixel），是画面中最小的点（单位色块）。像素的大小是没有固定长度值的，不同设备上一个单位像素色块的大小是不一样的。因此1个像素长度是相对于显示设备而言的，是相对于设备 _屏幕分辨率_ 而言的。


#### 屏幕分辨率

屏幕分辨率是屏幕每行的像素点数*每列的像素点数，每个屏幕有自己的分辨率。屏幕分辨率越高，所呈现的色彩越多，清晰度越高

如果一块屏幕的分辨率是 1024×768，也就是说设备屏幕的水平方向上有 1024 个像素点，垂直方向上有 768 个像素点。

尺寸面积大小相同的两块屏幕，分辨率大小可以是不一样的，分辨率高的屏幕上面像素点（色块）就多，所以屏幕内可以展示的画面就更细致，像素点（色块）更小。而分辨率低的屏幕上像素点（色块）更少，单个像素面积更大，可以显示的画面就没那么细致。

虽然不同设备上像素块大小会不一样，但是同一台硬件设备上的屏幕分辨率、像素块大小是不会变的。PC 电脑上之所以可以调整屏幕分辨率，其实也是通过算法转换了的。

#### 图像分辨率

图像分辨率是指每英寸图像内的像素点数。图像分辨率是有单位的，叫 _像素每英寸_（ppi）。分辨率越高，像素的点密度越高，图像越逼真。

图片的分辨率和图片的宽、高尺寸一起决定了图像文件的大小及图像质量。比如，一幅图宽 8 英寸、高 6 英寸，分辨率为 100PPI，如果保持图像文件的大小不变，也就是总的像素数不变，将分辨率降为 50PPI，在宽高比不变的情况下，图像的宽将变为 16 英寸、高将变为 12 英寸。

#### 输出分辨率

决定图像输出质量的是图像的输出分辨率，描述的是设备输出图像时每英寸可产生的点数，以 dpi 为单位。大部分时候我们说的输出分辨率主要是指 _印刷需要_ 的分辨率。

“像素”只存在于电脑等显示领域，而“点”只出现于打印或印刷领域。对电脑显示屏，分辨率是用像素数目衡量;对数字文件印刷，分辨率是通常用每英寸所含点或像素〔dpi〕来衡量。

相同的分辨率，更高的 DPI 表现为（印刷的）物理尺寸更小；而物理尺寸相同，DPI 较低则表现为较低的分辨率（每英寸的点数变少，同时每个像素都变大，图像变模糊）


## 相对长度单位

Relative length units specify a length relative to another length. Style sheets that use relative units can more easily scale from one output environment to another.

相对长度单位包括：

- `em`, 元素的字体尺寸
- `ex`，
- `ch`
- `rem`
- `vw`
- `vh`
- `vmin`
- `vmax`

css 中常用的长度单位有：

- px
- em
- rem

## px
