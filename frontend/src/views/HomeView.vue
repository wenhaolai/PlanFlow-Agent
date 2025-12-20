<template>
  <div class="flex h-screen bg-white">
    <!-- 左侧侧边栏 -->
    <aside class="w-64 bg-gray-50 border-r border-gray-200 flex flex-col">
      <!-- 新建对话按钮 -->
      <div class="p-4">
        <button 
          @click="startNewChat"
          class="w-full flex items-center gap-2 px-4 py-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 transition-colors text-gray-700 text-sm font-medium"
        >
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
          @click="loadTaskHistory(item.id)"
          :class="['group flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer text-gray-700 text-sm transition-colors',
            currentTaskId === item.id ? 'bg-gray-200' : 'hover:bg-gray-200']"
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
    <main class="flex-1 flex flex-col bg-white relative">
      <!-- 聊天区域 -->
      <div class="flex-1 overflow-y-auto p-4 space-y-6" ref="chatContainer">
        <!-- 欢迎页/空状态 -->
        <div v-if="chatHistory.length === 0" class="h-full flex flex-col items-center justify-center">
          <h1 class="text-4xl font-bold text-indigo-600 mb-4">Hello World</h1>
          <p class="text-xl text-gray-600">Welcome to PlanFlow Agent</p>
        </div>
        
        <!-- 消息列表 -->
        <div v-else v-for="(msg, index) in chatHistory" :key="index" 
             :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
             <!-- 消息气泡 -->
             <div :class="['max-w-3xl px-4 py-3 rounded-lg shadow-sm', 
                  msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-800 border border-gray-200']">
                <div class="whitespace-pre-wrap leading-relaxed">{{ msg.content }}</div>
             </div>
        </div>

        <!-- 等待动画 -->
        <div v-if="isSending" class="flex justify-start">
             <div class="bg-gray-100 text-gray-800 border border-gray-200 max-w-3xl px-4 py-3 rounded-lg shadow-sm">
                <div class="flex items-center space-x-1 h-6">
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                </div>
             </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="p-4 border-t border-gray-200 bg-white">
        <div class="max-w-4xl mx-auto relative">
            <textarea 
                v-model="inputMessage" 
                @keydown.enter.prevent="handleSendMessage"
                class="w-full p-4 pr-12 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none shadow-sm text-gray-700"
                rows="3"
                placeholder="输入您的问题..."
            ></textarea>
            <button 
                @click="handleSendMessage"
                :disabled="isSending || !inputMessage.trim()"
                class="absolute right-3 bottom-3 p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
                <el-icon v-if="isSending" class="is-loading"><Loading /></el-icon>
                <el-icon v-else><Position /></el-icon>
            </button>
        </div>
        <div class="text-center text-xs text-gray-400 mt-2">
          PlanFlow Agent 可能生成不准确的信息，请核对重要信息。
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Plus, 
  ChatDotRound, 
  Setting, 
  SwitchButton, 
  Help, 
  MagicStick,
  Brush,
  Position,
  Loading
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

const historyList = ref([])
const inputMessage = ref('')
const chatHistory = ref([])
const currentTaskId = ref(null)
const isSending = ref(false)
const chatContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const startNewChat = () => {
  currentTaskId.value = null
  chatHistory.value = []
  inputMessage.value = ''
}

const loadTaskHistory = async (taskId) => {
  if (currentTaskId.value === taskId) return
  
  try {
    const data = await http.get(`/task/${taskId}`)
    currentTaskId.value = taskId
    
    if (data.chats) {
      chatHistory.value = data.chats.sort((a, b) => {
        return new Date(a.timestamp) - new Date(b.timestamp)
      }).map(chat => ({
        role: chat.role,
        content: chat.content
      }))
    } else {
      chatHistory.value = []
    }
    scrollToBottom()
  } catch (error) {
    ElMessage.error('加载历史记录失败')
    console.error(error)
  }
}

const handleSendMessage = async () => {
  const msg = inputMessage.value.trim()
  if (!msg || isSending.value) return

  // Add user message
  chatHistory.value.push({ role: 'user', content: msg })
  inputMessage.value = ''
  isSending.value = true
  scrollToBottom()

  try {
    const payload = {
      message: msg,
      task_id: currentTaskId.value
    }
    
    const response = await http.post('/chat', payload)
    
    // Update task ID if it's new
    const isNewChat = !currentTaskId.value
    if (response.task_id) {
      currentTaskId.value = response.task_id
    }

    // Add assistant message
    chatHistory.value.push({ role: 'assistant', content: response.final_answer })
    
    // Refresh history list if it was a new chat
    if (isNewChat) {
      await fetchHistoryList()
    }
  } catch (error) {
    ElMessage.error(error.message || '发送消息失败')
    chatHistory.value.push({ role: 'assistant', content: '抱歉，发生了错误，请稍后重试。' })
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}

const fetchHistoryList = async () => {
  try {
    const data = await http.get('/task/gettasklist')
    historyList.value = data
  } catch (error) {
    console.error('获取历史记录失败:', error)
  }
}

onMounted(async () => {
  try {
    const data = await http.get('/user/profile')
    userInfo.value = data
    // 获取用户信息成功后，获取历史记录
    await fetchHistoryList()
  } catch (error) {
    ElMessage.error('获取用户信息失败，请重新登录')
    router.push('/login')
  }
})

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
