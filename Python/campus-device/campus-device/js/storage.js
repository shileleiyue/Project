/* ========================================
   Storage - localStorage 封装
   ======================================== */

const Storage = (function() {
  const TOKEN_KEY = 'campus_device_token';
  const USER_KEY = 'campus_device_user';

  /**
   * 获取令牌
   * @returns {string|null}
   */
  function getToken() {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * 设置令牌
   * @param {string} token
   */
  function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * 移除令牌
   */
  function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  }

  /**
   * 获取用户信息
   * @returns {Object|null}
   */
  function getUser() {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch (e) {
      return null;
    }
  }

  /**
   * 设置用户信息
   * @param {Object} user
   */
  function setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * 移除用户信息
   */
  function removeUser() {
    localStorage.removeItem(USER_KEY);
  }

  /**
   * 判断是否已登录
   * @returns {boolean}
   */
  function isLoggedIn() {
    return !!getToken();
  }

  /**
   * 获取用户角色
   * @returns {string|null}
   */
  function getUserRole() {
    const user = getUser();
    return user ? user.role : null;
  }

  return {
    getToken,
    setToken,
    removeToken,
    getUser,
    setUser,
    removeUser,
    isLoggedIn,
    getUserRole
  };
})();