<template>
  <view class="login-page">
    <view class="logo">学</view>
    <view class="title">个性化网络学习空间</view>
    <view class="subtitle">Personalized E-Learning Platform</view>

    <view class="role-switch">
      <view class="role-item" :class="{ active: role==='student' }" @tap="role='student'">学生</view>
      <view class="role-item" :class="{ active: role==='teacher' }" @tap="role='teacher'">教师</view>
      <view class="role-item" :class="{ active: role==='admin' }" @tap="role='admin'">管理员</view>
    </view>

    <view class="form-box">
      <input class="form-input" v-model="username" placeholder="用户名" />
      <input class="form-input" v-model="password" placeholder="密码" password />
      <view class="btn-primary" :class="{ loading: loading }" @tap="doLogin">登录</view>
    </view>

    <view class="tip">
      测试账号：<text>{{ tip }}</text>
    </view>
  </view>
</template>

<script>
import { login } from '@/utils/auth.js'
export default {
  data() {
    return { role: 'student', username: '', password: '', loading: false }
  },
  computed: {
    tip() {
      return { student: 'student / student123', teacher: 'teacher / teacher123', admin: 'admin / admin123' }[this.role]
    }
  },
  methods: {
    async doLogin() {
      if (!this.username || !this.password) { uni.showToast({ title: '请输入用户名密码', icon: 'none' }); return }
      this.loading = true
      try {
        const user = await login(this.username, this.password)
        if (user.role !== this.role) {
          uni.showToast({ title: '角色不匹配', icon: 'none' })
          this.loading = false
          return
        }
        uni.showToast({ title: '登录成功', icon: 'success' })
        setTimeout(() => uni.reLaunch({ url: '/pages/home/home' }), 500)
      } finally { this.loading = false }
    }
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; background: linear-gradient(135deg,#667eea,#764ba2); padding: 80rpx 60rpx 40rpx; }
.logo { width: 100rpx; height: 100rpx; border-radius: 24rpx; background: #fff; color: #764ba2; font-size: 54rpx; font-weight: bold; display: flex; align-items: center; justify-content: center; margin: 0 auto 30rpx; }
.title { text-align: center; font-size: 40rpx; color: #fff; font-weight: 600; }
.subtitle { text-align: center; font-size: 24rpx; color: rgba(255,255,255,.8); margin-bottom: 50rpx; }
.role-switch { display: flex; background: rgba(255,255,255,.2); border-radius: 12rpx; padding: 6rpx; margin-bottom: 40rpx; }
.role-item { flex: 1; text-align: center; padding: 16rpx 0; color: rgba(255,255,255,.7); border-radius: 10rpx; font-size: 28rpx; }
.role-item.active { background: #fff; color: #409eff; font-weight: 600; }
.form-box { background: #fff; border-radius: 16rpx; padding: 40rpx 36rpx; }
.form-input { height: 88rpx; border-bottom: 1rpx solid #eee; font-size: 30rpx; margin-bottom: 20rpx; }
.btn-primary { margin-top: 30rpx; }
.btn-primary.loading { opacity: .6; }
.tip { text-align: center; color: rgba(255,255,255,.8); font-size: 24rpx; margin-top: 30rpx; }
.tip text { color: #fff; font-family: Consolas, monospace; }
</style>
