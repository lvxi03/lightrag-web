<template>
  <div class="chat-container">
    <div class="chat-box">
      <div class="sidebar" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
        <div class="sidebar-title" @click="toggleSidebar">
          <img src="/assets/生成孙悟空头像.png" alt="Avatar" class="avatar">
          <span>西游记问答</span>
        </div>
        <div class="sidebar-button" @click="showGraphRAGIntroduction">
          <span>首页</span>
        </div>
        <div class="sidebar-button" @click="showCharacters">
          <span>主要人物</span>
        </div>
        <!-- 修改：将"智能问答"改为"智慧问答"，并调整点击跳转逻辑 -->
        <div class="sidebar-button" @click="navigateToKnowledgeManagement">
          <span>智慧问答</span>
        </div>
        <!-- 新增知识图谱按钮 -->
        <div class="sidebar-button" @click="navigateToKnowledgeGraph">
          <span>知识图谱</span>
        </div>
        <!-- <div class="sidebar-button" @click="showSettings">
          <span>设置</span>
        </div> -->
      </div>
      <div class="chat-content">
        <div class="toggle-button" v-if="isSidebarCollapsed" @click="toggleSidebar">
          <div class="hamburger-menu">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
          </div>
        </div>
        <div class="message-list">
          <!-- 显示 GraphRAG 介绍 -->
          <div v-if="showIntroduction" class="introduction">
            <h2>GraphRAG快速入门介绍</h2>
            <p>
              当前阶段大模型的应用落地亟需解决的核心问题有一个是：如何与私域数据交互。而私域数据主要的问题是：需要有效地将企业数据整合进大语言模型中，但由于大模型的上下文处理能力有限，必须精准的选择出哪些数据在当前对话上下文中是有效的。
            </p>
            <p>
              一个系统是否能成功地商业化落地，在很大程度上取决于复杂的市场环境，大模型的核心优势在于其内容生成的多样性和创新性，但这同样也是其最大的问题，因为大模型生成的内容是不可控的，尤其是在金融和医疗领域等领域，一次金额评估的错误，一次医疗诊断的失误，哪怕只出现一次都是致命的。
            </p>
            <p>
              此外，大模型有时也会输出看似合理但实则错误的信息，这对于非专业人士来说可能难以辨识，但从专业角度来看却存在着不小的问题。这些都是大模型当前面临的挑战，而且目前还没有能够百分之百解决这种情况的方案。
            </p>
            <p>
              通过人们不断地对大模型领域的探索，非常多的实验能够证明，当为大模型提供一定的上下文信息后，其输出会变得稳定。那么，将知识库中的信息或掌握的信息先输送给大模型，再由大模型服务用户，就是大家普遍达成共识的一个结论和方法。传统的对话系统、搜索引擎等核心依赖于检索技术，如果将这一检索过程融入大模型应用的构建中，既可以充分利用大模型在内容生成上的能力，也能通过引入的上下文信息显著约束大模型的输出范围和结果，同时还实现了将私有数据融入大模型中的目的，达到了双赢的效果。
            </p>
            <p>
              所以我们才看到RAG的实现是包括两个阶段的：检索阶段和生成阶段。在检索阶段，从知识库中找出与问题最相关的知识，为后续的答案生成提供素材。在生成阶段，RAG会将检索到的知识内容作为输入，与问题一起输入到语言模型中进行生成。这样，生成的答案不仅考虑了问题的语义信息，还考虑了相关私有数据的内容。
            </p>
            <p>
              传统RAG技术实现流程与技术瓶颈：检索增强生成（Retrieval-Augmented Generation）技术是一种结合了检索和生成两个阶段的自然语言处理技术，它由 Facebook AI 团队在 2020 年提出。这种方法的核心思想是利用大规模的预训练语言模型生成技术，并结合信息检索的策略，以改善回答的准确性和相关性。
            </p>
            <p>
              为了解决这些问题，2024年2月微软研究院正式提出一种基于知识图谱的RAG方法——GraphRAG，这种新方法利用LLM基于私人数据集创建知识图谱。然后，这个图谱与图机器学习技术结合，在查询时执行提示增强。GraphRAG在回答上述两类问题时展现出了显著的提升，显示出超越先前应用于私人数据集的其他方法的智能或掌握能力。
            </p>
            <p>
              研究报告地址：<a href="https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/" target="_blank">GraphRAG: A new approach for discovery using complex information</a>
            </p>
            <h3>一、GraphRAG介绍</h3>
            <h4>1.1 什么是 Graph RAG？</h4>
            <p>
              Graph RAG（Retrieval-Augmented Generation），是一种基于知识图谱的检索增强技术，通过构建图模型的知识表达，将实体和关系之间的联系用图的形式进行展示，然后利用大语言模型 LLM进行检索增强。
            </p>
            <p>
              GraphRAG是微软研究院开发的一种创新型检索增强生成（RAG）方法，基于MIT开源协议，旨在提高大语言模型LLM在处理复杂信息和私有数据集时的推理能力。
            </p>
            <h4>1.2 GraphRAG诞生背景</h4>
            <p>
              传统RAG是将一篇文章打碎拆分为几个小的章节(chunks)，然后embedding后存入向量库，在查询阶段，RAG将用户指令挨个在向量库与这些chunks的embedding向量进行相似度匹配，然后输出最匹配的k个作为prompt的上下文(context)，无论是在文档预处理进向量库阶段，还是用户查询阶段，都没加考虑各个chunk之间的关联，这就形成了普通RAG技术的先天设计缺陷。
            </p>
            <p>
              传统rag：解决外部知识的详情介绍，某些细节的检索。比如：比如孔乙己是哪里人？
            </p>
            <p>
              graphRAG：跨多个段落，甚至多个文章。文章中的主要主题是什么？
            </p>
            <p>
              GraphRAG提出了一种回答总结类问题的算法思路，下面展示了GraphRAG算法的工作流程，包括索引建立阶段(index time)和查询阶段(query time)。
            </p>
            <h4>1.3 graphrag的基本概念</h4>
            <p>
              Document(文档)- 系统中的输入文档。这些文档要么代表CSV 中的单独行，要么代表单独的 .txt文件。
            </p>
            <p>
              TextUnit(文本块)- 要分析的文本块。这些块的大小、重叠以及它们是否遵守任何数据边界可以在下面配置。一个常见的用例是设置CHUNK_BY_COLUMNS为id，以便文档和 TextUnits 之间存在一对多关系，而不是多对多关系。
            </p>
            <p>
              Entity(实体)- 从 TextUnit 中提取的实体。这些实体代表人物、地点、事件或您提供的其他实体模型。
            </p>
            <p>
              Relationship(关系)- 两个实体之间的关系。这些关系由协变量生成。
            </p>
            <p>
              Covariate(协变量)- 提取的声明信息，其中包含可能受时间限制的实体的陈述.
            </p>
            <p>
              Claim(声明)- 代表具有评估状态和时间限制的积极事实陈述，以协变量(Covariates)的称呼在各处使用。
            </p>
            <p>
              Community Report(社区报告)- 一旦生成实体，我们就对它们执行分层社区检测，并为该层次结构中的每个社区生成报告。
            </p>
            <p>
              Node（节点）- 包含已嵌入和聚集的实体和文档的呈现图形视图的布局信息。
            </p>
            <h5>1.3.1 索引建立(index time)</h5>
            <p>
              索引建立阶段，属于数据预处理阶段，主要目的是从提供的文档集合中，提取出知识图谱(Knowledge Graph)，然后以聚类算法(Leiden)，将知识图谱分为数个社区(community)，并总结每个社区(community)所表达的含义(community summary)。
            </p>
            <p>
              graphRAG索引阶段流程图：
            </p>
            <img src="/assets/31b9d68a57424590a6608f99526ed903.png" alt="流程图" style="width:500%; max-width: 600px;">
            <h5>1.3.2 Querying过程</h5>
            <p>
              从上面的介绍，我们了解到在构建索引的过程中，GraphRAG会生成实体关系图、社区层级结构，以及它们的summary、source chunk的各种维度的信息，以向量和结构化的方式进行存储。下面我们介绍在检索时如何使用这些信息来做信息增强。Query分两种类型，分别为Local Search和Global Search。
            </p>
            <h6>1.3.2.1 Local Search</h6>
            <p>
              Local Search是一种基于Entity的回答模式。它结合知识图谱中的结构化数据和输入文档中的非结构化数据，在查询时通过相关实体信息扩展LLM上下文。该方法非常适合回答需要理解输入文档中提到的具体实体的问题（例如，“孔乙己和掌柜的之间的关系？”）。
            </p>
            <p>
              其流程图如下所示：
            </p>
            <img src="/assets/a3c95d838fa8467db5b88115d14a3417.png" alt="流程图" style="width:500%; max-width: 600px;">
            <p>
              给定用户查询（或加上对话历史记录），Local Search会从知识图谱中识别出一组与用户输入在语义上相关的实体。这些实体作为进入知识图谱的入口点，能够提取进一步相关的细节，如相连实体、关系、实体协变量（与实体相关的变量）和社区报告。此外，它还从原始输入文档中提取与已识别实体相关的相关文本chunk。然后对这些候选数据源进行优先级排序和过滤，以适应预定义大小的单个上下文窗口，该窗口用于生成对用户查询的响应。
            </p>
            <h6>1.3.2.2 Global Search</h6>
            <p>
              Global Search是基于整个数据集的推理。常规RAG在处理需要跨数据集聚合信息后进行组合回答的场景时很难有很好的表现。例如，“本文的主题是什么？”这种问题查询效果会很差，因为常规RAG的处理方式是：依赖于数据集中存在语意相似的文本内容的向量检索。如果知识库中没有文本内容包含这个问题的答案，则无法给出高质量的回答。
            </p>
            <p>
              然而，使用GraphRAG可以回答此类问题，因为LLM生成的知识图谱的结构可以告诉我们整个数据集的结构（以及主题）。这使得私有数据集能够组织成有意义的语义clusters，并且这些clusters已被预先总结。通过使用我们的全局搜索方法，LLM在响应用户查询时可以使用这些cluster来总结这些主题，并回答用户对整个数据集的问题。
            </p>
            <p>
              其流程图如下所示：
            </p>
            <img src="/assets/5bacb43bdc484b52bf6a167f42eba813.png" alt="流程图" style="width:500%; max-width: 600px;">
            <p>
              给定用户查询（或加上对话历史记录），Global Search使用从图的社区层次结构中指定级别生成的一系列 LLM 社区报告作为上下文数据，以 map-reduce 方式生成响应。在 map 步骤中，社区报告被分割成预定义大小的文本chunks。每个文本chunk然后用于生成一个中间响应，其中包含一个要点列表，每个要点都附有一个表示该要点重要性的数值评级。在 reduce 步骤中，从中间响应中筛选出最重要的要点进行汇总，并将其用作上下文生成最终响应。
            </p>
            <p>
              全局搜索响应的质量会受到用于社区报告来源的社区层次结构级别的显著影响。较低的层次级别报告更为详细，通常会产生更为全面的响应，但由于报告数量的增加，这也可能增加生成最终响应所需的时间和 LLM 资源。
            </p>
            <h4>1.4 Graph RAG 思想一句话总结</h4>
            <p>
              Graph RAG 思想： 对用户输入的query提取实体，然后构造子图形成上下文，最后送入大模型完成生成。
            </p>
            <h3>二、知识图谱介绍</h3>
            <p>
              知识图谱（Knowledge Graph）是一种以结构化形式描述现实世界实体及其关系的技术，通过将数据组织为“节点-边-节点”的三元组（如“北京-是-中国首都”），构建出语义关联的网络。
            </p>
            <h4>核心组成‌‌：</h4>
            <p>
              实体（Entities）‌：表示具体或抽象的事物，如“李白”“北京”。‌
            </p>
            <p>
              关系（Relationships）‌：连接实体的边，定义交互方式，如“出生于”“首都”。‌
            </p>
            <p>
              属性（Attributes）‌：描述实体的特征，如“李白-字太白”“北京-人口2170万”。‌
            </p>
            <p>
              本体（Ontology）‌：领域内的概念体系与关系约束，如“城市-国家”间的“首都”关系。‌
            </p>
            <p>
              示例‌：在医疗领域，知识图谱可链接“糖尿病”“胰岛素”“高血糖”等实体，通过“治疗方法”“症状”等关系辅助诊断。
            </p>
            <h4>应用场景‌‌：</h4>
            <p>
              推荐系统‌：基于用户兴趣关联商品（如喜欢科幻电影的用户推荐《三体》）。‌
            </p>
            <p>
              智能问答‌：解析复杂问题（如“哪些法国导演获得过奥斯卡奖？”）。‌
            </p>
            <p>
              金融风控‌：通过企业关联网络识别欺诈风险。‌
            </p>
            <p>
              医疗健康‌：辅助诊断（如根据症状推荐可能的疾病及用药）。
            </p>
          </div>

          <!-- 显示主要人物 -->
          <CharacterList v-if="showCharactersList" class="characters-list" />

          <!-- 显示对话内容 -->
          <div v-if="showChatContent" class="chat-section">
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message', message.type]"
            >
              <div class="message-bubble">
                <span class="message-content">{{ message.content }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="input-box" v-if="showChatContent">
          <el-input
            v-model="userInput"
            placeholder="请输入消息..."
            @keyup.enter="sendMessage"
            class="input-field"
          />
          <el-button type="primary" @click="sendMessage" class="send-button">发送</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import CharacterList from '@/views/welcome/CharacterList.vue';
// 新增：导入路由
import { useRouter } from 'vue-router';

const router = useRouter();

const messages = ref([]); // 存储消息的数组
const userInput = ref(''); // 用户输入的内容
const showIntroduction = ref(false); // 控制是否显示GraphRAG介绍
const showCharactersList = ref(false); // 控制是否显示主要人物列表
const showChatContent = ref(false); // 控制是否显示对话内容
const isSidebarCollapsed = ref(false); // 控制菜单栏是否折叠

// 显示GraphRAG介绍
const showGraphRAGIntroduction = () => {
  showIntroduction.value = true;
  showCharactersList.value = false;
  showChatContent.value = false;
};

// 显示主要人物列表
const showCharacters = () => {
  showCharactersList.value = true;
  showIntroduction.value = false;
  showChatContent.value = false;
};

// 显示对话内容
const showChat = () => {
  showChatContent.value = true;
  showIntroduction.value = false;
  showCharactersList.value = false;
};

// 显示设置
const showSettings = () => {
  console.log('显示设置');
};

// 发送消息
const sendMessage = () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入消息内容！');
    return;
  }

  // 添加用户消息到消息列表
  messages.value.push({
    type: 'user',
    content: userInput.value,
  });

  // 清空输入框
  userInput.value = '';

  // 模拟平台回复
  setTimeout(() => {
    const response = `您好！您刚刚说：${messages.value[messages.value.length - 1].content}`;
    messages.value.push({
      type: 'platform',
      content: response,
    });
  }, 500); // 模拟延迟
};

// 切换菜单栏的显示和隐藏
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

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

// 在组件挂载时执行自动刷新逻辑
import { onMounted } from 'vue';
onMounted(autoReload);

// 新增：跳转至KnowledgeManagement界面的方法
const navigateToKnowledgeManagement = () => {
  router.push('/knowledge'); // 假设路由配置路径为/knowledge，具体需与项目路由定义一致
};

// 移除原showChat方法（或根据需要保留）
// const showChat = () => { ... };

// 新增：跳转至知识图谱界面的方法
const navigateToKnowledgeGraph = () => {
  router.push('/graph'); // 假设路由路径为/graph，需与项目实际路由配置一致
};
</script>

<style scoped>
html, body {
  overflow: hidden;
  margin: 0;
  padding: 0;
  height: 100%;
}

.chat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background-color: #f0f2f5;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.chat-box {
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 0;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: row;
}

.sidebar {
  width: 250px;
  background-color: #d3d3d3;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
  flex-shrink: 0;
  border: none;
  transition: width 0.3s ease;
  overflow: auto;
  max-height: 100vh;
}

.sidebar.sidebar-collapsed {
  width: 0px;
  padding: 0;
  overflow: hidden;
}

.sidebar-title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #333;
  margin: 10px 0;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
  border: none;
  padding: 0 10px;
}

.sidebar-title:hover {
  background-color: #e0e0e0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.sidebar-button {
  width: 100%;
  margin: 5px 0;
  text-align: center;
  background-color: transparent;
  color: #888;
  padding: 10px 0;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-button:hover {
  background-color: #e0e0e0;
  color: #000;
  border-color: #ccc;
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f0f2f5;
}

.chat-box {
  flex: 1;
  display: flex;
  flex-direction: row;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 250px;
  background-color: #d3d3d3;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
  transition: width 0.3s ease;
}

.sidebar.sidebar-collapsed {
  width: 0;
  padding: 0;
  overflow: hidden;
}

.sidebar-title {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #333;
  margin: 10px 0;
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.sidebar-button {
  width: 100%;
  margin: 5px 0;
  text-align: center;
  background-color: transparent;
  color: #888;
  padding: 10px 0;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.sidebar-button:hover {
  background-color: #e0e0e0;
  color: #000;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.toggle-button {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 40px;
  height: 40px;
  background-color: #d3d3d3;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hamburger-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar {
  width: 24px;
  height: 2px;
  margin-bottom: 4px;
  background-color: #333;
}

.bar:last-child {
  margin-bottom: 0;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message.user {
  justify-content: flex-end;
}

.message.platform {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background-color: #f3f3f3;
  word-wrap: break-word;
}

.message.user .message-bubble {
  background-color: #e0f7fa;
}

.message.platform .message-bubble {
  background-color: #f3f3f3;
}

.input-box {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.input-field {
  flex: 1;
  margin-right: 5px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.send-button {
  padding: 10px 20px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
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
  overflow: auto;
}

.introduction h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduction p {
  margin-bottom: 10px;
}

.introduction h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduction h4 {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduction h5 {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.introduction h6 {
  font-size: 0.8rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.characters-list {
  width: 100%;
  overflow: auto;
}
</style>