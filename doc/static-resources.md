# 静态资源开发指南

本指南说明如何在 Flask 项目中管理和使用静态资源。

## 📁 目录结构

```
app/
├── static/
│   ├── css/              # CSS 样式文件
│   │   └── main.css
│   ├── js/               # JavaScript 文件
│   │   └── main.js
│   ├── images/           # 图片资源
│   │   ├── logo.png
│   │   └── logo.svg
│   └── audio/            # 音频文件
│       └── sample.wav
└── templates/            # HTML 模板
    ├── base.html
    ├── index.html
    └── static_demo.html
```

## 🎨 CSS 样式

### 使用方式

```html
<!-- 在模板中引用 -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```

### 主要样式类

- `.container` - 容器
- `.navbar` - 导航栏
- `.btn` - 按钮
- `.alert` - 警告框
- `.hero-section` - 英雄区域

### 添加新样式

1. 在 `app/static/css/` 创建新 CSS 文件
2. 在模板中引用：
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/new-style.css') }}">
   ```

## ⚡ JavaScript

### 使用方式

```html
<!-- 在模板底部引用 -->
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
```

### 可用函数

- `showMessage(message, type)` - 显示消息
- `ajaxRequest(url, options)` - AJAX 请求

### 添加新功能

1. 在 `app/static/js/` 创建新 JS 文件
2. 在模板中引用：
   ```html
   <script src="{{ url_for('static', filename='js/new-feature.js') }}"></script>
   ```

## 🖼️ 图片资源

### 支持的格式

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- SVG (.svg)
- WebP (.webp)

### 使用方式

```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

### 添加新图片

1. 将图片放入 `app/static/images/`
2. 在模板中引用

## 🎵 音频文件

### 支持的格式

- WAV (.wav)
- MP3 (.mp3)
- OGG (.ogg)

### 使用方式

```html
<audio controls>
    <source src="{{ url_for('static', filename='audio/sound.mp3') }}" type="audio/mpeg">
    您的浏览器不支持音频元素。
</audio>
```

## 📄 HTML 模板

### 模板继承

所有页面都继承自 `base.html`：

```html
{% extends "base.html" %}

{% block title %}页面标题{% endblock %}

{% block content %}
<!-- 页面内容 -->
{% endblock %}

{% block extra_css %}
<!-- 额外的 CSS -->
{% endblock %}

{% block extra_js %}
<!-- 额外的 JavaScript -->
{% endblock %}
```

### 可用块

- `title` - 页面标题
- `content` - 主要内容
- `extra_css` - 额外的 CSS
- `extra_js` - 额外的 JavaScript

## 🚀 访问静态资源

### 路由

- `/static-pages/` - 静态资源首页
- `/static-pages/demo` - 静态资源演示

### 直接访问

- `/static/css/main.css`
- `/static/js/main.js`
- `/static/images/logo.png`
- `/static/audio/sound.mp3`

## 🛠️ 开发工具

### 压缩 CSS

```bash
# 安装 clean-css-cli
npm install -g clean-css-cli

# 压缩 CSS
cleancss -o main.min.css main.css
```

### 压缩 JavaScript

```bash
# 安装 uglify-js
npm install -g uglify-js

# 压缩 JS
uglifyjs main.js -o main.min.js
```

### 优化图片

```bash
# 安装 optipng
# Ubuntu/Debian
sudo apt-get install optipng

# macOS
brew install optipng

# 优化 PNG
optipng -o7 image.png
```

## 📝 最佳实践

### 1. 使用版本控制

```html
<!-- 添加版本号以便缓存控制 -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}?v=1.0.0">
```

### 2. 懒加载图片

```html
<img src="placeholder.jpg" data-src="actual-image.jpg" class="lazy-load">
```

### 3. 响应式图片

```html
<picture>
    <source media="(max-width: 600px)" srcset="{{ url_for('static', filename='images/small.jpg') }}">
    <source media="(max-width: 1200px)" srcset="{{ url_for('static', filename='images/medium.jpg') }}">
    <img src="{{ url_for('static', filename='images/large.jpg') }}" alt="Responsive">
</picture>
```

### 4. 使用 CDN

生产环境可以使用 CDN 加速：

```html
{% if config.DEBUG %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
{% else %}
    <link rel="stylesheet" href="https://cdn.example.com/css/main.css">
{% endif %}
```

## 🧪 测试

运行静态资源测试：

```bash
# 运行所有静态资源测试
pytest tests/test_routes/test_static_resources.py -v

# 运行特定测试
pytest tests/test_routes/test_static_resources.py::TestStaticResources::test_static_index_page -v
```

## ❓ 常见问题

### Q: 静态文件不更新？

A: 清除浏览器缓存或使用强制刷新（Ctrl+F5）

### Q: 404 错误？

A: 检查文件路径是否正确，确保文件在 `static` 目录下

### Q: 如何添加视频？

A: 在 `static` 下创建 `video/` 目录，使用 `<video>` 标签：

```html
<video controls>
    <source src="{{ url_for('static', filename='video/sample.mp4') }}" type="video/mp4">
</video>
```

## 📚 相关文档

- [Flask 静态文件文档](https://flask.palletsprojects.com/en/2.3.x/static-files/)
- [Jinja2 模板文档](https://jinja.palletsprojects.com/)
- [Web 性能优化](https://web.dev/performance/)

---

**最后更新**: 2026-03-16
