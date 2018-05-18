# 使用 web Storage API

## 基本概念

Storage 对象是简单的键值对存储，键和值都是字符串。可以像对象那样获取一个值，或者使用 `Storage.getItem()` 和 `Storage.setItem()` 方法，下面三种方法都是可以的：

```javascript
localStorage.colorSetting = '#a4509b';
localStorage['colorSetting'] = '#a4509b';
localStorage.setItem('colorSetting') = '#a4509b';
```

注意：推荐使用 Web Storage API 包括 `setItem`, `getItem`, `removeItem`, `key`, `length`

Web Storage 中有两种机制：

- `sessionStorage`，对于每一个给定的源，会维护一个独立的存储区域（只要浏览器保持开启状态，包括页面重载和恢复）
- `localStorage`，和 `sessionStorage` 的功能类似，但会一直保持这个存储区域，即使浏览器被关闭和重启


## Web Storage 的使用场景

