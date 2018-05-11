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