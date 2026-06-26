/* ========================================
   Admin JS - 管理后台业务逻辑 (IIFE)
   ======================================== */

const AdminModule = (function() {

  var DEVICE_TYPES = {
    '': '请选择类型',
    'laptop': '笔记本电脑',
    'phone': '手机',
    'tablet': '平板电脑',
    'camera': '相机',
    'projector': '投影仪',
    'other': '其他'
  };

  var STATUS_MAP = {
    'available': { label: '可借用', cls: 'status-available' },
    'pending_borrow': { label: '待审核', cls: 'status-pending_borrow' },
    'borrowed': { label: '已借出', cls: 'status-borrowed' },
    'pending_return': { label: '待归还', cls: 'status-pending_return' },
    'damaged': { label: '已损坏', cls: 'status-damaged' },
    'offline': { label: '已下架', cls: 'status-offline' },
    'scrapped': { label: '已报废', cls: 'status-scrapped' }
  };

  var currentPage = 1;
  var currentKeyword = '';

  /**
   * 加载管理设备列表
   */
  async function loadAdminDevices(page, keyword) {
    page = page || 1;
    keyword = keyword || '';
    currentPage = page;
    currentKeyword = keyword;

    var tbody = document.getElementById('admin-device-tbody');
    if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;">加载中...</td></tr>';

    try {
      var params = new URLSearchParams();
      params.append('page', page);
      params.append('page_size', AppConfig.PAGE_SIZE);
      if (keyword) params.append('keyword', keyword);

      var result = await API.get('/devices?' + params.toString());
      var devices = result.data?.list || result.data?.items || result.items || [];
      var total = result.data?.total || result.total || 0;
      var totalPages = Paginator.calcTotalPages(total);

      if (!devices || devices.length === 0) {
        if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:60px;color:#999;">暂无设备</td></tr>';
      } else {
        var html = '';
        devices.forEach(function(device) {
          var statusInfo = STATUS_MAP[device.status] || { label: device.status || '未知', cls: 'status-offline' };
          var typeName = DEVICE_TYPES[device.type] || device.type || '未知';

          html += '<tr>';
          html += '<td>' + Utils.escapeHtml(device.name) + '</td>';
          html += '<td>' + Utils.escapeHtml(typeName) + '</td>';
          html += '<td><span class="status-tag ' + statusInfo.cls + '">' + statusInfo.label + '</span></td>';
          html += '<td>' + Utils.escapeHtml(device.location || '-') + '</td>';
          html += '<td><div class="admin-actions">';
          html += '<button class="btn btn-outline" onclick="AdminModule.openDeviceForm(' + device.id + ')">编辑</button>';
          html += '<button class="btn btn-warning" style="background-color:#f59e0b;color:#fff;border-color:#f59e0b;padding:4px 12px;font-size:12px;" onclick="AdminModule.handleOffline(' + device.id + ')">下架</button>';
          html += '<button class="btn btn-danger" onclick="AdminModule.handleDelete(' + device.id + ')">删除</button>';
          html += '</div></td>';
          html += '</tr>';
        });
        tbody.innerHTML = html;
      }

      Paginator.render('#admin-device-paginator', page, totalPages, function(newPage) {
        loadAdminDevices(newPage, currentKeyword);
      });
    } catch (error) {
      if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:40px;color:#dc2626;">加载失败：' + Utils.escapeHtml(error.message) + '</td></tr>';
      Toast.show(error.message || '加载设备列表失败', 'error');
    }
  }

  /**
   * 打开新增/编辑设备表单
   */
  function openDeviceForm(device) {
    var isEdit = !!device;
    var title = isEdit ? '编辑设备' : '新增设备';

    // 如果传入的是设备ID，需要先获取设备详情
    if (typeof device === 'number' || typeof device === 'string') {
      loadDeviceAndOpenForm(device, title);
      return;
    }

    renderDeviceForm(device, title);
  }

  async function loadDeviceAndOpenForm(deviceId, title) {
    try {
      var result = await API.get('/devices/' + deviceId);
      var device = result.data || result;
      renderDeviceForm(device, title);
    } catch (error) {
      Toast.show(error.message || '获取设备信息失败', 'error');
    }
  }

  function renderDeviceForm(device, title) {
    var isEdit = !!device;
    var typeOptions = '';
    Object.keys(DEVICE_TYPES).forEach(function(key) {
      if (!key) return;
      var selected = device && device.type === key ? ' selected' : '';
      typeOptions += '<option value="' + key + '"' + selected + '>' + DEVICE_TYPES[key] + '</option>';
    });

    var contentHTML = '<div class="form-group">' +
      '<label for="device-name">设备名称 <span style="color:#dc2626;">*</span></label>' +
      '<input type="text" id="device-name" class="form-input" placeholder="请输入设备名称" value="' + Utils.escapeHtml(device ? device.name || '' : '') + '">' +
      '<span class="form-error" id="device-name-error"></span>' +
      '</div>' +
      '<div class="form-group">' +
      '<label for="device-type">设备类型 <span style="color:#dc2626;">*</span></label>' +
      '<select id="device-type" class="form-select">' +
      '<option value="">请选择类型</option>' + typeOptions +
      '</select>' +
      '<span class="form-error" id="device-type-error"></span>' +
      '</div>' +
      '<div class="form-group">' +
      '<label for="device-desc">描述</label>' +
      '<textarea id="device-desc" class="form-textarea" placeholder="请输入设备描述" rows="3">' + Utils.escapeHtml(device ? device.description || '' : '') + '</textarea>' +
      '</div>' +
      '<div class="form-group">' +
      '<label for="device-location">位置</label>' +
      '<input type="text" id="device-location" class="form-input" placeholder="请输入设备位置" value="' + Utils.escapeHtml(device ? device.location || '' : '') + '">' +
      '</div>' +
      '<div class="form-group">' +
      '<label for="device-image">图片URL</label>' +
      '<input type="text" id="device-image" class="form-input" placeholder="请输入图片URL" value="' + Utils.escapeHtml(device ? device.image || '' : '') + '">' +
      '</div>' +
      '<div class="modal-footer">' +
      '<button class="btn btn-outline" id="device-form-cancel">取消</button>' +
      '<button class="btn btn-primary" id="device-form-submit">' + (isEdit ? '保存修改' : '新增设备') + '</button>' +
      '</div>';

    var overlay = Modal.custom(title, contentHTML);

    overlay.querySelector('#device-form-cancel').addEventListener('click', function() {
      Modal.close(overlay);
    });

    overlay.querySelector('#device-form-submit').addEventListener('click', async function() {
      var name = overlay.querySelector('#device-name').value.trim();
      var type = overlay.querySelector('#device-type').value;
      var desc = overlay.querySelector('#device-desc').value.trim();
      var location = overlay.querySelector('#device-location').value.trim();
      var imageUrl = overlay.querySelector('#device-image').value.trim();

      var nameError = overlay.querySelector('#device-name-error');
      var typeError = overlay.querySelector('#device-type-error');
      nameError.textContent = '';
      typeError.textContent = '';

      var valid = true;
      if (!name) { nameError.textContent = '请输入设备名称'; valid = false; }
      if (!type) { typeError.textContent = '请选择设备类型'; valid = false; }
      if (!valid) return;

      var data = { name: name, type: type };
      if (desc) data.description = desc;
      if (location) data.location = location;
      if (imageUrl) data.image = imageUrl;

      var submitBtn = overlay.querySelector('#device-form-submit');
      submitBtn.disabled = true;
      submitBtn.textContent = '提交中...';

      try {
        if (isEdit) {
          await API.put('/devices/' + device.id, data);
          Toast.show('设备更新成功', 'success');
        } else {
          await API.post('/devices', data);
          Toast.show('设备新增成功', 'success');
        }
        Modal.close(overlay);
        loadAdminDevices(currentPage, currentKeyword);
      } catch (error) {
        Toast.show(error.message || '操作失败', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = isEdit ? '保存修改' : '新增设备';
      }
    });
  }

  /**
   * 下架设备
   */
  async function handleOffline(deviceId) {
    var confirmed = await Modal.confirm('下架设备', '确定要下架该设备吗？下架后设备将不可借用。');
    if (!confirmed) return;

    try {
      await API.put('/devices/' + deviceId + '/offline');
      Toast.show('设备已下架', 'success');
      loadAdminDevices(currentPage, currentKeyword);
    } catch (error) {
      Toast.show(error.message || '下架失败', 'error');
    }
  }

  /**
   * 删除设备
   */
  async function handleDelete(deviceId) {
    var confirmed = await Modal.confirm('删除设备', '确定要删除该设备吗？此操作不可恢复。');
    if (!confirmed) return;

    try {
      await API.del('/devices/' + deviceId);
      Toast.show('设备已删除', 'success');
      loadAdminDevices(currentPage, currentKeyword);
    } catch (error) {
      Toast.show(error.message || '删除失败', 'error');
    }
  }

  return { loadAdminDevices, openDeviceForm, handleOffline, handleDelete };
})();