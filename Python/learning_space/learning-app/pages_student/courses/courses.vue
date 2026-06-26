<template>
  <view class="page">
    <view class="card" v-for="c in courses" :key="c.id" @tap="openDetail(c)">
      <view class="cover">{{ c.name[0] }}</view>
      <view class="info">
        <view class="name">{{ c.name }}</view>
        <view class="desc">{{ c.description || '暂无简介' }}</view>
      </view>
    </view>
    <view v-if="!courses.length" class="empty">📖 暂无课程</view>
  </view>
</template>
<script>
import { API } from '@/api/request.js'
export default {
  data() { return { courses: [] } },
  onLoad() { API.courses().then(r => this.courses = r.results || r) },
  methods: {
    openDetail(c) { uni.showToast({ title: c.name, icon: 'none' }) }
  }
}
</script>
<style scoped>
.page { padding: 20rpx; }
.card { display: flex; background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 20rpx; }
.cover { width: 96rpx; height: 96rpx; border-radius: 16rpx; background: linear-gradient(135deg,#667eea,#764ba2); color: #fff; font-size: 48rpx; font-weight: 600; display: flex; align-items: center; justify-content: center; margin-right: 20rpx; }
.info { flex: 1; }
.name { font-size: 30rpx; font-weight: 600; color: #303133; }
.desc { font-size: 24rpx; color: #909399; margin-top: 8rpx; }
.empty { text-align: center; padding: 80rpx; color: #c0c4cc; }
</style>
