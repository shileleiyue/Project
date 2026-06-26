<template>
  <view>
    <!-- 学生首页 -->
    <block v-if="role==='student'">
      <view class="hero">
        <view class="hero-title">你好，{{ profile.first_name || profile.username }} 👋</view>
        <view class="hero-sub">今天也要加油学习哦～</view>
      </view>
      <view class="grid">
        <view class="stat" v-for="(v,k) in overview" :key="k">
          <view class="stat-num">{{ v }}</view>
          <view class="stat-label">{{ statLabel[k] }}</view>
        </view>
      </view>
      <view class="menu-grid">
        <view class="menu-item" @tap="go('/pages_student/courses/courses')">
          <view class="menu-icon" style="background:#409eff">📚</view><view>课程学习</view>
        </view>
        <view class="menu-item" @tap="go('/pages_student/exam/exam')">
          <view class="menu-icon" style="background:#e6a23c">📝</view><view>考试中心</view>
        </view>
        <view class="menu-item"><view class="menu-icon" style="background:#67c23a">📊</view><view>学习分析</view></view>
        <view class="menu-item"><view class="menu-icon" style="background:#f56c6c">⚠️</view><view>错题本</view></view>
      </view>
    </block>

    <!-- 教师首页 -->
    <block v-else-if="role==='teacher'">
      <view class="hero teacher">
        <view class="hero-title">李老师，你好 👋</view>
        <view class="hero-sub">今日已服务 {{ stats.questions || 0 }} 道题库</view>
      </view>
      <view class="grid">
        <view class="stat" v-for="(v,k) in stats" :key="k">
          <view class="stat-num">{{ v }}</view>
          <view class="stat-label">{{ statLabel[k] }}</view>
        </view>
      </view>
      <view class="menu-grid">
        <view class="menu-item"><view class="menu-icon" style="background:#409eff">📚</view><view>课程管理</view></view>
        <view class="menu-item" @tap="go('/pages_teacher/questions/questions')">
          <view class="menu-icon" style="background:#e6a23c">📝</view><view>题库管理</view>
        </view>
        <view class="menu-item"><view class="menu-icon" style="background:#67c23a">📄</view><view>试卷管理</view></view>
        <view class="menu-item"><view class="menu-icon" style="background:#909399">📊</view><view>学生成绩</view></view>
      </view>
    </block>

    <!-- 管理员首页 -->
    <block v-else>
      <view class="hero admin">
        <view class="hero-title">管理员控制台</view>
        <view class="hero-sub">系统整体运行良好</view>
      </view>
      <view class="grid">
        <view class="stat"><view class="stat-num">1</view><view class="stat-label">学生</view></view>
        <view class="stat"><view class="stat-num">1</view><view class="stat-label">教师</view></view>
        <view class="stat"><view class="stat-num">2</view><view class="stat-label">课程</view></view>
        <view class="stat"><view class="stat-num">7</view><view class="stat-label">题库</view></view>
      </view>
      <view class="menu-grid">
        <view class="menu-item" @tap="go('/pages_admin/students/students')">
          <view class="menu-icon" style="background:#409eff">👥</view><view>学生管理</view>
        </view>
        <view class="menu-item"><view class="menu-icon" style="background:#e6a23c">📚</view><view>课程列表</view></view>
        <view class="menu-item"><view class="menu-icon" style="background:#67c23a">👨‍🏫</view><view>教师列表</view></view>
        <view class="menu-item" @tap="logout"><view class="menu-icon" style="background:#f56c6c">🚪</view><view>退出登录</view></view>
      </view>
    </block>
  </view>
</template>

<script>
import { API } from '@/api/request.js'
import { getUser, logout as doLogout } from '@/utils/auth.js'
export default {
  data() { return { profile: {}, role: '', overview: {}, stats: {} } },
  computed: {
    statLabel() {
      return {
        today_duration_minutes: '今日学习(分)', week_duration_minutes: '本周学习(分)',
        total_materials: '累计资料数', days_active: '活跃天数',
        courses: '我教授的课程数', questions: '题库数量',
        exams: '试卷数量', materials: '资料上传',
      }
    }
  },
  onLoad() {
    const u = getUser()
    if (!u) { uni.reLaunch({ url: '/pages/login/login' }); return }
    this.profile = u; this.role = u.role
    if (u.role === 'student') API.overview().then(r => this.overview = r)
    if (u.role === 'teacher') {
      API.courses().then(r => this.stats.courses = r.count || r.length || 0)
      API.questions().then(r => this.stats.questions = r.count || r.length || 0)
    }
  },
  methods: {
    go(url) { uni.navigateTo({ url }) },
    logout() { doLogout(); uni.reLaunch({ url: '/pages/login/login' }) }
  }
}
</script>

<style scoped>
.hero { padding: 60rpx 40rpx 40rpx; background: linear-gradient(135deg,#409eff,#764ba2); color: #fff; }
.hero.teacher { background: linear-gradient(135deg,#e6a23c,#f56c6c); }
.hero.admin   { background: linear-gradient(135deg,#303133,#606266); }
.hero-title { font-size: 40rpx; font-weight: 600; }
.hero-sub { font-size: 26rpx; opacity: .85; margin-top: 8rpx; }
.grid { display: flex; flex-wrap: wrap; padding: 30rpx 20rpx; }
.stat { width: 50%; padding: 20rpx; box-sizing: border-box; }
.stat-num { font-size: 40rpx; font-weight: 700; color: #303133; }
.stat-label { font-size: 24rpx; color: #909399; margin-top: 6rpx; }
.menu-grid { display: flex; flex-wrap: wrap; padding: 10rpx; }
.menu-item { width: 25%; text-align: center; padding: 30rpx 10rpx; }
.menu-icon { width: 88rpx; height: 88rpx; border-radius: 20rpx; margin: 0 auto 10rpx; display: flex; align-items: center; justify-content: center; font-size: 36rpx; color: #fff; }
</style>
