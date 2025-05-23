import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router/index.js'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import formCreate from '@form-create/element-ui'


const app = createApp(App)
app.use(createPinia())     // 导入pinia 库
app.use(router)
app.use(ElementPlus)
app.use(formCreate)
//导入所有elementplus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.mount('#app')

