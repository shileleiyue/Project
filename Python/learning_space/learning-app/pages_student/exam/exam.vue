<template>
  <view class="page">
    <view class="card" v-for="e in exams" :key="e.id">
      <view class="e-title">{{ e.title }}</view>
      <view class="e-sub">时长 {{ e.duration_minutes }} 分 · 满分 {{ e.total_score }} · 及格 {{ e.passing_score }}</view>
      <view class="btn-primary" @tap="startExam(e)">开始考试</view>
    </view>
    <view v-if="!exams.length" class="empty">📝 暂无可用考试</view>
  </view>
</template>
<script>
import { API } from '@/api/request.js'
export default {
  data() { return { exams: [] } },
  onLoad() { API.exams().then(r => this.exams = r.results || r) },
  methods: {
    async startExam(e) {
      uni.showModal({
        title: e.title, content: `确定开始考试？共 ${e.total_score} 分`,
        success: async (res) => {
          if (res.confirm) {
            try {
              await API.startExam(e.id)
              uni.showToast({ title: '开考成功', icon: 'success' })
            } catch(err) {}
          }
        }
      })
    }
  }
}
</script>
<style scoped>
.page { padding: 20rpx; }
.card { background: #fff; border-radius: 16rpx; padding: 30rpx; margin-bottom: 20rpx; }
.e-title { font-size: 32rpx; font-weight: 600; color: #303133; margin-bottom: 10rpx; }
.e-sub { font-size: 24rpx; color: #909399; margin-bottom: 24rpx; }
.btn-primary { text-align: center; background: #409eff; color: #fff; padding: 20rpx 0; border-radius: 10rpx; }
.empty { text-align: center; padding: 80rpx; color: #c0c4cc; }
</style>
