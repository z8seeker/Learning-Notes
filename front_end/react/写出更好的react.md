
## propTypes 和 defaultProps

确保使用了 `props` 的每个组件都声明了 `propTypes` 和 `defaultProps`，这对写出更好的 React 代码很有帮助。

当 `props` 实际获取的数据和期望的不同时，错误日志就会让你知道：要么是你传递了错误的数据，要么就是没有得到期望值，特别是写可重用组件时，找出错误会更容易。这也会让这些可重用组件更可读一些。

```jsx
static propTypes = {
    userIsLoaded: PropTypes.boolean.isReuqired,
    user: PropTypes.shape({
        _id: PropTypes.string,
    }).isRequired,
}
```

如果我们声明 `userIsLoaded` 不是必需的值，那么我们就要为它定义一个 _默认值_。如果是必需的，就没有必要定义默认值。但是，规则还指出不应该使用像对象或数组这样不明确的 `propTypes`。

[了解更多 prop-types 的用法](https://www.npmjs.com/package/prop-types)


## 何时创建新组件

当考虑是否需要创建新组件时，问自己下面几个问题：

- 代码的功能变得笨重了吗？
- 它是否只代表了自己的东西？
- 是否需要重用这部分代码？

如果上面有一个问题的答案是肯定的，那你就需要创建一个新组件了。

```jsx
export default class Profile extends PureComponent {
    static propTypes = {
        userIsLoaded: PropTypes.bool,
        user: PropTypes.shape({
            _id: PropTypes.string,
        }).isReuqired,
    }

    static defaultProps = {
        userIsLoaded: false,
    }

    render() {
        const { userIsLoaded, user } = this.props;
        if (!userIsloaded) return <Loaded />;
        return (
            <div>
                <div className="two-col">
                    <section>
                        <MyOrders userId={user._id} />
                        <MyDownloads userId={user._id} />
                    </section>
                    <aside>
                        <MySubscriptions user={user} />
                        <MyVotes user={user} />
                    </aside>
                </div>
                <div className="one-col">
                    {isRole('affiliate', user={user._id}) &&
                        <MyAffiliateInfo userId={user._id} />
                    }
                </div>
            </div>
        )
    }
}
```

上面是一个名为 `Profile` 的组件。这个组件内部还有一些像 `MyOrder` 和 `MyDownloads` 这样的其它组件。因为它们从同一个数据源（`user`）获取数据，所以可以把所有这些组件写到一起。把这些小组件变成一个巨大的组件。

## Component vs PureComponent vs Stateless Functional Component

无状态函数式组件，为我们提供了一种非常简洁的方式来创建不使用任何 `state`、`refs` 或 `生命周期方法` 的组件。

无状态函数式组件的特点是没有状态并且只有一个函数。简单来说，无状态函数式组件就是返回 JSX 的函数：

```jsx
const Billboard = () => (
    <ZoneBlack>
        <Heading>React</Heading>
        <div className="billboard_product">
            <Link className="billboard_product-image" to="/">
                <img alt="#" src="#">
            </Link>
            <div className="billboard_product-details">
                <h3 className="sub">React</h3>
                <p>Lorem Ipsum</p>
            </div>
        </div>
    </ZoneBlack>
);
```

PureComponents

通常，一个组件获取了新的 `prop`，React 就会重新渲染这个组件。但有时，新传入的 `prop` 并没有真正改变，React 还是触发重新渲染。使用 `PureComponent` 可以避免这种重新渲染的浪费。

例如，一个 `prop` 是字符串或布尔值，它改变后，`PureComponent` 会识别到这个改变，但如果 `prop` 是一个对象，它的属性改变后，`PureComponent` 则不会触发重新渲染。

如果一个组件经常在更新时发生变化，那么 `PureComponent` 将会执行两次 diff 检查而不是一次（`props` 和 `state` 在 `shouldComponentUpdate` 中进行的严格相等比较，以及常规的元素 diff 检查）。这意味着通常它会变慢，偶尔会变快。



## 使用 React 开发者工具

通过 React 开发者工具，你可以看到整个应用结构和应用中正在使用的 props 和 state。

## 使用内联条件语句

使用内联条件语句非常简洁，可以明显简化 React 代码：

```jsx
<div className="one-col">
  {isRole('affiliate', user._id) &&
    <MyAffiliateInfo userId={user._id} />
  }
</div>
```

## 了解 React 如何工作

[React Internals](http://www.mattgreer.org/articles/react-internals-part-one-basic-rendering/)



## react 与 immutable

如果两个对象是不可变的，那么比较他们是否相等比较容易。React 就是利用了这个概念来进行性能优化的。

React 会对现在和更新前版本的虚拟 DOM 进行比较，来找出哪些改变了。这就是 __一致性比较__ 的过程。

这样，就只有有变化的元素会在真实 DOM 中更新。有时，一些 DOM 元素自身没变化，但会被其他元素影响，造成重新渲染。这种情况下，你可以通过 `shouldComponentUpdate` 方法来判断属性和方法是不是真的改变了，是否返回 `true` 来更新这个组件：



## react 最佳实践

### 组件中的 `bind()` 与箭头函数

在使用自定义函数作为组件属性之前将你的自定义函数写在 `constructor` 中，并进行绑定：

```jsx
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: ''
        };
        this.updateValue = this.updateValue.bind(this);
    }

    updateValue(evt) {
        this.setState({
            name: evt.target.value
        });
    }

    render() {
        return (
            <form>
                <input onChange={this.updateValue} value={this.state.name} />
            </form>
        )
    }

}
```

不建议的写法：

```jsx
<input onChange={this.updateValue.bind(this)} value={this.state.name} />
```

```jsx
<input onChange={ (evt) => this.setState({name: evt.target.value}) } value={this.state.name} />
```

这两种方法会导致每次 `render` __函数执行时都会创建一个新函数__，这会对性能造成一些影响。

### 在 key prop 中使用索引

遍历元素集合时，key 是必不可少的 prop。key 是用来帮助 React 轻松调和虚拟 DOM 与真实 DOM 间的差异的。key 应该是稳定，唯一，可预测的：

- 唯一的， 元素的 key 在它的兄弟元素中应该是唯一的。没有必要拥有全局唯一的 key。
- 稳定的， 元素的 key 不应随着时间，页面刷新或是元素重新排序而变。
- 可预测的，你可以在需要时拿到同样的 key，意思是 key 不应是随机生成的。

数组索引是唯一且可预测的。然而，并不稳定；由于随机数既不唯一也不稳定，使用随机数就相当于根本没有使用 key；时间戳既不稳定也不可预测。

通常，你应该依赖于数据库生成的 `ID` 如关系数据库的主键，Mongo 中的对象 ID。如果数据库 ID 不可用，你可以生成内容的哈希值来作为 key。

### setState 是异步的

React 组件主要由三部分组成：

- `state`，
- `props` 
- 标记（或其它组件）。

`props` 是不可变的，`state` 是可变的。`state` 的改变会导致组件重新渲染。如果 `state` 是由组件在内部管理的，则使用 `this.setState` 来更新 `state`。

注意：

由于 `this.props` 和 `this.state` 是异步更新的，你不应该依赖它们的值来计算下一个 `state`:

```jsx
this.setState({
    counter: this.state.counter + this.props.increment;
})
```

正确的方法是给 `setState` 传入一个接收 `currentState` 和 `currentProps` 作为参数的函数，这个函数的返回值会与当前 state 合并以形成新的 state:

```jsx
this.setState((prevState, props) => ({
    counter: prevState.counter + props.increment
}));
```

### 初始值中的 props

`constructor（getInitialState)` 仅仅在组件创建阶段被调用。也就是说，`constructor` 只被调用一次：

```jsx
import React, { Component } from 'react'

class MyComponent extends Component {
    constructor(props){
        super(props);
        this.state = {
            someValue: props.someValue,
        };
    }
}
```

因此，当你下一次改变 `props` 时，`state` 并不会更新，它仍然保持为之前的值。

正确的方法：

如果需要特定的行为即你希望 `state` 仅由 `props` 的值生成一次的话可以使用这种模式。

`state` 将由组件在内部管理。

在另一个场景下，可以通过生命周期方法 `componentWillReceiveProps` 保持 `state` 与 `props` 的同步:

```jsx
import React, { Component } from 'react'

class MyComponent extends Component {
    constructor(props){
        super(props);
        this.state = {
            someValue: props.someValue,
        };
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.inputValue !== this.props.inputValue) {
            this.setState({ inputVal: nextProps.inputValue })
        }
    }
}
```

最佳方法是使用状态管理库如 Redux 去 `connect` state 组件。

### 组件命名

在 React 中，如果你想使用 JSX 渲染你的组件，组件名必须以大写字母开头。但是也要明白，声明组件时无需遵从这一规则。因此，可以这样写：

```jsx
// 在这里以小写字母开头是可以的
class primaryButton extends Component {
  render() {
    return <div />;
  }
}

export default primaryButton;

// 在另一个文件中引入这个按钮组件。要确保以大写字母开头的名字引入。

import PrimaryButton from 'primaryButton';

<PrimaryButton />
```

