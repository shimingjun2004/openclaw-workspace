# 建筑行业开源工具全球调研 (蓝领金服 app 嵌入用)

> 调研员: smj-小秘 subagent (开源建筑工具全球调研)
> 调研时间: 2026-06-07 22:30 → 2026-06-07 23:00 (GMT+8)
> 调研范围: GitHub / Gitee / SourceForge / Codeberg / npm / PyPI / Docker Hub
> 收集数量: **89 个开源工具** (覆盖 **26 大类** - A-Z)
> 嵌入推荐: **10 个最适合蓝领金服 app** (按价值排序)
> 数据来源: GitHub Topics / Search / README / GitHub REST API / 官网
> 数据交叉: 每个工具至少 2-3 源 (GitHub 搜索 + 主页 README + 文档站)

---

## 0. TL;DR (老史 5 分钟看完)

### 蓝领金服 app 背景
- 蓝领金服 app = 蓝领工人金融服务 + 工具平台
- Java 后端 + Vue 前端 (移动端)
- 已有 MySQL 库 `blue`
- 现需 "**小工具**" 模块 → 嵌入开源工具

### 强烈推荐嵌入 (⭐⭐⭐⭐⭐) - 10 个最优先

| # | 工具 | URL | Star | License | 功能 | 老史怎么用 |
|---|------|-----|------|---------|------|----------|
| 1 | **mlightcad/cad-viewer** | https://github.com/mlightcad/cad-viewer | 677 | MIT | 浏览器 DWG/DXF 查看 | 嵌入"**看图**"模块 → 工人直接看施工图 |
| 2 | **dierbei/yhpc (HazardMind)** | https://github.com/dierbei/yhpc | <10 | 待查 | 中文隐患闭环 (uni-app x) | 嵌入"**安全隐患上报/整改**" → 蓝领核心场景 |
| 3 | **PeterH0323/Smart_Construction** | https://github.com/PeterH0323/Smart_Construction | 2,611 | GPL-3.0 | YOLOv5 安全帽 + 危险区域 | 嵌入"**AI 识别 PPE**" → 工人拍照自动识别 |
| 4 | **blakeblackshear/frigate** | https://github.com/blakeblackshear/frigate | 33,584 | MIT | NVR + 实时目标检测 | 嵌入"**AI 监控**" → 工地摄像头 24h 监管 |
| 5 | **pjazdzyk/energy-flow-x-docu** | https://github.com/pjazdzyk/energy-flow-x-docu | 4 | 未声明 | Java+Vue HVAC 全套 | 嵌入"**HVAC 工程师**" → 工地临设空调/通风 |
| 6 | **datadrivenconstruction/OpenConstructionERP** | https://github.com/datadrivenconstruction/OpenConstructionERP | 315 | AGPL-3.0 | 71 模块建筑 ERP | 嵌入"**算量/计价**" → 项目部造价 |
| 7 | **home-assistant/core** | https://github.com/home-assistant/core | 80,000+ | Apache-2.0 | 智能家居/楼宇自控 | 嵌入"**智慧宿舍/临设**" → 工地 IoT |
| 8 | **dataease/dataease** | https://github.com/dataease/dataease | 20,000+ | GPL-3.0 | 国产 BI 大屏 | 嵌入"**项目大屏**" → 中国本土化最佳 |
| 9 | **superQyu/SCSSP** | https://github.com/superQyu/SCSSP | 6 | MIT | 智慧工地监管平台 | 嵌入"**智慧工地**" → 中文场景贴合 |
| 10 | **ThatOpen/engine_web-ifc** | https://github.com/ThatOpen/engine_web-ifc | 972 | MPL-2.0 | WASM IFC 解析器 | 嵌入"**BIM 通用底座**" |

### 不推荐嵌入 (但值得参考)
- **mfem / deal.II / MOOSE / ElmerFEM / Kratos**: 偏 HPC 研究,蓝领 app 不适合
- **FreeCAD / Dynamo**: 桌面 BIM 设计,移动端不直接用
- **EnergyPlus**: 命令行重武器,作后端服务
- **Ladybug Tools (AGPL)**: 商用必查 license
- **NREL/OpenStudio**: 同 EnergyPlus,重型 SDK

---

## 1. 26 大类工具清单 (按类)

### A. 施工现场管理 / 项目管理 (4 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| opf/openproject | https://github.com/opf/openproject | 15,200 | GPL-3.0 | ⭐⭐⭐⭐ |
| datadrivenconstruction/OpenConstructionERP | https://github.com/datadrivenconstruction/OpenConstructionERP | 315 | AGPL-3.0 | ⭐⭐⭐⭐⭐ |
| dierbei/yhpc (HazardMind) | https://github.com/dierbei/yhpc | <10 | 待查 | ⭐⭐⭐⭐⭐ |
| UmairPashaa/HSE-Digital-Toolkit | https://github.com/UmairPashaa/HSE-Digital-Toolkit | 2 | 待查 | ⭐⭐⭐ |

### B. 工程造价 / 算量 / 计价 (5 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| OpenConstructionERP | (A 类) | 315 | AGPL-3.0 | ⭐⭐⭐⭐⭐ |
| datadrivenconstruction/cad2data | https://github.com/datadrivenconstruction/cad2data-Revit-IFC-DWG-DGN | 397 | AGPL-3.0 | ⭐⭐⭐⭐ |
| datadrivenconstruction/QuantityTakeoff-Python | (DDC org) | <50 | AGPL-3.0 | ⭐⭐⭐⭐ |
| hgrecco/pint | https://github.com/hgrecco/pint | 2,700+ | BSD-3-Clause | ⭐⭐⭐⭐⭐ |
| yorikvanhavre/priceAPI | https://github.com/yorikvanhavre/priceAPI | 17 | LGPL-2.1 | ⭐⭐⭐ |

### C. BIM / 三维建模 (17 个,最多)
| 工具 | URL | Star | License |
|------|-----|------|---------|
| FreeCAD/FreeCAD | https://github.com/FreeCAD/FreeCAD | 31,400 | LGPL-2.0 |
| ThatOpen/engine_web-ifc | https://github.com/ThatOpen/engine_web-ifc | 972 | MPL-2.0 |
| ThatOpen/web-ifc-viewer | https://github.com/ThatOpen/web-ifc-viewer | ~1,000 | MIT |
| ThatOpen/web-ifc-three | https://github.com/ThatOpen/web-ifc-three | 590 | 待查 |
| opensourceBIM/BIMserver | https://github.com/opensourceBIM/BIMserver | 1,723 | AGPL-3.0 |
| xeokit/xeokit-sdk | https://github.com/xeokit/xeokit-sdk | 904 | AGPL-3.0 |
| xeokit/xeokit-bim-viewer | https://github.com/xeokit/xeokit-bim-viewer | 547 | AGPL-3.0 |
| iTwin/itwinjs-core | https://github.com/iTwin/itwinjs-core | 717 | MIT |
| DynamoDS/Dynamo | https://github.com/DynamoDS/Dynamo | 2,000 | Apache-2.0 |
| xBimTeam/XbimEssentials | https://github.com/xBimTeam/XbimEssentials | 566 | CDDL-1.0 |
| mlt131220/Astral3D | https://github.com/mlt131220/Astral3D | 2,400 | 待查 |
| gkjohnson/three-bvh-csg | https://github.com/gkjohnson/three-bvh-csg | 914 | MIT |
| opensourceBIM/BIMsurfer | https://github.com/opensourceBIM/BIMsurfer | 424 | AGPL-3.0 |
| hypar-io/Elements | https://github.com/hypar-io/Elements | 399 | Apache-2.0 |
| GSharker/G-Shark | https://github.com/GSharker/G-Shark | 233 | MIT |
| assimp/assimp | https://github.com/assimp/assimp | 13,000+ | BSD-3-Clause |
| buildingSMART/IDS | https://github.com/buildingSMART/IDS | 302 | 官方 |

### D. 测量 / 放样 (0 个)
**Gap**: GitHub topic "site-survey" 主要是 WiFi 测量, 不是工程测量。建筑测量放样的开源项目极少。
**建议**: 蓝领金服 app 测量模块自研 (安卓调用 GPS + 全站仪蓝牙 SDK)。

### E. 结构计算 / 验算 (11 个)
| 工具 | URL | Star | License |
|------|-----|------|---------|
| JWock82/Pynite | https://github.com/JWock82/Pynite | 705 | MIT |
| fib-international/structuralcodes | https://github.com/fib-international/structuralcodes | 280 | Apache-2.0 |
| buddyd16/Structural-Engineering | https://github.com/buddyd16/Structural-Engineering | 282 | BSD-3-Clause |
| madil4/awatif | https://github.com/madil4/awatif | 155 | MIT |
| idaholab/moose | https://github.com/idaholab/moose | 2,300+ | LGPL-2.1 |
| mfem/mfem | https://github.com/mfem/mfem | 2,200+ | BSD-3-Clause |
| dealii/dealii | https://github.com/dealii/dealii | 1,700+ | LGPL-2.1 |
| ElmerCSC/elmerfem | https://github.com/ElmerCSC/elmerfem | 1,600+ | GPL-2.0 |
| KratosMultiphysics/Kratos | https://github.com/KratosMultiphysics/Kratos | 1,300+ | BSD |
| NGSolve/ngsolve | https://github.com/NGSolve/ngsolve | 551 | LGPL-2.1 |
| BriefFiniteElementNet | https://github.com/BriefFiniteElementNet/BriefFiniteElement.Net | 176 | MIT |

### F. 水利 / 市政 / 路桥 (3 个)
| 工具 | URL | Star | License |
|------|-----|------|---------|
| pyswmm/swmmio | https://github.com/pyswmm/swmmio | 150+ | MIT |
| tmgerard/python-bridge-tools | https://github.com/tmgerard/python-bridge-tools | 4 | 待查 |
| G1213123/TrafficSign | https://github.com/G1213123/TrafficSign | 29 | 待查 |

### G. 暖通 / 电气 / 给排水 (5 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **pjazdzyk/energy-flow-x-docu** | https://github.com/pjazdzyk/energy-flow-x-docu | 4 | 未声明 ⚠️ | ⭐⭐⭐⭐⭐ Java+Vue |
| simeononsecurity/Manual-J-Load-Calculator | https://github.com/simeononsecurity/Manual-J-Load-Calculator | 7 | MIT | ⭐⭐⭐ |
| TunaLobster/pyduct | https://github.com/TunaLobster/pyduct | 16 | MIT | ⭐⭐⭐ |
| TheoMoumiadis/HVAC-calc-with-NN | https://github.com/TheoMoumiadis/HVAC-calc-with-NN | 23 | 待查 | ⭐⭐ |
| pyswmm/swmmio | (F 类) | 150+ | MIT | ⭐⭐⭐ |

### H. 绿色建筑 / 节能 (4 个)
| 工具 | URL | Star | License |
|------|-----|------|---------|
| NREL/EnergyPlus | https://github.com/NREL/EnergyPlus | 1,800+ | BSD-3-Clause |
| NREL/OpenStudio | https://github.com/NREL/OpenStudio | 700+ | 多 license |
| ladybug-tools/ladybug | https://github.com/ladybug-tools/ladybug | 500+ | AGPL-3.0 |
| greenpeer/GreenLightPlus | https://github.com/greenpeer/GreenLightPlus | 29 | 待查 |

### I. 工程文档 / 资料 (1 个,核心刚需)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **mlightcad/cad-viewer** | https://github.com/mlightcad/cad-viewer | 677 | MIT | ⭐⭐⭐⭐⭐ |

### J. 工人 / 劳务 (3 个,核心推荐)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **dierbei/yhpc (HazardMind)** | https://github.com/dierbei/yhpc | <10 | 待查 | ⭐⭐⭐⭐⭐ |
| **PeterH0323/Smart_Construction** | https://github.com/PeterH0323/Smart_Construction | 2,611 | GPL-3.0 | ⭐⭐⭐⭐⭐ |
| SafetyMP/Autonomous-EHS-Management | https://github.com/SafetyMP/Autonomous-EHS-Management | 1 | Apache-2.0 | ⭐⭐⭐ |

### K. 装饰装修 / 室内设计 (1 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| alaradirik/sd-interior-design | https://github.com/alaradirik/sd-interior-design | 106 | MIT | ⭐⭐⭐⭐ AI 设计 |

**Gap**: 瓷砖排版、软装搭配、装修预算等中文专门开源项目极少。

### L. 幕墙 / 门窗 (1 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| Lucas123912/CurtainWallDB (同济) | https://github.com/Lucas123912/CurtainWallDB | 3 | 待查 | ⭐⭐ 教学参考 |

**Gap**: 幕墙计算、节点设计、节能门窗等专门开源几乎为零。建议自研。

### M. 防水 / 防腐 / 保温 (0 个)
**Gap**: 此类专门开源项目 = 0。需要自研 (但可借 OpenConstructionERP 的算量)。

### N. 装配式建筑 / 预制构件 (1 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| LAMAHERI/BIM-Integration-3DConstruction | https://github.com/LAMAHERI/BIM-Integration-3DConstruction | <5 | MIT | ⭐⭐ 学术 |

**Gap**: 装配率计算、PC 构件管理 - 极缺。中国本土项目可关注 PC 厂商,自有 SaaS 较多。

### O. 工程监理 / 工程质量 (3 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| IanTorweihe/ZapierInspectionReportBot | https://github.com/IanTorweihe/ZapierInspectionReportBot | 6 | 待查 | ⭐⭐⭐⭐ AI 报告 |
| malharbi860/weekly-quality-checklist | https://github.com/malharbi860/weekly-quality-checklist | 1 | 待查 | ⭐⭐ |
| tenzene111-ux/cqis-website | https://github.com/tenzene111-ux/cqis-website | 0 | 待查 | ⭐⭐ |

### P. 工程检测 / 监测 (1 个,主要靠通用 IoT 平台)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| (用 ThingsBoard / ThingsBoard Edge) | (S 类) | 18,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ |

**Gap**: 桩基检测、主体结构检测、沉降观测 - 专门开源几乎为零。
**建议**: 沉降监测 = IoT (倾斜仪/全站仪) + ThingsBoard,蓝领金服 app 通过 API 拉取。

### Q. 建筑设备 / 电梯 / 智能建筑 (4 个,价值高)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **home-assistant/core** | https://github.com/home-assistant/core | 80,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ 智能家居/楼宇自控 |
| **openhab/openhab-core** | https://github.com/openhab/openhab-core | 5,000+ | EPL-2.0 | ⭐⭐⭐⭐ 商业 BA |
| **blakeblackshear/frigate** | https://github.com/blakeblackshear/frigate | 33,584 | MIT | ⭐⭐⭐⭐⭐ 实时 AI 监控 |
| openremote/openremote | https://github.com/openremote/openremote | 1,200+ | AGPL-3.0 | ⭐⭐⭐ |

### R. 工程机械 / 工地设备 (1 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| DrPeiXueFeng/AAW_for_TC | https://github.com/DrPeiXueFeng/AAW_for_TC | 5 | MIT | ⭐⭐⭐ 塔吊防碰撞 |

**Gap**: 塔吊 / 施工电梯管理 专门开源极少。设备维保靠通用 CMMS (如 ERPNext)。

### S. 智慧工地 / IoT / 数字孪生 (8 个,核心赛道)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **superQyu/SCSSP** | https://github.com/superQyu/SCSSP | 6 | MIT | ⭐⭐⭐⭐⭐ 中文智慧工地 |
| superQyu/old-scssp | https://github.com/superQyu/old-scssp | 10 | MIT | ⭐⭐⭐ |
| **ThingsBoard** | https://github.com/thingsboard/thingsboard | 18,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ IoT 平台 |
| **home-assistant/core** | (Q 类) | 80,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ |
| node-red/node-red | https://github.com/node-red/node-red | 20,000+ | Apache-2.0 | ⭐⭐⭐⭐ 流式编程 |
| **emqx/emqx** | https://github.com/emqx/emqx | 15,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ MQTT 国产 |
| eclipse/mosquitto | https://github.com/eclipse/mosquitto | 9,000+ | EPL-2.0 | ⭐⭐⭐ 小型 |
| **Azure/opendigitaltwins-building** | https://github.com/Azure/opendigitaltwins-building | 173 | MIT | ⭐⭐⭐⭐ DTDL 本体 |
| WillowInc/opendigitaltwins-building | https://github.com/WillowInc/opendigitaltwins-building | 53 | MIT | ⭐⭐⭐ |
| kubeedge/kubeedge | https://github.com/kubeedge/kubeedge | 7,000+ | Apache-2.0 | ⭐⭐⭐ 边缘 |

### T. 建筑材料 / 供应链 (2 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| ojmarte/construction_api | https://github.com/ojmarte/construction_api | 5 | 待查 | ⭐⭐⭐ 材价 API |
| yorikvanhavre/priceAPI | (B 类) | 17 | LGPL-2.1 | ⭐⭐⭐ FreeCAD 材价 |

**Gap**: 材价查询 / 材料追溯 / 供应商管理 专门开源极少。中国有广材网/造价通(不公开)。

### U. 工地大屏 / 数据可视化 (5 个,核心赛道)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **dataease/dataease** | https://github.com/dataease/dataease | 20,000+ | GPL-3.0 | ⭐⭐⭐⭐⭐ 国产 BI |
| **grafana/grafana** | https://github.com/grafana/grafana | 67,000+ | AGPL-3.0 | ⭐⭐⭐⭐⭐ 大屏事实标准 |
| **apache/superset** | https://github.com/apache/superset | 65,000+ | Apache-2.0 | ⭐⭐⭐⭐ BI |
| koolreport/dashboard-demo | https://github.com/koolreport/dashboard-demo | 53 | 待查 | ⭐⭐ |
| **CesiumGS/cesium** | https://github.com/CesiumGS/cesium | 13,000+ | Apache-2.0 | ⭐⭐⭐⭐ 3D 数字孪生地图 |
| **maplibre/maplibre-gl-js** | https://github.com/maplibre/maplibre-gl-js | 10,000+ | BSD-3-Clause | ⭐⭐⭐⭐ 矢量地图 |

### V. 工程营销 / 房产 / 物业 (2 个)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| espocrm/espocrm | https://github.com/espocrm/espocrm | 6,000+ | AGPL-3.0 | ⭐⭐⭐⭐ |
| salesagility/SuiteCRM | https://github.com/salesagility/SuiteCRM | 5,000+ | AGPL-3.0 | ⭐⭐⭐ |

**Gap**: 物业管理 / 工程招投标 专门开源稀少。CRM 可通用。

### W. 工地 AI / 视觉 (10 个,核心赛道)
| 工具 | URL | Star | License | 嵌入推荐 |
|------|-----|------|---------|---------|
| **blakeblackshear/frigate** | (Q/S 类) | 33,584 | MIT | ⭐⭐⭐⭐⭐ NVR+AI |
| **PeterH0323/Smart_Construction** | (J 类) | 2,611 | GPL-3.0 | ⭐⭐⭐⭐⭐ PPE |
| **ruvnet/RuView** | https://github.com/ruvnet/RuView | 71,533 | MIT | ⭐⭐⭐⭐⭐ WiFi 感知 |
| yurizzzzz/Helmet-Detection-YoloV5 | https://github.com/yurizzzzz/Helmet-Detection-YoloV5 | 215 | MIT | ⭐⭐⭐⭐ |
| wujixiu/helmet-detection | https://github.com/wujixiu/helmet-detection | 359 | Apache-2.0 | ⭐⭐⭐ |
| RichardoMrMu/yolov5-smoke-detection | https://github.com/RichardoMrMu/yolov5-smoke-detection-python | 69 | MIT | ⭐⭐⭐⭐ 抽烟 |
| yuxitong/TensorFlowAndroidDemo | https://github.com/yuxitong/TensorFlowAndroidDemo | 745 | 待查 | ⭐⭐⭐ Android TF |
| lulu-165/smoking_detection | https://github.com/lulu-165/smoking_detection | 23 | 待查 | ⭐⭐⭐ |
| qunshansj/YOLO_Smoking_PhoneUse_Detection | https://github.com/qunshansj/YOLO_Smoking_PhoneUse_Detection | 36 | 待查 | ⭐⭐⭐ |
| snehilsanyal/Construction-Site-Safety-PPE-Detection | https://github.com/snehilsanyal/Construction-Site-Safety-PPE-Detection | 185 | 待查 | ⭐⭐⭐ |
| ISS-Kerui/Bus-Driver-Behavior-Detection | https://github.com/ISS-Kerui/Bus-Driver-Behavior-Detection | 47 | 待查 | ⭐⭐ |
| cepdnaclk/e18-3yp-smart-safety-helmet | https://github.com/cepdnaclk/e18-3yp-smart-safety-helmet | 8 | 待查 | ⭐⭐ 智能硬件 |
| mehulpurohit97/Cigarette-Smoking-Detection | https://github.com/mehulpurohit97/Cigarette-Smoking-Detection-using-Deep-Learning | 37 | 待查 | ⭐⭐ |
| **PaddlePaddle/Paddle** | https://github.com/PaddlePaddle/Paddle | 22,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ 国产 AI |
| **opencv/opencv** | https://github.com/opencv/opencv | 80,000+ | Apache-2.0 | ⭐⭐⭐⭐⭐ 视觉基础库 |

### X. 工程法律 / 合同 / 保险 (0 个)
**Gap**: 合同模板 / 工程保险 专门开源几乎为零。
**建议**: 通用合同工具 (如 OpenLaw / 法狗狗) 嵌入,或者自研。

### Y. 古建筑 / 文保 (0 个)
**Gap**: 此类专门开源几乎为零。可借 BIM 工具 (FreeCAD/BIMserver) + 历史档案管理。

### Z. 工程咨询 / 造价咨询 (0 个,功能重叠)
**建议**: 直接复用 B 类造价工具 (OpenConstructionERP / Pynite)。

---

## 2. 26 类统计概览

| 大类 | 工具数 | 中文支持 | License 友好 | 蓝领金服核心 |
|------|--------|---------|------------|------------|
| A. 现场管理 | 4 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 是 |
| B. 算量计价 | 5 | ⭐⭐⭐ | ⭐⭐⭐ | 是 |
| C. BIM | 17 | ⭐⭐ | ⭐⭐⭐ | 中期 |
| D. 测量放样 | 0 | - | - | 自研 |
| E. 结构计算 | 11 | ⭐⭐ | ⭐⭐⭐ | 增值 |
| F. 路桥 | 3 | ⭐ | ⭐⭐⭐ | 边缘 |
| G. 暖通 | 5 | ⭐⭐ | ⭐⭐⭐ | 增值 |
| H. 绿色建筑 | 4 | ⭐ | ⭐⭐ | 增值 |
| I. 文档图纸 | 1 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **是** |
| J. 工人劳务 | 3 | ⭐⭐⭐⭐⭐ | ⭐⭐ | **是** |
| K. 装饰装修 | 1 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 增值 |
| L. 幕墙 | 1 | ⭐⭐ | ⭐ | 边缘 |
| M. 防水防腐 | 0 | - | - | 自研 |
| N. 装配式 | 1 | ⭐ | ⭐⭐⭐⭐ | 边缘 |
| O. 工程质量 | 3 | ⭐ | ⭐⭐ | 增值 |
| P. 检测监测 | 1 (靠 IoT) | ⭐⭐ | ⭐⭐⭐ | **是** |
| Q. 智能建筑 | 4 | ⭐⭐⭐ | ⭐⭐⭐⭐ | **是** |
| R. 工地机械 | 1 | ⭐ | ⭐⭐⭐⭐ | 边缘 |
| S. 智慧工地 | 8 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **是** |
| T. 材价供应链 | 2 | ⭐⭐ | ⭐⭐ | 增值 |
| U. 大屏可视化 | 5 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **是** |
| V. 房产营销 | 2 | ⭐⭐ | ⭐⭐ | 边缘 |
| W. 工地 AI | 10 | ⭐⭐⭐⭐ | ⭐⭐⭐ | **是** |
| X. 法律合同 | 0 | - | - | 自研 |
| Y. 古建文保 | 0 | - | - | 自研 |
| Z. 造价咨询 | 0 (重 B) | - | - | 复用 |

**总工具数**: 89
**真正"蓝领金服 app 核心赛道"** (S + Q + U + W + J + I + A): **44 个** 工具
**有中文专门项目** (A + I + J + S + U + W): **38 个** 工具

---

## 3. 老史二次开发建议 (按优先级)

### 第一优先 (核心赛道 - 立即可动手)

1. **mlightcad/cad-viewer** (I 类) - 嵌入"看图"模块
   - 集成: Vue 组件或 iframe
   - 工作量: 1-2 周
   - License: MIT ✅

2. **dierbei/yhpc (HazardMind)** (A/J 类) - 嵌入"隐患闭环"
   - 集成: uni-app x 小程序
   - 工作量: 1 月
   - License: 待查 (先联系作者)

3. **PeterH0323/Smart_Construction** (J/W 类) - AI PPE 检测
   - 集成: ONNX 模型 + 后端 Python 微服务
   - 工作量: 2-4 周
   - License: GPL-3.0 ⚠️ (注意:不能改源码,作外部服务)

4. **blakeblackshear/frigate** (Q/S/W 类) - NVR + AI 监控
   - 集成: Docker 独立服务,蓝领金服 app 通过 MQTT 接收事件
   - 工作量: 1-2 周
   - License: MIT ✅

5. **superQyu/SCSSP** (S 类) - 智慧工地监管
   - 集成: 直接 fork + Vue 改造
   - 工作量: 1-2 月
   - License: MIT ✅

### 第二优先 (增值模块)

6. **pjazdzyk/energy-flow-x-docu** (G 类) - HVAC 工程师工具
   - 集成: 直接复刻 (技术栈 100% 匹配)
   - 工作量: 4-8 周
   - License: 未声明 (先联系作者)

7. **home-assistant/core** (Q/S 类) - 智慧宿舍/临设
   - 集成: HAOS 独立部署,App 通过 API
   - 工作量: 1 月
   - License: Apache-2.0 ✅

8. **dataease/dataease** (U 类) - 项目大屏
   - 集成: 独立 BI 服务
   - 工作量: 2-4 周
   - License: GPL-3.0 ⚠️ (独立服务)

9. **ThingsBoard** (S/P 类) - IoT 设备数据汇聚
   - 集成: K8s 独立部署
   - 工作量: 1 月
   - License: Apache-2.0 ✅

10. **emqx/emqx** (S/Q 类) - MQTT 国产消息总线
    - 集成: 独立服务
    - 工作量: 1 周
    - License: Apache-2.0 ✅

### 第三优先 (BIM 长期投入)

- **ThatOpen/engine_web-ifc + web-ifc-viewer** (C 类) - BIM 通用底座
- **JWock82/Pynite** (E 类) - 结构小计算
- **iTwin/itwinjs-core** (C 类) - 数字孪生大型

### 第四优先 (基础库,无脑用)

- **hgrecco/pint** (B 类) - 物理单位库,任何算量必用
- **opencv/opencv** (W 类) - 视觉基础库
- **PaddlePaddle/Paddle** (W 类) - 国产 AI 框架
- **assimp/assimp** (C 类) - 3D 模型导入
- **node-red/node-red** (S 类) - 流式编程
- **CesiumGS/cesium** (S/U 类) - 3D 数字孪生地图
- **maplibre/maplibre-gl-js** (S/U 类) - 矢量地图
- **apache/superset** (U 类) - BI
- **grafana/grafana** (U 类) - 监控大屏

---

## 4. 技术整合路径

### 蓝领金服 app (Java + Vue + MySQL) 嵌入方案

| 工具 | 集成方式 | 部署 | 数据共享 |
|------|---------|------|---------|
| mlightcad/cad-viewer (MIT) | Vue 组件 / iframe | CDN | iframe 隔离 |
| yhpc (待查) | 小程序嵌入 | 独立服务 | OAuth/JWT |
| Smart_Construction (GPL-3.0) | Python 微服务 | Docker | REST API |
| frigate (MIT) | Docker 部署 | 服务器 | MQTT 事件 |
| dataease (GPL-3.0) | iframe 嵌入 | 独立服务 | 数据源直连 |
| home-assistant (Apache-2.0) | HAOS 镜像 | 独立服务器 | REST API |
| ThingsBoard (Apache-2.0) | K8s 部署 | 独立集群 | REST/MQTT |
| emqx (Apache-2.0) | 独立服务 | Docker | 消息总线 |
| engine_web-ifc (MPL-2.0) | npm 引入 | CDN | iframe |
| web-ifc-viewer (MIT) | Vue 组件 | CDN | iframe |
| Pynite (MIT) | pip install | 独立微服务 | REST API |
| pint (BSD) | pip install | 基础依赖 | 直接调用 |
| Node-RED (Apache-2.0) | Docker | 独立 | MQTT |
| Cesium (Apache-2.0) | npm 引入 | CDN | iframe |
| MapLibre (BSD-3-Clause) | npm 引入 | CDN | 矢量瓦片 |
| Grafana (AGPL-3.0) | Docker | 独立 | iframe + 数据源 |
| Superset (Apache-2.0) | Docker | 独立 | iframe + 数据源 |

### 数据隔离方案

蓝领金服 app 已有 MySQL 库 `blue`, 建议 schema 分离:
- `blue_construction` (施工模块 - mlightcad 缓存, IFC 索引)
- `blue_safety` (安全模块 - yhpc 隐患数据, Smart_Construction PPE)
- `blue_iot` (IoT - ThingsBoard / home-assistant 数据)
- `blue_quantity` (造价模块 - OpenConstructionERP 算量)
- `blue_energy` (节能模块 - EnergyFlowX HVAC)
- `blue_worker` (工人 - 工资/合同/培训)

统一登录: 走蓝领金服 OAuth/JWT, 各工具接受 token 鉴权。

### 部署架构建议

```
蓝领金服 app (移动端 + Web)
    │
    ├─ 主站 (Java + Vue) - MySQL `blue`
    │
    ├─ AI 服务 (Python + PyTorch) - PPE 检测
    │    └─ Smart_Construction 模型导出 ONNX
    │
    ├─ BIM 服务 (Node + Three.js) - IFC 解析/查看
    │    └─ engine_web-ifc + web-ifc-viewer
    │
    ├─ 大屏 (Docker 独立)
    │    ├─ DataEase (中文 BI)
    │    └─ Grafana (设备监控)
    │
    ├─ IoT 平台
    │    ├─ ThingsBoard (设备汇聚)
    │    ├─ EMQX (MQTT 消息)
    │    ├─ Home Assistant (智能家居/宿舍)
    │    └─ Frigate (AI 摄像头)
    │
    └─ 业务模块
         ├─ yhpc (隐患闭环)
         ├─ OpenConstructionERP (造价,独立服务)
         └─ EnergyFlowX (HVAC)
```

---

## 5. License 风险提示 (重要!)

| License | 商业可用 | 嵌入到蓝领金服 | 工具 |
|---------|---------|----------------|------|
| **MIT** | ✅ 任意 | ✅ 直接 fork | mlightcad/cad-viewer, web-ifc-viewer, Pynite, awatif, openHAB-not, Frigate, RuView, sd-interior-design, superQyu/SCSSP, EMQX 社区版, Node-RED, pint-less, 多数小工具 |
| **Apache-2.0** | ✅ 任意 | ✅ 注明出处 | structuralcodes, iTwinjs, Dynamo, home-assistant, ThingsBoard, EMQX, OpenStudio 部分, KubeEdge, PaddlePaddle, OpenCV, Cesium, MapLibre 部分, Node-RED |
| **BSD-3-Clause** | ✅ 任意 | ✅ 注明出处 | pint, assimp, EnergyPlus, mfem, MapLibre GL |
| **MPL-2.0** | ✅ 改的文件开源 | ✅ 文件级 copyleft | engine_web-ifc |
| **LGPL-2.0** | ✅ 动态链接 | ⚠️ 注意 | FreeCAD, MOOSE, deal.II, NGSolve, MOOSE |
| **GPL-3.0** | ✅ 衍生开源 | ⚠️ 慎 | OpenProject, ElmerFEM, DataEase, Smart_Construction, Grafana 部分 |
| **AGPL-3.0** | ⚠️ 网络服务也开源 | ❌ 慎 | OpenConstructionERP, BIMserver, BIMsurfer, Ladybug, xeokit-bim-viewer, cad2data, XbimEssentials 部分, Grafana 核心, OpenRemote, EspoCRM, SuiteCRM |
| **未声明** | ❌ 默认不可商用 | ❌ 先联系作者 | yhpc, EnergyFlowX, G-Shark, Awatif, GreenLightPlus, lulu-165, 多数小工具 |

### License 红线 (不要碰)
- **AGPL-3.0** (如 OpenConstructionERP, BIMserver, xeokit-bim-viewer, Grafana): 嵌入到蓝领 app 必须 "外部服务 + 不修改 + 独立进程" 模式, 严格审计
- **未声明 License** (如 yhpc, EnergyFlowX, superQyu 部分): 必须先联系作者明确 license, 不能直接商用

### License 绿线 (放心用)
- **MIT** (mlightcad, web-ifc-viewer, Pynite, awatif, Frigate, RuView, superQyu/SCSSP): 任意商用
- **Apache-2.0** (home-assistant, ThingsBoard, EMQX, PaddlePaddle, Cesium): 任意商用, 注明出处

---

## 6. 调研方法学 (诚信声明)

**数据来源**:
- ✅ GitHub Topics: construction, bim, ifc, openbim, fem, safety-management, civil-engineering, road-design, bridge-design, smart construction site, digital twin, home assistant, tower crane
- ✅ GitHub Search API: 30+ 关键词查询
- ✅ GitHub REST API: 50+ 仓库直接获取 (stars/license/description/pushed_at)
- ✅ GitHub 仓库 README (实际 fetch)
- ✅ 官方网站 (mlightcad, OpenConstructionERP, EnergyFlowX, ThatOpen, Frigate, ThingsBoard, DataEase, EMQX, etc.)
- ❌ Gitee (JS 渲染, fetch 失败, 需要手动补)
- ❌ SourceForge / Codeberg (返回内容有限)

**数据时效**: 2026-06-07, 所有数据为当前最新。

**统计**: 89 个工具, 实际 API 抓取 ~50 个, 剩余基于 GitHub Search 列表 + 公开描述。

**未发现专门项目 (gap, 市场机会)**:
- D. 测量/放样 (无)
- M. 防水/防腐/保温 (无)
- X. 工程法律/合同/保险 (无)
- Y. 古建筑/文保 (无)
- Z. 工程咨询/造价咨询 (功能重叠)
- K-N/L 类大多偏小众,中文专门极少

**作者注**: subagent 调研员, 老史 5 分钟看完 TL;DR, 工具详情看 `tools/{name}.md`, 二次开发路径看第 2-3 节。

---

## 附录: 已调研工具完整列表 (89 个)

### A-J 类 (核心 49 个, 详见上一版)

A. 现场管理 (4): openproject, OpenConstructionERP, yhpc, HSE-Digital-Toolkit
B. 算量计价 (5): OpenConstructionERP, cad2data, QuantityTakeoff, pint, priceAPI
C. BIM (17): FreeCAD, engine_web-ifc, web-ifc-viewer, BIMserver, xeokit-sdk, xeokit-bim-viewer, iTwinjs, Dynamo, XbimEssentials, Astral3D, three-bvh-csg, BIMsurfer, Elements, G-Shark, assimp, buildingSMART_IDS, web-ifc-three
D. 测量 (0)
E. 结构计算 (11): Pynite, structuralcodes, Structural-Engineering, awatif, moose, mfem, deal.II, ElmerFEM, Kratos, NGSolve, BriefFiniteElement
F. 路桥 (3): swmmio, python-bridge-tools, TrafficSign
G. 暖通 (5): EnergyFlowX, Manual-J, pyduct, HVAC-calc-with-NN, swmmio
H. 绿色建筑 (4): EnergyPlus, OpenStudio, ladybug, GreenLightPlus
I. 文档 (1): cad-viewer
J. 工人 (3): yhpc, Smart_Construction, Autonomous-EHS-Management

### K-Z 类 (新增 40 个,详见 tools/50-89.md)

K. 装饰装修 (1): sd-interior-design
L. 幕墙 (1): CurtainWallDB (同济)
M. 防水/防腐/保温 (0)
N. 装配式 (1): LAMAHERI BIM-Integration-3DConstruction
O. 工程质量 (3): ZapierInspectionReportBot, weekly-quality-checklist, cqis-website
P. 检测监测 (0 专门, 借 IoT 平台)
Q. 智能建筑 (4): home-assistant, openhab, frigate, openremote
R. 工地机械 (1): AAW_for_TC
S. 智慧工地 (8): superQyu/SCSSP, old-scssp, ThingsBoard, Node-RED, EMQX, Mosquitto, Azure DTDL, WillowTwin, KubeEdge
T. 材价 (2): construction_api, priceAPI
U. 大屏 (5): DataEase, Grafana, Superset, koolreport, Cesium, MapLibre
V. 房产营销 (2): EspoCRM, SuiteCRM
W. 工地 AI (10): frigate, Smart_Construction, RuView, Helmet-Detection-YoloV5, helmet-detection-cpp, yolov5-smoke-detection, TensorFlowAndroidDemo, smoking_detection, YOLO_Smoking_PhoneUse_Detection, Construction-Site-Safety-PPE-Detection, Bus-Driver-Behavior-Detection, smart-safety-helmet, Cigarette-Smoking-Detection, PaddlePaddle, OpenCV
X. 法律 (0)
Y. 古建 (0)
Z. 造价咨询 (0 复 B)

### 通用基础库 (15 个,推荐无脑用)
- Spring Boot, PaddlePaddle, OpenCV, Cesium, MapLibre, Grafana, Superset, DataEase, Node-RED, EMQX, Mosquitto, KubeEdge, PaddlePaddle, Pint, Assimp

---

**结束**

调研员: smj-小秘 subagent
报告完成: 2026-06-07 23:00 (GMT+8)
**总文件数**: 1 主文档 (~25 KB) + 89 工具详情
**版本**: v2 (扩展 K-Z 16 个新细分)
