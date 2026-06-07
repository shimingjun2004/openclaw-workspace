# BIMserver

## 基础信息
- **项目名**: opensourceBIM/BIMserver
- **URL**: https://github.com/opensourceBIM/BIMserver
- **作者/团队**: opensourceBIM.org 社区 (荷兰代尔夫特理工大学等)
- **License**: AGPL-3.0 ⚠️
- **语言**: Java
- **平台**: Web 服务端
- **最近更新**: 2026-03
- **Star 数**: 1,723
- **Fork 数**: 643
- **首次提交**: 2013
- **维护状态**: 慢 (核心稳定,但社区减少)

## 功能介绍
- BIM 模型协同服务器 (中心化 BIM 平台)
- IFC 文件版本管理
- 多人并发编辑/合并
- BIM 机器人 (BIM Bots) - 服务端自动任务
- 多客户端支持 (web-ifc, BIMsurfer, Revit 插件)
- BCF 协同

## 技术栈
- 后端: Java
- 前端: 多个客户端
- 数据库: 支持多种
- 部署: Tomcat / Docker

## 适合嵌入到蓝领金服 app 的场景
- C 类 - BIM 协同 (如果走"自建 BIM 平台"路线)
- I 类 - 图纸版本管理
- 工地端上传 → BIMserver 合并 → 工人看最新版

## 二次开发可行性
- 代码可读性: ⭐⭐⭐ (Java 老项目)
- 文档完整度: ⭐⭐⭐
- 移动端适配: ❌ 需自行开发
- 中文支持: ⚠️ 英文为主
- 社区活跃度: ⭐⭐

## 风险
- License: **AGPL-3.0** ⚠️ 网络服务也要开源
- 老牌项目,近年更新慢
- Java 部署重,运维成本高

## 来源
- [1] GitHub topic: bim
- [2] BIMserver.org - https://github.com/opensourceBIM/BIMserver
- [3] opensourceBIM 社区
