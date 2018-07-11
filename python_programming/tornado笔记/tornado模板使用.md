# 使用 tornado 的模板

阅读 intoducing to tornado 笔记

## 基本语法

在模板中使用 python 表达式：

```
{{ }}
```

在模板中使用 if for else：

```
{% for name in names %}
    <li title="{{ name }}">{{ name }}</li>
{% end %}
```


## 模板继承

扩展一个已存在的模板：

```
{% entends "filename.html" %}
```

这个语法将使新文件继承 filename.html 中的所有标签，当需要的时候还可以重写相应的内容。


### 使用 Blocks

一个 blocks 语句块，封装了模板中的一些元素，可以进行扩展：

```
# main.html
<html>
<body>
    <header>
        {% block header %} {% end %}
    </header>
    <content>
        {% block body %}{% end %}
    </content>
    <footer>
        {% block footer %}{% end %}
    </footer>
</body>
</html>
```

```
{% extends main.html %}

{% block header %}
    <h1>Hello World!</h1>
{% end %}
```

## autoesacpe

tornado 模板默认开启转义，这会影响下面几个函数的功能：

- `linkify()`
- `xsrf_form_html()`

可以通过使用 `{% raw %}` block 对当前语句块不进行转义。


## UI Modules

UI Modules 是可复用的组件，它封装了 markup， style 和 behavior


Modules 本身是 python 类，这些类需要继承 tornado 的 `UIModule` 类，并定义一个  `render` 方法。

在 模板中使用 Module：

```
{% module Foo(...) %}
```
 Tornado 的模板引擎会调用这个模块的 render 方法，用返回的字符串代替这个 module block。

 还可以定义： `embedded_javasrcipt`, `embedded_css`, `javascript_files`, `css_files` 方法，在 Module 中嵌入自己的静态文件。

 模板中的 `locale.format_date()` 方法可以用来处理日期，有以下几个选项：

 - relative, True or False
 - full_format, True or False
 - shorter, True or False

嵌入 JavaScript 和 CSS 文件

- embedded_javascript,  insert JavaScript right before the closing <body> tag
- embedded_css,  insert CSS rule before the closing <head> tag
- html_body, insert full HTML markup right before the closing </body> tag
- javascript_files or css_files, include full files both from locally and externally

## 总结

