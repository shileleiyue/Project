// API 封装（axios CDN 版）
window.API = axios.create({ baseURL: 'http://127.0.0.1:8000/api', timeout: 20000 });

// 关键拦截：给所有请求 URL 自动补 trailing slash，避免 Django APPEND_SLASH 在 POST 时抛 RuntimeError
API.interceptors.request.use(cfg => {
  const tok = localStorage.getItem('ls_access');
  if (tok) cfg.headers.Authorization = 'Bearer ' + tok;
  if (cfg.url && !cfg.url.endsWith('/') && !cfg.url.includes('.')) {
    const q = cfg.url.indexOf('?');
    if (q >= 0) cfg.url = cfg.url.slice(0, q) + '/' + cfg.url.slice(q);
    else cfg.url = cfg.url + '/';
  }
  return cfg;
});
API.interceptors.response.use(r => r, err => {
  const msg = err.response?.data?.detail || err.response?.data?.message || err.message;
  ElementPlus.ElMessage.error(msg || '请求失败');
  if (err.response?.status === 401) {
    localStorage.clear(); location.href = 'index.html';
  }
  return Promise.reject(err);
});

// =========== helpers ===========
window.roleLabel = (r) => ({ admin: '管理员', teacher: '教师', student: '学生' }[r] || r);
window.questionTypeLabel = (t) => ({ single: '单选', multi: '多选', judge: '判断' }[t] || t);
window.formatDuration = (sec) => {
  sec = sec || 0; const m = Math.floor(sec/60), h = Math.floor(m/60);
  if (h) return h + '小时' + (m%60) + '分钟';
  return m + '分钟';
};

window.confirm = (msg) => ElementPlus.ElMessageBox.confirm(msg, '提示', {
  confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
}).then(() => true).catch(() => false);
