# EnergyPlus (NREL)

## 基础信息
- **项目名**: NREL/EnergyPlus
- **URL**: https://github.com/NREL/EnergyPlus
- **作者/团队**: NREL (美国国家可再生能源实验室) + DOE + LBNL
- **License**: BSD-3-Clause ✅
- **语言**: C++ + Fortran
- **平台**: Windows / Linux / macOS (CLI)
- **最近更新**: 2026 (活跃)
- **Star 数**: ~1,800
- **Fork 数**: ~500
- **首次提交**: 2002
- **维护状态**: 极其活跃 (DOE 长期投入)

## 功能介绍
- **建筑能耗模拟黄金标准** (DOE 官方)
- 整年逐时能耗分析
- HVAC 系统仿真
- 采光/通风/热舒适
- 输入: IDF / Output: CSV/SQLite
- 与 OpenStudio / Ladybug 集成

## 技术栈
- 核心: C++ + Fortran (历史悠久)
- 输入: EnergyPlus IDF 文件
- 部署: Docker / Windows Installer / Linux

## 演示
- 下载: https://energyplus.net
- 文档: https://energyplus.net/documentation

## 适合嵌入到蓝领金服 app 的场景
- H 类 - **建筑能耗/节能计算** (权威)
- 工地节能评估、绿色建筑认证
- 重型工具,适合独立子服务

## 二次开发可行性
- 代码可读性: ⭐⭐ (Fortran + C++ 老)
- 文档完整度: ⭐⭐⭐⭐⭐
- 移动端: ❌ 不适合
- 中文支持: ⚠️
- 社区活跃度: ⭐⭐⭐⭐⭐

## 风险
- License: **BSD-3-Clause** ✅
- 学习曲线极陡
- 中国有清华/天正等本土工具,需要做差异化
- **不直接嵌入**, 通过 JSON-RPC/IPC 集成

## 来源
- [1] NREL 官网 https://www.nrel.gov
- [2] EnergyPlus 官网
