/* ========================================
   Config - 全局配置
   ======================================== */

const AppConfig = (function() {
  const API_BASE_URL = 'http://localhost:8000/api';
  const PAGE_SIZE = 10;

  return { API_BASE_URL, PAGE_SIZE };
})();