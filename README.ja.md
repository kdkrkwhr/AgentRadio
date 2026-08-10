<p align="center">
  <img src="main.png" alt="AgentRadio — マルチエージェント協調のための受動的アウェアネス" width="100%">
</p>

<h1 align="center">📻 AgentRadio</h1>

<h3 align="center">長期タスクのマルチエージェント協調に受動的アウェアネスを——4 体のコーディングエージェントが<b>働きながら</b>聞く</h3>

<p align="center">
  <a href="https://arxiv.org/abs/2607.28430"><img src="https://img.shields.io/badge/論文-arXiv-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="論文"></a>
  <a href="https://github.com/Coral-Protocol/AgentRadio"><img src="https://img.shields.io/badge/コード-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/ライセンス-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="ライセンス: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://github.com/scaleapi/SWE-Atlas"><img src="https://img.shields.io/badge/ベンチマーク-SWE--Atlas_QnA-0E9B9B?style=for-the-badge&logo=github&logoColor=white" alt="ベンチマーク"></a>
  <a href="https://github.com/laude-institute/harbor"><img src="https://img.shields.io/badge/オーケストレーション-Harbor-4B32C3?style=for-the-badge&logo=github&logoColor=white" alt="Harbor"></a>
  <a href="https://modal.com"><img src="https://img.shields.io/badge/計算基盤-Modal-7FEE64?style=for-the-badge&logo=modal&logoColor=black" alt="Modal"></a>
</p>

<p align="center">
  <a href="https://github.com/Coral-Protocol/AgentRadio/discussions"><img src="https://img.shields.io/badge/ディスカッション-参加-5865F2?style=for-the-badge&logo=github&logoColor=white" alt="ディスカッション"></a>
  <a href="https://github.com/Coral-Protocol"><img src="https://img.shields.io/badge/Coral_Protocol-Org-FF5C8A?style=for-the-badge&logo=github&logoColor=white" alt="Coral Protocol"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.es.md">Español</a> |
  <b>日本語</b> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ar.md">العربية</a>
</p>

<p align="center">
  <i>4 体のコーディングエージェントに共有の無線チャンネルを与える。彼らは作業を分担し、計画を
  交渉し、<b>働きながら</b>発見を発信し続ける——「聞くこと」がバックグラウンドタスクとして走り、
  行動の 1 ターンを奪わないからだ。</i>
</p>

本リポジトリは、論文 *AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration*
（[arXiv:2607.28430](https://arxiv.org/abs/2607.28430)）の実験を再現するためのコードとデータを
収録しています。

### 🏆 1 つのプロトコル、4 体のエージェント——単一エージェント比 +29.8 ポイント

| 構成 | 追加される要素 | タスク正解率（Opus 4.6） | タスク正解率（DeepSeek V4 Pro） |
|---|---|:---:|:---:|
| **B0** 単一エージェント | — | 32.3 % | 29.0 % |
| **B1** 単独実行 6 回のベスト | 6 倍の予算、協調なし | 37.9 % | 31.4 % |
| **L1** 4 エージェント + 分担 | 作業分担 | 39.5 % | 31.4 % |
| **L2** + 交渉 | 共同計画 + 相互レビュー（ブロッキング受信） | 51.6 % | 39.5 % |
| **L3** + 受動的アウェアネス（**AgentRadio**） | バックグラウンドの `wait_for_mention` | **62.1 %** | **50.8 %** |

L2 から L3 への一歩で変わるのは通信モード**だけ**です。Opus 4.6 では 15 タスクで勝ち 2 タスクで
負け（正確 McNemar 検定、p = 0.0023）、DeepSeek では 17 勝 3 敗（p = 0.0026）。AgentRadio 下の
Opus 4.6 エージェント 4 体（62.1 %）は、単一エージェントのリーダーボード最高記録である
新しい Opus 4.8 の Claude Code（57.2 %）を上回ります。

→ [詳細な結果を見る](#-結果) · [論文](https://arxiv.org/abs/2607.28430) · [自分で再現する](#-4-つの構成を実行する)

## 📣 ニュース

- **2026-07** — AgentRadio 論文を [arXiv](https://arxiv.org/abs/2607.28430) で公開しました。🎉
- **2026-07** — コード、アダプタ、および 124 タスク分の SWE-Atlas QnA 設定一式をオープンソース化しました。🚀

## 💡 AgentRadio を使う理由

* **通信が作業ステップを消費しない** — `wait_for_mention` はハーネスの*バックグラウンドタスク*
  として走るため、仲間のメッセージはターンを消費せず次のステップ境界で自然に現れます。
  エージェントはもはや「働く」か「聞く」かを選ぶ必要がありません。
* **実行の途中で軌道修正できる** — ブロッキング方式では、ある発見は次のフェーズ境界まで仲間に
  届きません。受動的アウェアネスなら即座に届き、仲間は進行中のタスクにそれを織り込めます。
* **ハーネスの改造が不要** — ハーネスに求められるのはシェルコマンドをバックグラウンドで実行
  できることだけで、主要なコーディングハーネスはすでにこれを備えています。AgentRadio は独立した
  メッセージサーバと 3 つの薄いシェルスクリプトとして提供されます。
* **追加の LLM 呼び出しなし** — ウォッチャーはエージェントのステップではなく通常の OS プロセス
  です。エージェントが新たに支払うトークンは、実際に浮上したメッセージ分だけです。
* **モデル非依存** — 同一のプロトコル、プロンプト、起動スクリプトが Claude Opus 4.6 でも、
  LiteLLM 変換プロキシ経由の DeepSeek-V4-Pro でも動作します。
* **きれいなアブレーションの階段** — B0 → L1 → L2 → L3 が、同一のハーネス設定のもとで分担・交渉・
  受動的アウェアネスの寄与を一層ずつ切り分けます。

## 🧩 仕組み

### 3 つのプリミティブ

AgentRadio は各エージェントに 3 つの操作を提供します。

| プリミティブ | 挙動 |
|---|---|
| `create_thread(name, participants)` | メッセージサーバ上に名前付きの会話スレッドを開き、その識別子を返します。 |
| `send_message(thread, content, mentions)` | スレッドにメッセージを追加し、誰かが聞いているかどうかに関わらず即座に戻ります。特定のエージェントを @ メンションできます。 |
| `wait_for_mention(timeout)` | 呼び出し元をメンションするメッセージが届くまでブロックし、全スレッドの完全なスナップショットとともに返します。そのため文脈の再構築に 2 度目の読み取りは不要です。 |

このレイヤはエージェントが*いつ*聞くかについては何も規定しません。`wait_for_mention` が
どこで走るかが、2 つの通信モードを分ける唯一の自由度です。

- **フォアグラウンド** → *ブロッキング受信*。エージェントは聞くために作業を止めます。
  メッセージを 1 通聞くたびに作業ステップ 1 つ分のコストがかかります。これが L2 のベースラインです。
- **バックグラウンドタスク** → *受動的アウェアネス*。エージェントは働き続け、メンションは次の
  ステップ境界で浮上します。聞くためのステップは一切消費しません。これが L3、完全な AgentRadio です。

それ以外——プリミティブ、スレッド、プロトコル——はすべて固定です。実験が切り分けるのは、この
「1 ビット」の差だけです。

### 5 フェーズのプロトコル

4 体のエージェントが、作業分担と交渉からなる固定のプロトコルを実行します。agent-1 は加えて
**アセンブラ**を務め、計画スレッド・作業ログスレッド・最終回答スレッドを開き、すべての遷移を
管理します。フェーズは、全エージェントから明示的な承認を集めて初めて終了します。

1. **P1・探索** — 各エージェントがバックグラウンドウォッチャーを起動し、独立してリポジトリを
   探索し、見えたサブ質問を書き出します。この段階では何も送信しません。
2. **P2・分担** — アセンブラが計画スレッドを開きます。各エージェントは発見を持ち寄り、サブ質問の
   分割案を交渉し、全員が承認するまで修正を重ねます。
3. **P3・実行** — 各エージェントが自分のサブ質問に取り組みます。発見があった瞬間に作業ログへ
   投稿します——仲間に影響する発見、合意した計画との矛盾、障害、放棄した袋小路など。
4. **P4・レビュー** — 各エージェントが自分の結果スレッドで、発見を証拠とともに共有します。
   レビュアーは事実の矛盾、証拠の薄さ、言及されていない観察を指摘し、サブ質問を P3 に差し戻せます。
5. **P5・提出** — アセンブラが承認済みの結果から最終回答を構成し、最後の承認ラウンドのために
   草案を共有してから提出します。

ブロッキング受信では同じ 5 フェーズがそのまま走りますが、P3 のリアルタイム共有が消えます。
メッセージを聞くにはフォアグラウンドでの待機が必要になるため、エージェントは作業中は沈黙し、
発見は P4 より前に仲間へ届きません。

## 🗂️ リポジトリ構成

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

`data/qa/` 配下の各タスクディレクトリには、指示文、固定された実行環境、および検証器が使用する
ルーブリック一式が含まれています。

---

## 📦 セットアップ

実行は [Modal](https://modal.com) 上の Docker コンテナで行われ、
[Harbor](https://github.com/laude-institute/harbor) がオーケストレーションします。
1 タスク = メッセージサーバと 4 体の Claude Code エージェントが動く 1 コンテナです。

### 1. Docker Desktop

https://www.docker.com/products/docker-desktop/ からインストールし、`docker run hello-world` で確認します。

### 2. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Harbor（0.6.4 に固定）

新しい Harbor（0.7 以降）には破壊的な API 変更があり、これらのアダプタが動作しません。
バージョンを固定してください。

| コンポーネント | 動作するバージョン |
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

エージェントには **Claude Max サブスクリプション**が必要です。検証器にはさらに
**Anthropic API キー**が必要です。

### 6. メッセージサーバの JAR

106 MB のサーバ JAR は匿名化されたアーティファクトとしてホストされています（git blob には
大きすぎるため）。`confirm=t` パラメータは大容量ファイルのスキャン中間ページを回避し、
`curl` がバイナリを直接取得できるようにします。

```bash
curl -L -o multi_agent/coral-server.jar \
  "https://drive.usercontent.google.com/download?id=17b40_1kXFrAC0pnN8w_7PPY13O7pYVke&export=download&confirm=t"
```

アダプタがこの JAR を各タスクコンテナへアップロードします。ローカルで何かを動かす必要はなく、
ローカルの JDK も不要です。

### 7. トークンヘルパーと .env

```bash
cp run_config/qa/claude-token ~/.local/bin/claude-token
chmod +x ~/.local/bin/claude-token
cp .env.example .env      # then fill in your Anthropic API key
```

### 各実行の前に：OAuth トークンを更新する

Claude Code の OAuth トークンはローテーションします。各コンテナは起動時に静的なスナップショットを
受け取るだけなので、期限切れのトークンは実行中に 4 体すべてのエージェントを 401 で停止させます。
セッションごとに更新してください。

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

## ⚡ 4 つの構成を実行する

すべてのコマンドはリポジトリのルートで、`source .env` の後に実行します。タスク ID は
`data/qa/` 配下のディレクトリ名です（`-i` を繰り返せばバッチ指定、`-i` を完全に省けば 124 件
すべてを実行）。`-n` は同時実行タスク数です（L1–L3 では 1 タスク = 4 エージェント）。

### B0 — 単一エージェント（ベースライン）

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

### L1 — 4 エージェント + 作業分担

agent-1 が簡単に探索して質問を分割し、各エージェントが自分の担当分を独立に解きます。
回答はレビューなしでマージされます。

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

### L2 — + 交渉（ブロッキング受信）

完全な 5 フェーズプロトコル——共同探索、全員一致までの分割交渉、実行、相互レビュー、統合提出——
ですが、`wait_for_mention` は**フォアグラウンド**で走るため、エージェントは聞くために作業を
止めます。

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

### L3 — + 受動的アウェアネス（完全な AgentRadio）

プロトコルは同一ですが、`wait_for_mention` が**バックグラウンドタスク**として走ります。
エージェントは働き続け、メッセージはステップの合間に浮上します。Claude Code に MCP 設定は
与えられず、通信はすべて `passive_scripts/` の薄いシェルラッパー経由で行われます。

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

`run_config/qa/run_passive_multi_agent.sh` は同じコマンドをバッチランナーとしてラップし、
タスク ID ごとに 1 つの harbor ジョブを起動します。

---

## 🔀 DeepSeek-V4-Pro で実行する

マルチエージェント構成（L1–L3）は Opus 4.6 の代わりに **DeepSeek-V4-Pro** エージェントで実行でき、
結果表の DeepSeek 列を再現できます。プロトコル、プロンプト、起動スクリプト、レジューム
ガードはすべて同一で、変わるのは LLM のバックエンドだけです。

Claude Code は Anthropic Messages API しか話しませんが、DeepSeek は OpenRouter（OpenAI 互換のみ）
経由で提供されます。両者を **Modal 上に一度だけホストした LiteLLM 変換プロキシ**で橋渡しします。
タスクコンテナには何もインストールせず、`ANTHROPIC_BASE_URL` をプロキシの公開 URL に向けるだけです。

ルーブリック検証器は変更ありません。引き続きあなたの Anthropic ジャッジ（`OPENAI_API_KEY` /
`EVAL_MODEL`）を使います。DeepSeek は*エージェント*側のバックエンドにすぎません。

### 一度だけのプロキシ構築

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

プロキシはウォームな状態を維持します（`min_containers=1`）。再デプロイが必要なのは編集した
ときだけです。アイドル時の課金を止めるには `modal app stop deepseek-litellm-proxy`
（後で `modal deploy` すれば復帰します）。

### DeepSeek での L1 / L2 / L3

上記の Opus 用コマンドと同一で、インポートパスが DeepSeek アダプタを指し、
`-m "deepseek-v4-pro"` がプロキシ経由でルーティングされる点だけが異なります。`source .env` で
`AGENTRADIO_PROXY_URL` がエクスポートされている必要があります。タスク ID と `-i` によるバッチ
指定は上記とまったく同じです。

#### DeepSeek B0 — 単一エージェント（ベースライン）

DeepSeek のベースラインは組み込み `claude-code` エージェントの薄いサブクラスを使います
（プロキシのエンドポイントを強制し、組み込みエージェントが再発行してしまう OAuth トークンを
破棄します）。そのため `-a claude-code` ではなく `--agent-import-path` を取ります。

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

#### DeepSeek L1 — 分担のみ

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

#### DeepSeek L2 — + 交渉

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

#### DeepSeek L3 — + 受動的アウェアネス

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

マルチエージェントのロジック、起動スクリプト、レジュームガードをすべて継承したまま LLM
バックエンドを差し替える共有のプロキシ注入は `multi_agent/deepseek_proxy.py` にあります。
B0 ベースラインのサブクラスは `multi_agent/claude_code_deepseek.py` です。

### 中断・失敗したジョブを再開する

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
harbor job resume -p results/qa/<job-name> -f CancelledError -f RuntimeError
```

### ライブモニタリング（任意、別ターミナル）

```bash
bash multi_agent/monitor_coral_log.sh   # renders coral://state from the running container
```

---

## 🧪 採点

各トライアルはチームの回答を `<trial>/agent/answer.txt` に書き出します。ベンチマークの LLM
ジャッジで採点してください。

```bash
source .env
python3 verify_local.py <task-id> <trial-dir>
# e.g.
python3 verify_local.py task-6905333b74f22949d97ba998 \
  results/qa/divneg-ba998/task-6905333b74f22949d97ba998__XXXXX
```

これにより `<trial>/verifier/reward.txt`（すべてのルーブリックを通過した場合のみ 1）と
`evaluation_results.json`（ルーブリックごとのスコア）が書き出されます。未導入なら
`pip install openai` を実行してください。

### トライアルの出力構造

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

## 📊 結果

SWE-Atlas QnA での完全な結果（124 タスク、1,306 ルーブリック）。カテゴリ行は解決したタスク数で、
括弧内はそのカテゴリのタスク総数です。各モデル列の中では、すべての構成が同一のハーネスと
設定を使用しています。

`B0` = 単一の Claude Code · `L1` = 4× Claude Code + 作業分担 · `L2` = L1 + 交渉 ·
`L3` = L2 + 受動的アウェアネス（AgentRadio）。

**Opus 4.6**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| アーキテクチャとシステム設計（44） | 15 | 13 | 24 | **30** |
| 根本原因分析（37） | 9 | 16 | 18 | **20** |
| コードオンボーディング（28） | 11 | 12 | 14 | **18** |
| セキュリティ（11） | 4 | **7** | **7** | **7** |
| API・ライブラリ統合（4） | 1 | 1 | 1 | **2** |
| **解決したタスク数（124）** | 40 | 49 | 64 | **77** |
| **タスク正解率（%）** | 32.3 | 39.5 | 51.6 | **62.1** |
| **ルーブリック通過率（%）** | 84.2 | 86.1 | 91.3 | **93.1** |

**DeepSeek V4 Pro**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| アーキテクチャとシステム設計（44） | 14 | 13 | 17 | **24** |
| 根本原因分析（37） | 11 | 13 | 15 | **18** |
| コードオンボーディング（28） | 7 | 8 | 10 | **13** |
| セキュリティ（11） | 4 | 4 | 6 | **7** |
| API・ライブラリ統合（4） | 0 | 0 | 1 | **1** |
| **解決したタスク数（124）** | 36 | 39 | 49 | **63** |
| **タスク正解率（%）** | 29.0 | 31.4 | 39.5 | **50.8** |
| **ルーブリック通過率（%）** | 81.2 | 83.7 | 85.9 | **90.2** |

**L3 対 L2、対応のあるタスク結果に対する正確 McNemar 検定** — Opus 4.6：15 勝 2 敗、p = 0.0023。
DeepSeek V4 Pro：17 勝 3 敗、p = 0.0026。

ルーブリック単位の分析では、受動的アウェアネスによる改善はタスクの難易度が上がるほど大きく
なっており、根底のメカニズムが「実行途中での軌道修正」であることと整合します。

---

## 🛠️ トラブルシューティング

- **実行中の 401 エラー** — OAuth トークンのスナップショットが失効しています。上記の手順で
  更新した後、`harbor job resume -p results/qa/<job-name> -f NonZeroAgentExitCodeError` を実行します。
- **coral-server.log の `claude: not found`** — 起動スクリプトは
  `PATH="$HOME/.local/bin:$PATH"` をエクスポートします。コンテナ内に Claude Code が
  インストールされたか確認してください。
- **Alpine ベースのタスク** — 一部のタスクは Alpine イメージを使います。アダプタが自動検出し、
  Alpine 互換の JDK をインストールします。
- **通信内容の確認** —
  `grep "sent message\|created thread" <trial>/agent/coral-server.log | sed 's/\x1b\[[0-9;]*m//g'`

---

## 🙏 謝辞

タスクデータは Scale AI による [SWE-Atlas QnA](https://github.com/scaleapi/SWE-Atlas)
ベンチマーク（harbor データセット `scale-ai/swe-atlas-qna`）です。実行は
[Modal](https://modal.com) 上で [Harbor](https://github.com/laude-institute/harbor) により
オーケストレーションされています。

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

## Star History

<picture>
  <source
    media="(prefers-color-scheme: dark)"
    srcset="https://api.star-history.com/svg?repos=Coral-Protocol/AgentRadio&type=Date&theme=dark"
  />
  <source
    media="(prefers-color-scheme: light)"
    srcset="https://api.star-history.com/svg?repos=Coral-Protocol/AgentRadio&type=Date"
  />
  <img
    alt="Star History Chart"
    src="https://api.star-history.com/svg?repos=Coral-Protocol/AgentRadio&type=Date"
  />
</picture>

---

## 📄 ライセンス

[Apache License 2.0](LICENSE) のもとで公開されています。

---

Coral AI Labs、ルクセンブルク大学 SnT、キングス・カレッジ・ロンドン、ハル大学にて開発。
