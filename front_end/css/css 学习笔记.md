# css 布局

参考自 [学习 css 布局](http://zh.learnlayout.com/)


## display 属性

`display` 是 css 中最重要的用于控制布局的属性。

每个元素都有一个默认的 `display` 值，这与元素的类型有关。对于大多数元素它们的默认值通常是 `block` 或 `inline` :

- 一个 `block` 元素通常被叫做块级元素。
  - 块级元素只能出现在 `<body>` 元素内 
  - `address`, `article`, `aside`, `audio`, `blockquote`, `canvas`, `dd`, `div`, `dl`, `fieldset`, `figcaption`, `figure`, `footer`, `form`, `h1-h6`, `header`, `hgroup`, `hr`, `noscript`, `ol`, `output`, `p`, `pre`, `section`, `table`, `tfoot`, `ul`, `video`
- 一个 `inline` 元素通常被叫做行内元素。
  - 行内元素可以在段落中包裹一些文字而不会打乱段落的布局 
  - `a`, `abbr`, `acronym`, `b`, `bdo`, `big`, `br`, `button`, `cite`, `code`, `dfn`, `em`, `i`, `img`, `input`, `kbd`, `label`, `map`, `object`, `q`, `samp`, `script`, `select`, `small`, `span`, `strong`, `sub`, `sup`, `textarea`, `time`, `tt`, `var`
  

块级元素与行内元素的主要区别：

- 格式。
  - 默认情况下，块级元素会新起一行并且尽可能撑满容器
  - 行内元素不会进行强制换行
- 内容模型。
  - 通常块级元素可以包含行内元素和其他块级元素，因此块级元素可以创建更大的结构
  - 行内元素只包含数据和其他行内元素，不能包含块级元素

另一个常用的 `display` 值是 `none`。`display:none` 通常被 JavaScript 用来在不删除元素的情况下隐藏或显示元素。

这和 `visibility` 属性不一样。把 `display` 设置成 `none` 元素不会占据它本来应该显示的空间，但是设置成 `visibility: hidden`; 还会占据空间。
 
## margin:auto

设置块级元素的 `width` 可以防止它从左到右撑满整个容器。然后你就可以设置左右外边距为 `auto` 来使其水平居中。元素会占据你所指定的宽度，然后剩余的宽度会一分为二成为左右外边距。

```css
#main {
    width: 600px;
    margin: 0 auto;
}
```

这样做的问题是，当浏览器窗口比元素的宽度还要窄时，浏览器会显示一个水平滚动条来容纳页面。

## max-width

使用 `max-width` 替代 `width` 可以使浏览器更好地处理小窗口的情况。这点在移动设备上显得尤为重要

```css
#main {
    max-width: 600px;
    margin: 0 auto;
}
```

## 盒模型

盒模型由四部分组成：
- margin 外边距,
- border 边框,
- padding 内填充,
- content 内容（中心部分0x0的那个框）

![盒模型示意图](http://7rf34y.com2.z0.glb.qiniucdn.com/c/9b861d920728a04e2702e81f2231fc39)

### 盒模型的种类

- W3C定义的盒模型包括 margin、border、padding、content，元素的宽度 width=content 的宽度
- IE盒模型与W3C盒模型的唯一区别就是元素的宽度，元素的 width=border + padding + content

### 理解盒模型

以 `div` 类比盒子来理解盒模型：
- 两个 `div` 之间的空隙就是 `margin`。
- 每个 `div` 也有自己的边框，而且不同 `div` 的边框厚度也可能不同，这个边框就是 `border`，边框的厚度就是指 `border` 的大小
- `div` 里可以有各种块级元素和行内元素，所有这些元素就是 `content` 了
- `div` 里的元素也可能没有把这个 `div` 装满，那么 `div` 里除了 `content` 外的空白区域就是 `padding` 了


### 盒模型的宽度计算

一个盒模型的宽度，不只是计算其 content 的宽度，还要加上 padding 和 border 的宽度。

这样对于计算盒模型宽度是不利的，因为比较繁琐。于是后来人为了解决这个问题，在 CSS3 中给盒模型加入了新属性：`box-sizing`。 

`box-sizing` 共两个属性:

- 一个是 `content-box`，
- 一个是 `border-box`

设置为 `content-box` 则盒模型宽度计算方法同 CSS2.1，计算内边距和边框；当设置一个盒模型为 `box-sizing: border-box` 时，这个盒子的内边距和边框都不会再增加它的宽度。这是因为内边距和边框都在设定的宽度内进行绘制，元素宽度需要由设定宽度减去内边距和边框得到。

详细描述：

- 如果 `box-sizing` 为默认值， `width`, `min-width`, `max-width`, `height`, `min-height` 与 `max-height` 控制内容大小
- 内边距区域 padding area 延伸到包围 padding 的边框。如果内容区域 content area 设置了背景、颜色或者图片，这些样式将会延伸到 padding上 (而不仅仅是作用于内容区域)。它位于内边距边界内部, 它的大小为 `padding-box` 宽与 `padding-box` 高
- 内边距与内容边界之间的空间可以由 `padding-top`, `padding-right`, `padding-bottom`, `padding-left` 和简写属性 `padding` 控制。
- 边框区域 border area 是包含边框的区域，扩展了内边距区域。它位于边框边界内部，大小为 `border-box` 宽和 `border-box` 高。由 `border-width` 及简写属性 `border` 控制。
- 外边距区域 margin area 用空白区域扩展边框区域，以分开相邻的元素。它的大小为 `margin-box` 的高宽。外边距区域大小由 `margin-top`, `margin-right`, `margin-bottom`, `margin-left` 及简写属性 `margin` 控制。


## position

position 属性有很多值，可以用来制作复杂的布局

### static

```css
.static {
    position: static;
}
```
`static` 是默认值。任意 `position: static`; 的元素不会被特殊的定位。一个 `static` 元素表示它不会被“positioned”，一个 position 属性被设置为其他值的元素表示它会被“positioned”。 

### relative

```css
.relative1 {
    position: relative;
}
.relative2 {
    position: relative;
    top: -20px;
    left: 20px;
    background-color: white;
    width: 500px;
}
```

`relative` 表现的和 `static` 一样，除非你添加了一些额外的属性。 

在一个相对定位（position属性的值为relative）的元素上设置 `top` 、 `right` 、 `bottom` 和 `left` 属性会使其偏离其正常位置。其他的元素的位置则不会受该元素的影响发生位置改变来弥补它偏离后剩下的空隙。 

### fixed

一个固定定位（position属性的值为fixed）元素会相对于视窗来定位，这意味着即便页面滚动，它还是会停留在相同的位置。和 relative 一样， `top` 、 `right` 、 `bottom` 和 `left` 属性都可用。 

```css
.fixed {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 200px;
    background-color: white;
}
```

一个固定定位元素不会保留它原本在页面应有的空隙（脱离文档流）。 

### absolute

 `absolute` 与 `fixed` 的表现类似，但是它不是相对于视窗而是相对于最近的“positioned”祖先元素。如果绝对定位（position属性的值为absolute）的元素没有“positioned”祖先元素，那么它是相对于文档的 `body` 元素，并且它会随着页面滚动而移动。
 
 ```css
 .relative {
     position: relative;
     width: 600px;
     height: 400px;
 }
 .absolute {
     position: absolute;
     top: 120px;
     right: 0;
     width: 300px;
     height: 200px;
 }
 ```
 
### 一个示例

```css
.container {
    position: relative;
}
nav {
    position: absolute;
    left: 0px;
    width: 200px;
}
section {
    margin-left: 200px;
}
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    height: 70px;
    background-color: white;
    width: 100%;
}
body {
    margin-bottom: 120px;
}
```

这个例子在容器比 `nav` 元素高的时候可以正常工作。如果容器比nav元素低，那么 `nav` 会溢出到容器的外面。


## float

另一个布局中常用的 CSS 属性是 `float`。Float 可用于实现文字环绕图片：

```css
img {
    float: right;
    margin: 0 0 1em 1em;
}
```

## clear

`clear` 属性被用于控制浮动。

```html
<div class="box">...</div>
<section class="after-box">...</section>
```

```css
.box {
    float: left;
    width: 200px;
    height: 100px;
    margin: 1em;
}
```

在这个例子中， `section` 元素实际上是在 `div` 之后的。然而 `div` 元素是浮动到左边的，于是 `section` 中的文字就围绕了 `div` ，并且 `section` 元素包围了整个元素。如果我们想让 `section` 显示在浮动元素之后呢？ 这时就用到了 clear 属性：

```css
.box {
    float: left;
    width: 200px;
    height: 100px;
    margin: 1em;
}
.after-box {
    clear: left;
}
```
使用 `clear` 就可以将这个段落移动到浮动元素 `div` 下面。你需要用 `left` 值才能清除元素的向左浮动。你还可以用 `right` 或 `both` 来清除向右浮动或同时清除向左向右浮动。 

## clearfix hack

在使用浮动的时候经常会遇到这样的事情： 如果图片比包含它的元素还高， 而且它是浮动的，于是它就溢出到了容器外面。

```css
img {
    float: right;
}
```

可以使清除浮动（比较丑陋）的方法解决这个问题：

```css
.clearfix {
    overflow: auto;
}
```

## 浮动布局示例

使用 float 实现之前用 position 实现的布局：

```css
nav {
    float: left;
    width: 200px;
}
section {
    margin-left: 200px;
}
```

## 百分比宽度

百分比是一种相对于包含块的计量单位。它对图片很有用，甚至还可以同时使用 `min-width` 和 `max-width` 来限制图片的最大或最小宽度:

```css
article img {
    float: right;
    width: 50%;
}
```

还可以用百分比做布局，但是这需要更多的工作:

```css
nav {
    float: left;
    width: 25%;
}
section {
    margin-left: 25%;
}
```

当布局很窄时， `nav` 就会被挤扁。更糟糕的是，你不能在 `nav` 上使用 `min-width` 来修复这个问题，因为右边的那列是不会遵守它的。


## 媒体查询

为什么需要媒体查询？

“响应式设计（Responsive Design” 是一种让网站针对不同的浏览器和设备“呈现”不同显示效果的策略，这样可以让网站在任何情况下显示的很棒！而媒体查询是做此事所需的最强大的工具。

```css
@media screen and (min-width:600px) {
    nav {
        float: left;
        width: 25%;
    }
    section {
        margin-left: 25%;
    }
}
@media screen and (max-width: 599px) {
    nav li {
        display: inline;
    }
}
```
这样的布局在移动浏览器上也会显示的很棒。


## inline-block

你可以创建很多网格来铺满浏览器。在过去很长的一段时间内使用 `float` 是一种选择，但是使用 `inline-block` 会更简单。

```css
.box {
    float: left;
    width: 200px;
    height: 100px;
    margin: 1em;
}
.after-box {
    clear: left;
}
```

使用 `clear`，所以不会浮动到上面那堆盒子的旁边。 

```css
.box2 {
    display: inline-block;
    width: 200px;
    height: 100px;
    margin: 1em;
}
```
