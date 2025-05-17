<!-- filepath: c:\Users\ASUS\Desktop\final\frontend\src\views\KnowledgeGraph.vue -->
<template>
  <div class="kg-root">
    <!-- 顶部工具栏 -->
    <div class="kg-toolbar">
      <div class="kg-toolbar-left">
        <el-select v-model="layoutType" placeholder="选择布局" size="small" @change="switchLayout" class="kg-select">
          <el-option label="散点分布（cose）" value="cose" />
          <el-option label="同心圆（concentric）" value="concentric" />
          <el-option label="层次布局（breadthfirst）" value="breadthfirst" />
          <el-option label="圆形布局（circle）" value="circle" />
        </el-select>
        <el-upload
          ref="graphUploadRef"
          :show-file-list="false"
          :before-upload="beforeUploadGraphFile"
          accept=".json"
        >
          <el-button size="small" icon="el-icon-upload">上传图谱</el-button>
        </el-upload>
        <el-input
          v-model="searchNode"
          placeholder="搜索节点"
          @keyup.enter="searchGraphNode"
          clearable
          size="small"
          class="kg-search"
        >
          <template #append>
            <el-button size="small" @click="searchGraphNode" icon="el-icon-search"></el-button>
          </template>
        </el-input>
        <span v-if="uploadedFileName" class="file-tip">已加载：{{ uploadedFileName }}</span>
      </div>
      <div class="kg-toolbar-right">
        <span class="kg-title">知识图谱</span>
      </div>
    </div>
    <!-- 左侧侧边栏 -->
    <div class="kg-sidebar">
      <div
        class="kg-sidebar-btn"
        v-for="item in sidebarBtns"
        :key="item.icon"
        :title="item.tip"
        @click="handleSidebarClick(item)"
      >
        <i :class="item.icon"></i>
      </div>
    </div>
    <!-- 图谱主区域 -->
    <div class="kg-main">
      <div id="cy" class="kg-graph"></div>
      <!-- 右下角图例，支持显示/隐藏 -->
      <div class="kg-legend" v-if="showLegend">
        <div class="kg-legend-title">图例</div>
        <div
          v-for="(color, type) in dynamicLegendMap"
          :key="type"
          class="kg-legend-item"
        >
          <span class="kg-legend-dot" :style="{ background: color }"></span>
          <span class="kg-legend-label">{{ typeNameMap[type] || type }}</span>
        </div>
        <div class="kg-legend-item">
          <span class="kg-legend-dot" style="background:#bbb"></span>
          <span class="kg-legend-label">连接</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import cytoscape from 'cytoscape';
import { ElMessage } from 'element-plus';

const searchNode = ref('');
let cyInstance = null;
const uploadedFileName = ref('');
let uploadedGraphData = null;
const graphUploadRef = ref(null);
const layoutType = ref('cose');
const showLegend = ref(true); // 控制图例显示/隐藏

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

// 类型英文到中文的映射
const typeNameMap = {
  person: '人物',
  event: '事件',
  geo: '地点',
  organization: '组织',
  equipment: '装备',
  category: '类别',
  // 你可以继续补充
  '地理学的': '地理学的',
  '人': '人物',
  '事件': '事件',
  '类别': '类别',
  '组织': '组织',
  '设备': '设备',
  '位置': '位置',
  '未知': '未知'
};

// 颜色盘
const legendColorMap = {
  person: '#409EFF',
  event: '#67C23A',
  geo: '#B37FEB',
  organization: '#F56C6C',
  equipment: '#13C2C2',
  category: '#E6A23C',
  // 兼容部分中文类型
  '地理学的': '#FFB6C1',
  '人': '#409EFF',
  '事件': '#67C23A',
  '类别': '#E6A23C',
  '组织': '#F56C6C',
  '设备': '#13C2C2',
  '位置': '#B37FEB',
  '未知': '#FFB940'
};
const colorPalette = [
  "#409EFF", "#67C23A", "#E6A23C", "#F56C6C", "#909399", "#13C2C2", "#B37FEB", "#FF85C0", "#FFB940", "#36CFC9"
];

// 动态图例
const dynamicLegendMap = ref({});

// 侧边栏按钮（最后一个为图例按钮）
const sidebarBtns = [
  { icon: 'kg-icon-play', tip: '播放', action: 'play' },
  { icon: 'kg-icon-grid', tip: '切换布局', action: 'layout' },
  { icon: 'kg-icon-rotate-cw', tip: '顺时针旋转', action: 'rotateCW' },
  { icon: 'kg-icon-rotate-ccw', tip: '逆时针旋转', action: 'rotateCCW' },
  { icon: 'kg-icon-target', tip: '定位中心', action: 'center' },
  { icon: 'kg-icon-zoom-in', tip: '放大', action: 'zoomIn' },
  { icon: 'kg-icon-zoom-out', tip: '缩小', action: 'zoomOut' },
  { icon: 'kg-icon-fullscreen', tip: '全屏', action: 'fullscreen' },
  { icon: 'kg-icon-book', tip: '图例', action: 'legend' }
];

// 侧边栏按钮功能实现
function handleSidebarClick(item) {
  switch (item.action) {
    case 'play':
      ElMessage.info('播放功能可自定义实现');
      break;
    case 'layout':
      // 可弹出布局切换菜单
      break;
    case 'rotateCW':
      rotateGraph(90);
      break;
    case 'rotateCCW':
      rotateGraph(-90);
      break;
    case 'center':
      if (cyInstance) cyInstance.fit();
      break;
    case 'zoomIn':
      if (cyInstance) cyInstance.zoom(cyInstance.zoom() * 1.2);
      break;
    case 'zoomOut':
      if (cyInstance) cyInstance.zoom(cyInstance.zoom() * 0.8);
      break;
    case 'fullscreen':
      toggleFullscreen();
      break;
    case 'legend':
      showLegend.value = !showLegend.value;
      break;
    default:
      break;
  }
}

// 旋转图谱
function rotateGraph(deg) {
  if (cyInstance) {
    const center = { x: cyInstance.width() / 2, y: cyInstance.height() / 2 };
    const rad = (deg * Math.PI) / 180;
    cyInstance.nodes().forEach(node => {
      const pos = node.position();
      const x = pos.x - center.x;
      const y = pos.y - center.y;
      const nx = x * Math.cos(rad) - y * Math.sin(rad);
      const ny = x * Math.sin(rad) + y * Math.cos(rad);
      node.position({
        x: nx + center.x,
        y: ny + center.y
      });
    });
    cyInstance.fit();
  }
}

// 全屏切换
function toggleFullscreen() {
  const el = document.documentElement;
  if (!document.fullscreenElement) {
    el.requestFullscreen && el.requestFullscreen();
  } else {
    document.exitFullscreen && document.exitFullscreen();
  }
}

const beforeUploadGraphFile = (file) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result);
      uploadedFileName.value = file.name;
      uploadedGraphData = data;
      renderKnowledgeGraph(data);
      ElMessage.success('知识图谱文件加载成功！');
    } catch (err) {
      ElMessage.error('知识图谱文件格式错误！');
    }
  };
  reader.readAsText(file);
  return false;
};

const renderKnowledgeGraph = (graphData) => {
  if (!graphData || !graphData.nodes || !graphData.edges) {
    ElMessage.warning('知识图谱数据为空或格式错误！');
    return;
  }
  // 自动捕获实际类型
  const typeColorMap = {};
  let colorIdx = 0;
  const legendTypes = {};
  graphData.nodes.forEach(node => {
    // 优先 entity_type，其次 label
    let type = node.entity_type || node.label || "未知";
    if (!typeColorMap[type]) {
      typeColorMap[type] = legendColorMap[type] || colorPalette[colorIdx % colorPalette.length];
      colorIdx++;
    }
    legendTypes[type] = typeColorMap[type];
  });
  dynamicLegendMap.value = legendTypes;

  // 统计每个节点的度数
  const nodeDegreeMap = {};
  graphData.edges.forEach(edge => {
    nodeDegreeMap[edge.source] = (nodeDegreeMap[edge.source] || 0) + 1;
    nodeDegreeMap[edge.target] = (nodeDegreeMap[edge.target] || 0) + 1;
  });

  const mainNodeId = graphData.nodes[0]?.id || '';
  const connectedIds = new Set(graphData.edges.map(e => e.source).concat(graphData.edges.map(e => e.target)));
  const extraEdges = graphData.nodes
    .filter(n => !connectedIds.has(n.id))
    .map(n => ({
      data: {
        id: `virtual_${n.id}`,
        source: mainNodeId,
        target: n.id,
        virtual: true
      }
    }));

  const elements = {
    nodes: graphData.nodes.map((node, idx) => {
      let type = node.entity_type || node.label || "未知";
      const degree = nodeDegreeMap[node.id] || 1;
      const size = Math.max(18, Math.min(80, 18 + Math.sqrt(degree) * 15));
      return {
        data: {
          id: node.id,
          label: node.label || node.id,
          color: typeColorMap[type],
          size,
          ...node
        }
      };
    }),
    edges: [
      ...graphData.edges.map(edge => ({
        data: {
          id: edge.id,
          source: edge.source,
          target: edge.target,
          ...edge
        }
      })),
      ...extraEdges
    ]
  };

  // 若已存在实例，先销毁
  if (cyInstance) {
    cyInstance.destroy();
    cyInstance = null;
  }

  cyInstance = cytoscape({
    container: document.getElementById('cy'),
    elements: elements,
    style: [
      {
        selector: 'node',
        style: {
          'background-color': 'data(color)',
          'width': 'data(size)',
          'height': 'data(size)',
          'border-width': 0,
          'label': '',
          'text-opacity': 0,
          'transition-property': 'width height background-color',
          'transition-duration': '0.3s'
        }
      },
      {
        selector: 'node[label]',
        style: {
          'text-margin-y': -30,
          'text-halign': 'center',
          'text-valign': 'center',
          'text-background-color': '#222',
          'text-background-opacity': 0.8,
          'text-background-shape': 'roundrectangle',
          'text-background-padding': 6,
          'text-border-color': '#444',
          'text-border-width': 1,
          'text-border-opacity': 1,
          'text-outline-color': '#222',
          'text-outline-width': 0,
          'font-size': 16,
          'font-weight': 'bold',
          'color': '#fff',
          'text-shadow-color': '#000',
          'text-shadow-blur': 8,
          'text-shadow-opacity': 0.4,
          'label': 'data(label)',
          'text-opacity': 1
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 1.5,
          'line-color': '#bbb',
          'curve-style': 'bezier',
          'opacity': 0.4
        }
      },
      {
        selector: '.faded',
        style: {
          'opacity': 0.08,
          'text-opacity': 0.08
        }
      }
    ],
    layout: getLayoutConfig()
  });
  addHoverEffect();
};

// 根据 layoutType 返回不同布局配置
function getLayoutConfig() {
  if (layoutType.value === 'concentric') {
    return {
      name: 'concentric',
      padding: 80,
      animate: true,
      animationDuration: 1500,
      fit: true,
      concentric: function(node) {
        return node.degree();
      },
      levelWidth: function(nodes) {
        return 1;
      },
      minNodeSpacing: 10,
      startAngle: 3.14 / 2,
      clockwise: true,
    };
  } else if (layoutType.value === 'breadthfirst') {
    return {
      name: 'breadthfirst',
      padding: 80,
      animate: true,
      animationDuration: 1500,
      fit: true,
      spacingFactor: 1.3,
      directed: false,
      grid: false
    };
  } else if (layoutType.value === 'circle') {
    return {
      name: 'circle',
      padding: 80,
      animate: true,
      animationDuration: 1500,
      fit: true,
      spacingFactor: 1.2
    };
  } else {
    // 默认为cose
    return {
      name: 'cose',
      padding: 80,
      animate: true,
      animationDuration: 1500,
      fit: true,
      nodeRepulsion: 120000,
      idealEdgeLength: 180,
      edgeElasticity: 0.2,
      gravity: 0.18,
      numIter: 2000,
      initialTemp: 200,
      coolingFactor: 0.95,
      componentSpacing: 120,
      nestingFactor: 1.2,
      randomize: true
    };
  }
}

// 切换布局时重新布局
function switchLayout() {
  if (cyInstance) {
    cyInstance.layout(getLayoutConfig()).run();
  }
}

const searchGraphNode = () => {
  if (!cyInstance || !searchNode.value.trim()) return;
  const name = searchNode.value.trim();
  const node = cyInstance.nodes().filter(ele =>
    (ele.data('label') && ele.data('label').includes(name)) ||
    (ele.data('id') && ele.data('id').includes(name))
  )[0];
  if (!node) {
    ElMessage.warning('未找到该节点');
    return;
  }
  const neighborhood = node.closedNeighborhood();
  cyInstance.elements().addClass('faded');
  neighborhood.removeClass('faded');
  cyInstance.fit(neighborhood, 80);
};

const addHoverEffect = () => {
  if (!cyInstance) return;
  cyInstance.on('mouseover', 'node', function(evt){
    const node = evt.target;
    const neighborhood = node.closedNeighborhood();
    cyInstance.elements().addClass('faded');
    neighborhood.removeClass('faded');
  });
  cyInstance.on('mouseout', 'node', function(evt){
    cyInstance.elements().removeClass('faded');
  });
  // 点击空白处恢复全图
  cyInstance.on('tap', function(evt){
    if (evt.target === cyInstance) {
      cyInstance.elements().removeClass('faded');
    }
  });
};

onMounted(async () => {
  // 默认加载本地json
  try {
    const resp = await fetch('/graph_data.json');
    const data = await resp.json();
    renderKnowledgeGraph(data);
  } catch (e) {
    // 忽略
  }
});

onUnmounted(() => {
  if (cyInstance) {
    cyInstance.destroy();
    cyInstance = null;
  }
});

// 在组件挂载时执行自动刷新逻辑

onMounted(autoReload);
</script>

<style scoped>
.kg-root {
  width: 100vw;
  height: 100vh;
  background: #18191c;
  position: relative;
  overflow: hidden;
}
.kg-toolbar {
  width: 100vw;
  height: 56px;
  background: #232428;
  border-bottom: 1px solid #232428;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 36px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 20;
}
.kg-toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.kg-toolbar-right {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  letter-spacing: 2px;
}
.kg-title {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}
.kg-select,
.kg-search {
  background: #232428;
}
.file-tip {
  color: #aaa;
  font-size: 13px;
  margin-left: 8px;
}
.kg-sidebar {
  position: fixed;
  top: 56px;
  left: 0;
  width: 48px;
  height: calc(100vh - 56px);
  background: #18191c;
  border-radius: 16px 0 0 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 0;
  z-index: 15;
  gap: 6px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  border: 1px solid #232428;
}
.kg-sidebar-btn {
  width: 36px;
  height: 36px;
  margin: 2px 0;
  background: #232428;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 20px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.kg-sidebar-btn:hover {
  background: #33343a;
  color: #409EFF;
}
.kg-main {
  position: absolute;
  left: 56px;
  top: 56px;
  width: calc(100vw - 56px);
  height: calc(100vh - 56px);
  background: #18191c;
  overflow: hidden;
}
.kg-graph {
  width: 100%;
  height: 100%;
  background: #18191c;
  border-radius: 0;
  box-shadow: none;
  transition: box-shadow 0.3s;
}
.kg-legend {
  position: absolute;
  right: 24px;
  bottom: 24px;
  background: rgba(30,32,36,0.95);
  border-radius: 12px;
  padding: 16px 18px 12px 18px;
  color: #fff;
  font-size: 15px;
  min-width: 120px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  z-index: 30;
}
.kg-legend-title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
  color: #fff;
}
.kg-legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
}
.kg-legend-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-right: 8px;
  border: 2px solid #222;
  display: inline-block;
}
.kg-legend-label {
  color: #fff;
  font-size: 14px;
}
.faded {
  opacity: 0.08 !important;
  transition: opacity 0.3s;
}
/* 自定义icon字体（可用iconfont、svg或element-plus图标库） */
.kg-icon-play::before { content: "\25B6"; }
.kg-icon-grid::before { content: "\25A6"; }
.kg-icon-rotate-cw::before { content: "\21BB"; }
.kg-icon-rotate-ccw::before { content: "\21BA"; }
.kg-icon-target::before { content: "\25CE"; }
.kg-icon-zoom-in::before { content: "\002B"; }
.kg-icon-zoom-out::before { content: "\2212"; }
.kg-icon-fullscreen::before { content: "\26F6"; }
.kg-icon-book::before { content: "\1F4D6"; }
.kg-icon-settings::before { content: "\2699"; }
</style>