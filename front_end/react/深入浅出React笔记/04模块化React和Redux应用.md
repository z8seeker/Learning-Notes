# React 和 Redux 应用的模块化设计

开始一个新的 React 应用时，要考虑清楚一下事情：

- 代码文件的组织结构
- 确定模块化的边界
- Store 的状态树设计

## 代码文件的组织方式

按角色组织

在 MVC 框架下，一般是把所有的 controller 代码放在 controllers 目录下，把所有的 Model 代码放在 models 目录下，把 View 代码放在 views 目录下。

这种组织方式下，当需要对一个功能进行修改时，需要在不同的目录之间跳转。

按功能组织

Redux 应用适合于“按功能组织”：把完成同一个应用的代码放在一个目录下，一个应用功能包含多个角色的代码。在 Redux 中，不同的角色就是：

- reducer，
- actions 
- 和视图

而应用功能对应的是用户界面上的交互模块。每个基本功能对应一个目录，每个目录下包含同样名字的角色文件：

- actionTypes.js，定义 action 类型
- actions.js，定义 action 的构造函数
- reducer.js，定义这个功能模块如何响应 actions.js 中定义的动作
- views 目录，包含这个功能模块中所有的 React 组件，包括展示组件和容器组件
- index.js，

## 模块接口


