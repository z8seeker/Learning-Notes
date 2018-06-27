# vue 基本操作

## 声明式渲染

Vue.js 的核心是一个允许采用简洁的 __模板语法__ 来声明式地将数据渲染进 DOM 的系统：

```html
<div id="app">
    {{ message }}
</div>
```

```javascript
var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    }
})
```

现在数据和 DOM 已经被建立了关联，所有东西都是响应式的。


使用指令绑定元素特性。

指令带有前缀 `v-`，以表示它们是 Vue 提供的特殊特性：

```html
<div id="app-2">
    <span v-bind:title="message">
         鼠标悬停几秒钟查看此处动态绑定的提示信息！
    </span>
</div>
```

```javascript
var app2 = new Vue({
    el: '#app-2',
    data: {
        message: '页面加载于' + new Date().toLocaleString()
    }
})
```

指令的意思是：“将这个 span 元素节点的 title 特性和 Vue 实例的 message 属性保持一致”。


## 条件与循环

我们不仅可以把数据绑定到 DOM 文本或特性，还可以绑定到 DOM 结构：

```html
<div id="app-3">
    <p v-if="seen">现在你看到我了</p>
</div>
```

```javascript
var app3 = new Vue({
    el: "#app-3",
    data: {
        seen: true
    }
})
```


`v-for` 指令可以绑定数组的数据来渲染一个项目列表：

```html

```