# FreeCAD

## 基础信息
- **项目名**: FreeCAD/FreeCAD
- **URL**: https://github.com/FreeCAD/FreeCAD
- **作者/团队**: FreeCAD 社区 (国际)
- **License**: LGPL-2.0 ✅
- **语言**: C++ + Python
- **平台**: 桌面 (Windows / macOS / Linux)
- **最近更新**: 2026 (活跃)
- **Star 数**: ~24,000+ (顶级开源)
- **Fork 数**: ~4,500
- **首次提交**: 2002
- **维护状态**: 非常活跃

## 功能介绍
- **开源参数化 3D CAD/BIM 建模**
- 类似 AutoCAD/Revit/SolidWorks
- BIM 工作台 (Arch/BIM)
- 完整 Python API
- 可做有限元分析 (FEM 工作台)
- IFC 导入导出

## 技术栈
- C++ (Qt) + Python
- OpenCascade (几何内核)
- Coin3D (可视化)

## 演示
- 官网: https://www.freecad.org
- BIM 工作台: https://github.com/yorikvanhavre/BIM_Workbench

## 适合嵌入到蓝领金服 app 的场景
- C 类 - BIM 建模 (蓝领 app "看 BIM" 需求)
- I 类 - 图纸编辑
- **不直接嵌入**, 后端 Python 进程通信

## 二次开发可行性
- 代码可读性: ⭐⭐⭐ (C++ + Python)
- 文档完整度: ⭐⭐⭐⭐
- 移动端: ❌
- 中文支持: ✅ (社区翻译)
- 社区活跃度: ⭐⭐⭐⭐⭐

## 风险
- License: **LGPL-2.0** ✅ (动态链接)
- 桌面级,移动端需要 Web 包装 (Three.js / xeokit)
- 学习曲线中等

## 来源
- [1] FreeCAD 官网
- [2] GitHub topic: bim
