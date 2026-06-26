/**
 * uni.request 封装
 * 统一处理：baseURL、JWT 鉴权、错误拦截、loading
 */
export function request(options) {
  const app = getApp()
  const token = uni.getStorageSync('ls_access')
  const url = (options.url.startsWith('http') ? options.url : app.globalData.baseUrl + options.url)
  const header = { 'Content-Type': 'application/json', ...(options.header || {}) }
  if (token) header['Authorization'] = 'Bearer ' + token

  return new Promise((resolve, reject) => {
    uni.request({
      url,
      method: options.method || 'GET',
      data: options.data,
      header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(res.data)
        else if (res.statusCode === 401) {
          uni.removeStorageSync('ls_access')
          uni.removeStorageSync('ls_user')
          uni.reLaunch({ url: '/pages/login/login' })
          reject(res)
        } else {
          const msg = res.data?.detail || res.data?.message || `请求失败 ${res.statusCode}`
          uni.showToast({ title: msg, icon: 'none' })
          reject(res)
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      }
    })
  })
}

export const API = {
  // 鉴权
  login: (username, password) => request({ url: '/auth/login', method: 'POST', data: { username, password } }),
  me: () => request({ url: '/auth/me' }),
  // 学生
  students: (params) => request({ url: '/students', data: params }),
  studentMe: () => request({ url: '/students/me' }),
  // 成绩
  scores: (params) => request({ url: '/student-courses', data: params }),
  myScores: () => request({ url: '/student-courses/my-scores' }),
  // 课程 & 知识点
  courses: () => request({ url: '/courses' }),
  kpTree: (courseId) => request({ url: `/courses/${courseId}/knowledge` }),
  // 资料
  materials: (params) => request({ url: '/materials', data: params }),
  // 题库 & 试卷
  questions: (params) => request({ url: '/questions', data: params }),
  exams: () => request({ url: '/exams' }),
  startExam: (id) => request({ url: `/exams/${id}/start`, method: 'POST' }),
  submitExam: (id, answers) => request({ url: `/exams/${id}/submit`, method: 'POST', data: { answers } }),
  examRecords: () => request({ url: '/exam-records' }),
  wrongTopics: (id) => request({ url: `/exam-records/${id}/wrong` }),
  // 学习分析
  overview: () => request({ url: '/stats/overview' }),
  dailyTrend: () => request({ url: '/stats/daily-trend' }),
  weakPoints: () => request({ url: '/stats/weak-points' }),
  preferences: () => request({ url: '/stats/preferences' }),
  recommendations: () => request({ url: '/stats/recommendations' }),
}
