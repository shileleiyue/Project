/* ========================================
   Paginator - 分页器组件
   ======================================== */

const Paginator = (function() {

  /**
   * 计算总页数
   * @param {number} total - 总记录数
   * @param {number} [pageSize] - 每页条数，默认使用 AppConfig.PAGE_SIZE
   * @returns {number}
   */
  function calcTotalPages(total, pageSize) {
    pageSize = pageSize || AppConfig.PAGE_SIZE;
    return Math.max(1, Math.ceil(total / pageSize));
  }

  /**
   * 获取页码数组（含省略号逻辑）
   * 始终显示首尾页，当前页前后各2页
   * @param {number} currentPage - 当前页码
   * @param {number} totalPages - 总页数
   * @returns {Array<number|string>} 页码数组，字符串 '...' 表示省略号
   */
  function getPageNumbers(currentPage, totalPages) {
    if (totalPages <= 7) {
      // 总页数 <= 7，全部显示
      const pages = [];
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
      return pages;
    }

    const pages = [];
    pages.push(1);

    // 计算当前页前后的范围
    const rangeStart = Math.max(2, currentPage - 2);
    const rangeEnd = Math.min(totalPages - 1, currentPage + 2);

    // 判断是否需要前面的省略号
    if (rangeStart > 2) {
      pages.push('...');
    }

    // 添加中间页码
    for (let i = rangeStart; i <= rangeEnd; i++) {
      pages.push(i);
    }

    // 判断是否需要后面的省略号
    if (rangeEnd < totalPages - 1) {
      pages.push('...');
    }

    // 末页
    pages.push(totalPages);

    return pages;
  }

  /**
   * 渲染分页器
   * @param {string} containerSelector - 容器选择器
   * @param {number} currentPage - 当前页码
   * @param {number} totalPages - 总页数
   * @param {Function} onPageChange - 页码变化回调，接收新页码
   */
  function render(containerSelector, currentPage, totalPages, onPageChange) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const pageNumbers = getPageNumbers(currentPage, totalPages);

    let html = '<div class="paginator">';

    // 上一页按钮
    html += `<button class="paginator-btn prev" data-page="${currentPage - 1}"`;
    if (currentPage <= 1) {
      html += ' disabled';
    }
    html += '>上一页</button>';

    // 页码列表
    html += '<div class="paginator-pages">';
    pageNumbers.forEach((page) => {
      if (page === '...') {
        html += '<span class="paginator-ellipsis">...</span>';
      } else {
        const isActive = page === currentPage ? ' active' : '';
        html += `<button class="paginator-btn page${isActive}" data-page="${page}">${page}</button>`;
      }
    });
    html += '</div>';

    // 下一页按钮
    html += `<button class="paginator-btn next" data-page="${currentPage + 1}"`;
    if (currentPage >= totalPages) {
      html += ' disabled';
    }
    html += '>下一页</button>';

    // 总数信息
    html += `<span class="paginator-info">共 ${totalPages} 页</span>`;

    html += '</div>';

    container.innerHTML = html;

    // 绑定点击事件
    container.querySelectorAll('.paginator-btn.page').forEach((btn) => {
      btn.addEventListener('click', () => {
        const page = parseInt(btn.dataset.page);
        if (!isNaN(page) && page !== currentPage && !btn.disabled) {
          onPageChange(page);
        }
      });
    });

    // 上一页/下一页
    const prevBtn = container.querySelector('.paginator-btn.prev');
    const nextBtn = container.querySelector('.paginator-btn.next');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentPage > 1 && !prevBtn.disabled) {
          onPageChange(currentPage - 1);
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages && !nextBtn.disabled) {
          onPageChange(currentPage + 1);
        }
      });
    }
  }

  /**
   * 设置分页器加载状态（禁用所有按钮）
   * @param {string} containerSelector - 容器选择器
   * @param {boolean} loading - 是否加载中
   */
  function setLoading(containerSelector, loading) {
    const container = document.querySelector(containerSelector);
    if (!container) return;
    const buttons = container.querySelectorAll('.paginator-btn');
    buttons.forEach((btn) => {
      if (loading) {
        btn.setAttribute('disabled', 'disabled');
      } else {
        btn.removeAttribute('disabled');
      }
    });
  }

  // 注入分页器样式
  (function injectStyle() {
    if (document.getElementById('paginator-style')) return;
    const style = document.createElement('style');
    style.id = 'paginator-style';
    style.textContent = `
      .paginator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 16px 0;
        user-select: none;
      }
      .paginator-pages {
        display: flex;
        align-items: center;
        gap: 4px;
      }
      .paginator-btn {
        padding: 6px 14px;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        background-color: #fff;
        color: #1a1a2e;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
      }
      .paginator-btn:hover:not(:disabled) {
        border-color: #2563eb;
        color: #2563eb;
      }
      .paginator-btn.active {
        background-color: #2563eb;
        color: #fff;
        border-color: #2563eb;
      }
      .paginator-btn:disabled {
        opacity: 0.4;
        cursor: not-allowed;
      }
      .paginator-ellipsis {
        padding: 6px 4px;
        color: #999;
        font-size: 14px;
      }
      .paginator-info {
        margin-left: 12px;
        font-size: 13px;
        color: #999;
      }
    `;
    document.head.appendChild(style);
  })();

  return { calcTotalPages, getPageNumbers, render, setLoading };
})();