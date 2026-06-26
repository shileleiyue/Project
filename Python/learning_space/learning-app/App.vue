<script>
export default {
  globalData: {
    userInfo: null,
    // 开发环境（H5 / 模拟器）用本机，微信小程序正式部署时改成后端域名
    baseUrl: 'http://127.0.0.1:8000/api'
  },
  onLaunch() {
    const token = uni.getStorageSync('ls_access')
    const user = uni.getStorageSync('ls_user')
    if (token && user) {
      this.globalData.userInfo = JSON.parse(user)
    }
  },
  onShow() {},
  onHide() {}
}
</script>
<style>
/* 全局样式 */
page { background: #f5f6fa; font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif; }
.card { background: #fff; border-radius: 12rpx; padding: 24rpx; margin-bottom: 20rpx; }
.btn-primary { background: #409eff; color: #fff; border-radius: 8rpx; padding: 20rpx 0; text-align: center; }
.btn-danger  { background: #f56c6c; color: #fff; border-radius: 8rpx; padding: 20rpx 0; text-align: center; }
.role-tag { display: inline-block; padding: 4rpx 12rpx; border-radius: 20rpx; font-size: 22rpx; }
.role-student { background: #ecf5ff; color: #409eff; }
.role-teacher { background: #fdf6ec; color: #e6a23c; }
.role-admin   { background: #fef0f0; color: #f56c6c; }
</style>
