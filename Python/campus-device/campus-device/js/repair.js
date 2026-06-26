/* ========================================
   Repair JS - 维修工单业务逻辑 (IIFE)
   ======================================== */

const RepairModule = (function() {

  var STATUS_MAP = {
    'pending': { label: '待处理', cls: 'status-repair_pending' },
    'assigned': { label: '已分配', cls: 'status-repair_pending' },
    'repairing': { label: '维修中', cls: 'status-repairing' },
    'repaired': { label: '已修复', cls: 'status-repaired' },
    'unfixable': { label: '无法修复', cls: 'status-damaged' },
    'completed': { label: '已完成', cls: 'status-available' }
  };

  /**
   * 加载分配给当前维修人员的工单
   */
  async function loadAssignedRepairs(page) {
    page = page || 1;

    var tbody = document.getElementById('repair-task-tbody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:40px;">加载中...</td></tr>';
    }

    try {
      var result = await API.get('/repairs/assigned?page=' + page + '&page_size=' + AppConfig.PAGE_SIZE);
      var repairs = result.data?.list || result.data?.items || result.items || [];
      var total = result.data?.total || result.total || 0;
      var totalPages = Paginator.calcTotalPages(total);

      renderRepairTable(repairs);
      Paginator.render('#repair-task-paginator', page, totalPages, function(newPage) {
        loadAssignedRepairs(newPage);
      });
    } catch (error) {
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:40px;color:#dc2626;">加载失败：' + Utils.escapeHtml(error.message) + '</td></tr>';
      }
      Toast.show(error.message || '加载维修工单失败', 'error');
    }
  }

  /**
   * 渲染维修工单表格
   */
  function renderRepairTable(repairs) {
    var tbody = document.getElementById('repair-task-tbody');
    if (!tbody) return;

    if (!repairs || repairs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:60px;color:#999;">暂无维修工单</td></tr>';
      return;
    }

    var html = '';
    repairs.forEach(function(item) {
      var statusInfo = STATUS_MAP[item.status] || { label: item.status || '未知', cls: 'status-offline' };
      var deviceName = (item.device && item.device.name) ? item.device.name : (item.device_name || '未知设备');

      html += '<tr>';
      html += '<td>' + Utils.escapeHtml(deviceName) + '</td>';
      html += '<td>' + Utils.escapeHtml(item.description || item.fault_description || '-') + '</td>';
      html += '<td><span class="status-tag ' + statusInfo.cls + '">' + statusInfo.label + '</span></td>';
      html += '<td>' + Utils.formatDate(item.created_at) + '</td>';
      html += '<td><button class="btn btn-outline" style="padding:4px 12px;font-size:12px;" onclick="window.location.href=\'repair-detail.html?id=' + item.id + '\'">查看详情</button></td>';
      html += '</tr>';
    });

    tbody.innerHTML = html;
  }

  return { loadAssignedRepairs, renderRepairTable };
})();