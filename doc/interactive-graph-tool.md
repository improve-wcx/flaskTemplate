# 交互式架构关系图可视化工具

**版本**: 1.0  
**最后更新**: 2026-03-16

---

## 1. 项目概述

### 1.1 项目目标

开发一个 **基于 Web 的交互式架构图可视化工具**，用于展示和维护系统组件之间的依赖关系。

该工具通过 **简单 JSON 数据** 描述图结构，并在网页中进行 **可视化展示与交互编辑**，适用于：

- 系统架构关系展示
- 模块调用关系分析
- 组件依赖维护
- 技术架构文档可视化

### 1.2 典型使用场景

- 浏览器架构（如 Chromium）
- 微服务调用关系
- 组件依赖图
- 软件模块结构

### 1.3 项目特点

- ✅ **纯前端实现** - 无需后端 API 支持
- ✅ **交互式编辑** - 可视化 CRUD 操作
- ✅ **力导向布局** - 自动优化节点位置
- ✅ **JSON 数据** - 简单易懂的数据格式
- ✅ **即开即用** - 单 HTML 文件，无依赖

---

## 2. 访问方式

### 2.1 Web 界面

```
GET /relationship-map
```

访问后可以看到：
- 交互式架构图画布
- 组件编辑器侧边栏
- 数据导入/导出功能

### 2.2 文件位置

- **源文件**: `app/static/html/releationships_map.html`
- **路由**: `app/routes/rel_map.py`
- **访问 URL**: `http://127.0.0.1:5000/relationship-map`

---

## 3. 功能特性

### 3.1 图结构可视化

- ✅ 力导向图自动布局
- ✅ 拖拽调整节点位置
- ✅ 动态连线显示关系
- ✅ 箭头指示依赖方向
- ✅ 节点自动分散，减少重叠

### 3.2 节点管理（CRUD）

- ✅ 添加新组件
- ✅ 编辑组件关系
- ✅ 删除组件
- ✅ 实时更新视图
- ✅ 点击节点自动填充编辑器

### 3.3 关系管理

- ✅ 定义节点间的依赖关系
- ✅ 自动清理无效引用
- ✅ 有向箭头显示关系方向

### 3.4 数据管理

- ✅ 导出为 JSON 文件
- ✅ 从 JSON 文件导入
- ✅ 本地数据操作
- ✅ 数据校验和错误提示

---

## 4. 数据模型设计

### 4.1 节点数据结构

系统使用 **JSON 数组** 表示整个图结构。每个节点结构如下：

```json
{
  "name": "NodeName",
  "relationships": ["TargetNode1", "TargetNode2"]
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | String | 节点唯一名称（全局唯一标识符） |
| `relationships` | String[] | 指向的下游节点列表 |

### 4.2 节点唯一性

- `name` 作为 **全局唯一标识符**
- 系统 **不使用 id 字段**
- 名称不能重复

### 4.3 关系语义

`relationships` 表示：

```
当前节点 → 下游节点
```

**示例**:

```json
{
  "name": "Browser",
  "relationships": ["Renderer", "Network"]
}
```

表示：

```
Browser → Renderer
Browser → Network
```

### 4.4 数据纯净性要求

导入导出数据 **必须保持纯净**，只允许以下字段：

**允许字段**:
- `name`
- `relationships`

**禁止字段**（运行时布局信息）:
- `x`, `y` (坐标)
- `index` (索引)
- `vx`, `vy` (速度)
- `fx`, `fy` (固定位置)

---

## 5. 可视化设计

### 5.1 节点样式

节点使用 **矩形结构**，要求：

- 节点为矩形
- 矩形宽度根据 `name` 自动调整
- 节点文字居中
- 节点具有背景颜色
- 每个节点颜色可区分

**示意**:

```
┌─────────────┐
│   Browser   │
└─────────────┘
```

### 5.2 节点尺寸

矩形宽度规则：

```
width = name 长度 × 字符宽度 + padding
```

高度固定。

### 5.3 关系连线

关系使用 **带箭头的有向边**，表现规则：

- 直线连接
- 箭头指向 **目标节点**
- 箭头终点 **贴近目标节点边缘**

**示意**:

```
A ─────▶ B
```

### 5.4 颜色策略

**节点颜色**:
- 每个节点具有独特的背景色
- 使用 D3.js 的色板（Tableau 10）

**连线颜色**:
- 根据 **目标节点** 进行区分
- 指向同一节点的所有连线颜色一致

---

## 6. 布局系统

### 6.1 布局算法

系统使用 **力导向布局（Force-directed layout）**，特点：

- 节点自动分散
- 自动减少重叠
- 自动形成可读结构
- 节点之间具有排斥力
- 连线具有拉力
- 系统自动居中

### 6.2 布局行为

| 行为 | 说明 |
|------|------|
| 节点拖拽 | 用户可以拖拽节点改变位置 |
| 连线更新 | 拖拽时连线实时更新 |
| 箭头更新 | 拖拽时箭头实时更新 |

---

## 7. 交互功能

### 7.1 节点拖拽

用户可以拖拽节点改变位置，要求：

- ✅ 节点可自由拖动
- ✅ 连线实时更新
- ✅ 箭头实时更新

### 7.2 节点选择

点击节点后，系统自动：

- ✅ 选中节点
- ✅ 在侧边栏显示节点信息
- ✅ 填充 `name` 和 `relationships` 字段

---

## 8. 节点管理（CRUD）

### 8.1 新增节点

**用户输入**:
- 节点名称
- relationships（逗号分隔）

**点击"保存数据"**:
- 若节点不存在 → 新建节点
- 若节点已存在 → 更新节点

### 8.2 更新节点

**修改步骤**:
1. 点击节点或手动输入
2. 修改 `relationships` 字段
3. 点击"保存数据"

**行为**:
- 更新节点关系
- 重新渲染图结构

### 8.3 删除节点

**删除步骤**:
1. 选中节点（点击）
2. 点击"删除节点"

**系统行为**:
1. 从节点列表删除
2. 清理其他节点中的引用

**示例**:

删除前:
```
A → B
C → B
```

删除 B 后:
```
A
C
```

### 8.4 查询节点

**查询方式**: 点击节点

**系统行为**:
- 在表单中显示节点信息
- 自动填充 `name` 和 `relationships`

---

## 9. 数据导入导出

### 9.1 JSON 导出

**操作**: 点击"导出 JSON"

**导出要求**:
- 数据格式化（缩进 2 空格）
- UTF-8 编码
- 文件名：`architecture_map.json` 或 `graph.json`

**导出内容**: 纯净的节点数据（不含布局信息）

### 9.2 JSON 导入

**操作流程**:
1. 点击"导入 JSON"
2. 选择本地 JSON 文件
3. 系统解析 JSON
4. 更新数据
5. 重新生成布局

### 9.3 数据校验

导入数据必须满足：

- ✅ JSON 格式正确
- ✅ 节点包含 `name` 字段
- ✅ `relationships` 为数组
- ✅ 节点名称唯一

**错误处理**:
- 格式错误 → 显示错误提示
- 数据无效 → 保持原数据不变

---

## 10. 用户界面结构

### 10.1 页面布局

```
+----------------------------------+------------------+
|                                  |                  |
|                                  |  组件编辑器      |
|                                  |                  |
|         Graph Canvas             |  +------------+  |
|                                  |  | 节点名称   |  |
|    (力导向图可视化区域)           |  | relationships| |
|                                  |  +------------+  |
|                                  |                  |
|                                  |  [保存数据]      |
|                                  |  [删除节点]      |
|                                  |                  |
|                                  |  [导出 JSON]     |
|                                  |  [导入 JSON]     |
|                                  |                  |
+----------------------------------+------------------+
```

### 10.2 图形区域

用于显示：
- 节点（矩形）
- 关系连线（带箭头）
- 箭头方向

### 10.3 侧边栏

**节点编辑表单**:
- 字段：`name`, `relationships`
- 按钮：保存数据、删除节点

**数据管理**:
- 按钮：导出 JSON、导入 JSON

**状态消息**:
- 操作成功/失败提示
- 自动消失（3 秒）

---

## 11. 使用步骤

### 11.1 添加组件

1. 在"组件名称"输入框输入组件名（如：`WebApp`）
2. 在"下游组件"输入依赖（如：`Database, Cache`）
3. 点击"保存数据"

### 11.2 编辑组件

1. 点击画布上的节点
2. 编辑器自动填充该节点信息
3. 修改内容后点击"保存数据"

### 11.3 删除组件

1. 选中节点（点击）
2. 点击"删除节点"

### 11.4 导出数据

1. 点击"导出 JSON"
2. 文件自动下载到本地

### 11.5 导入数据

1. 点击"导入 JSON"
2. 选择本地 JSON 文件
3. 画布自动更新

---

## 12. 技术实现

### 12.1 技术栈

**前端**:
- HTML5
- CSS3
- JavaScript (ES6+)
- **D3.js v7** (可视化库)

**后端**:
- Flask (仅提供静态文件服务)
- 无 API 接口

### 12.2 D3.js 功能用途

| 功能 | D3 模块 |
|------|--------|
| 力导向布局 | `d3.forceSimulation` |
| 连线渲染 | `d3.forceLink` |
| 节点排斥 | `d3.forceManyBody` |
| 中心定位 | `d3.forceCenter` |
| 拖拽交互 | `d3.drag` |
| 箭头标记 | SVG `<marker>` |

### 12.3 代码结构

```html
<!DOCTYPE html>
<html>
<head>
  <script src="d3.v7.min.js"></script>
  <style>...</style>
</head>
<body>
  <div id="sidebar">...</div>
  <div id="canvas-container">
    <svg id="chart"></svg>
  </div>
  <script>
    // 数据
    let rawData = [...]
    
    // 初始化 D3
    const svg = d3.select("#chart")
    const simulation = d3.forceSimulation(...)
    
    // 更新图
    function updateGraph() { ... }
    
    // 交互函数
    function saveNode() { ... }
    function deleteNode() { ... }
    function exportCleanJSON() { ... }
    function importJSON(input) { ... }
  </script>
</body>
</html>
```

---

## 13. 示例数据

### 13.1 Chrome 浏览器架构（预置）

```json
[
  {
    "name": "BrowserMain",
    "relationships": ["NetworkService", "StoragePartition"]
  },
  {
    "name": "NetworkService",
    "relationships": ["MojoIPC"]
  },
  {
    "name": "StoragePartition",
    "relationships": ["SQLiteCookieStore"]
  },
  {
    "name": "MojoIPC",
    "relationships": ["BrowserMain"]
  },
  {
    "name": "SQLiteCookieStore",
    "relationships": []
  }
]
```

**可视化结构**:

```
BrowserMain ───▶ NetworkService ───▶ MojoIPC ───┐
    │                                              │
    └──▶ StoragePartition ───▶ SQLiteCookieStore  │
                                                   │
                    └──────────────────────────────┘
```

### 13.2 微服务架构示例

```json
[
  {
    "name": "API Gateway",
    "relationships": ["AuthService", "UserService", "OrderService"]
  },
  {
    "name": "AuthService",
    "relationships": ["UserDB", "Redis"]
  },
  {
    "name": "UserService",
    "relationships": ["UserDB"]
  },
  {
    "name": "OrderService",
    "relationships": ["OrderDB", "PaymentService"]
  },
  {
    "name": "PaymentService",
    "relationships": ["PaymentGateway"]
  },
  {
    "name": "UserDB",
    "relationships": []
  },
  {
    "name": "OrderDB",
    "relationships": []
  },
  {
    "name": "Redis",
    "relationships": []
  },
  {
    "name": "PaymentGateway",
    "relationships": []
  }
]
```

### 13.3 前端应用架构示例

```json
[
  {
    "name": "App",
    "relationships": ["Router", "Store", "API"]
  },
  {
    "name": "Router",
    "relationships": ["Pages"]
  },
  {
    "name": "Store",
    "relationships": ["Actions", "Reducers"]
  },
  {
    "name": "API",
    "relationships": ["Axios"]
  },
  {
    "name": "Pages",
    "relationships": ["Components"]
  },
  {
    "name": "Components",
    "relationships": []
  }
]
```

---

## 14. 非功能需求

### 14.1 性能

**支持规模**:
- 100 - 3000 节点
- 流畅的拖拽和布局更新

### 14.2 兼容性

**支持浏览器**:
- ✅ Chrome (推荐)
- ✅ Edge
- ✅ Firefox
- ✅ Safari

**最低要求**:
- 支持 ES6+
- 支持 SVG
- 支持 File API

### 14.3 可维护性

**代码要求**:
- 单页 HTML
- 无后端依赖
- JSON 可直接维护
- 代码注释清晰

---

## 15. 注意事项

### 15.1 数据持久化

- ⚠️ 数据保存在浏览器内存中
- ⚠️ 刷新页面会丢失数据
- ✅ 重要数据请定期导出 JSON 文件

### 15.2 性能建议

- 建议节点数量控制在 100 以内
- 过多节点可能影响性能
- 复杂关系建议分开展示

### 15.3 浏览器兼容

- 推荐使用现代浏览器
- 避免使用 IE
- 确保 JavaScript 启用

---

## 16. 快捷操作

| 操作 | 方法 |
|------|------|
| 拖拽节点 | 点击并拖动 |
| 编辑节点 | 点击节点 |
| 保存数据 | 点击"保存数据" |
| 删除节点 | 选中后点击"删除节点" |
| 导出 JSON | 点击"导出 JSON" |
| 导入 JSON | 点击"导入 JSON" 选择文件 |

---

## 17. 故障排除

### 17.1 常见问题

**Q: 节点重叠怎么办？**  
A: 力导向布局会自动调整，等待几秒或拖拽节点触发重新布局。

**Q: 导入 JSON 失败？**  
A: 检查 JSON 格式是否正确，确保包含 `name` 和 `relationships` 字段。

**Q: 箭头不显示？**  
A: 检查浏览器是否支持 SVG `<marker>` 元素。

**Q: 拖拽不流畅？**  
A: 减少节点数量或简化关系。

### 17.2 调试方法

1. 打开浏览器开发者工具（F12）
2. 查看 Console 中的错误信息
3. 检查 JSON 数据格式
4. 验证节点名称唯一性

---

## 18. 后续改进建议

1. **持久化存储**: 集成后端数据库
2. **用户认证**: 添加访问控制
3. **版本管理**: 支持架构图版本历史
4. **协作功能**: 多人实时编辑
5. **导出格式**: 支持 PNG、SVG 等图片格式
6. **模板库**: 提供常用架构模板
7. **搜索功能**: 快速定位节点
8. **缩放功能**: 支持画布缩放
9. **撤销/重做**: 操作历史管理

---

## 19. 相关文档

- [路由结构说明](./routing-structure.md)
- [快速开始](../README.md)
- [API 列表](http://127.0.0.1:5000/api/apis)

---

## 20. 变更历史

### 2026-03-16

- ✅ 创建初始文档
- ✅ 综合需求文档和使用文档
- ✅ 完善功能说明和数据模型
- ✅ 添加示例数据和故障排除

---

**文档维护**: 项目团队  
**联系方式**: 查看项目 README
