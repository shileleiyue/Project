<template>
  <view class="page">
    <view class="header">
      <view class="h-title">题库管理</view>
      <view class="btn-primary" style="padding:10rpx 24rpx;font-size:26rpx">+ 新建</view>
    </view>
    <view class="card" v-for="q in list" :key="q.id">
      <view class="q-tag">{{ typeLabel[q.question_type] }}</view>
      <view class="q-title">{{ q.title }}</view>
      <view class="q-sub">难度 {{ q.difficulty }} · 解析：{{ q.analysis || '—' }}</view>
    </view>
  </view>
</template>
<script>
import { API } from '@/api/request.js'
export default {
  data() { return { list: [], typeLabel: { single: '单选', multi: '多选', judge: '判断' } } },
  onLoad() { API.questions({ page_size: 100 }).then(r => this.list = r.results || r) }
}
</script>
<style scoped>
.page { padding: 20rpx; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20rpx; }
.h-title { font-size: 32rpx; font-weight: 600; }
.btn-primary { display: inline-block; background: #409eff; color: #fff; border-radius: 8rpx; }
.card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 16rpx; }
.q-tag { display: inline-block; background: #f0f2f5; color: #606266; font-size: 22rpx; padding: 4rpx 12rpx; border-radius: 20rpx; margin-bottom: 10rpx; }
.q-title { font-size: 28rpx; color: #303133; font-weight: 500; }
.q-sub { font-size: 24rpx; color: #909399; margin-top: 10rpx; }
</style>
