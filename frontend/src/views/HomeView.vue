<template>
  <div class="flex h-screen bg-white">
    <!-- 左侧侧边栏 -->
    <aside class="w-64 bg-gray-50 border-r border-gray-200 flex flex-col">
      <!-- 新建对话按钮 -->
      <div class="p-4">
        <button class="w-full flex items-center gap-2 px-4 py-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors text-gray-700 text-sm font-medium">
          <el-icon><Plus /></el-icon>
          <span>新对话</span>
        </button>
      </div>

      <!-- 历史记录列表 -->
      <div class="flex-1 overflow-y-auto px-2 py-2 space-y-1">
        <div class="px-3 py-2 text-xs font-medium text-gray-500">最近</div>
        <div 
          v-for="item in historyList" 
          :key="item.id"
          class="group flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-200 cursor-pointer text-gray-700 text-sm transition-colors"
        >
          <el-icon class="text-gray-400"><ChatDotRound /></el-icon>
          <span class="truncate">{{ item.title }}</span>
        </div>
      </div>

      <!-- 底部用户中心 -->
      <div class="p-4 border-t border-gray-200">
        <el-popover
          placement="top-start"
          :width="240"
          trigger="click"
          popper-class="user-menu-popover"
        >
          <template #reference>
            <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-200 cursor-pointer transition-colors">
              <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-medium text-sm">
                {{ userInitial }}
              </div>
              <div class="flex-1 min-w-0 text-left">
                <div class="text-sm font-medium text-gray-900 truncate">{{ userInfo.username }}</div>
                <div class="text-xs text-gray-500 truncate">免费版</div>
              </div>
            </div>
          </template>

          <!-- 弹出菜单内容 -->
          <div class="py-1">
            <div class="px-4 py-3 border-b border-gray-100 mb-1">
              <div class="font-medium text-gray-900">{{ userInfo.username }}</div>
              <div class="text-xs text-gray-500">{{ userInfo.email }}</div>
            </div>
            
            <div class="menu-item">
              <el-icon><MagicStick /></el-icon>
              <span>升级套餐</span>
            </div>
            <div class="menu-item">
              <el-icon><Brush /></el-icon>
              <span>个性化</span>
            </div>
            <div class="menu-item">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </div>
            
            <div class="my-1 border-t border-gray-100"></div>
            
            <div class="menu-item">
              <el-icon><Help /></el-icon>
              <span>帮助</span>
            </div>
            <div class="menu-item text-red-600 hover:bg-red-50" @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </div>
          </div>
        </el-popover>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main class="flex-1 flex flex-col items-center justify-center bg-white">
      <h1 class="text-4xl font-bold text-indigo-600 mb-4">Hello World</h1>
      <p class="text-xl text-gray-600">Welcome to PlanFlow Agent</p>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Plus, 
  ChatDotRound, 
  Setting, 
  SwitchButton, 
  Help, 
  MagicStick,
  Brush
} from '@element-plus/icons-vue'
import http from '@/utils/http'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userInfo = ref({
  username: 'Loading...',
  email: 'loading...'
})

// 计算属性：获取用户名的首字母（大写）
const userInitial = computed(() => {
  return userInfo.value.username ? userInfo.value.username.charAt(0).toUpperCase() : 'U'
})

onMounted(async () => {
  try {
    const data = await http.get('/user/profile')
    userInfo.value = data
  } catch (error) {
    ElMessage.error('获取用户信息失败，请重新登录')
    router.push('/login')
  }
})

// 模拟历史记录数据
const historyList = ref([
  { id: 1, title: '如何使用 Vue 3' },
  { id: 2, title: 'PlanFlow 项目规划' },
  { id: 3, title: '前端组件库选型' },
  { id: 4, title: 'Python 后端接口设计' },
  { id: 5, title: 'Docker 部署方案' },
])

const handleLogout = () => {
  // 清除 token
  localStorage.removeItem('token')
  // 跳转到登录页
  router.push('/login')
}
</script>

<style>
/* 全局样式调整，确保 popover 样式正确 */
.user-menu-popover {
  padding: 0 !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: #f3f4f6;
}

.menu-item .el-icon {
  font-size: 16px;
}
</style>
