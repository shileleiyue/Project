<template>
  <view class="page">
    <view class="card" v-for="s in list" :key="s.id">
      <view class="row">
        <view class="s-name">{{ s.name }}</view>
        <view class="s-no">{{ s.student_no }}</view>
      </view>
      <view class="s-sub">{{ s.college }} · {{ s.major }} · {{ s.grade }}</view>
      <view class="s-contact">{{ s.contact || '未填写联系方式' }}</view>
    </view>
    <view v-if="!list.length" class="empty">👥 暂无学生</view>
  </view>
</template>
<script>
import { API } from '@/api/request.js'
export default {
  data() { return { list: [] } },
  onLoad() { API.students({ page_size: 500 }).then(r => this.list = r.results || r) }
}
</script>
<style scoped>
.page { padding: 20rpx; }
.card { background: #fff; border-radius: 16rpx; padding: 24rpx; margin-bottom: 16rpx; }
.row { display: flex; justify-content: space-between; }
.s-name { font-size: 30rpx; font-weight: 600; color: #303133; }
.s-no { font-size: 24rpx; color: #409eff; }
.s-sub { font-size: 24rpx; color: #606266; margin-top: 6rpx; }
.s-contact { font-size: 24rpx; color: #909399; margin-top: 6rpx; }
.empty { text-align: center; padding: 80rpx; color: #c0c4cc; }
</style>
