// 主 JavaScript 文件

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask Application 已加载');
    
    // 初始化任何需要的功能
    initFlashMessages();
    initNavigation();
});

// 自动隐藏警告消息
function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

// 导航栏交互
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            // 可以在这里添加导航前的确认或其他逻辑
            console.log('导航到:', this.href);
        });
    });
}

// 工具函数：显示消息
function showMessage(message, type = 'info') {
    const container = document.querySelector('.main-content .container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const flashContainer = container.querySelector('.flash-messages');
    if (flashContainer) {
        flashContainer.appendChild(alertDiv);
    } else {
        const newFlashContainer = document.createElement('div');
        newFlashContainer.className = 'flash-messages';
        newFlashContainer.appendChild(alertDiv);
        container.insertBefore(newFlashContainer, container.firstChild);
    }
    
    // 5 秒后自动隐藏
    setTimeout(function() {
        alertDiv.style.opacity = '0';
        alertDiv.style.transition = 'opacity 0.5s';
        setTimeout(function() {
            alertDiv.remove();
        }, 500);
    }, 5000);
}

// 工具函数：AJAX 请求
async function ajaxRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('请求失败:', error);
        showMessage('请求失败：' + error.message, 'error');
        throw error;
    }
}

// 导出全局函数
window.showMessage = showMessage;
window.ajaxRequest = ajaxRequest;
