# web-ifc-viewer (ThatOpen)

## 基础信息
- **项目名**: ThatOpen/web-ifc-viewer
- **URL**: https://github.com/ThatOpen/web-ifc-viewer
- **作者/团队**: ThatOpen
- **License**: MIT ✅
- **语言**: TypeScript + WebGL
- **平台**: Web (桌面 + 移动浏览器)
- **最近更新**: 2026-06
- **Star 数**: ~1,000
- **Fork 数**: ~200
- **首次提交**: 2020
- **维护状态**: 活跃

## 功能介绍
- 基于 Three.js 的 BIM/IFC 浏览器查看器
- 加载 IFC 文件 → 3D 渲染 + 属性查询
- 剖切/测量/批注
- BCF 协同 (BIM Collaboration Format)
- 移动端支持
- 一行代码集成: `<ifc-viewer>` 组件

## 技术栈
- 前端: TypeScript + Three.js + WebGL
- 渲染: WebGL 2.0
- 部署: CDN / npm / iframe

## 演示 / 在线试用
- Demo: https://thatopen.github.io/engine_web-ifc/demo
- 组件: npm install web-ifc-viewer
- 文档: https://docs.thatopen.com

## 适合嵌入到蓝领金服 app 的场景
- C 类 - **BIM/IFC 3D 查看** (蓝领 app 嵌入式 3D 模型)
- I 类 - 图纸/BIM 协同
- 工地现场"扫一眼就知道钢筋怎么摆、管道怎么走"

## 二次开发可行性
- 代码可读性: ⭐⭐⭐⭐
- 文档完整度: ⭐⭐⭐⭐⭐
- 移动端适配: ⭐⭐⭐⭐
- 中文支持: ✅
- 社区活跃度: ⭐⭐⭐⭐

## 风险
- License: **MIT** ✅ 任意商用
- WASM 依赖 engine_web-ifc,需一起打包
- 性能:大型 BIM 模型移动端需要降级渲染

## 来源
- [1] GitHub topic: ifc
- [2] ThatOpen 官网 - https://thatopen.com
- [3] NPM - https://www.npmjs.com/package/web-ifc-viewer
