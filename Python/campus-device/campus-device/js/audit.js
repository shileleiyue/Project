/* ========================================
   AuditViewer - 审核记录查看组件
   ======================================== */

const AuditViewer = (function() {

  // 操作动作翻译映射
  var ACTION_MAP = {
    'create': '创建',
    'approve': '通过',
    'reject': '驳回',
    'return': '归还',
    'confirm_return': '确认归还',
    'assign': '分配',
    'confirm': '确认完成',
    'scrap': '报废',
    'repairing': '维修中',
    'repaired': '已修复',
    'unfixable': '无法修复'
  };

  /**
   * 翻译操作动作
   * @param {string} action - 原始动作名
   * @returns {string} 翻译后的动作名
   */
  function translateAction(action) {
    return ACTION_MAP[action] || action || '未知';
  }

  /**
   * 格式化状态变更显示
   * @param {string|null} fromStatus - 变更前状态
   * @param {string|null} toStatus - 变更后状态
   * @returns {string} 格式化后的HTML
   */
  function formatStatusChange(fromStatus, toStatus) {
    if (fromStatus && toStatus) {
      return Utils.escapeHtml(fromStatus) + ' &rarr; ' + Utils.escapeHtml(toStatus);
    } else if (toStatus) {
      return Utils.escapeHtml(toStatus);
    }
    return '-';
  }

  /**
   * 渲染审核记录列表
   * @param {HTMLElement} overlay - 弹窗遮罩层
   * @param {string} targetType - 目标类型
   * @param {number} targetId - 目标ID
   * @param {number} page - 当前页码
   */
  async function renderLogs(overlay, targetType, targetId, page) {
    var body = overlay.querySelector('#audit-modal-body');
    body.innerHTML = '<div class="loading-spinner">加载中...</div>';

    try {
      var result = await API.get('/audit-logs?target_type=' + targetType + '&target_id=' + targetId + '&page=' + page + '&page_size=10');
      var logs = result.data.list || result.data || [];
      var total = result.data.total || 0;
      var totalPages = result.data.total_pages || 1;
      var currentPage = result.data.page || page;

      if (!logs || logs.length === 0) {
        body.innerHTML = '<div class="empty-state"><p>暂无审核记录</p></div>';
        return;
      }

      var html = '<div class="table-container"><table><thead><tr>' +
        '<th>操作时间</th><th>操作人</th><th>操作动作</th><th>状态变更</th><th>备注</th>' +
        '</tr></thead><tbody>';

      logs.forEach(function(log) {
        var operatorName = (log.operator && log.operator.username) ? log.operator.username : '未知';
        html += '<tr>' +
          '<td>' + Utils.formatDate(log.created_at) + '</td>' +
          '<td>' + Utils.escapeHtml(operatorName) + '</td>' +
          '<td>' + translateAction(log.action) + '</td>' +
          '<td>' + formatStatusChange(log.from_status, log.to_status) + '</td>' +
          '<td>' + Utils.escapeHtml(log.remark || '-') + '</td>' +
          '</tr>';
      });

      html += '</tbody></table></div>';

      // 分页控件
      if (totalPages > 1) {
        html += '<div style="display:flex;align-items:center;justify-content:center;gap:10px;margin-top:16px;padding-top:16px;border-top:1px solid var(--color-border);">' +
          '<button class="btn btn-outline" id="audit-prev-btn" ' + (currentPage <= 1 ? 'disabled' : '') + ' style="padding:4px 14px;font-size:12px;">上一页</button>' +
          '<span style="line-height:32px;font-size:13px;color:#666;">第 ' + currentPage + ' / ' + totalPages + ' 页（共 ' + total + ' 条）</span>' +
          '<button class="btn btn-outline" id="audit-next-btn" ' + (currentPage >= totalPages ? 'disabled' : '') + ' style="padding:4px 14px;font-size:12px;">下一页</button>' +
          '</div>';
      }

      body.innerHTML = html;

      // 绑定分页事件
      var prevBtn = body.querySelector('#audit-prev-btn');
      var nextBtn = body.querySelector('#audit-next-btn');
      if (prevBtn) {
        prevBtn.addEventListener('click', function() {
          renderLogs(overlay, targetType, targetId, currentPage - 1);
        });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', function() {
          renderLogs(overlay, targetType, targetId, currentPage + 1);
        });
      }
    } catch (error) {
      body.innerHTML = '<div style="text-align:center;padding:40px;color:#dc2626;">加载失败：' + Utils.escapeHtml(error.message) + '</div>';
      Toast.show(error.message || '加载审核记录失败', 'error');
    }
  }

  /**
   * 显示审核记录弹窗
   * @param {string} targetType - 目标类型：'borrow' / 'repair' / 'device'
   * @param {number} targetId - 目标记录ID
   * @param {string} title - 弹窗标题
   */
  async function show(targetType, targetId, title) {
    var contentHTML = '<div id="audit-modal-body"><div class="loading-spinner">加载中...</div></div>';
    var overlay = Modal.custom(title, contentHTML);
    renderLogs(overlay, targetType, targetId, 1);
  }

  return { show };
})();