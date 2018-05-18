# 使用 react-router

React-Router 是官方维护的路由库，它通过管理 URL，实现组件的切换和状态的变化，开发复杂的应用几乎肯定会用到。

使用时  路由器 `Router` 就是 React 的一个组件。 `Router` 组件本身只是一个容器，真正的路由要通过 `Route` 组件来定义

```javascript
import {Router, Route, hashHistory} from 'react-router'

render((
    <Router history={hashHistory}>
        <Route path="/" component={App}/>
    </Router>
), document.getElementById('app'));
```

用户访问根路由 `/` 时，组件 `App` 就会加载到 `document.getElementById('app')`


## react-router v4

### 包容性路由

V4 的路由默认为“包含”的，这意味着多个 <Route> 可以同时进行匹配和渲染：

```jsx
const PrimaryLayout = () => (
  <div className="primary-layout">
    <header>
      Our React Router 4 App
      <Route path="/users" component={UsersMenu} />
    </header>
    <main>
      <Route path="/" exact component={HomePage} />
      <Route path="/users" component={UsersPage} />
    </main>
  </div>
)
```

当用户访问 `/users` 时，UserMenu 和  UsersPage 两个组件都会被渲染。


### 排他性路由

如果只需要在路由列表里匹配一个路由，则使用 `<Switch>` 来启用排他路由：

```jsx
const PrimaryLayout = () => (
  <div className="primary-layout">
    <PrimaryHeader />
    <main>
      <Switch>
        <Route path="/" exact component={HomePage} />
        <Route path="/users/add" component={UserAddPage} />
        <Route path="/users" component={UsersPage} />
        <Redirect to="/" />
      </Switch>
    </main>
  </div>
)
```

在 `HomePage` 路由上，我们仍然需要 `exact` 属性，尽管我们会先把它列出来。否则，当访问诸如 `/users` 或 `/users/add` 的路径时，主页路由也将匹配。
事实上，战略布局是使用排他路由策略（因为它总是像传统路由那样使用）时的关键。
注意：我们在 `/users` 之前策略性地放置了 `/users/add` 的路由，以确保正确匹配。由于路径 `/users/add` 将匹配 `/users` 和 `/users/add`，所以最好先把 `/users/add` 放在前面。

如果遇到，`<Redirect>` 组件将会始终执行浏览器重定向，但是当它位于 `<Switch>` 语句中时，只有在其他路由不匹配的情况下，才会渲染重定向组件。


### “默认路由”和“未找到”

尽管在 v4 中已经没有 `<IndexRoute>` 了，但可以使用 `<Route exact>` 来达到同样的效果。


### 嵌套布局

首先了解一个新 API 概念：`props.match`

`props.match` 被赋到由 `<Route>` 渲染的任何组件。你可以看到，`userId` 是由 `props.match.params` 提供的。如果任何组件需要访问 `props.match`，而这个组件没有由 `<Route>` 直接渲染，那么我们可以使用 `withRouter()` 高阶组件。

```jsx
const PrimaryLayout = props => {
  return (
    <div className="primary-layout">
      <PrimaryHeader />
      <main>
        <Switch>
          <Route path="/" exact component={HomePage} />
          <Route path="/users" component={UserSubLayout} />
          <Route path="/products" component={ProductSubLayout} />
          <Redirect to="/" />
        </Switch>
      </main>
    </div>
  )
}
```

注意: 上述示例中 `/users` 和 `products` 没有使用 `exact` 属性，因为我们希望 `/users` 匹配任何以 `/users` 开头的路由，同样适用于 `/products`。


我们在布局结构中深入嵌套时，路由仍然需要识别它们的完整路径才能匹配。为了节省重复输入（以防你决定将“用户”改为其他内容），我们可以改用 `props.match.path`

```jsx
const UserSubLayout = props => (
  <div className="user-sub-layout">
    <aside>
      <UserNav />
    </aside>
    <div className="primary-content">
      <Switch>
        <Route path={props.match.path} exact component={BrowseUsersPage} />
        <Route path={`${props.match.path}/:userId`} component={UserProfilePage} />
      </Switch>
    </div>
  </div>
)
```

### 匹配

props.match 有几个常见的属性：

- props.match.path
- props.match.params
- props.match.url


`match.url` 是浏览器 URL 中的实际路径，而 `match.path` 是为路由编写的路径。应该选择使用 `match.path` 来构建路由路径。文档中说：

- path，用于匹配路径模式，用于构建嵌套的 `<Route>`
- url, URL 匹配的部分，用于构建嵌套的 `<Link>`

避免匹配冲突：

我们希望能够通过访问 `/users/add` 和 `/users/5/edit` 来新增和编辑用户。如果 `users/:userId` 已经指向了 `UserProfilePage`。那么这是否意味着带有 `users/:userId` 的路由现在需要指向另一个子布局来容纳编辑页面和详情页面？不需要这么做，因为 _编辑和详情页面共享相同的用户子布局_，所以下面这个策略是可行的：

```jsx
const UserSubLayout = ({ match }) => (
    <div className="user-sub-layout">
      <aside>
        <UserNav />
      </aside>
      <div className="primary-content">
        <Switch>
          <Route exact path={props.match.path} component={BrowseUsersPage} />
          <Route path={`${match.path}/add`} component={AddUserPage} />
          <Route path={`${match.path}/:userId/edit`} component={EditUserPage} />
          <Route path={`${match.path}/:userId`} component={UserProfilePage} />
        </Switch>
      </div>
    </div>
)
```

注意：

- 为了确保进行适当的匹配，新增和编辑路由需要放在详情路由之前。如果详情路径在前面，那么访问 `/users/add` 时将匹配详情（因为 "add" 将匹配 `:userId`）。
- 或者，如果我们这样创建路径 `${match.path}/:userId(\\d+)`，来确保 `:userId` 必须是一个数字，那么我们就可以先放置详情路由。然后访问 `/users/add` 将不会产生冲突


### 授权路由

v4 中一个惊人的新功能是能够为特定的目的创建你自己的路由。它不是将 `component` 的属性传递给 `<Route>`，而是传递一个 `render` 回调函数：

```jsx
class AuthorizedRoute extends React.Component {
    ComponentWillMount() {
        logged_user()
    }

    render() {
        const { component: Component, pending, logged, ...rest } = this.props
        return (
            <Route {...rest} render={props => {
                if (pending) return <div>Loading...</div>
                return logged
                  ? <Component {...this.props} />
                  : <Redirect to="/auth/login" />
            }} />
        )
    }
}

const stateToProps = ({ loggedUserState }) => ({
    pending: loggedUserState.pending,
    logged: loggedUserState.logged
})

export default connect(stateToProps)(AuthorizedRoute)
```

这里使用网络请求来获得 `logged_user()`, 并将 pending 和 logged 插入 Redux 的状态中。

