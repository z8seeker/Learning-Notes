# react 入门


## JSX 语法

利用 JSX 编写 DOM 结构，可以用原生的 HTML 标签，也可以直接像普通标签一样引用 React 组件。这两者约定通过大小写来区分：

- 小写的字符串是 HTML 标签，
- 大写开头的变量是 React 组件。

HTML 里的 `class` 在 JSX 里要写成 `className`，因为 `class` 在 JS 里是保留关键字。同理某些属性比如 `for` 要写成 `htmlFor`。

JSX 的基本语法规则：遇到 HTML 标签（以 `<` 开头），就用 HTML 规则解析；遇到代码块（以 `{` 开头），就用 JavaScript 规则解析。

下面是一个例子：

```jsx
// 使用 html 标签
import React from 'react';
import { render } from 'react-dom';

var myDivElement = <div className="foo" />;
render(myDivElement, document.getElementById('mountNode'));

// 使用组件
import MyComponent from './MyComponet';

var myElement = <MyComponent someProperty={true} />;
render(myElement, document.body);
```

标签或组件的属性值使用表达式表示，只要用 `{}` 替换 `""`，此外，子组件也可以作为表达式使用：

```jsx
var person = <Person name={window.isLoggedIn ? window.name : ''} />;
var content = <Container>{window.isLoggedIn ? <Nav /> : <Login />}</Container>;
```

JSX 允许直接在模板插入 JavaScript 变量。如果这个变量是一个数组，则会展开这个数组的所有成员:

```jsx
var arr = [
    <h1>Hello world!</h1>,
    <h2>React is awesome</h2>,
];
ReactDOM.render(
    <div>{arr}</div>,
    document.getElementById('example')
);
```


在 JSX 里使用注释也很简单，就是沿用 JavaScript，唯一要注意的是在一个组件的 _子元素位置_ 使用注释要用 {} 包起来：

```jsx
var content = (
  <Nav>
      {/* child comment, put {} around */}
      <Person
        /* multi
           line
           comment */
        name={window.isLoggedIn ? window.name : ''} // end of line comment
      />
  </Nav>
);
```

### HTML 转义

React 会将所有要显示到 DOM 的字符串转义，防止 XSS。如果 JSX 中含有转义后的实体字符，可以使用一下几种解决办法：

- 直接使用 UTF-8 字符 ©
- 使用对应字符的 Unicode 编码，查询编码
- 使用数组组装 `<div>{['cc ', <span>&copy;</span>, ' 2015']}</div>`
- 直接插入原始的 HTML

`<div dangerouslySetInnerHTML={{__html: 'cc &copy; 2015'}} />`

### 自定义 HTML 属性

如果在 JSX 中使用的属性不存在于 HTML 的规范中，这个属性会被忽略。如果要使用自定义属性，可以用 `data-` 前缀。

可访问性属性的前缀 `aria-` 也是支持的。


### 属性扩散

有时候你需要给组件设置多个属性，你不想一个个写下这些属性，或者有时候你甚至不知道这些属性的名称，这时候 `spread attributes` 的功能就很有用了：

```jsx
var props = {};
props.foo = x;
props.bar = y;
var component = <Component {...props} />;
```

属性也可以被覆盖，写在后面的属性值会覆盖前面的属性：

```jsx
var props = { foo: 'default' };
var component = <Component {...props} foo={'override'} />;
console.log(component.props.foo); // 'override'
```

`...` 操作符，也叫 spread operator。


## 组件

React 允许将代码封装成组件（component），然后像插入普通 HTML 标签一样，在网页中插入这个组件。`React.createClass` 方法就用于生成一个组件类。

```jsx
var HelloMessage = React.createClass({
    render: function() {
        return <h1>Hello {this.props.name}</h1>;
    }
});

ReactDOM.render(
    <HelloMessage name="John" />,
    document.getElementById('example')
);
```

上面 `HelloMessage` 就是一个组件类。模板插入 `<HelloMessage />` 时，会自动生成 `HelloMessage` 的一个实例。所有组件类都必须有自己的 `render` 方法，用于输出组件。

注意：

- 组件类的第一个字母必须大写，否则将报错
- 组件类只能包含一个顶层标签，否则也将报错

```jsx
// 报错
var HelloMessage = React.createClass({
    render: function() {
        return <h1>
            Hello {this.props.name}
            </h1><p>
                some text
            </p>;
    }
});
```

组件的用法与原生的 HTML 标签完全一致，可以任意加入属性，组件的属性可以在组件类的 `this.props` 对象上获取，比如 `name` 属性就可以通过 `this.props.name` 读取。

添加组件属性，有一个地方需要注意，就是 `class` 属性需要写成 `className` ，`for` 属性需要写成 `htmlFor` ，这是因为 `class` 和 `for` 是 JavaScript 的保留字。


## this.props.children

`this.props` 对象的属性与组件的属性一一对应，但是有一个例外，就是 `this.props.children` 属性。它表示组件的所有子节点:

```jsx
var NotesList = React.createClass({
    render: function() {
        return (
            <ol>
            {
                React.Children.map(this.props.children, function (child) {
                    return <li>{child}</li>;
                })
            }
            </ol>
        );
    }
});

ReactDOM.render(
    <NotesList>
        <span>hello</span>
        <span>world</span>
    </NotesList>,
    document.body
    );
```

`this.props.children` 的值有三种可能：

- 如果当前组件没有子节点，它就是 `undefined` ;
- 如果有一个子节点，数据类型是 `object` ；
- 如果有多个子节点，数据类型就是 `array` 。

所以，处理 `this.props.children` 的时候要小心。React 提供一个工具方法 `React.Children` 来处理 `this.props.children` 。我们可以用 `React.Children.map` 来遍历子节点，而不用担心 `this.props.children` 的数据类型是 `undefined` 还是 `object`。


## PropTypes

组件类的 `PropTypes` 属性，可以用来验证组件实例的属性是否符合要求：

```jsx
var MyTitle = React.createClass({
    propTypes: {
        title: React.PropTypes.string.isRequired,
    },

render: function() {
    return <h1> {this.props.title} </h1>;
    }
});
```

上面的 `Mytitle` 组件有一个 `title` 属性。`PropTypes` 告诉 React，这个 `title` 属性是必须的，而且它的值必须是字符串。

此外，`getDefaultProps` 方法可以用来设置组件属性的默认值:

```jsx

var MyTitle = React.createClass({
    getDefaultProps : function () {
        return {
          title : 'Hello World'
        };
    },

    render: function() {
         return <h1> {this.props.title} </h1>;
    }
});

ReactDOM.render(
    <MyTitle />,
    document.body
);
```


## 获取真实的 DOM 节点

组件并不是真实的 DOM 节点，而是存在于内存之中的一种 _数据结构_，叫做虚拟 DOM （virtual DOM），只有当它插入文档以后，才会变成真实的 DOM。

根据 React 的设计，所有的 DOM 变动，都先在虚拟 DOM 上发生，然后再将实际发生变动的部分，反映在真实 DOM上，这种算法叫做 `DOM diff` ，它可以极大提高网页的性能表现。

但是，有时需要从组件获取真实 DOM 的节点，这时就要用到 `ref` 属性:

```jsx
var MyComponent = React.createClass({
    handleClick: function() {
        this.refs.myTextInput.focus();
    },
    render: function() {
        return (
            <div>
                <input type="text" ref="myTextInput" />
                <input type="button" value="Focus the text input" onClick={this.handleClick} />
            </div>
        );
    }
});

ReactDOM.render(
    <MyComponent />,
    document.getElementById('example')
);
```

文本输入框必须有一个 `ref` 属性，然后 `this.refs.[refName]` 就会返回这个真实的 DOM 节点。由于 `this.refs.[refName]` 属性获取的是真实 DOM ，所以必须等到虚拟 DOM 插入文档以后，才能使用这个属性，否则会报错。


## this.state

组件免不了要与用户互动，react 将组件看成是一个状态机，一开始有一个初始状态，然后用户互动导致状态变化，从而触发重新渲染 UI。

```jsx
var LikeButton = React.createClass({
    getInitialState: function() {
        return {liked: false};
    },
    handleClick: function(event) {
        this.setState({liked: !this.state.liked});
    },
    render: function() {
        var text = this.state.liked ? 'like' : 'haven\'t liked';
        return (
            <p onClick={this.handleClick}>
                You {text} this. Click to toggle.
            </p>
        );
    }
});

ReactDOM.render(
    <LikeButton />,
    document.getElementById('example')
);
```

`getInitialState` 方法用于定义初始状态，也就是一个对象，这个对象可以通过 `this.state` 属性读取。当用户点击组件，导致状态变化，`this.setState` 方法就修改状态值，每次修改以后，自动调用 `this.render` 方法，再次渲染组件。

`this.props` 和 `this.state` 都用于描述组件的特性:

- `this.props` 表示那些一旦定义，就不再改变的特性
- `this.state` 是会随着用户互动而产生变化的特性


## 表单

用户在表单填入的内容，属于用户根组件的互动，所以不能用 `this.props` 读取：

```jsx
var Input = React.createClass({
    getInitialState: function() {
        return {value: 'Hello!'};
    },
    handleChange: function(event) {
        this.setState({value: event.target.value});
    },
    render: function () {
        let value = this.state.value;
        return (
            <div>
                <input type="text" value={value} onChange={this.handleChange} />
                <p>{value}</p>
            </div>
        );
    }
});

ReactDOM.render(<Input/>, document.getElementById('example'));
```

文本输入框的值，不能用 `this.props.value` 读取，而要定义一个 `onChange` 事件的回调函数，通过 `event.target.value` 读取用户输入的值。`textarea` 元素、`select` 元素、`radio` 元素都属于这种情况。

注意：

对于数据的流向，React是强制单向数据流的，也就是说，数据只能由状态单向得传递到视图层，而不能直接由视图层传回来，视图层对状态的影响只能通过绑定事件来实现。这可以预防双向绑定带来的状态预测困难问题，当然，双向绑定也有其好处，但个人认为其好处是远小于负面影响的。 


## 组件的生命周期

组件的生命周期可分为三个状态：

- Mounting: 已插入真实 DOM
- Updating: 正在被重写渲染
- Unmounting: 已移出真实 DOM

React 为每个状态都提供了两种处理函数，`will` 函数在进入状态之前调用，`did` 函数在进入状态之后调用，三种状态共计五种处理函数。此外，React 还提供两种特殊状态的处理函数：

- `componentWillReceiveProps(object nextProps)`，已加载组件收到新的参数时调用
- `shouldComponentUpdate(object nextProps, object nextState)`，组件判断是否重新渲染时调用

下面是一个例子：

```jsx

var Hello = React.createClass({
    getInitialState: function () {
        return {
            opacity: 1.0
        };
    },

    componentDidMount: function () {
        this.timer = setInterval(function () {
            var opacity = this.state.opacity;
            opacity -= .05;
            if (opacity < 0.1) {
                opacity = 1.0;
            }
            this.setState({
                opacity: opacity
            });
        }.bind(this), 100);
    },

    render: function () {
        return (
            <div style={{opacity: this.state.opacity}}>
            Hello {this.props.name}
            </div>
        );
    }
});

ReactDOM.render(
    <Hello name="world"/>,
    document.body
);
```

上面代码在 `hello` 组件加载以后，通过 `componentDidMount` 方法设置一个定时器，每隔100毫秒，就重新设置组件的透明度，从而引发重新渲染。

另外，组件的 style 属性的设置方式也值得注意，React 组件样式是一个对象，所以 _第一重大括号_ 表示这是 JavaScript 语法，_第二重大括号_ 表示样式对象。


## Ajax

组件的数据来源，通常是通过 Ajax 请求从服务器获取，可以使用 `componentDidMount` 方法设置 Ajax 请求，等到请求成功，再用 `this.setState` 方法重新渲染 UI :

```jsx
var UserGist = React.createClass({
    getInitialState: function () {
        return {
            username: '',
            lastGistUrl: ''
        };
    },

    componentDidMount: function () {
        $.get(this.props.source, function (result) {
            var lastGist = result[0];
            this.setState({
                username: lastGist.owner.login,
                lastGistUrl: lastGist.html_url
            });
        }.bind(this));
    },

    render: function () {
        return (
            <div>
                {this.state.username}'s last gist is <a href={this.state.lastGistUrl}>here</a>.
            </div>
        );
    }
});

ReactDOM.render(
    <UserGist source="https://api.github.com/users/octocat/gists"/>,
        document.getElementById('example')
);
```

我们甚至还可以把一个 `Promise` 对象传入组件:

```jsx
var RepoList = React.createClass({
    getInitialState: function () {
        return {
            loading: true,
            error: null,
            data: null
        };
    },

    componentDidMount() {
        this.props.promise.then(
            value => this.setState({loading: false, data: value}),
            error => this.setState({loading: false, error: error}));
    },

    render: function () {
        if (this.state.loading) {
            return <span>Loading...</span>;
        }
        else if (this.state.error !== null) {
            return <span>Error: {this.state.error.message}</span>;
        }
        else {
            var repos = this.state.data.items;
            var repoList = repos.map(function (repo, index) {
                return (
                    <li key={index}><a
                        href={repo.html_url}>{repo.name}</a> ({repo.stargazers_count} stars) <br/> {repo.description}
                    </li>
                );
            });
            return (
                <main>
                    <h1>Most Popular JavaScript Projects in Github</h1>
                    <ol>{repoList}</ol>
                </main>
            );
        }
    }
});

ReactDOM.render(
    <RepoList promise={$.getJSON('https://api.github.com/search/repositories?q=javascript&sort=stars')}/>,
    document.getElementById('example')
);
```

如果Promise对象正在抓取数据（pending状态），组件显示"正在加载"；如果Promise对象报错（rejected状态），组件显示报错信息；如果Promise对象抓取数据成功（fulfilled状态），组件显示获取的数据。
