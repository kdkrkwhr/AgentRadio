<p align="center">
  <img src="main.png" alt="AgentRadio — 多智能体协作的被动感知" width="100%">
</p>

<h1 align="center">📻 AgentRadio</h1>

<h3 align="center">面向长周期多智能体协作的被动感知——四个编程智能体<b>一边工作一边倾听</b></h3>

<p align="center">
  <a href="https://arxiv.org/abs/2607.28430"><img src="https://img.shields.io/badge/论文-arXiv-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="论文"></a>
  <a href="https://github.com/Coral-Protocol/AgentRadio"><img src="https://img.shields.io/badge/代码-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/许可证-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="许可证：Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://github.com/scaleapi/SWE-Atlas"><img src="https://img.shields.io/badge/基准-SWE--Atlas_QnA-0E9B9B?style=for-the-badge&logo=github&logoColor=white" alt="基准"></a>
  <a href="https://github.com/laude-institute/harbor"><img src="https://img.shields.io/badge/编排-Harbor-4B32C3?style=for-the-badge&logo=github&logoColor=white" alt="Harbor"></a>
  <a href="https://modal.com"><img src="https://img.shields.io/badge/算力-Modal-7FEE64?style=for-the-badge&logo=modal&logoColor=black" alt="Modal"></a>
</p>

<p align="center">
  <a href="https://discord.gg/GSHKNXF8U"><img src="https://img.shields.io/badge/Discord-加入-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/Coral-Protocol"><img src="https://img.shields.io/badge/Coral_Protocol-组织-FF5C8A?style=for-the-badge&logo=github&logoColor=white" alt="Coral Protocol"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <b>简体中文</b> |
  <a href="README.es.md">Español</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ar.md">العربية</a>
</p>

<p align="center">
  <i>给四个编程智能体一条共享的无线电频道。它们分工、协商方案，并在<b>工作的同时</b>不断
  播报新发现——因为「倾听」作为后台任务运行，不再占用一次行动机会。</i>
</p>

本仓库包含复现论文 *AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration*
（[arXiv:2607.28430](https://arxiv.org/abs/2607.28430)）实验所需的代码与数据。

### 🏆 一套协议，四个智能体——比单智能体高出 29.8 个百分点

| 配置 | 新增的能力 | 任务准确率（Opus 4.6） | 任务准确率（DeepSeek V4 Pro） |
|---|---|:---:|:---:|
| **B0** 单智能体 | — | 32.3 % | 29.0 % |
| **B1** 六次单智能体运行取最优 | 6 倍预算，无协作 | 37.9 % | 31.4 % |
| **L1** 四智能体 + 分工 | 分工 | 39.5 % | 31.4 % |
| **L2** + 协商 | 联合规划 + 交叉评审（阻塞式接收） | 51.6 % | 39.5 % |
| **L3** + 被动感知（**AgentRadio**） | 后台 `wait_for_mention` | **62.1 %** | **50.8 %** |

从 L2 到 L3 **只**改变了通信方式。在 Opus 4.6 上它赢 15 题、输 2 题（精确 McNemar 检验，
p = 0.0023）；在 DeepSeek 上赢 17 题、输 3 题（p = 0.0026）。四个 Opus 4.6 智能体在
AgentRadio 下达到 62.1 %，超过了最强的单智能体榜单成绩——使用更新的 Opus 4.8 的
Claude Code（57.2 %）。

→ [查看完整结果](#-完整结果) · [论文](https://arxiv.org/abs/2607.28430) · [自己动手复现](#-运行四种配置)

## 📣 最新动态

- **2026-08** — AgentRadio 被美国主流科技媒体 [VentureBeat](https://venturebeat.com/) 报道：[《四个 AI 智能体实时协作，在企业级编程任务上超越 Claude Opus 4.8》](https://venturebeat.com/orchestration/four-ai-agents-coordinating-in-real-time-outperformed-claude-opus-4-8-on-enterprise-coding-tasks)。📰
- **2026-07** — AgentRadio 论文发布于 [arXiv](https://arxiv.org/abs/2607.28430)。🎉
- **2026-07** — 代码、适配器以及完整的 124 个 SWE-Atlas QnA 任务配置全部开源。🚀

## 💡 为什么选择 AgentRadio

* **通信不再消耗工作步骤** — `wait_for_mention` 作为 harness 的*后台任务*运行，队友的消息
  会在下一个步骤边界自然浮现，而不是占用一次行动。智能体不必再在「工作」和「倾听」之间二选一。
* **执行中途即可纠偏** — 在阻塞式系统里，一个发现要等到下一个阶段边界才能传达给队友。
  在被动感知下它立刻送达，队友可以把它折叠进正在进行的任务里。
* **无需修改 harness** — harness 只需要能在后台运行一条 shell 命令，主流编程 harness 本就
  具备该能力。AgentRadio 由一个独立的消息服务器加三个轻量 shell 脚本构成。
* **不增加 LLM 调用** — 监听进程是普通的操作系统进程，而非一次智能体步骤。智能体新增的
  token 开销只有真正浮现出来的那些消息。
* **与模型无关** — 同一套协议、提示词和启动脚本既能跑在 Claude Opus 4.6 上，也能通过
  LiteLLM 转译代理跑在 DeepSeek-V4-Pro 上。
* **干净的消融阶梯** — B0 → L1 → L2 → L3 在完全相同的 harness 设置下，逐层隔离出分工、
  协商与被动感知各自的贡献。

## 🧩 工作原理

### 三个通信原语

AgentRadio 向每个智能体暴露三个操作：

| 原语 | 行为 |
|---|---|
| `create_thread(name, participants)` | 在消息服务器上开启一个具名会话线程，并返回其标识符。 |
| `send_message(thread, content, mentions)` | 向线程追加一条消息并立即返回，无论此刻是否有人在听。消息可以 @ 提及特定智能体。 |
| `wait_for_mention(timeout)` | 阻塞直到出现一条提及调用者的消息，然后连同所有线程的完整快照一并返回——因此调用者无需二次读取即可重建上下文。 |

这一层本身不规定智能体*何时*倾听。`wait_for_mention` 在哪里运行，是区分两种通信模式的
唯一自由度：

- **前台运行** → *阻塞式接收*。智能体必须停下工作才能倾听，每听到一条消息就要付出一个
  工作步骤的代价。这就是 L2 基线。
- **后台任务** → *被动感知*。智能体持续工作，任何提及都会在下一个步骤边界浮现，不占用
  任何倾听步骤。这就是 L3，即完整的 AgentRadio。

其余一切——原语、线程、协议——全部保持不变。实验隔离出来的正是这一「一比特」的差异。

### 五阶段协议

四个智能体运行一套固定的分工与协商协议。Agent-1 同时担任**汇总者**：由它开启规划线程、
工作日志线程与最终答案线程，并把守每一次阶段切换——只有在收集到每个智能体的明确批准后，
当前阶段才会结束。

1. **P1 · 探索** — 每个智能体启动自己的后台监听器，独立探索代码仓库，并起草它所看到的
   子问题。此阶段不发送任何消息。
2. **P2 · 分工** — 汇总者开启规划线程。各智能体汇集各自的发现，协商子问题的划分方案，
   反复修订直到所有智能体一致批准。
3. **P3 · 执行** — 每个智能体处理自己负责的子问题。一旦有新发现就立即发到工作日志：
   与队友相关的发现、与既定方案相矛盾之处、遇到的障碍，或已放弃的死胡同。
4. **P4 · 评审** — 每个智能体在自己的结果线程中广播其发现与证据。评审者指出事实冲突、
   证据不足之处以及未被提及的观察，并可以把某个子问题打回 P3。
5. **P5 · 提交** — 汇总者根据已批准的结果撰写最终答案，广播草稿进行最后一轮批准，然后提交。

在阻塞式接收下，同样的五个阶段照常运行，但 P3 的实时共享消失了：听消息要付出前台等待
的代价，于是智能体在工作时保持沉默，一个发现在 P4 之前无法传达给队友。

## 🗂️ 仓库结构

```
data/qa/                          124 SWE-Atlas QnA tasks (harbor dataset scale-ai/swe-atlas-qna)
multi_agent/
  coral_multi_agent.py            L2 adapter: division + negotiation (blocking receive)
  coral_multi_agent_ablation.py   L1 adapter: division only
  coral_multi_agent_passive.py    L3 adapter: full AgentRadio (passive awareness)
  startup.sh / startup_ablation.sh / startup_passive.sh
                                  per-agent bootstrap + protocol prompts (CLAUDE.md)
  coral-agent*.toml               message-server agent definitions
  passive_scripts/                MCP-over-HTTP shell primitives (create_thread /
                                  send_message / wait_for_mention / read_resource)
  coral-server.jar                message server (download from Releases, see below)
  monitor_coral_log.sh            live thread/message monitor for running containers
run_config/qa/
  claude-token                    OAuth token helper
  full_run.sh                     B0 baseline batch runner (all 124 tasks)
  run_passive_multi_agent.sh      L3 batch runner
verify_local.py                   rubric verifier (LLM judge), run locally on a trial dir
```

`data/qa/` 下的每个任务目录都包含任务说明、已固定的执行环境，以及验证器所使用的评分细则集。

---

## 📦 环境准备

所有运行都在 [Modal](https://modal.com) 上的 Docker 容器中执行，由
[Harbor](https://github.com/laude-institute/harbor) 编排。一个任务 = 一个容器，其中运行
消息服务器加四个 Claude Code 智能体。

### 1. Docker Desktop

从 https://www.docker.com/products/docker-desktop/ 安装，并用 `docker run hello-world` 验证。

### 2. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Harbor（锁定 0.6.4）

较新的 Harbor 版本（0.7+）存在破坏性 API 变更，会导致这些适配器失败。请锁定版本：

| 组件 | 可用版本 |
|-----------|-----------------|
| harbor | **0.6.4** |
| modal | **1.4.2** |

```bash
uv tool uninstall harbor 2>/dev/null || true
uv tool install 'harbor[modal]==0.6.4'
harbor --version   # must show 0.6.4
```

### 4. Modal

```bash
pip install 'modal==1.4.2'
modal --version    # must show 1.4.2
modal setup        # opens browser to log in
```

### 5. Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | sh
claude --version
```

智能体需要 **Claude Max 订阅**。验证器还额外需要一个 **Anthropic API key**。

### 6. 消息服务器 JAR

这个 106 MB 的服务器 JAR 以匿名化产物的形式托管（体积过大，无法作为 git blob 存放）。
`confirm=t` 参数用于跳过大文件扫描的中间页，让 `curl` 直接拿到二进制文件：

```bash
curl -L -o multi_agent/coral-server.jar \
  "https://drive.usercontent.google.com/download?id=17b40_1kXFrAC0pnN8w_7PPY13O7pYVke&export=download&confirm=t"
```

适配器会把这个 JAR 上传进每个任务容器。本地无需运行任何东西，因此不需要本地 JDK。

### 7. Token 助手与 .env

```bash
cp run_config/qa/claude-token ~/.local/bin/claude-token
chmod +x ~/.local/bin/claude-token
cp .env.example .env      # then fill in your Anthropic API key
```

### 每次运行前：刷新 OAuth token

Claude Code 的 OAuth token 会轮换。每个容器在启动时只拿到一份静态快照，过期的 token 会让
四个智能体在运行中途全部因 401 而中止。请在每次会话前刷新：

```bash
claude /login    # opens browser

security find-generic-password -s "Claude Code-credentials" -w | python3 -c "
import json, sys, os
data = json.loads(sys.stdin.read())
oauth = data.get('claudeAiOauth', {})
with open(os.path.expanduser('~/.claude/.credentials.json'), 'w') as f:
    json.dump({'claudeAiOauth': oauth}, f, indent=2)
print(f'Token refreshed. Expires at: {oauth.get(\"expiresAt\")}')
"

~/.local/bin/claude-token --check
source .env
```

---

## ⚡ 运行四种配置

所有命令都在仓库根目录、执行 `source .env` 之后运行。任务 ID 就是 `data/qa/` 下的目录名
（重复 `-i` 可批量指定；完全去掉 `-i` 则运行全部 124 个任务）。`-n` 是并发任务数
（对 L1–L3 而言，一个任务 = 四个智能体）。

### B0 —— 单智能体（基线）

```bash
source .env

harbor run \
  -p ./data/qa \
  -a claude-code \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "baseline-ba998" \
  -y
```

### L1 —— 四智能体 + 分工

Agent-1 简单探索后对问题进行划分，各智能体独立解决自己的那份，答案直接合并，不做评审。

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_ablation:CoralMultiAgentAblation' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "division-ba998" \
  -y
```

### L2 —— + 协商（阻塞式接收）

完整的五阶段协议——联合探索、协商到全体一致的任务划分、实时执行、交叉评审、汇总提交——
但 `wait_for_mention` 运行在**前台**，因此智能体必须停下工作才能倾听。

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent:CoralMultiAgent' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "divneg-ba998" \
  -y
```

### L3 —— + 被动感知（完整 AgentRadio）

协议完全相同，但 `wait_for_mention` 作为**后台任务**运行：智能体持续工作，消息在步骤之间
浮现。Claude Code 不配置任何 MCP——所有通信都通过 `passive_scripts/` 里的轻量 shell 封装完成。

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_passive:CoralMultiAgentPassive' \
  -m "anthropic/claude-opus-4-6" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "passive-ba998" \
  -y
```

`run_config/qa/run_passive_multi_agent.sh` 把同样的命令封装成批量运行脚本，每个任务 ID
对应一个 harbor job。

---

## 🔀 使用 DeepSeek-V4-Pro 运行

多智能体配置（L1–L3）可以用 **DeepSeek-V4-Pro** 智能体替代 Opus 4.6 来运行，从而复现结果
表中的 DeepSeek 一列。协议、提示词、启动脚本和续跑保护全部相同，只有 LLM 后端发生变化。

Claude Code 只讲 Anthropic Messages API，而 DeepSeek 通过 OpenRouter 提供服务（仅兼容
OpenAI 接口）。我们用一个**部署在 Modal 上的 LiteLLM 转译代理**来打通两者。任务容器无需
安装任何东西——只要把 `ANTHROPIC_BASE_URL` 指向代理的公开 URL 即可。

评分验证器保持不变：它仍然使用你的 Anthropic 评判模型（`OPENAI_API_KEY` / `EVAL_MODEL`）。
DeepSeek 只作为*智能体*后端。

### 一次性的代理部署

```bash
# 1. An OpenRouter API key with deepseek-v4-pro access (https://openrouter.ai/keys)
#    is stored as a Modal secret — it never leaves your Modal account.
modal secret create openrouter-deepseek OPENROUTER_API_KEY=sk-or-...

# 2. Deploy the proxy. This prints your personal URL.
modal deploy multi_agent/deepseek_litellm_modal.py
# -> https://<your-user>--deepseek-litellm-proxy-serve.modal.run

# 3. Put that URL in .env so the adapters can find it:
echo 'export AGENTRADIO_PROXY_URL=https://<your-user>--deepseek-litellm-proxy-serve.modal.run' >> .env
source .env
```

代理会保持热启动（`min_containers=1`）；只有修改过它之后才需要重新部署。空闲时想停止计费：
`modal app stop deepseek-litellm-proxy`（之后再执行一次 `modal deploy` 即可恢复）。

### 用 DeepSeek 跑 L1 / L2 / L3

命令与上面的 Opus 版本完全一致，只是 import path 指向 DeepSeek 适配器，并用
`-m "deepseek-v4-pro"` 经由代理路由。`source .env` 必须已经导出了 `AGENTRADIO_PROXY_URL`。
任务 ID 和 `-i` 批量方式与上文完全相同。

#### DeepSeek B0 —— 单智能体（基线）

DeepSeek 基线使用内置 `claude-code` 智能体的一个轻量子类（它强制使用代理端点，并丢弃内置
智能体本会重新签发的 OAuth token），因此要用 `--agent-import-path` 而不是 `-a claude-code`。

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.claude_code_deepseek:ClaudeCodeDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-baseline-ba998" \
  -y
```

#### DeepSeek L1 —— 仅分工

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_ablation_deepseek:CoralMultiAgentAblationDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-division-ba998" \
  -y
```

#### DeepSeek L2 —— + 协商

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_deepseek:CoralMultiAgentDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-divneg-ba998" \
  -y
```

#### DeepSeek L3 —— + 被动感知

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"

harbor run \
  -p ./data/qa \
  --agent-import-path='multi_agent.coral_multi_agent_passive_deepseek:CoralMultiAgentPassiveDeepseek' \
  -m "deepseek-v4-pro" \
  -e modal -k 1 -n 1 \
  -i "task-6905333b74f22949d97ba998" \
  --ak reasoning_effort=high \
  -o results/qa/ \
  --job-name "deepseek-passive-ba998" \
  -y
```

共享的代理注入逻辑（在继承全部多智能体逻辑、启动脚本和续跑保护的同时替换 LLM 后端）位于
`multi_agent/deepseek_proxy.py`；B0 基线子类是 `multi_agent/claude_code_deepseek.py`。

### 续跑被取消或失败的作业

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
harbor job resume -p results/qa/<job-name> -f CancelledError -f RuntimeError
```

### 实时监控（可选，另开一个终端）

```bash
bash multi_agent/monitor_coral_log.sh   # renders coral://state from the running container
```

---

## 🧪 评分

每次试验会把团队的答案写入 `<trial>/agent/answer.txt`。用基准自带的 LLM 评判器打分：

```bash
source .env
python3 verify_local.py <task-id> <trial-dir>
# e.g.
python3 verify_local.py task-6905333b74f22949d97ba998 \
  results/qa/divneg-ba998/task-6905333b74f22949d97ba998__XXXXX
```

它会写出 `<trial>/verifier/reward.txt`（只有当所有评分细则全部通过时才为 1）和
`evaluation_results.json`（逐条细则的得分）。若缺少依赖，执行 `pip install openai`。

### 试验输出结构

```
task-xxx__randomId/
├── config.json / result.json / trial.log
├── agent/
│   ├── answer.txt                # final answer (written by agent-1)
│   ├── coral-server.log          # threads and messages
│   └── agent-{1..4}-claude-code.txt
└── verifier/
    ├── reward.txt
    └── evaluation_results.json
```

---

## 📊 完整结果

SWE-Atlas QnA 上的完整结果（124 个任务，1,306 条评分细则）。分类行给出的是解决的任务数，
括号内为该类别的任务总数。在每个模型列内，所有配置都使用相同的 harness 与设置。

`B0` = 单个 Claude Code · `L1` = 4× Claude Code + 分工 · `L2` = L1 + 协商 ·
`L3` = L2 + 被动感知（AgentRadio）。

**Opus 4.6**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| 架构与系统设计（44） | 15 | 13 | 24 | **30** |
| 根因分析（37） | 9 | 16 | 18 | **20** |
| 代码上手（28） | 11 | 12 | 14 | **18** |
| 安全（11） | 4 | **7** | **7** | **7** |
| API 与库集成（4） | 1 | 1 | 1 | **2** |
| **解决的任务总数（124）** | 40 | 49 | 64 | **77** |
| **任务准确率（%）** | 32.3 | 39.5 | 51.6 | **62.1** |
| **细则通过率（%）** | 84.2 | 86.1 | 91.3 | **93.1** |

**DeepSeek V4 Pro**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| 架构与系统设计（44） | 14 | 13 | 17 | **24** |
| 根因分析（37） | 11 | 13 | 15 | **18** |
| 代码上手（28） | 7 | 8 | 10 | **13** |
| 安全（11） | 4 | 4 | 6 | **7** |
| API 与库集成（4） | 0 | 0 | 1 | **1** |
| **解决的任务总数（124）** | 36 | 39 | 49 | **63** |
| **任务准确率（%）** | 29.0 | 31.4 | 39.5 | **50.8** |
| **细则通过率（%）** | 81.2 | 83.7 | 85.9 | **90.2** |

**L3 对比 L2，在配对任务结果上的精确 McNemar 检验** —— Opus 4.6：赢 15、输 2，p = 0.0023。
DeepSeek V4 Pro：赢 17、输 3，p = 0.0026。

细则层面的分析显示，被动感知带来的收益随任务难度上升而增大，这与「执行中途纠偏」这一
底层机制相吻合。

---

## 🛠️ 疑难排查

- **运行中途出现 401** —— OAuth token 快照已过期。按上文刷新后执行
  `harbor job resume -p results/qa/<job-name> -f NonZeroAgentExitCodeError`。
- **coral-server.log 中出现 `claude: not found`** —— 启动脚本会导出
  `PATH="$HOME/.local/bin:$PATH"`；请检查 Claude Code 是否已在容器内安装成功。
- **基于 Alpine 的任务** —— 部分任务使用 Alpine 镜像；适配器会自动检测并安装兼容 Alpine 的 JDK。
- **检查通信内容** ——
  `grep "sent message\|created thread" <trial>/agent/coral-server.log | sed 's/\x1b\[[0-9;]*m//g'`

---

## 🙏 致谢

任务数据来自 Scale AI 的 [SWE-Atlas QnA](https://github.com/scaleapi/SWE-Atlas) 基准
（harbor 数据集 `scale-ai/swe-atlas-qna`）。运行由
[Harbor](https://github.com/laude-institute/harbor) 在 [Modal](https://modal.com) 上编排。

---

## 📚 引用

```bibtex
@misc{ren2026agentradio,
  title  = {AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration},
  author = {Xinxing Ren and Qianbo Zang and Ziyan Wang and Caelum Forder and
            Suman Deb and Peter Carroll and Zekun Guo},
  year   = {2026},
  eprint = {2607.28430},
  archivePrefix = {arXiv},
  url    = {https://arxiv.org/abs/2607.28430}
}
```

---

## 📄 许可证

基于 [Apache License 2.0](LICENSE) 发布。

---

由 Coral AI Labs、卢森堡大学 SnT、伦敦国王学院与赫尔大学共同完成。
