# Auto_Claude_CLI 🤖👐

### The True hands-free Software Development
**从想法到交付，只需一个脚本。体验真正的“解放双手”。**

> **Liberate your hands.** Experience true hands-free software development.
>
> Auto_Claude_CLI 是一个由单脚本驱动的 **轻量化** 软件工厂。它指挥一个虚拟 AI Agent 团队（产品经理、架构师、开发、测试），在你睡觉时将原始想法转化为功能完整、重构过且测试通过的代码库。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude CLI](https://img.shields.io/badge/Driver-Claude%20CLI-purple)](https://anthropic.com)

---

## 💸 节约成本 & 支持Me
**全自动运行成本,一天不到5角钱**

拒绝高昂的编程费用。强烈推荐结合 GLM-Coding 模型使用 Claude CLI，以获得最佳性价比。

> [**👉 试用 GLM-Coding (高性能，低成本)**](https://www.bigmodel.cn/glm-coding?ic=ODKVSPWHNC)
>
> *通过此链接注册可大幅降低您的 API 成本，并直接支持我的开源工作！*

---

## ⚡ 快速开始 (Quick Start)

10秒内启动。无需复杂的环境配置。

### 1. 前置要求：Claude CLI
安装底层驱动（需要 Node.js 环境）。

```bash
npm install -g @anthropic-ai/claude-code
```
选项 A (推荐): 获取 GLM-Coding Key ( < 0.5元 /天，高性价比)

选项 B: 使用官方 Anthropic Key (100元/月)

### 2. 安装 auto_claude_cli
零依赖逻辑，极简 Python 需求。

```Bash
git clone https://github.com/vincentzzh424/auto_claude_cli.git
cd auto_claude_cli
# (可选) 创建一个演示目录以保持整洁
mkdir demo && cd demo 
```


### 3. 让想法变为现实

```Bash
# 在上级目录运行脚本（或将其加入环境变量），附带你的想法。

python ../run.py "创建一个带有暗黑模式切换功能的个人主页"
```

### 💡 4. 使用示例 (Examples)

简单工具

```Bash
python ../run.py "写一个 CLI 工具，批量调整文件夹内图片的大小并添加水印"
复杂系统 提示：在粘贴前，先用 ChatGPT/Gemini 将你的提示词优化为详细的规格说明，效果更佳。
```

```Bash
python ../run.py "构建一个类似彭博终端的加密货币交易系统。功能要求：对接 BTC/ETH 的 WebSocket 数据源，使用 mplfinance 实现实时 K 线可视化，并计算 MACD/RSI 指标。不要使用 Mock 数据。"
```
[复杂商城案例](example/shopping_system.md)


### ⚠️ 安全警告 (Safety Warning)
使用前请务必阅读

为了实现真正的“全自动”编程，本工具在执行 Claude CLI 时默认开启了 --dangerously-skip-permissions 标志。

风险：Agent 拥有完整的文件系统权限（读/写/删除）。

建议：请务必在 沙箱、Docker 容器 或 独立的空目录 中运行此工具，以防数据意外丢失。

### 🤝 贡献 (Contributing)
我们相信自主 Agent 的力量。欢迎提交 PR 改进驱动逻辑或提示词工程。

📄 许可证 (License)
MIT © [vincentzzh424]
