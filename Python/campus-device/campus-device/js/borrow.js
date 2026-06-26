/* ========================================
   Borrow JS - 借用记录业务逻辑 (IIFE)
   ======================================== */

const BorrowModule = (function() {

  var STATUS_MAP = {
    'pending': { label: '待审核', cls: 'status-pending_borrow' },
    'approved': { label: '已通过', cls: 'status-available' },
    'rejected': { label: '已驳回', cls: 'status-damaged' },
    'borrowing': { label: '借用中', cls: 'status-borrowed' },
    'pending_return': { label: '待归还确认', cls: 'status-pending_return' },
    'returned': { label: '已归还', cls: 'status-available' },
    'damaged_returned': { label: '已损坏', cls: 'status-damaged' }
  };

  /**
   * 加载我的借用记录
   */
  async function loadMyBorrows(page) {
    page = page || 1;

    var tbody = document.getElementById('borrow-tbody');
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;">加载中...</td></tr>';
    }

    try {
      var result = await API.get('/borrows/my?page=' + page + '&page_size=' + AppConfig.PAGE_SIZE);
      var borrows = result.data?.list || result.data?.items || result.items || [];
      var total = result.data?.total || result.total || 0;
      var totalPages = Paginator.calcTotalPages(total);

      renderBorrowTable(borrows);
      Paginator.render('#borrow-paginator', page, totalPages, function(newPage) {
        loadMyBorrows(newPage);
      });
    } catch (error) {
      if (tbody) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;color:#dc2626;">加载失败：' + Utils.escapeHtml(error.message) + '</td></tr>';
      }
      Toast.show(error.message || '加载借用记录失败', 'error');
    }
  }

  /**
   * 渲染借用记录表格
   */
  function renderBorrowTable(borrows) {
    var tbody = document.getElementById('borrow-tbody');
    if (!tbody) return;

    if (!borrows || borrows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:60px;color:#999;">暂无借用记录</td></tr>';
      return;
    }

    var html = '';
    borrows.forEach(function(item) {
      var statusInfo = STATUS_MAP[item.status] || { label: item.status || '未知', cls: 'status-offline' };
      var deviceName = (item.device && item.device.name) ? item.device.name : (item.device_name || '未知设备');

      html += '<tr>';
      html += '<td>' + Utils.escapeHtml(deviceName) + '</td>';
      html += '<td>' + Utils.formatDate(item.created_at || item.borrow_time) + '</td>';
      html += '<td>' + Utils.formatDate(item.expected_return_time) + '</td>';
      html += '<td><span class="status-tag ' + statusInfo.cls + '">' + statusInfo.label + '</span></td>';
      html += '<td><div class="action-btns">';

      if (item.status === 'borrowing') {
        html += '<button class="btn btn-primary btn-sm" onclick="BorrowModule.handleReturn(' + item.id + ')">归还</button>';
      }

      html += '<button class="btn btn-outline btn-sm" onclick="BorrowModule.viewDetail(' + item.id + ')">查看详情</button>';
      html += '</div></td>';
      html += '</tr>';
    });

    tbody.innerHTML = html;
  }

  /**
   * 处理归还操作
   */
  function handleReturn(borrowId) {
    var contentHTML = '<p style="margin-bottom:16px;">请选择归还方式：</p>' +
      '<div style="display:flex;gap:12px;margin-bottom:16px;">' +
      '<button class="btn btn-success" id="return-normal-btn">正常归还</button>' +
      '<button class="btn btn-danger" id="return-damaged-btn">损坏归还</button>' +
      '</div>' +
      '<div id="return-damage-form" style="display:none;">' +
      '<div class="form-group">' +
      '<label for="damage-desc">损坏描述 <span style="color:#dc2626;">*</span></label>' +
      '<textarea id="damage-desc" class="form-textarea" placeholder="请描述损坏情况" rows="3"></textarea>' +
      '<span class="form-error" id="damage-desc-error"></span>' +
      '</div>' +
      '<div class="form-group">' +
      '<label>损坏图片（选填）</label>' +
      '<div id="damage-upload-area"></div>' +
      '</div>' +
      '<div style="display:flex;gap:10px;margin-top:12px;">' +
      '<button class="btn btn-outline" id="return-cancel-btn">取消</button>' +
      '<button class="btn btn-danger" id="return-submit-btn">确认损坏归还</button>' +
      '</div>' +
      '</div>';

    var overlay = Modal.custom('归还设备', contentHTML);

    var damageFiles = [];

    // 正常归还
    overlay.querySelector('#return-normal-btn').addEventListener('click', async function() {
      var confirmed = await Modal.confirm('确认归还', '确定要正常归还该设备吗？');
      if (!confirmed) return;
      Modal.close(overlay);

      try {
        await API.put('/borrows/' + borrowId + '/return', { return_status: 'normal' });
        Toast.show('归还成功', 'success');
        loadMyBorrows(1);
      } catch (error) {
        Toast.show(error.message || '归还失败', 'error');
      }
    });

    // 损坏归还
    overlay.querySelector('#return-damaged-btn').addEventListener('click', function() {
      overlay.querySelector('#return-damage-form').style.display = 'block';
      Upload.createUploadArea('#damage-upload-area', {
        onChange: function(files) {
          damageFiles = files;
        },
        onError: function(msg) {
          Toast.show(msg, 'error');
        }
      });
    });

    overlay.querySelector('#return-cancel-btn').addEventListener('click', function() {
      Modal.close(overlay);
    });

    overlay.querySelector('#return-submit-btn').addEventListener('click', async function() {
      var desc = overlay.querySelector('#damage-desc').value.trim();
      var descError = overlay.querySelector('#damage-desc-error');
      descError.textContent = '';

      if (!desc) {
        descError.textContent = '请输入损坏描述';
        return;
      }

      var submitBtn = overlay.querySelector('#return-submit-btn');
      submitBtn.disabled = true;
      submitBtn.textContent = '提交中...';

      try {
        if (damageFiles.length > 0) {
          var formData = new FormData();
          formData.append('return_status', 'damaged');
          formData.append('damage_description', desc);
          damageFiles.forEach(function(file) {
            formData.append('images', file);
          });
          await API.put('/borrows/' + borrowId + '/return', formData, true);
        } else {
          await API.put('/borrows/' + borrowId + '/return', {
            return_status: 'damaged',
            damage_description: desc
          });
        }
        Toast.show('归还申请已提交', 'success');
        Modal.close(overlay);
        loadMyBorrows(1);
      } catch (error) {
        Toast.show(error.message || '提交失败', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '确认损坏归还';
      }
    });
  }

  /**
   * 查看详情
   */
  function viewDetail(borrowId) {
    window.location.href = 'device-detail.html?id=' + borrowId;
  }

  return { loadMyBorrows, renderBorrowTable, handleReturn, viewDetail };
})();