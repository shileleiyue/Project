/* ========================================
   Device JS - 设备大厅业务逻辑 (IIFE)
   ======================================== */

const DeviceModule = (function() {

  const DEVICE_TYPES = {
    '': '全部类型',
    'laptop': '笔记本电脑',
    'phone': '手机',
    'tablet': '平板电脑',
    'camera': '相机',
    'projector': '投影仪',
    'other': '其他'
  };

  const STATUS_MAP = {
    'available': { label: '可借用', cls: 'status-available' },
    'pending_borrow': { label: '待审核', cls: 'status-pending_borrow' },
    'borrowed': { label: '已借出', cls: 'status-borrowed' },
    'pending_return': { label: '待归还', cls: 'status-pending_return' },
    'damaged': { label: '已损坏', cls: 'status-damaged' },
    'offline': { label: '已下架', cls: 'status-offline' },
    'scrapped': { label: '已报废', cls: 'status-scrapped' }
  };

  let currentPage = 1;
  let currentKeyword = '';
  let currentType = '';
  let currentStatus = '';

  /**
   * 加载设备列表
   */
  async function loadDevices(page, keyword, type, status) {
    page = page || 1;
    keyword = keyword || '';
    type = type || '';
    status = status || '';

    currentPage = page;
    currentKeyword = keyword;
    currentType = type;
    currentStatus = status;

    const grid = document.getElementById('device-grid');
    const paginatorContainer = '#device-paginator';

    // 显示加载状态
    if (grid) {
      grid.innerHTML = '<div class="loading-spinner">加载中...</div>';
    }

    try {
      const params = new URLSearchParams();
      params.append('page', page);
      params.append('page_size', AppConfig.PAGE_SIZE);
      if (keyword) params.append('keyword', keyword);
      if (type) params.append('type', type);
      if (status) params.append('status', status);

      const result = await API.get('/devices?' + params.toString());

      const devices = result.data?.list || result.data?.items || result.items || [];
      const total = result.data?.total || result.total || 0;
      const totalPages = Paginator.calcTotalPages(total);

      renderDeviceList(devices);
      Paginator.render(paginatorContainer, page, totalPages, function(newPage) {
        loadDevices(newPage, currentKeyword, currentType, currentStatus);
      });

      // 更新结果计数
      var countEl = document.getElementById('device-count');
      if (countEl) {
        countEl.textContent = '共 ' + total + ' 台设备';
      }
    } catch (error) {
      if (grid) {
        grid.innerHTML = '<div class="empty-state"><p>加载失败：' + Utils.escapeHtml(error.message) + '</p></div>';
      }
      Toast.show(error.message || '加载设备列表失败', 'error');
    }
  }

  /**
   * 渲染设备卡片列表
   */
  function renderDeviceList(devices) {
    const grid = document.getElementById('device-grid');
    if (!grid) return;

    if (!devices || devices.length === 0) {
      grid.innerHTML = '<div class="empty-state"><p>暂无设备</p></div>';
      return;
    }

    var html = '';
    devices.forEach(function(device) {
      var statusInfo = STATUS_MAP[device.status] || { label: device.status || '未知', cls: 'status-offline' };
      var typeName = DEVICE_TYPES[device.type] || device.type || '未知';

      html += '<div class="device-card" onclick="window.location.href=\'pages/device-detail.html?id=' + device.id + '\'">';
      html += '<img class="device-card-img" src="' + Utils.escapeHtml(device.image || '') + '" alt="' + Utils.escapeHtml(device.name) + '" onerror="this.src=\'assets/placeholder.png\'">';
      html += '<div class="device-card-body">';
      html += '<div class="device-card-name">' + Utils.escapeHtml(device.name) + '</div>';
      html += '<div class="device-card-meta">';
      html += '<span class="device-card-type">' + Utils.escapeHtml(typeName) + '</span>';
      html += '<span class="status-tag ' + statusInfo.cls + '">' + statusInfo.label + '</span>';
      html += '</div>';
      html += '<div class="device-card-location">' + Utils.escapeHtml(device.location || '未指定位置') + '</div>';
      html += '</div>';
      html += '</div>';
    });

    grid.innerHTML = html;
  }

  /**
   * 初始化搜索和筛选事件
   */
  function initSearchListeners() {
    var searchInput = document.getElementById('search-keyword');
    var typeSelect = document.getElementById('search-type');
    var statusSelect = document.getElementById('search-status');

    var doSearch = Utils.debounce(function() {
      loadDevices(1, searchInput ? searchInput.value.trim() : '', typeSelect ? typeSelect.value : '', statusSelect ? statusSelect.value : '');
    }, 300);

    if (searchInput) {
      searchInput.addEventListener('input', doSearch);
    }
    if (typeSelect) {
      typeSelect.addEventListener('change', doSearch);
    }
    if (statusSelect) {
      statusSelect.addEventListener('change', doSearch);
    }
  }

  return { loadDevices, renderDeviceList, initSearchListeners };
})();