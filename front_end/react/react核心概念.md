# react 的五大核心概念

- 组件
- JSX
- Props & State
- 组件 API
- 组件类型


## React 组件

React组件能够像原生的HTML标签一样输出特定的界面元素，并且也能包括一些元素相关逻辑功能的代码。现在我们一般会用 ES6 的 Class 语法来声明一个 React 组件(也可以用函数声明)：

```jsx
class MyComponent extends React.Component {
    render() {
        return <p>Hello, World!</p>;
    }
}
```

## JSX


## Props & State

只要你对HTML有所了解，应该能够理解 `<a>` 标签的 href 属性是什么意思。延伸到 React 当中，属性就被称作 props（properties的缩写）。组件之间可以通过 Props 进行交互:

```jsx
class ParentComponent extends React.Component {
  render() {
    return <ChildComponent message="Hello World"/>;
  }
}
class ChildComponent extends React.Component {
  render() {
    return <p>And then I said, “{this.props.message}”</p>;
  }
}
```

正因为此，React 当中的数据流是单向的：数据只能从父组件传向子组件。但组件有时不仅需要接受从父组件传来的数据，比如还要处理用户在input当中的输入，这时 state 就派上用场了。要注意，组件的 state 同样也能被传入到子组件中作为子组件 prop 的值。

需要明确的是在 React当中整个数据流都是向下传递的，包括路由、数据层、各个组件等等，从整个应用的 state 中来并汇聚到一起。

在组件中，我们可以通过一个叫 setState 的方法来修改 state，一般在事件处理的方法中调用此方法：

```jsx
class MyComponent extends React.Component {
    handleClick = (e) => {
        this.setState({clicked: true});
    }
    render() {
        return <a href="#" onClick={this.handleClick}>Click me</a>;
    }
}
```


## 组件 API

- render
- setState
- constructor
- 生命周期函数


## 组件类型

用函数定义的组件，无法使用 setState 方法，因此也叫无状态组件：

```jsx
const myComponent = props => {
    return <p>Hello, {props.name}! Today is {new Date()}.</p>
}
```

组件可分为两种角色：

- 展示组件。一种关注 UI 逻辑，用来展示或隐藏内容
- 容器组件。一种关注数据交互，如加载服务器端的数据

```jsx
//presentational component

class CommentList extends React.Component {
  constructor(props) {
    super(props);
  }

  render() { 
    return <ul> {this.props.comments.map(renderComment)} </ul>;
  }

  renderComment({body, author}) {
    return <li>{body}—{author}</li>;
  }
}

//container component

class CommentListContainer extends React.Component {
  constructor() {
    super();
    this.state = { comments: [] }
  }

  componentDidMount() {
    $.ajax({
      url: "/my-comments.json",
      dataType: 'json',
      success: function(comments) {
        this.setState({comments: comments});
      }.bind(this)
    });
  }

  render() {
    return <CommentList comments={this.state.comments} />;
  }
}
```

高阶组件 higher-order components HOCs

可以把高阶组件理解为一个工厂方法，你可以传入一个组件并得到一个 HOC 返回的附加了更多功能的新组件。HOC 不能直接在 render 方法中调用。
