/**
 * 音频播放器核心逻辑
 * 适配后端递归扫描接口，支持多级目录展示
 */
document.addEventListener('DOMContentLoaded', () => {
    const audioSelect = document.getElementById('audio-select');
    const playBtn = document.getElementById('play-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const mainAudio = document.getElementById('main-audio');
    const statusText = document.getElementById('status-text');

    // 基础路径：对应 Flask 的 static/audio 映射
    const BASE_PATH = '/static/audio/';

    /**
     * 从后端 API 获取音频列表并填充下拉框
     */
    async function loadAudioList() {
        try {
            const response = await fetch('/api/get_audio_list');
            const data = await response.json();

            if (data.success && data.files && data.files.length > 0) {
                // 清空现有选项
                audioSelect.innerHTML = '';

                data.files.forEach(fileObj => {
                    const option = document.createElement('option');
                    // file_path 包含了子目录路径，如 "animals/lion.ogg"
                    option.value = fileObj.file_path;
                    // display_name 用于界面展示
                    option.textContent = fileObj.display_name;
                    audioSelect.appendChild(option);
                });

                // 初始加载第一个音频
                updateAudioSource();
            } else {
                audioSelect.innerHTML = '<option value="">未找到 .ogg 音频文件</option>';
                statusText.innerText = '暂无音频';
            }
        } catch (err) {
            console.error('API 请求失败:', err);
            statusText.innerText = '列表加载失败';
            audioSelect.innerHTML = '<option value="">服务不可用</option>';
        }
    }

    /**
     * 根据下拉框选中的值更新音频源
     */
    function updateAudioSource() {
        const selectedFile = audioSelect.value;
        if (selectedFile) {
            // 拼接完整路径：/static/audio/animals/lion.ogg
            mainAudio.src = BASE_PATH + selectedFile;
            statusText.innerText = '就绪: ' + selectedFile.split('/').pop(); // 仅显示文件名
            mainAudio.load(); // 强制加载新资源
        }
    }

    /**
     * 播放逻辑，处理浏览器自动播放策略限制
     */
    function playAudio() {
        if (!mainAudio.src) return;

        mainAudio.play()
            .then(() => {
                statusText.innerText = '正在播放...';
                statusText.classList.add('playing'); // 可用于扩展 CSS 动画
            })
            .catch(err => {
                console.warn('播放被拦截:', err);
                statusText.innerText = '请点击页面后再播放';
            });
    }

    // 事件监听
    audioSelect.addEventListener('change', updateAudioSource);

    playBtn.addEventListener('click', playAudio);

    pauseBtn.addEventListener('click', () => {
        mainAudio.pause();
        statusText.innerText = '已暂停';
        statusText.classList.remove('playing');
    });

    // 音频播放完毕监听
    mainAudio.addEventListener('ended', () => {
        statusText.innerText = '播放结束';
        statusText.classList.remove('playing');
    });

    // 文件加载错误处理
    mainAudio.addEventListener('error', () => {
        statusText.innerText = '音频文件损坏或丢失';
    });

    // 执行初始化
    loadAudioList();
});