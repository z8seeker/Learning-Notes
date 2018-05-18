# React 技术栈

React 由 Facebook 公司2013年推出的前端框架，现在有最好的社区支持和生态圈，以及大量的第三方工具。


## React 的优缺点

react 有以下优点：

- 组件模式，利于代码复用和分工
- 虚拟 DOM，带来性能优势
- 移动端支持，可跨终端使用

react 的缺点：

- 学习曲线较陡峭
- 全新的一套概念，与其他所有框架截然不同
- 只有采用它的整个技术栈，才能发挥最大威力

总结：React 非常先进和强大，但是学习和实现成本都不低。


## JSX 语法

React 使用 JSX 语法，JavaScript 代码中可以写 HTML 代码：

```jsx
let myTitle = <h1>Hello, world!</h1>;
```

JSX 语法解释：

- JSX 语法的最外层，只能有一个节点
- JSX 语法中可以插入 JavaScript 代码，使用大括号

```jsx
// 错误
let myTitle = <p>Hello</p><p>World</p>;

// 插入 js 代码，使用大括号
let myTitle = <p>{'Hello' + 'World'}</p>
```

## Babel 转码器

JavaScript 引擎（包括浏览器和 Node）都不认识 JSX，需要首先使用 Babel 转码，然后才能运行。

```javascript
<script src="react.js"></script>
<script src="react-dom.js"></script>
<script src="babel.min.js"></script>
<script type="text/babel">
  // ** Our code goes here! **
</script>
```

React 需要加载两个库：React 和 React-DOM，前者是 React 的核心库，后者是 React 的 DOM 适配库。Babel 用来在浏览器转换 JSX 语法，如果服务器已经转好了，浏览器就不需要加载这个库。

## 练习

JSX 语法

`ReactDOM.render` 是 React 的最基本方法，用于将模板转为 HTML 语言，并插入指定的 DOM 节点。

`ReactDOM.render` 方法接受两个参数：一个虚拟 DOM 节点和一个真实 DOM 节点，作用是将虚拟 DOM 挂载到真实 DOM。

```jsx
ReactDOM.render(
  <span>Hello World!</span>,
  document.getElementById('example')
);
```

React 组件

React 允许用户定义自己的组件，插入网页。

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="react.js"></script>
    <script src="react-dom.js"></script>
    <script src="babel.min.js"></script>
  </head>
  <body>
    <div id="example"></div>
    <script type="text/babel">
  class MyTitle extends React.Component {
    render() {
      return <h1>Hello World</h1>;
    }
  };

  ReactDOM.render(
    <MyTitle/>,
    document.getElementById('example')
  );
    </script>
  </body>
</html>
```

注意事项：

- `MyTitle` 类继承了基类 `React.Component` 的所有属性和方法。
- React 规定，自定义组件的第一个字母必须大写，比如 `MyTitle` 不能写成`myTitle`，以便与内置的原生类相区分。
- 每个组件都必须有 render 方法，定义输出的样式。
- `<MyTitle/>` 表示生成一个组件类的实例，每个实例一定要有 _闭合标签_，写成 `<MyTilte></MyTitle>` 也可。


React 组件的参数

组件可以从外部传入参数，内部使用 `this.props` 获取参数。

```jsx
class MyTitle extends React.Component {
  render() {
    return <h1
      style={{color: this.props.color}}
    >Hello World</h1>;
  }
};

<MyTitle color="red" />,
```

可以看到，组件内部通过 `this.props` 对象获取参数

React 组件的状态

组件往往会有内部状态，使用 `this.state` 表示。通过组件状态的变动，可以引发对组件的重新渲染。

```jsx
class MyTitle extends React.Component {
    constructor(...args) {
      super(...args);
      this.state = {
        name: '访问者'
      };
    }

    handleChange(e) {
      let name = e.target.value;
      this.setState({
        name: name
      });
    }

    render() {
      return <div>
        <input type="text" onChange={this.handleChange.bind(this)} />
        <p>你好，{this.state.name}</p>
      </div>;
    }
};

ReactDOM.render(
    <MyTitle/>,
    document.getElementById('example')
);
```

`constructor` 是组件的构造函数，会在创建实例时自动调用。`...args` 表示组件参数，`super(...args)` 是 ES6 规定的写法。`this.state` 对象用来存放 _内部状态_，这里是定义初始状态。

`this.state.name` 表示读取 `this.state` 的 `name` 属性。每当输入框有变动，就会自动调用 `onChange` 指定的监听函数，这里是`this.handleChange`，`.bind(this)` 表示 _该方法内部的this，绑定当前组件_。

`this.setState` 方法用来重置 `this.state`，每次调用这个方法，就会 _引发组件的重新渲染_。

React 组件的生命周期

React 为组件的不同生命阶段，提供了近十个钩子方法，我们可以利用这些钩子自动完成一些操作：

- `componentWillMount()`：组件加载前调用
- `componentDidMount()`：组件加载后调用
- `componentWillUpdate()`: 组件更新前调用
- `componentDidUpdate()`: 组件更新后调用
- `componentWillUnmount()`：组件卸载前调用
- `componentWillReceiveProps()`：组件接受新的参数时调用

组件可以通过 Ajax 请求，从服务器获取数据。Ajax 请求一般在组件加载后调用，也就是从 `componentDidMount` 方法里面发出：

```jsx
componentDidMount() {
    const url = '...';
    $.getJSON(url)
        .done()
        .fail();
}
```

- `componentDidMount` 方法在组件加载后执行，只执行一次。本例在这个方法里向服务器请求数据，操作结束前，组件都显示Loading。
- `$.getJSON` 方法用于向服务器请求 `JSON` 数据。本例的数据从 Github API 获取，可以打开源码里面的链接，看看原始的数据结构。

React 组件库

React 的一大优势，就是网上有很多已经写好的组件库，可以使用。

```jsx
<LineChart width={1000} height={400} data={data}>
  <XAxis dataKey="name"/>
  <YAxis/>
  <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
  <Line type="monotone" dataKey="uv" stroke="#8884d8" />
  <Line type="monotone" dataKey="pv" stroke="#82ca9d" />
</LineChart>
```

## React 的核心思想

View 是 State 的输出:

`view = f(state)`

上式中， f 表示函数关系，只要 State 发生变化，View 也要随之变化。React 的本质是将图形界面（GUI）函数化

```jsx
const person = {
    name: "micheal",
    age: 31
}

const App = ({ person }) => <h1>{ person.name }</h1>

ReactDOM.render(<App person={person} />, document.body)
```

React 本身只是一个 DOM 的抽象层，使用组件构建虚拟 DOM。如果开发大应用，还需要解决两个问题：

- 架构：大型应用程序应该如何组织代码？
  - React 只是视图层的解决方案，可以用于任何一种架构，那么哪一种架构最适合 React 呢
- 通信：组件之间如何通信？
  - 向子组件发消息
  - 向父组件发消息
  - 向其他组件发消息
  - React 只提供了一种通信手段：传参。对于大应用是很不方便的


React 状态的同步

React 同步状态的基本方法：找到通信双方最近的共同父组件，通过它的 `state`，使得子组件的状态保持同步。


## Flux 架构

Facebook 提出 Flux 架构的概念，被认为是 React 应用的标准架构：

```
Action --> Dispatcher --> Store --> View
```

这种架构最大的特点是数据单向流动，这与 MVVM 的数据双向绑定形成鲜明对比。

Flux 的核心思想是：

- 不同组件的 `state`，存放在一个外部的，公共的 Store 上面
- 组件订阅 Store 的不同部分
- 组件分发（dispatch）动作（action），引发 Store 的更新

Flux 只是一个概念，有 30 多种实现，目前最流行的两个 React 架构是：

- MobX：响应式（Reactive）管理，state 是可变对象，适合中小型项目
- Redux：函数式（Functional）管理，state 是不可变对象，适合大型项目

React 架构的最重要作用就是 _管理 Store 与 View 之间的关系_。

## MobX 简介

MobX 的核心是观察者模式：

- Store 是被观察者（observable）
- 组件是观察者（observer）

一旦 `Store` 有变化，会立刻被组件观察到，从而引发重新渲染。

`@observer` 是一种新的语法，叫做“装饰器”，表示对整个类的行为进行修改，即将 `App` 类作为参数传入 `observer` 函数。这里的意思是，整个 `App` 类都是一个“观察者”，观察 `store` 的变化，只要一有变化，立刻重新渲染：

```jsx
@observer
class App extends React.Component {
  render() {
    // ...
  }
}
```

数据保存在 `Store` 里面。`Store` 的属性分成两种：被观察的属性（`@observable`），和自动计算得到的属性 `@computed`：

```jsx
class Store {
  @observable name = 'Bartek';
  @computed get decorated() {
    return `${this.name} is awesome!`;
  }
}
```

`Store` 的变化由用户引发。组件观察到 `Store` 的变化，自动重新渲染：

```jsx
<div className="index">
<p>
  {this.props.store.decorated}
</p>
<input
  defaultValue={this.props.store.name}
  onChange={
    (event) =>
      this.props.store.name = event.currentTarget.value
  }
/>
</div>
```


## Redux 简介

Redux 有以下核心概念：

- 所有的状态都存放在 `Store` 里，组件每次重新渲染，都必须由状态变化引起
- 用户在 UI 上发出 `action`
- `reducer` 函数接收 `action`，然后根据当前的 `state`，计算出新的 `state`

```
Dispatch    -->    Reducer    --> Store (New State)
{current state}
{action}
```

Redux 应用架构里，Redux 层保存所有状态，React 组件拿到状态以后，渲染出 HTML 代码。

Redux 要求 UI 的渲染组件都是纯组件，即不包括任何状态 (`this.state`) 的组件：

```jsx
// MyComponent 是纯的 UI 组件
<div className="index">
  <p>{this.props.text}</p>
  <input
    defaultValue={this.props.name}
    onChange={this.props.onChange}
  />
</div>
```

进行数据处理、并包含状态的组件，称为“容器组件”。 Redux 使用 `connect` 方法，自动生成 UI 组件对应的“容器组件”。`mapStateToProps` 函数返回一个对象，表示一种映射关系，将 UI 组件的参数映射到 `state`。`mapDispatchToProps` 函数也是返回一个对象，表示一种映射关系，但定义的是哪些用户的操作应该当作 `Action`，传给 `Store`:

```javascript
import { connect } from 'react-redux';
import MyComponent from './myComponent';

// Map Redux state to component props
function mapStateToProps(state) {
  return {
    text: state.text,
    name: state.name
  };
}

// Map Redux actions to component props
function mapDispatchToProps(dispatch) {
  return {
    onChange: (e) => dispatch({
      type: 'change',
      payload: e.target.value
    })
  }
}

// Connected Component
const App = connect(
  mapStateToProps,
  mapDispatchToProps
)(MyComponent);

export default App;
```

reducer 函数用来接收 `action`，算出新的 `state`:

```javascript
function reducer(state = {
  text: '你好，访问者',
  name: '访问者'
}, action) {
  switch (action.type) {
    case 'change':
      return {
        name: action.payload,
        text: '你好，' + action.payload
      };
    default:
      return state;
  }
}

export default reducer;
```

`Store` 由 `Redux` 提供的 `createStore` 方法生成，该方法接受 `reducer` 作为参数:

```jsx
const store = createStore(reducer);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.body.appendChild(document.createElement('div'))
);
```
为了把 `Store` 传入组件，必须使用 `Redux` 提供的 `Provider` 组件在应用的最外面，包裹一层。

