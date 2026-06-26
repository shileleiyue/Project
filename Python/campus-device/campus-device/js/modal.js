/* ========================================
   Modal - 弹窗组件
   ======================================== */

const Modal = (function() {

  /**
   * 创建弹窗遮罩层
   * @param {string} innerHTML - 弹窗内容HTML
   * @returns {HTMLElement} overlay元素
   */
  function createOverlay(innerHTML) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = innerHTML;
    return overlay;
  }

  /**
   * 关闭弹窗
   * @param {HTMLElement} overlay
   */
  function closeModal(overlay) {
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.2s ease';
    setTimeout(() => {
      if (overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }, 200);
  }

  /**
   * 确认弹窗 - 返回 Promise
   * @param {string} title - 标题
   * @param {string} message - 消息内容
   * @returns {Promise<boolean>} true=确认, false=取消
   */
  function confirm(title, message) {
    return new Promise((resolve) => {
      const html = `
        <div class="modal-content">
          <div class="modal-header">
            <h3>${Utils.escapeHtml(title)}</h3>
          </div>
          <div class="modal-body">
            <p>${Utils.escapeHtml(message)}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline" id="modal-cancel-btn">取消</button>
            <button class="btn btn-primary" id="modal-confirm-btn">确认</button>
          </div>
        </div>
      `;
      const overlay = createOverlay(html);
      document.body.appendChild(overlay);

      overlay.querySelector('#modal-cancel-btn').addEventListener('click', () => {
        closeModal(overlay);
        resolve(false);
      });

      overlay.querySelector('#modal-confirm-btn').addEventListener('click', () => {
        closeModal(overlay);
        resolve(true);
      });

      // 点击遮罩层关闭
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          closeModal(overlay);
          resolve(false);
        }
      });
    });
  }

  /**
   * 提示弹窗
   * @param {string} title - 标题
   * @param {string} message - 消息内容
   * @returns {Promise<void>}
   */
  function alert(title, message) {
    return new Promise((resolve) => {
      const html = `
        <div class="modal-content">
          <div class="modal-header">
            <h3>${Utils.escapeHtml(title)}</h3>
          </div>
          <div class="modal-body">
            <p>${Utils.escapeHtml(message)}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" id="modal-ok-btn">确定</button>
          </div>
        </div>
      `;
      const overlay = createOverlay(html);
      document.body.appendChild(overlay);

      const close = () => {
        closeModal(overlay);
        resolve();
      };

      overlay.querySelector('#modal-ok-btn').addEventListener('click', close);
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) close();
      });
    });
  }

  /**
   * 自定义内容弹窗
   * @param {string} title - 标题
   * @param {string} contentHTML - 自定义内容HTML
   * @param {Function} [onOpen] - 弹窗打开后的回调，接收overlay作为参数
   * @returns {HTMLElement} overlay元素
   */
  function custom(title, contentHTML, onOpen) {
    const html = `
      <div class="modal-content">
        <div class="modal-header">
          <h3>${Utils.escapeHtml(title)}</h3>
          <span class="modal-close">&times;</span>
        </div>
        <div class="modal-body">
          ${contentHTML}
        </div>
      </div>
    `;
    const overlay = createOverlay(html);
    document.body.appendChild(overlay);

    overlay.querySelector('.modal-close').addEventListener('click', () => {
      closeModal(overlay);
    });

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal(overlay);
    });

    if (onOpen) {
      onOpen(overlay);
    }

    return overlay;
  }

  /**
   * 关闭指定弹窗
   * @param {HTMLElement} overlay
   */
  function close(overlay) {
    closeModal(overlay);
  }

  return { confirm, alert, custom, close };
})();