# web-ifc (engine_web-ifc)

## 基础信息
- **项目名**: ThatOpen/engine_web-ifc
- **URL**: https://github.com/ThatOpen/engine_web-ifc
- **作者/团队**: ThatOpen (西班牙 BIM 开源公司)
- **License**: MPL-2.0 (Mozilla Public License)
- **语言**: C++ (核心) + TypeScript/WASM (JS 绑定)
- **平台**: Web / Node.js / 任何 WASM 环境
- **最近更新**: 2026-06-03
- **Star 数**: 972
- **Fork 数**: 267
- **首次提交**: 2020-12
- **Issues 活跃度**: 高 (65 open)
- **维护状态**: 活跃

## 功能介绍
- 浏览器原生读写 IFC 文件 (业界最快的 JS IFC 解析器)
- WASM 编译,接近原生 C++ 速度
- 支持 IFC2x3 / IFC4 / IFC4x3
- 支持 800+ IFC 实体类型
- 与 Three.js / web-ifc-viewer 完美集成
- Docker 镜像可用

## 技术栈
- 核心: C++ + Emscripten → WASM
- 绑定: TypeScript
- 部署: npm / Docker

## 演示 / 在线试用
- Demo: https://thatopen.github.io/engine_web-ifc/demo
- NPM: https://www.npmjs.com/package/web-ifc
- 文档: https://github.com/ThatOpen/engine_web-ifc

## 适合嵌入到蓝领金服 app 的场景
- C 类 - **IFC 模型查看器** (蓝领 app 看施工图,直接打开 BIM 模型)
- I 类 - 工程文档 (图纸管理)
- 工地端 WebView 打开 BIM → 直接看结构/管线

## 二次开发可行性
- 代码可读性: ⭐⭐⭐ (C++ 复杂,JS 包装层清晰)
- 文档完整度: ⭐⭐⭐⭐
- 移动端适配: ⭐⭐⭐⭐ (WASM 在现代移动浏览器表现良好)
- 中文支持: ✅ (无 i18n 问题)
- 社区活跃度: ⭐⭐⭐⭐

## 风险
- License: **MPL-2.0** - 文件级 copyleft, 改的源文件要开源, 整体商用 OK ✅
- WASM 包体积 ~3MB,移动端首屏加载需考虑
- 需要 BIM 模型,实际工地 BIM 普及率还不高

## 来源
- [1] GitHub topic: ifc - https://github.com/topics/ifc
- [2] ThatOpen 官网 - https://thatopen.com
- [3] GitHub README - https://github.com/ThatOpen/engine_web-ifc
