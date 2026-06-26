/* ========================================
   App - 主入口 / 路由分发
   ======================================== */

const App = (function() {

  /**
   * 获取当前页面名称（不含路径和扩展名）
   * @returns {string}
   */
  function getCurrentPage() {
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1);
    return filename.replace('.html', '');
  }

  /**
   * 高亮当前页面的导航栏菜单项
   */
  function highlightNav() {
    const currentPage = getCurrentPage();
    const navItems = document.querySelectorAll('.navbar-item');
    navItems.forEach((item) => {
      const page = item.dataset.page;
      if (page === currentPage) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  }

  /**
   * 高亮侧边栏当前菜单项
   */
  function highlightSidebar() {
    const currentPage = getCurrentPage();
    const sidebarItems = document.querySelectorAll('.sidebar-menu-item');
    sidebarItems.forEach((item) => {
      const page = item.dataset.page;
      if (page === currentPage) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  }

  /**
   * 页面路由映射与初始化
   * 根据当前页面路径执行对应的初始化逻辑
   */
  function init() {
    highlightNav();
    highlightSidebar();

    const page = getCurrentPage();

    switch (page) {
      case 'login':
        initLoginPage();
        break;
      case 'register':
        initRegisterPage();
        break;
      case 'devices':
        initDevicesPage();
        break;
      case 'device-detail':
        initDeviceDetailPage();
        break;
      case 'device-form':
        initDeviceFormPage();
        break;
      case 'borrow':
        initBorrowPage();
        break;
      case 'repairs':
        initRepairsPage();
        break;
      case 'repair-detail':
        initRepairDetailPage();
        break;
      case 'repair-form':
        initRepairFormPage();
        break;
      case 'dashboard':
        initDashboardPage();
        break;
      case 'users':
        initUsersPage();
        break;
      default:
        // 未知页面，不执行特殊初始化
        break;
    }
  }

  // ---- 各页面初始化函数（占位，后续Task中实现具体逻辑） ----

  function initLoginPage() {
    // 登录页初始化逻辑
  }

  function initRegisterPage() {
    // 注册页初始化逻辑
  }

  function initDevicesPage() {
    // 设备列表页初始化逻辑
  }

  function initDeviceDetailPage() {
    // 设备详情页初始化逻辑
  }

  function initDeviceFormPage() {
    // 设备表单页初始化逻辑
  }

  function initBorrowPage() {
    // 借用管理页初始化逻辑
  }

  function initRepairsPage() {
    // 维修管理页初始化逻辑
  }

  function initRepairDetailPage() {
    // 维修详情页初始化逻辑
  }

  function initRepairFormPage() {
    // 维修表单页初始化逻辑
  }

  function initDashboardPage() {
    // 仪表盘页初始化逻辑
  }

  function initUsersPage() {
    // 用户管理页初始化逻辑
  }

  // DOM 加载完成后自动初始化
  document.addEventListener('DOMContentLoaded', init);

  return { init, getCurrentPage };
})();