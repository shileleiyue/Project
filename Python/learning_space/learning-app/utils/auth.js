import { API } from '@/api/request.js'

export async function login(username, password) {
  const { access, refresh } = await API.login(username, password)
  uni.setStorageSync('ls_access', access)
  uni.setStorageSync('ls_refresh', refresh)
  const user = await API.me()
  uni.setStorageSync('ls_user', JSON.stringify(user))
  return user
}

export function logout() {
  uni.removeStorageSync('ls_access')
  uni.removeStorageSync('ls_refresh')
  uni.removeStorageSync('ls_user')
}

export function getUser() {
  return JSON.parse(uni.getStorageSync('ls_user') || 'null')
}

export function isLoggedIn() {
  return !!uni.getStorageSync('ls_access')
}
