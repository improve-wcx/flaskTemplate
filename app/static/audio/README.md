# 示例音频文件说明

此目录用于存放音频文件（.wav, .mp3 等）。

## 使用方法

```python
# 在模板中引用
<audio controls>
    <source src="{{ url_for('static', filename='audio/your-audio.mp3') }}" type="audio/mpeg">
</audio>
```

## 支持的格式

- WAV (.wav)
- MP3 (.mp3)
- OGG (.ogg)

## 添加音频文件

1. 将音频文件放入此目录
2. 在模板中使用 `url_for('static', filename='audio/filename.ext')` 引用
3. 确保文件大小适中，避免影响加载速度
