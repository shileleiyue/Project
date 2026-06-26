/* ========================================
   Toast - 消息提示组件
   ======================================== */

const Toast = (function() {
  let container = null;

  /**
   * 确保容器存在
   */
  function ensureContainer() {
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 8px;
        pointer-events: none;
      `;
      document.body.appendChild(container);
    }
  }

  /**
   * 显示消息提示
   * @param {string} message - 消息内容
   * @param {string} [type='success'] - 消息类型: success / error / warning
   */
  function show(message, type) {
    type = type || 'success';
    ensureContainer();

    const colors = {
      success: { bg: '#dcfce7', border: '#16a34a', text: '#166534' },
      error: { bg: '#fee2e2', border: '#dc2626', text: '#991b1b' },
      warning: { bg: '#fef9c3', border: '#f59e0b', text: '#854d0e' }
    };

    const color = colors[type] || colors.success;

    const toast = document.createElement('div');
    toast.style.cssText = `
      background-color: ${color.bg};
      color: ${color.text};
      border-left: 4px solid ${color.border};
      padding: 12px 20px;
      border-radius: 6px;
      font-size: 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      pointer-events: auto;
      animation: toastIn 0.3s ease;
      max-width: 400px;
      word-break: break-all;
    `;

    toast.textContent = message;
    container.appendChild(toast);

    // 3秒后自动消失
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, 3000);
  }

  // 注入动画样式
  (function injectStyle() {
    if (document.getElementById('toast-style')) return;
    const style = document.createElement('style');
    style.id = 'toast-style';
    style.textContent = `
      @keyframes toastIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
      }
    `;
    document.head.appendChild(style);
  })();

  return { show };
})();