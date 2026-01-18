# Auto_Claude_CLI 🤖👐

### The Zero-Intervention Software Factory
**从想法到交付，只需一个脚本。体验真正的“解放双手”。**

> **Liberate your hands.** Experience true hands-free software development.
> Auto_Claude_CLI is a **headless** software factory powered by a single script. It orchestrates a virtual team of AI agents (PM, Architect, Developer, QA) to transform raw ideas into fully functional, refactored, and tested codebases while you sleep.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude CLI](https://img.shields.io/badge/Driver-Claude%20CLI-purple)](https://anthropic.com)

---

## 💸 Cost-Efficiency & SupportMe
**Run full autonomous cycles for < $0.10 / day.**

Don't overpay for coding. I highly recommend using the GLM-Coding model with Claude CLI for the best cost-to-performance ratio.

> [**👉 Try GLM-Coding (High Performance, Low Cost)**](https://www.bigmodel.cn/glm-coding?ic=ODKVSPWHNC)
>
> *Signing up via this link reduces your API costs and directly supports my open-source work!*

---

## ⚡ Quick Start

Get up and running in 10 seconds. No complex environment setup required.

### 1. Prerequisite: Claude CLI
Install the underlying driver (Node.js required).

```bash
npm install -g @anthropic-ai/claude-code
```

Option A (Recommended): [**Get GLM-Coding Key (~$0.1/day)**](https://www.bigmodel.cn/glm-coding?ic=ODKVSPWHNC)

Option B: Use Official Anthropic Key ($20/month)

### 2. Init Auto_Claude_CLI
Dependency-free , minimal python requirements.

```Bash
git clone https://github.com/vincentzzh424/auto_claude_cli.git
cd auto_claude_cli
# (Optional) Create a workspace to keep things clean
mkdir demo && cd demo 
```

### 3. Make Your Idea Come True
```Bash
# Run the script from the parent directory (or add to path) with your idea.
python ../run.py "Create a Personal Website with a dark mode toggle"
💡 Usage Examples
```

### 💡4. Simple Utility

```Bash
python ../run.py "Create a CLI tool to resize and watermark images in a folder"
```

💡Complex System Tip: Use ChatGPT/Gemini to refine your prompt into a detailed specification before pasting it here.

```Bash
python ../run.py "Build a Bloomberg-like terminal for crypto trading. Features: WebSocket data feed for BTC/ETH, real-time K-line visualization using mplfinance, and MACD/RSI indicator calculation. No mock data."
```

[Shopping System Example](example/shopping_system.md)

---

### ⚠️ Safety Warning
Please Read Before Use

To achieve true "hands-free" autonomy, this tool executes the Claude CLI with the --dangerously-skip-permissions flag enabled.

Risk: The agent has full filesystem access (read/write/delete).

Recommendation: Always run this tool inside a Sandbox, Docker container, or a dedicated empty directory to prevent accidental data loss.

### 🤝 Contributing
We believe in the power of autonomous agents. Pull Requests to improve the driver logic or prompt engineering are welcome.

📄 License
MIT © [vincentzzh424]