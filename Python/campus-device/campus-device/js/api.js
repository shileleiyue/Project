/* ========================================
   API - 请求封装
   ======================================== */

const API = (function() {

  /**
   * 统一请求方法
   * @param {string} method - 请求方法 GET/POST/PUT/DELETE
   * @param {string} path - 请求路径（不含baseURL）
   * @param {Object|FormData} [data] - 请求体数据
   * @param {boolean} [isFormData=false] - 是否为FormData
   * @returns {Promise<Object>} 响应数据
   */
  async function request(method, path, data, isFormData) {
    const url = AppConfig.API_BASE_URL + path;
    const token = Storage.getToken();

    const headers = {};

    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }

    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }

    const options = {
      method: method,
      headers: headers
    };

    if (data && method !== 'GET') {
      if (isFormData) {
        options.body = data;
      } else {
        options.body = JSON.stringify(data);
      }
    }

    try {
      const response = await fetch(url, options);

      // 401 未授权，清除token并跳转登录页
      if (response.status === 401) {
        Storage.removeToken();
        Storage.removeUser();
        window.location.href = '/login.html';
        return Promise.reject(new Error('登录已过期，请重新登录'));
      }

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || result.detail || '请求失败');
      }

      return result;
    } catch (error) {
      // 网络错误
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
        throw new Error('网络连接失败，请检查网络');
      }
      throw error;
    }
  }

  /**
   * GET 请求
   * @param {string} path
   * @returns {Promise<Object>}
   */
  function get(path) {
    return request('GET', path);
  }

  /**
   * POST 请求
   * @param {string} path
   * @param {Object|FormData} data
   * @param {boolean} [isFormData=false]
   * @returns {Promise<Object>}
   */
  function post(path, data, isFormData) {
    return request('POST', path, data, isFormData);
  }

  /**
   * PUT 请求
   * @param {string} path
   * @param {Object|FormData} data
   * @param {boolean} [isFormData=false]
   * @returns {Promise<Object>}
   */
  function put(path, data, isFormData) {
    return request('PUT', path, data, isFormData);
  }

  /**
   * DELETE 请求
   * @param {string} path
   * @returns {Promise<Object>}
   */
  function del(path) {
    return request('DELETE', path);
  }

  return { get, post, put, del, request };
})();