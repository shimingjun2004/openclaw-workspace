# Smart_Construction (PPE 安全帽检测)

## 基础信息
- **项目名**: PeterH0323/Smart_Construction
- **URL**: https://github.com/PeterH0323/Smart_Construction
- **作者/团队**: PeterH0323 (个人开发者,中国)
- **License**: 待确认
- **语言**: Python + PyTorch
- **平台**: Python + Web 可视化
- **最近更新**: 2024-04
- **Star 数**: 2,600
- **Fork 数**: ~600
- **维护状态**: 慢 (中文圈知名)

## 功能介绍
- **基于 YOLOv5 的工地安全帽 + 禁入危险区域识别**
- 实时检测工人是否戴安全帽
- 危险区域入侵报警
- 配套 Web 可视化界面
- 完整数据集 + 训练教程

## 技术栈
- 深度学习: YOLOv5 + PyTorch
- 后端: Python + Flask
- 前端: Vue (简单)
- 硬件: 摄像头/视频流

## 演示
- B 站视频教程
- README 有完整训练指南

## 适合嵌入到蓝领金服 app 的场景
- A 类 - **工地安全管理** ⭐⭐⭐⭐⭐
- 工人/班组长 → 摄像头检测 → 违规报警
- 蓝领金服 app "安全管理"模块直接嵌入 YOLOv5 模型
- 工人通过 app 上传现场照片 → 自动识别 PPE 穿戴

## 二次开发可行性
- 代码可读性: ⭐⭐⭐⭐ (有详细教程)
- 文档完整度: ⭐⭐⭐⭐⭐ (中文! 完整)
- 移动端适配: ⭐⭐⭐ (有 Web 界面)
- 中文支持: ✅✅ 完美
- 社区活跃度: ⭐⭐⭐⭐ (中文圈高知名度)

## 风险
- License: 待查
- 仅 Python 后端 + Web,需要做移动端封装
- YOLOv5 老旧,建议升级到 YOLOv8/v10
- 隐私合规: 工地摄像头采集需员工知情同意

## 来源
- [1] GitHub search: construction safety - 排名第 1, 2.6k stars
- [2] 中文社区
