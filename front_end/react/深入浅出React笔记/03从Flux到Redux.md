# 从 Flux 到 Redux

- 单向数据流框架的始祖 Flux
- 后起之秀 Redux
- 结合 React 和 Redux

## Flux

```
Action --> Dispatcher --> Store --> View
              ^                      |
              |                      |
              ------- Action --------
```

- Dispatcher，处理动作分发，维持 Store 之间的依赖关系
- Store，负责存储数据和处理数据相关的逻辑
- Action，驱动 Dispatcher 的 JavaScript 对象
- View，视图部分，负责显示用户界面

与 MVC 框架的比较：

在 MVC 框架中，系统提供的服务通过 Controller 暴露的函数来实现，每增加一个功能，Controller 往往就需要增加一个函数。

而在 Flux 里，当需要新增加功能时，要做的只是增加一种新的 Action 类型，Dispatcher 对外的接口不用改变。

在 Flux 架构下，应用的状态被放在了 store 里，React 组件只是扮演 View 的作用，被动根据 Store 的状态来渲染（React 组件依然可以有自己的状态，但是已经完全沦落为 Store 组件的一个映射，而不是主动变化的数据）。

在 Flux 里，用户的交互操作（点击按钮），引发的是一个“动作”的派发，这个派发的动作会发送给所有的 Store 对象，引起 store 对象的状态改变，而不是直接引发组件的状态改变。

要改变界面 <-- 必须改变 Store 中的状态 <-- 必须派发一个 action 对象

在 Flux 的体系下，驱动界面改变始于一个动作的派发，舍此别无他法，因此，React 组件需要实现一下几个功能：

- 创建时读取 Store 上状态来初始化组件内部状态
- View 如果要改变 Store 状态，必须而且只能派发 action
- 当 Store 上状态发生变化时，组件要立刻同步更新内部状态保持一致

### Flux 的不足

- Store 之间依赖关系，必须用上 Dispatcher 的 waitFor 函数
- 难以进行服务端渲染，Flux 有一个全局的 Dispatcher，然后每一个 Store 都是一个全局唯一的对象
- Store 混杂了逻辑和状态


## Redux 

Redux 在 Flux 的基础上强调了三个基本原则：

- 唯一数据源
- 保持状态只读
- 数据改变只能通过纯函数完成

唯一数据源指的是应用的状态数据应该只存储在唯一的一个 Store 上，Store 上的状态是一个树形的对象。如何 _设计 Store 上状态的结构_ 是 Redux 应用的核心问题。

保持状态只读是指要修改 Store 的状态，必须通过派发一个 action 对象完成。详细的说，改变状态的方法不是去修改状态的值，而是创建一个新的状态对象返回给 Redux，由 Redux 来完成新状态的组装。

数据改变只能通过纯函数完成，这里的纯函数就是 Reducer。

在 Redux 中 每个 reducer 的函数签名：

```
reducer(state, action)
```
reducer 函数返回的结果必须完全由参数 state 和 action 决定，而且不产生任何负作用，也不能修改 state 和 action 对象。


关于 aciton 对象的定义，Redux 应用一般把 action 类型和 action 构造函数分成两个文件定义。

Redux 的 Store 状态设计的一个主要原则是：避免冗余的数据。

在 Redux 框架下，一个 React 组件基本上就是要完成一下两个功能：

- 和 Redux Store 交互。读取 Store 的状态，进行初始化组件的状态，并监听 Store 的状态变化；当 Store 状态改变时，更新组件状态，从而驱动组件重新渲染；当需要更新 Store 状态时，就要派发 action 对象
- 根据当前 props 和 state，渲染出用户界面

 对于上面两个功能，可以考虑拆分组件，让一个组件只专注做一件事情，然后把这两个组件嵌套起来，完成原来一个组件完成的所有任务：

 - 负责和 Redux Store 打交道的组件处于外层，被称为容器组件
 - 负责渲染界面的组件，处于内层，叫做展示组件或无状态组件

 展示组件是纯函数，只需要根据 props 来渲染，不需要 state。那么状态去哪里了呢？状态全都交给容器组件去处理，然后容器组件通过 props 把状态传递给展示组件。

React 支持只用一个函数代表的无状态组件，对于一个只有 render 方法的组件，缩略为一个函数正合适。使用这种写法，获取 props 就不能用 this.props，而要通过函数的参数 props 获取；还有一种惯常写法，就是把解构赋值直接放在参数部分

### 组件 Context

虽然 Redux 应用全局就一个 Store，但在组件中直接导入 Store 是非常不利于组件复用的。React 提供了一个叫 context 的功能，能够完美的解决这个问题：

- 上级组件要宣称自己支持 context，并提供一个函数来返回代表 Context 的对象
- 所有子孙组件只要宣称自己需要这个 context，就可以通过 this.context 访问到这个共同的环境对象

创建一个特殊的 React 组件 `<Provider />` 作为通用 context 的提供者，它的 render 函数就是简单地把子组件渲染出来，此外还要提供一个函数用于返回代表 Context 的对象。

为让 Provider 被 React 认可为一个 Context 的提供者，还需要指定 Provider 的 childContextTypes 属性

### React-Redux

可以从 react-redux 库直接导入：

- `Provider`，提供包含 store 的context
- `connect`，连接包含 store 的 context

connect 方法接受两个参数 mapStateToProps，和 mapDispatchToProps，执行结果仍然是一个函数，将展示组件作为参数传入其中，最后产生的就是容器组件。

connect 函数具体做了什么呢：

- 把 Store 上的状态转化为内层展示组件的 prop
- 把内层展示组件中的用户动作转化为派送给 Store 的动作


react-redux 中的 Provider 要求 store 必须是一个包含三个函数的 object：

- subscribe
- dispatch
- getState
