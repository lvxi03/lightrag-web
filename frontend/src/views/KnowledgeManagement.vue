<template>
  <!-- 修改外层容器为flex布局 -->
  <div class="knowledge-container">
    <!-- 左侧功能面板 -->
    <div class="left-panel">
      <!-- 模型切换 -->
      <div class="model-switcher">
        <h3>模型选择</h3>
        <el-select 
          v-model="selectedModel" 
          placeholder="选择对话模型"
          style="width: 100%"
        >
          <el-option label="local模型" value="local"></el-option>
          <el-option label="global模型" value="global"></el-option>
          <el-option label="hybrid模型" value="hybrid"></el-option>
          <el-option label="naive模型" value="naive"></el-option>
          <el-option label="mix模型" value="mix"></el-option>
          <el-option label="bypass模型" value="bypass"></el-option>
        </el-select>
      </div>

      <!-- 历史记录 -->
      <div class="history-list">
        <h3>对话历史</h3>
        <div class="history-items" v-if="chatHistory.length">
          <div 
            v-for="(item, index) in chatHistory" 
            :key="index" 
            class="history-item"
            @click="loadHistory(item)"
          >
            <p class="history-time">{{ item.time }}</p>
            <p class="history-summary">
              {{ item.summary }} (模型：{{ item.model }}) <!-- 新增模型显示 -->
            </p>
          </div>
        </div>
        <div v-else class="no-history">暂无对话历史</div>
      </div>
    </div>

    <!-- 右侧对话区域（原内容） -->
    <div class="main-content">
      <!-- 聊天区域（可滚动） -->
      <div class="chat-section">
        <div class="message-list" ref="messageList">
          <!-- 显示对话内容 -->
          <div class="chat-section">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message', message.type]"
            >
              <!-- 新增：platform类型消息左侧头像 -->
              <div class="avatar" v-if="message.type === 'platform'"></div>
              <div class="message-bubble">
                <span class="message-content" v-if="message.type === 'user'">{{ message.content }}</span>
                <span class="message-content" v-else v-html="message.displayContent"></span>
              </div>
            </div>
    
            <!-- 思考圈 -->
            <div v-if="isThinking" class="thinking-container">
              <div class="thinking-bubble">
                <div class="spinner"></div>
                <span class="thinking-text">正在思考中...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 输入框（固定在底部） -->
      <div class="input-box">
        <!-- 修改输入框禁用条件：同时依赖 isReplying 和 isThinking -->
        <el-input
          v-model="userInput"
          placeholder="请输入消息..."
          @keyup.enter="sendMessage"
          class="input-field"
          :disabled="isReplying || isThinking" 
        />
        <!-- 修改发送按钮禁用条件：同时依赖 isReplying 和 isThinking -->
        <el-button type="primary" @click="sendMessage" class="send-button" :disabled="isReplying || isThinking">  <!-- 关键修改 -->
          发送
        </el-button>
        <!-- 新增终止按钮 -->
        <el-button type="danger" @click="stopProcessing" class="send-button" :disabled="!isThinking && !isReplying">
          终止处理
        </el-button>
      </div>
    </div>
  </div>
</template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'; // 新增watch导入
  import { ElMessage } from 'element-plus';
  import axios from 'axios';
  
  
  const messages = ref([]); // 建议使用 Pinia 共享状态
  const userInput = ref('');
  const isThinking = ref(false);
  const isReplying = ref(false);
  

// 页面加载时自动刷新一次
const autoReload = () => {
  // 检查是否已经刷新过页面
  if (!localStorage.getItem('hasReloaded')) {
    // 设置标志变量
    localStorage.setItem('hasReloaded', 'true');
    // 刷新页面
    window.location.reload();
  } else {
    // 如果已经刷新过，清除标志变量
    localStorage.removeItem('hasReloaded');
  }
};

  const sendMessage = () => {
    if (!userInput.value.trim()) {
      ElMessage.warning('请输入消息内容！');
      return;
    }
  
    messages.value.push({ type: 'user', content: userInput.value });
    userInput.value = '';
    submitData();
  };
  
  const submitData = async () => {
    const lastUserMessage = messages.value.findLast(msg => msg.type === 'user')?.content;
    if (!lastUserMessage) return;
  
    const url = 'http://10.32.12.176:9621/query'; 
    // 关键修改：mode 动态绑定选中模型
    const data = {
      query: lastUserMessage,
      mode: selectedModel.value // 使用当前选中的模型
    };

    try {
      isThinking.value = true; // 开始请求时显示思考圈
      
      // 修复：明确传递 headers
      const response = await axios.post(url, data, { 
        headers: { 'Content-Type': 'application/json' } 
      });
      const apiResponse = response.data;

      // 处理空响应的情况
      if (!apiResponse.response?.trim()) {
        messages.value.push({
          type: 'platform',
          content: '抱歉，此问题暂时无法解答'
        });
        return;
      }

      // 解析主内容和参考文献
      let mainContent = apiResponse.response;
      let references = [];
      const refSplit = mainContent.match(/(-{3,}|={3,})\s*\n?\s*(\*\*?References\*\*?|参考文献)\s*\n?/i);

      if (refSplit) {
        const splitIndex = mainContent.indexOf(refSplit[0]);
        const main = mainContent.slice(0, splitIndex).trim();
        const refs = mainContent.slice(splitIndex + refSplit[0].length).trim();
        mainContent = main;
        references = refs
          .split('\n')
          .map(r => r.replace(/^[-*]\s*/, '').trim())
          .filter(r => r.length > 0);
      }

      // 清理主内容首尾空格
      mainContent = mainContent.replace(/^\s+|\s+$/g, '');

      // 组合最终内容
      let formattedContent = mainContent;
      if (references.length > 0) {
        formattedContent += '\n\n**参考文献：**\n';
        formattedContent += references.map((ref, idx) => `${idx + 1}. ${ref}`).join('\n');
      }

      // 转为HTML
      const htmlContent = formatMarkdownToHtml(formattedContent);

      // 添加平台消息
      messages.value.push({
        type: 'platform',
        content: htmlContent,  // 存储完整内容
        displayContent: '',    // 逐字显示的内容
        currentIndex: 0        // 当前显示的字符索引
      });

      // 启动逐字显示定时器
      const messageIndex = messages.value.length - 1;
      const platformMessage = messages.value[messageIndex];
      const totalLength = platformMessage.content.length;

      const timer = setInterval(() => {
        if (platformMessage.currentIndex < totalLength) {
          platformMessage.currentIndex++;
          platformMessage.displayContent = platformMessage.content.substring(0, platformMessage.currentIndex);
        } else {
          clearInterval(timer);
          isReplying.value = false; // 消息输出完成，启用发送功能
        }
      }, 30);

      isReplying.value = true; // 启动定时器时禁用发送功能
    } catch (error) {
      console.error('请求失败：', error);
      messages.value.push({
        type: 'platform',
        content: `请求失败：${error.response?.status || '暂时还不能回答此问题'}`
      });
    } finally {
        isThinking.value = false; // 请求结束隐藏思考圈
        scrollToBottom(); // 关键新增：消息更新后自动滚动
      // 添加平台消息后，更新历史记录
      const now = new Date().toLocaleString(); 
      const lastUserMsg = messages.value.findLast(m => m.type === 'user');
      const lastPlatformMsg = messages.value.findLast(m => m.type === 'platform');
      const userSummary = lastUserMsg?.content?.slice(0, 20) + (lastUserMsg?.content?.length > 20 ? '...' : '');
      const platformSummary = lastPlatformMsg?.content?.slice(0, 20) + (lastPlatformMsg?.content?.length > 20 ? '...' : '');
      
      chatHistory.value.push({
        time: now,
        summary: `${userSummary}`, // 优化摘要格式
        model: selectedModel.value, // 新增：记录当前模型
        messages: [lastUserMsg, lastPlatformMsg] 
      });
    }
  };

  // 在 sendMessage 或 submitData 的消息新增后添加
const scrollToBottom = () => {
  const messageList = document.querySelector('.message-list');
  if (messageList) {
    messageList.scrollTop = messageList.scrollHeight; // 滚动到最底部
  }
};

  // Markdown简单加粗和标题转HTML
  function formatMarkdownToHtml(text) {
    // 处理 ### 标题
    text = text.replace(/^### (.*)$/gm, '<strong style="font-size:1.1em;">$1</strong>');
    // 处理 #### 标题
    text = text.replace(/^#### (.*)$/gm, '<strong style="font-size:1.1em;">$1</strong>');
    // 处理 **加粗**
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // 处理 *加粗*（可选）
    text = text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
    return text;
  }

  // 新增状态：模型选择、对话历史
const selectedModel = ref('global'); // 默认使用全局模型
const chatHistory = ref([

]);

// 监听模型切换，清空聊天内容（添加watch监听）
watch(selectedModel, (newVal) => {
  messages.value = []; // 清空消息列表
  ElMessage.info(`已切换至${newVal}模型，聊天记录已清空`);
});

// 加载历史对话
const loadHistory = (item) => {
  // 直接赋值历史消息（无需逐个添加）
  messages.value = JSON.parse(JSON.stringify(item.messages)); // 深拷贝避免引用问题

  // 遍历消息，将平台消息的displayContent直接设置为完整内容
  messages.value.forEach(msg => {
    if (msg.type === 'platform') {
      msg.displayContent = msg.content; // 关键修改：直接显示完整内容
    }
  });

  // 滚动到消息底部
  setTimeout(() => {
    const messageList = document.querySelector('.message-list');
    if (messageList) messageList.scrollTop = messageList.scrollHeight;
  }, 100);
  
  ElMessage.success('已加载历史对话');
};

// 在组件挂载时执行自动刷新逻辑

onMounted(autoReload);
  </script>
  
  <style scoped>
/* 整体容器改为垂直布局 */
.knowledge-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
  flex-direction: row; /* 保持左右分栏 */
}

/* 右侧主区域 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column; /* 子元素垂直排列 */
}

/* 聊天区域（可滚动） */
.chat-section {
  flex: 1; /* 占据剩余空间 */
  overflow-y: auto; /* 内容超出时滚动 */
  padding: 20px 30px;
}

/* 输入框固定在底部 */
.input-box {
  position: sticky; /* 粘性定位 */
  bottom: 0; /* 固定在底部 */
  z-index: 1; /* 确保在聊天内容上方 */
}

/* 消息列表自动滚动到底部（新增样式） */
.message-list {
  display: flex;
  flex-direction: column;
  min-height: 100%; /* 确保内容撑满容器 */
}


/* 左侧功能面板（独立小界面） */
.left-panel {
  width: 220px; 
  padding: 15px;
  background-color: #ffffff;
  border-right: 1px solid #e9ecef;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  border-radius: 0 12px 12px 0;
  margin-right: 8px;
  height: 100vh; /* 新增：固定高度为视口高度 */
  overflow-y: auto; /* 新增：内容超出时内部滚动 */
  position: sticky; /* 新增：粘性定位保持位置 */
  top: 0; /* 新增：配合sticky固定在顶部 */
}

.model-switcher {
  margin-bottom: 30px;
}

.model-switcher h3 {
  font-size: 16px;
  color: #2d3436;
  margin-bottom: 10px;
}

.history-list h3 {
  font-size: 16px;
  color: #2d3436;
  margin-bottom: 10px;
}

.history-items {
  max-height: 400px;
  overflow-y: auto;
}

.history-item {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.history-item:hover {
  background-color: #e9f5ff;
  transform: translateX(2px);
}

.history-time {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 4px;
}

.history-summary {
  font-size: 14px;
  color: #2d3436;
  line-height: 1.4;
}

.no-history {
  color: #6c757d;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

/* 右侧对话区域优化 */
.chat-content {
  flex: 1;
  padding: 20px 30px;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 18px;
  border-radius: 12px; /* 更大的圆角 */
  box-shadow: 0 1px 3px rgba(0,0,0,0.1); /* 消息气泡阴影 */
  margin: 8px 12px;
}

.message.user .message-bubble {
  background-color: #007bff; /* 蓝色用户消息 */
  color: rgb(0, 0, 0);
}

.message.platform .message-bubble {
  background-color: #ffffff; /* 白色平台消息 */
  color: #2d3436;
  border: 1px solid #e9ecef;
}

.input-box {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 16px; /* 输入框圆角 */
  box-shadow: 0 -2px 8px rgba(0,0,0,0.05); /* 顶部阴影 */
  margin-top: 20px;
}

.input-field {
  border: 1px solid #dee2e6;
  border-radius: 12px;
  padding: 16px 20px;
  font-size: 15px;
  background-color: #f8f9fa;
}

.send-button {
  background-color: #007bff;
  border-radius: 12px;
  padding: 0 24px;
  font-size: 15px;
}

.send-button:hover {
  background-color: #0056b3;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  overflow: hidden;
  border: none;
  padding: 0;
  min-height: 100vh;  /* 确保容器至少占满视口高度 */
  position: relative;  /* 为子元素粘性定位提供参考 */
}

/* 关键修改：固定输入框在底部 */
.input-box {
  display: flex;
  padding: 0;
  border-top: 1px solid #ddd;
  width: 100%;
  height: 75px;
  border: none;
  position: sticky;  /* 粘性定位 */
  bottom: 0;         /* 固定在底部 */
  background-color: #fff;  /* 设置背景色避免内容覆盖 */
  z-index: 1;        /* 确保输入框在消息列表上方 */
}
.message-list {
  padding: 0;
  flex: 1;
  overflow-y: auto;  /* 保持滚动功能 */
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border: none;
  /* 新增隐藏滚动条样式 */
  -ms-overflow-style: none;  /* IE和Edge */
  scrollbar-width: none;     /* Firefox */
}

/* 隐藏WebKit浏览器的滚动条 */
.message-list::-webkit-scrollbar {
  display: none;
}

.message {
  margin: 0;
  width: 100%;
  display: flex;
  align-items: flex-end;
  border: none;
}

.message.user {
  flex-direction: row-reverse;
}

.message.platform {
  flex-direction: row;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background-color: #f3f3f3;
  word-wrap: break-word;
  margin: 0 10px;
  transition: all 0.3s ease;
  border: none;
}

.message.user .message-bubble {
  background-color: #e0f7fa;
}

.input-box {
  display: flex;
  padding: 0;
  border-top: 1px solid #ddd;
  width: 100%;
  height: 75px;
  border: none;
}

.input-field {
  flex: 1;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 20px;
  font-size: 1rem;
}

.send-button {
  width: 80px;
  border-radius: 8px;
  background-color: #409eff;
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border: none;
  height: 100%;  /* 新增：继承父容器(input-box)的75px高度 */
  box-sizing: border-box;  /* 新增：让height包含padding和border */
  padding: 0 16px;  /* 调整：保持文字居中同时匹配输入框高度 */
}

.send-button:hover {
  background-color: #66b1ff;
}

.introduction {
  margin: 0;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.introduction h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduction p {
  margin-bottom: 10px;
}

.characters-list {
  width: 100%;
  overflow: auto;
}

.message-content {
  white-space: pre-wrap; /* 添加：保留空白并自动换行 */
  word-wrap: break-word; /* 补充：长单词/URL自动换行 */
}

.thinking-container {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 10px 0;
}

.thinking-bubble {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-radius: 15px;
  background-color: #f0f0f0;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #999;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.thinking-text {
  color: #666;
  font-size: 0.9rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 新增：消息头像样式 */
.avatar {
  width: 30px;          /* 45x45尺寸 */
  height: 30px;
  border-radius: 50%;   /* 圆形 */
  background-image: url('@/img/global.jpg');
  background-size: cover;  
  flex-shrink: 0;       /* 防止被压缩 */
  margin-right: 10px;   /* 与消息气泡的间距 */
}

/* 调整platform类型消息的布局 */
.message.platform {
  align-items: flex-start; /* 头像顶部对齐 */
  padding-top: 8px;        /* 顶部留白 */
}
  </style>
