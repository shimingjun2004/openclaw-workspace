# Hermes Agent PVE 虚拟机部署方案

> 编制日期：2026-04-19
> 负责人：smj-小秘
> 状态：研究完毕，待实施
> 目标主机：老史 PVE 软路由虚拟机

---

## 一、官方要求 vs 实际规划

| 项目 | 官方最低要求 | 咱们规划 |
|------|------------|---------|
| 内存 | 8GB+ | **12GB**（给VM充足） |
| 磁盘 | 2GB+ | **60GB**（SSD） |
| 系统 | Linux/macOS/WSL2 | **Ubuntu 22.04 Server** |
| 网络 | 能访问GitHub | PVE宿主机已有科学上网 |
| Python | 3.11（自动安装）| 自动 |
| Node.js | v22（自动安装）| 自动 |

---

## 二、安装方式：一键脚本（最简）

官方单行安装命令：
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

安装脚本自动处理：
- 安装 `uv`（Python包管理器）
- 下载 Python 3.11（如未安装）
- 安装 Node.js v22
- 安装 ripgrep（文件搜索）
- 安装 ffmpeg（音视频）
- 克隆仓库到 `~/.hermes/hermes-agent`
- 创建虚拟环境
- 注册 `hermes` 全局命令

---

## 三、部署流程（我远程操作）

### 第一步：创建 VM（你来创建，我来操作）

**VM 配置建议：**
- 类型：Virtual Machine
- OS：Ubuntu 22.04 Server LTS（下载ISO）
- 内存：12GB
- CPU：4核
- 磁盘：60GB（SSD）
- 网络：桥接模式（和宿主机同网段，重要！）
- 安装方式：挂载ISO → 手动装系统（跟普通装Ubuntu一样）

**装系统时注意：**
- 用户名：`hermes`（建议，不是必须）
- 开启 SSH 服务（`sudo apt install openssh-server`）
- 防火墙：允许 22 端口

### 第二步：我远程连接配置

VM 起来后，告诉我：
- VM 的 IP 地址
- 登录用户名 + 密码

然后我连接上去，按顺序执行：

```bash
# 1. 先确保网络通（科学上网）
export https_proxy=http://你的代理:端口
export http_proxy=http://你的代理:端口

# 2. 安装 Hermes Agent
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 3. 重新加载shell
source ~/.bashrc

# 4. 配置模型后端
hermes model
# （这里选择用哪个LLM，我会指导老史配置API Key）
```

---

## 四、模型后端选择（重要）

Hermes 支持很多模型，按国内可用的优先排序：

| 优先级 | 模型 | 说明 |
|--------|------|------|
| ⭐⭐⭐ | **MiniMax** | 老史已有 MiniMax API Key，直接可用 |
| ⭐⭐⭐ | **OpenRouter** | 200+模型，但同样需要代理 |
| ⭐⭐ | **Kimi/Moonshot** | 国内可访问，Kimi API |
| ⭐⭐ | **GLM/Zhipu** | 国内可访问 |
| ⭐ | **Anthropic Claude** | 需要代理 |

**建议：** 先用 MiniMax（已有 Key，直接用），后续可切换。

---

## 五、已知坑点（提前标记）

### 坑1：GitHub访问（最大问题）⚠️
**问题：** 安装脚本需要从 GitHub 拉代码，国内可能超时/失败
**解决：** 需要在 VM 里配置代理（和老史 PVE 宿主机一样的方式）
**操作：** 安装前先设置 `https_proxy` + `http_proxy`

### 坑2：GitHub 代理白名单（重要）
**需要的白名单：**
- `github.com`
- `raw.githubusercontent.com`
- `objects.githubusercontent.com`

### 坑3：安装后找不到命令
**问题：** 安装成功但输入 `hermes` 报 command not found
**原因：** PATH 未刷新
**解决：** `source ~/.bashrc` 或重新打开终端

### 坑4：Python 路径问题
**解决：** 绝对不要手动 `sudo apt install python3.11`，用 uv 自动安装的即可

### 坑5：60%记忆捕获率
**说明：** Episodic Memory 有40%内容会丢失，高风险任务不要依赖它

### 坑6：Windows不支持
**说明：** 不支持原生 Windows，必须用 WSL2 或 Linux VM

---

## 六、我（smj-小秘）和 Hermes 的协作模式

```
老史 → 给我任务（研究/分析/判断）
         ↓
  我思考方案，制定计划
         ↓
  Hermes Agent 执行（部署/写代码/操作）
         ↓
  我持续跟踪结果，反馈老史
```

**分工：**
- 我（smj-小秘）= 指挥塔 + 研究员 + 分析师
- Hermes = 执行者 + 程序员 + 运维

**老史不需要同时管两个，直接找我即可。**

---

## 七、待老史确认的信息

| 项目 | 需要确认 |
|------|---------|
| VM 的 IP | 安装好Ubuntu后告诉我 |
| SSH 用户密码 | 安装时设的用户名密码 |
| 代理信息 | PVE 宿主机的代理地址+端口（用于VM科学上网） |
| 模型 API Key | 如果用 MiniMax，直接用已有的 Key |

---

## 八、安装检查清单（我来执行）

```
VM 创建
  ↓
网络配置 + 代理
  ↓
SSH 连接验证
  ↓
安装 hermes-agent（一键脚本）
  ↓
配置 LLM 后端（hermes model）
  ↓
测试运行（hermes --tui）
  ↓
配置我和 Hermes 的协作方式
```

---

## 九、最终目标状态

部署完成后：

1. **Hermes Agent** 在 VM 里跑着，7×24 小时运行
2. **老史通过 Telegram/Discord/或CLI** 向 Hermes 发任务
3. **我（smj-小秘）** 负责给 Hermes 分派任务、跟踪结果、分析问题
4. **老史** 只需要跟我说"帮我部署XX"，我来协调 Hermes 干活

---

*本方案由 smj-小秘 研究编制，等老史提供 VM IP 后即可开始部署*
