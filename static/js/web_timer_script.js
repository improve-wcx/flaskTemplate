/**
 * Web 提醒助手 (Web Reminder Assistant) - 核心逻辑
 */

// ==========================================
// 全局常量与状态定义
// ==========================================

const STATUS = {
    NOT_STARTED: '未开始',
    RUNNING: '运行中',
    PAUSED: '已暂停',
    COMPLETED: '已完成'
};

const STATUS_WEIGHT = {
    [STATUS.RUNNING]: 0,
    [STATUS.PAUSED]: 1,
    [STATUS.NOT_STARTED]: 2,
    [STATUS.COMPLETED]: 3
};

const AUDIO_BASE_PATH = '/static/audio/';
let previewAudioInstance = null; // [新增] 用于保存当前试听的音频实例

// ==========================================
// 数据持久化管理
// ==========================================

let tasks = JSON.parse(localStorage.getItem('timer_tasks')) || [];

function saveData() {
    localStorage.setItem('timer_tasks', JSON.stringify(tasks));
}

function saveAndRender() {
    saveData();
    renderTasks();
}

// ==========================================
// 核心计时引擎
// ==========================================

function updateGlobalClock() {
    const clockEl = document.getElementById('global-clock');
    if (!clockEl) return;
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const time = now.toTimeString().split(' ')[0];
    clockEl.innerText = `${year}-${month}-${day} ${time}`;
}

function engineTick() {
    const now = Date.now();
    let hasChanged = false; 

    tasks.forEach(task => {
        if (task.status === STATUS.RUNNING) {
            const diff = task.endTime - now;
            if (diff <= 0) {
                completeTask(task);
                hasChanged = true;
            } else {
                const currentRemaining = Math.ceil(diff / 1000);
                if (task.remainingSeconds !== currentRemaining) {
                    task.remainingSeconds = currentRemaining;
                    hasChanged = true; 
                }
            }
        }
    });

    if (hasChanged) {
        saveData(); 
        renderTasks(); 
    }
}

// ==========================================
// 任务操作逻辑
// ==========================================

async function loadAudioList() {
    const audioSelect = document.getElementById('input-audio');
    if (!audioSelect) return;

    try {
        const response = await fetch('/api/get_audio_list');
        const data = await response.json();
        
        if (data.success && data.files && data.files.length > 0) {
            audioSelect.innerHTML = '';
            data.files.forEach(fileObj => {
                const option = document.createElement('option');
                option.value = fileObj.file_path;
                option.textContent = fileObj.display_name;
                audioSelect.appendChild(option);
            });
            if (audioSelect.options.length > 0) {
                audioSelect.selectedIndex = 0;
            }
        } else {
            audioSelect.innerHTML = '<option value="">暂无 .ogg 音频文件</option>';
        }
    } catch (err) {
        console.error('加载音频列表失败:', err);
        audioSelect.innerHTML = '<option value="">加载失败</option>';
    }
}

function addTask() {
    const h = parseInt(document.getElementById('input-h').value) || 0;
    const m = parseInt(document.getElementById('input-m').value) || 0;
    const s = parseInt(document.getElementById('input-s').value) || 0;
    const audioPath = document.getElementById('input-audio').value;
    const remark = document.getElementById('input-remark').value.trim();

    const totalSeconds = h * 3600 + m * 60 + s;
    if (totalSeconds <= 0) {
        alert("请输入有效的倒计时时间");
        return;
    }
    if (!audioPath) {
        alert("请选择提醒铃声");
        return;
    }

    const newTask = {
        id: Date.now(),
        initialSeconds: totalSeconds,
        remainingSeconds: totalSeconds,
        remark: remark || "无备注",
        audioPath: audioPath,
        status: STATUS.NOT_STARTED,
        startTime: null,
        endTime: null,
        pausedRemainingMs: null,
        createdAt: Date.now()
    };

    tasks.push(newTask);
    resetForm();
    saveAndRender();
}

function startTask(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    const now = Date.now();
    task.status = STATUS.RUNNING;
    if (!task.startTime) {
        task.startTime = now;
    }
    task.endTime = now + (task.remainingSeconds * 1000);
    saveAndRender();
}

function togglePause(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    const now = Date.now();
    if (task.status === STATUS.RUNNING) {
        task.status = STATUS.PAUSED;
        task.pausedRemainingMs = task.endTime - now;
        task.endTime = null;
    } else if (task.status === STATUS.PAUSED) {
        task.status = STATUS.RUNNING;
        task.endTime = now + task.pausedRemainingMs;
        task.pausedRemainingMs = null;
    }
    saveAndRender();
}

function deleteTask(id) {
    if (confirm("确定要删除这条提醒任务吗？")) {
        tasks = tasks.filter(t => t.id !== id);
        saveAndRender();
    }
}

function completeTask(task) {
    task.status = STATUS.COMPLETED;
    task.remainingSeconds = 0;
    task.endTime = null;

    if (task.audioPath) {
        const audio = new Audio(AUDIO_BASE_PATH + task.audioPath);
        audio.play().catch(err => {
            console.warn("自动播放被浏览器拦截，请确保之前点击过页面", err);
            alert(`【定时提醒】时间到！\n备注：${task.remark}`);
        });
    }
}


/**
 * [新增] 试听/停止当前选择的铃声
 */
function togglePreview() {
    const audioPath = document.getElementById('input-audio').value;
    const previewBtn = document.getElementById('preview-btn');

    if (!audioPath) {
        alert("请先选择一个提醒铃声。");
        return;
    }

    // 如果当前正在播放，则停止播放
    if (previewAudioInstance && !previewAudioInstance.paused) {
        previewAudioInstance.pause();
        previewAudioInstance.currentTime = 0; // 重置进度
        previewBtn.innerHTML = '▶ 试听';
        previewBtn.classList.remove('playing');
        return;
    }

    // 播放新的试听音频
    previewAudioInstance = new Audio(AUDIO_BASE_PATH + audioPath);
    
    previewAudioInstance.play().then(() => {
        // 播放成功，按钮变成停止状态
        previewBtn.innerHTML = '■ 停止';
        previewBtn.classList.add('playing');
    }).catch(err => {
        console.error("试听失败:", err);
        alert("试听失败，可能文件不存在或被浏览器拦截。");
    });

    // 监听音频播放结束事件，自动恢复按钮状态
    previewAudioInstance.onended = () => {
        previewBtn.innerHTML = '▶ 试听';
        previewBtn.classList.remove('playing');
    };
}

/**
 * [新增] 当用户切换下拉框的音频时，自动停止正在试听的旧音频
 */
function stopPreviewOnChange() {
    const previewBtn = document.getElementById('preview-btn');
    if (previewAudioInstance && !previewAudioInstance.paused) {
        previewAudioInstance.pause();
        previewAudioInstance.currentTime = 0;
        previewBtn.innerHTML = '▶ 试听';
        previewBtn.classList.remove('playing');
    }
}

// ==========================================
// 数据导入/导出逻辑 (JSON 格式)
// ==========================================

function exportData() {
    if (tasks.length === 0) {
        alert("当前没有任务可以导出。");
        return;
    }

    const jsonData = JSON.stringify(tasks, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    const now = new Date();
    const timestamp = now.toISOString().replace(/T/, '_').replace(/:/g, '').split('.')[0];
    a.download = `reminder_tasks_${timestamp}.json`;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function triggerImport() {
    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.click();
}

function handleImport(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.json')) {
        alert("请上传有效的 .json 任务文件。");
        event.target.value = '';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const importedTasks = JSON.parse(e.target.result);

            if (!Array.isArray(importedTasks)) {
                throw new Error("无效的 JSON 格式：根节点必须是数组。");
            }

            const processedTasks = importedTasks.map(task => {
                if (typeof task.id === 'undefined' ||
                    typeof task.initialSeconds === 'undefined' ||
                    typeof task.remainingSeconds === 'undefined' ||
                    typeof task.audioPath === 'undefined') {
                    throw new Error("文件包含无效的任务数据结构：缺少必需字段。");
                }

                // --- 【核心修复：智能状态恢复逻辑】 ---
                if (task.status === STATUS.COMPLETED) {
                    // 已经是完成状态的，保留其完成状态和 startTime，仅清除无用的运行数据
                    task.endTime = null;
                    task.pausedRemainingMs = null;
                } else if (task.status === STATUS.NOT_STARTED) {
                    // 原本就是未开始的，保持原样
                    task.endTime = null;
                    task.pausedRemainingMs = null;
                } else {
                    // 运行中(RUNNING) 或 暂停(PAUSED) 的任务：
                    // 由于导出的时间上下文（endTime）在当前已经失效，强制重置为“未开始”，并恢复初始倒计时时长
                    task.status = STATUS.NOT_STARTED;
                    task.remainingSeconds = task.initialSeconds; // 恢复到满血状态
                    task.startTime = null;
                    task.endTime = null;
                    task.pausedRemainingMs = null;
                }
                return task;
            });

            const mode = confirm(`数据已加载。\n\n点击'确定'：【覆盖】当前列表 (原有任务将清空)。\n点击'取消'：【合并】到当前列表中。`);

            if (mode) {
                tasks = processedTasks;
            } else {
                tasks = tasks.concat(processedTasks);
            }

            saveAndRender();
            alert(`成功导入 ${processedTasks.length} 条提醒任务！(运行中的任务已安全重置)`);
            event.target.value = '';

        } catch (err) {
            console.error("JSON 导入失败:", err);
            alert(`导入失败: ${err.message}`);
            event.target.value = '';
        }
    };

    reader.readAsText(file);
}

// ==========================================
// 界面渲染与辅助函数
// ==========================================

function renderTasks() {
    const tbody = document.getElementById('task-tbody');
    if (!tbody) return;
    
    const sortedTasks = [...tasks].sort((a, b) => {
        if (STATUS_WEIGHT[a.status] !== STATUS_WEIGHT[b.status]) {
            return STATUS_WEIGHT[a.status] - STATUS_WEIGHT[b.status];
        }
        const timeA = a.startTime || a.createdAt;
        const timeB = b.startTime || b.createdAt;
        return timeB - timeA;
    });

    tbody.innerHTML = '';

    sortedTasks.forEach(task => {
        const isRunning = task.status === STATUS.RUNNING;
        const isCompleted = task.status === STATUS.COMPLETED;
        const isPaused = task.status === STATUS.PAUSED;

        const tr = document.createElement('tr');
        if (isRunning) tr.classList.add('status-running');
        if (isCompleted) tr.classList.add('status-completed');

        const displaySeconds = isCompleted ? task.initialSeconds : task.remainingSeconds;
        const timeText = formatTime(displaySeconds);
        const startTimeText = task.startTime ? new Date(task.startTime).toLocaleString() : '-';

        tr.innerHTML = `
            <td><span class="countdown-text">${timeText}</span></td>
            <td><small>${startTimeText}</small></td>
            <td>
                <div class="remark-cell" title="${task.remark}">
                    ${truncateString(task.remark, 20)}
                </div>
            </td>
            <td><small>${task.audioPath.split('/').pop()}</small></td>
            <td class="btn-group">
                <button class="btn btn-sm btn-start" onclick="startTask(${task.id})" 
                    ${task.status !== STATUS.NOT_STARTED ? 'disabled' : ''}>开始</button>
                <button class="btn btn-sm btn-pause" onclick="togglePause(${task.id})" 
                    ${(!isRunning && !isPaused) ? 'disabled' : ''}>
                    ${isPaused ? '继续' : '暂停'}
                </button>
                <button class="btn btn-sm btn-delete" onclick="deleteTask(${task.id})">删除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function formatTime(totalSeconds) {
    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;
    return [h, m, s].map(v => String(v).padStart(2, '0')).join(':');
}

function truncateString(str, num) {
    if (!str) return '-';
    if (str.length <= num) return str;
    return str.slice(0, num) + '...';
}

function resetForm() {
    const hInput = document.getElementById('input-h');
    const mInput = document.getElementById('input-m');
    const sInput = document.getElementById('input-s');
    const remarkInput = document.getElementById('input-remark');

    if (hInput) hInput.value = 0;
    if (mInput) mInput.value = 0;
    if (sInput) sInput.value = 0;
    if (remarkInput) remarkInput.value = '';
}

// ==========================================
// 初始化与事件绑定
// ==========================================

async function init() {
    setInterval(updateGlobalClock, 1000);
    updateGlobalClock(); 

    setInterval(engineTick, 100);

    await loadAudioList();
    renderTasks();
}

document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-btn');
    if (addBtn) addBtn.addEventListener('click', addTask);

    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) exportBtn.addEventListener('click', exportData);

    const importBtn = document.getElementById('import-btn');
    if (importBtn) importBtn.addEventListener('click', triggerImport);

    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.addEventListener('change', handleImport);

    // [新增] 绑定试听按钮点击事件
    const previewBtn = document.getElementById('preview-btn');
    if (previewBtn) previewBtn.addEventListener('click', togglePreview);

    // [新增] 绑定下拉框切换事件（切换选项时自动停止试听）
    const audioSelect = document.getElementById('input-audio');
    if (audioSelect) audioSelect.addEventListener('change', stopPreviewOnChange);

    init();
});