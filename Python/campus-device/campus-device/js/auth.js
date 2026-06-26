/* ========================================
   Auth - 鉴权模块
   ======================================== */

const Auth = (function() {

  /**
   * 路由守卫 - 检查登录状态和角色权限
   * 管理员(admin)可访问所有页面
   * 维修员(repairer)只能访问维修相关页面
   * @param {string} [requiredRole] - 需要的角色，不传则只检查登录
   */
  function checkAuth(requiredRole) {
    if (!Storage.isLoggedIn()) {
      window.location.href = '/login.html';
      return false;
    }

    if (requiredRole) {
      const userRole = Storage.getUserRole();

      // 管理员可访问所有页面
      if (userRole === 'admin') {
        return true;
      }

      // 维修员只能访问维修相关页面
      if (requiredRole === 'repairer' && userRole !== 'repairer') {
        alert('无权限访问该页面');
        window.history.back();
        return false;
      }

      // 角色不匹配
      if (userRole !== requiredRole) {
        alert('无权限访问该页面');
        window.history.back();
        return false;
      }
    }

    return true;
  }

  /**
   * 登录
   * @param {string} phone - 手机号
   * @param {string} password - 密码
   * @returns {Promise<Object>}
   */
  async function login(phone, password) {
    const result = await API.post('/auth/login', { phone, password });
    var data = result.data || result;
    if (data.token) {
      Storage.setToken(data.token);
    }
    if (data.user) {
      Storage.setUser(data.user);
    }
    return result;
  }

  /**
   * 注册
   * @param {string} username - 用户名
   * @param {string} phone - 手机号
   * @param {string} password - 密码
   * @param {string} role - 角色
   * @returns {Promise<Object>}
   */
  async function register(username, phone, password, role) {
    const result = await API.post('/auth/register', {
      username,
      phone,
      password,
      role
    });
    return result;
  }

  /**
   * 退出登录
   */
  function logout() {
    Storage.removeToken();
    Storage.removeUser();
    window.location.href = '/login.html';
  }

  return { checkAuth, login, register, logout };
})();