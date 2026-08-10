<p align="center">
  <img src="main.png" alt="AgentRadio — conciencia pasiva para agentes de programación" width="100%">
</p>

<h1 align="center">📻 AgentRadio</h1>

<h3 align="center">Conciencia pasiva para la colaboración multiagente de horizonte largo: cuatro agentes de programación que siguen trabajando <b>mientras</b> escuchan</h3>

<p align="center">
  <a href="https://arxiv.org/abs/2607.28430"><img src="https://img.shields.io/badge/Art%C3%ADculo-arXiv-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="Artículo"></a>
  <a href="https://github.com/Coral-Protocol/AgentRadio"><img src="https://img.shields.io/badge/C%C3%B3digo-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licencia-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="Licencia: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://github.com/scaleapi/SWE-Atlas"><img src="https://img.shields.io/badge/Benchmark-SWE--Atlas_QnA-0E9B9B?style=for-the-badge&logo=github&logoColor=white" alt="Benchmark"></a>
  <a href="https://github.com/laude-institute/harbor"><img src="https://img.shields.io/badge/Orquestaci%C3%B3n-Harbor-4B32C3?style=for-the-badge&logo=github&logoColor=white" alt="Harbor"></a>
  <a href="https://modal.com"><img src="https://img.shields.io/badge/C%C3%B3mputo-Modal-7FEE64?style=for-the-badge&logo=modal&logoColor=black" alt="Modal"></a>
</p>

<p align="center">
  <a href="https://github.com/Coral-Protocol/AgentRadio/discussions"><img src="https://img.shields.io/badge/Discusiones-Unirse-5865F2?style=for-the-badge&logo=github&logoColor=white" alt="Discusiones"></a>
  <a href="https://github.com/Coral-Protocol"><img src="https://img.shields.io/badge/Coral_Protocol-Org-FF5C8A?style=for-the-badge&logo=github&logoColor=white" alt="Coral Protocol"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <b>Español</b> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ar.md">العربية</a>
</p>

<p align="center">
  <i>Dale a cuatro agentes de programación un canal de radio compartido. Se reparten el
  trabajo, negocian el plan y siguen transmitiendo hallazgos <b>mientras</b> trabajan, porque
  escuchar corre como una tarea en segundo plano en lugar de robar un turno.</i>
</p>

Este repositorio contiene el código y los datos para reproducir los experimentos del artículo
*AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration*
([arXiv:2607.28430](https://arxiv.org/abs/2607.28430)).

### 🏆 Un protocolo, cuatro agentes: +29,8 puntos sobre un solo agente

| Configuración | Qué añade | Precisión (Opus 4.6) | Precisión (DeepSeek V4 Pro) |
|---|---|:---:|:---:|
| **B0** un solo agente | — | 32,3 % | 29,0 % |
| **B1** la mejor de seis ejecuciones individuales | 6× presupuesto, sin coordinación | 37,9 % | 31,4 % |
| **L1** cuatro agentes + división | división del trabajo | 39,5 % | 31,4 % |
| **L2** + negociación | planificación conjunta + revisión cruzada (recepción bloqueante) | 51,6 % | 39,5 % |
| **L3** + conciencia pasiva (**AgentRadio**) | `wait_for_mention` en segundo plano | **62,1 %** | **50,8 %** |

El paso de L2 a L3 cambia **únicamente** el modo de comunicación. Gana 15 tareas y pierde 2
con Opus 4.6 (test exacto de McNemar, p = 0,0023) y gana 17 mientras pierde 3 con DeepSeek
(p = 0,0026). Cuatro agentes Opus 4.6 bajo AgentRadio (62,1 %) superan la mejor entrada de
agente único en la tabla de clasificación: Claude Code con el más reciente Opus 4.8 (57,2 %).

→ [Ver los resultados completos](#-resultados) · [artículo](https://arxiv.org/abs/2607.28430) · [reprodúcelo tú mismo](#-ejecutar-las-cuatro-configuraciones)

## 📣 Novedades

- **2026-08** — [VentureBeat](https://venturebeat.com/) cubrió AgentRadio: [«Cuatro agentes de IA coordinándose en tiempo real superaron a Claude Opus 4.8 en tareas de programación empresarial»](https://venturebeat.com/orchestration/four-ai-agents-coordinating-in-real-time-outperformed-claude-opus-4-8-on-enterprise-coding-tasks). 📰
- **2026-07** — El artículo de AgentRadio se publica en [arXiv](https://arxiv.org/abs/2607.28430). 🎉
- **2026-07** — Se liberan el código, los adaptadores y la configuración completa de las 124 tareas de SWE-Atlas QnA. 🚀

## 💡 Por qué AgentRadio

* **Comunicar deja de costar trabajo** — `wait_for_mention` corre como *tarea en segundo
  plano* del harness, así que el mensaje de un compañero aflora en el siguiente límite de
  paso en vez de consumir un turno. Los agentes ya no eligen entre trabajar y escuchar.
* **Corrección a mitad de ejecución** — en los sistemas bloqueantes, un hallazgo no llega a
  un compañero hasta el siguiente límite de fase. Con conciencia pasiva llega de inmediato y
  el compañero lo integra en la tarea que ya tiene en marcha.
* **Sin modificar el harness** — el harness solo debe poder ejecutar un comando de shell en
  segundo plano, algo que los harnesses de programación habituales ya hacen. AgentRadio se
  distribuye como un servidor de mensajes independiente más tres scripts de shell ligeros.
* **Sin llamadas extra al LLM** — el vigía es un proceso ordinario del sistema operativo, no
  un paso del agente. Los únicos tokens nuevos que paga un agente son los mensajes que
  realmente afloran.
* **Independiente del modelo** — el mismo protocolo, prompts y scripts de arranque funcionan
  con Claude Opus 4.6 y con DeepSeek-V4-Pro a través de un proxy de traducción LiteLLM.
* **Una escalera de ablación limpia** — B0 → L1 → L2 → L3 aísla la división del trabajo, la
  negociación y la conciencia pasiva capa por capa, con ajustes de harness idénticos.

## 🧩 Cómo funciona

### Las tres primitivas

AgentRadio expone tres operaciones a cada agente:

| Primitiva | Comportamiento |
|---|---|
| `create_thread(name, participants)` | Abre una conversación con nombre en el servidor de mensajes y devuelve su identificador. |
| `send_message(thread, content, mentions)` | Añade un mensaje a un hilo y retorna de inmediato, haya alguien escuchando o no. Puede mencionar con @ a agentes concretos. |
| `wait_for_mention(timeout)` | Bloquea hasta que llega un mensaje que menciona a quien llama y lo devuelve junto con una instantánea completa de todos los hilos, de modo que nunca hace falta una segunda lectura para reconstruir el contexto. |

La capa no opina sobre *cuándo* escucha un agente. Dónde corre `wait_for_mention` es el único
grado de libertad que separa los dos modos de comunicación:

- **En primer plano** → *recepción bloqueante*. El agente deja de trabajar para escuchar.
  Cada mensaje oído cuesta un paso de trabajo. Esta es la línea base L2.
- **Tarea en segundo plano** → *conciencia pasiva*. El agente sigue trabajando y cualquier
  mención aflora en el siguiente límite de paso, sin gastar ningún paso en escuchar. Esto es
  L3, AgentRadio completo.

Todo lo demás —las primitivas, los hilos, el protocolo— permanece fijo. Esa diferencia de un
solo bit es justamente lo que aíslan los experimentos.

### El protocolo de cinco fases

Cuatro agentes ejecutan un protocolo fijo de división del trabajo y negociación. Agent-1 actúa
además como **ensamblador**: abre los hilos de planificación, de bitácora y de respuesta final,
y controla cada transición — una fase solo termina cuando ha reunido la aprobación explícita
de todos los agentes.

1. **P1 · Explorar** — cada agente arranca su vigía en segundo plano, explora el repositorio
   por su cuenta y redacta las subpreguntas que ve. No se envía nada.
2. **P2 · Dividir** — el ensamblador abre un hilo de planificación. Los agentes ponen en común
   sus hallazgos, negocian un reparto de las subpreguntas y lo revisan hasta que todos aprueban.
3. **P3 · Ejecutar** — cada agente trabaja sus subpreguntas. Un descubrimiento dispara una
   entrada en la bitácora en el momento en que se produce: un hallazgo que afecta a un
   compañero, una contradicción con el plan acordado, un obstáculo o un callejón sin salida abandonado.
4. **P4 · Revisar** — cada agente difunde sus hallazgos con evidencia en su propio hilo de
   resultados. Los revisores señalan conflictos factuales, evidencia insuficiente y
   observaciones no mencionadas, y pueden devolver una subpregunta a P3.
5. **P5 · Enviar** — el ensamblador redacta la respuesta final a partir de los resultados
   aprobados, difunde el borrador para una última ronda de aprobaciones y la envía.

Con recepción bloqueante, las mismas cinco fases se ejecutan sin cambios, pero desaparece el
intercambio en vivo de P3: oír un mensaje cuesta una espera en primer plano, así que los
agentes callan mientras trabajan y un hallazgo no puede llegar a un compañero antes de P4.

## 🗂️ Estructura del repositorio

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

Cada directorio de tarea bajo `data/qa/` incluye la instrucción, el entorno de ejecución
fijado y el conjunto de rúbricas que usa el verificador.

---

## 📦 Instalación

Las ejecuciones corren en contenedores Docker sobre [Modal](https://modal.com), orquestadas por
[Harbor](https://github.com/laude-institute/harbor). Una tarea = un contenedor que ejecuta el
servidor de mensajes más cuatro agentes de Claude Code.

### 1. Docker Desktop

Instálalo desde https://www.docker.com/products/docker-desktop/ y verifica con `docker run hello-world`.

### 2. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Harbor (fijado en 0.6.4)

Las versiones más recientes de Harbor (0.7+) traen cambios de API incompatibles que hacen
fallar estos adaptadores. Fija las versiones:

| Componente | Versión válida |
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

Necesitas una **suscripción Claude Max** para los agentes. El verificador requiere además una
**clave de API de Anthropic**.

### 6. JAR del servidor de mensajes

El JAR del servidor, de 106 MB, se aloja como artefacto anonimizado (demasiado grande para un
blob de git). El parámetro `confirm=t` salta la pantalla intermedia de análisis de archivos
grandes para que `curl` reciba el binario directamente:

```bash
curl -L -o multi_agent/coral-server.jar \
  "https://drive.usercontent.google.com/download?id=17b40_1kXFrAC0pnN8w_7PPY13O7pYVke&export=download&confirm=t"
```

Los adaptadores suben este JAR a cada contenedor de tarea. No hace falta ejecutar nada en
local, así que no se necesita ningún JDK local.

### 7. Ayudante de token y .env

```bash
cp run_config/qa/claude-token ~/.local/bin/claude-token
chmod +x ~/.local/bin/claude-token
cp .env.example .env      # then fill in your Anthropic API key
```

### Antes de cada ejecución: refresca el token OAuth

El token OAuth de Claude Code rota. Cada contenedor recibe una instantánea estática al
lanzarse, y un token caducado mata a los cuatro agentes con un 401 a mitad de ejecución.
Refréscalo antes de cada sesión:

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

## ⚡ Ejecutar las cuatro configuraciones

Todos los comandos se ejecutan desde la raíz del repositorio, tras `source .env`. Los IDs de
tarea son los nombres de directorio bajo `data/qa/` (repite `-i` para agrupar; omite `-i` por
completo para ejecutar las 124). `-n` es el número de tareas concurrentes (una tarea = cuatro
agentes en L1–L3).

### B0 — un solo agente (línea base)

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

### L1 — cuatro agentes + división del trabajo

Agent-1 explora brevemente, reparte la pregunta y cada agente resuelve su parte de forma
independiente. Las respuestas se fusionan sin revisión.

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

### L2 — + negociación (recepción bloqueante)

El protocolo completo de cinco fases —exploración conjunta, reparto negociado hasta la
unanimidad, ejecución en vivo, revisión cruzada, envío ensamblado— con `wait_for_mention`
corriendo en **primer plano**, de modo que los agentes dejan de trabajar para escuchar.

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

### L3 — + conciencia pasiva (AgentRadio completo)

El mismo protocolo, pero `wait_for_mention` corre como **tarea en segundo plano**: los agentes
siguen trabajando y los mensajes afloran entre pasos. Claude Code no recibe configuración MCP;
toda la comunicación pasa por los envoltorios de shell ligeros de `passive_scripts/`.

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

`run_config/qa/run_passive_multi_agent.sh` envuelve el mismo comando como ejecutor por lotes,
un job de harbor por cada ID de tarea.

---

## 🔀 Ejecutar con DeepSeek-V4-Pro

Las configuraciones multiagente (L1–L3) pueden ejecutarse con agentes **DeepSeek-V4-Pro** en
lugar de Opus 4.6, reproduciendo la columna DeepSeek de la tabla de resultados. El protocolo,
los prompts, los scripts de arranque y la protección de reanudación son idénticos; solo cambia
el backend del LLM.

Claude Code solo habla la Messages API de Anthropic, mientras que DeepSeek se sirve a través de
OpenRouter (solo compatible con OpenAI). Unimos ambos con un **proxy de traducción LiteLLM
alojado una sola vez en Modal**. Los contenedores de tarea no instalan nada: simplemente
apuntan `ANTHROPIC_BASE_URL` a la URL pública del proxy.

El verificador de rúbricas no cambia: sigue usando tu juez de Anthropic (`OPENAI_API_KEY` /
`EVAL_MODEL`). DeepSeek es solo el backend del *agente*.

### Configuración única del proxy

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

El proxy se mantiene caliente (`min_containers=1`); vuelve a desplegarlo solo si lo editas.
Para dejar de facturar cuando está inactivo: `modal app stop deepseek-litellm-proxy` (un
`modal deploy` posterior lo restaura).

### L1 / L2 / L3 con DeepSeek

Idénticos a los comandos de Opus anteriores, pero la ruta de importación apunta al adaptador de
DeepSeek y `-m "deepseek-v4-pro"` enruta por el proxy. `source .env` debe haber exportado
`AGENTRADIO_PROXY_URL`. Los IDs de tarea y el agrupado con `-i` funcionan exactamente igual.

#### DeepSeek B0 — un solo agente (línea base)

La línea base de DeepSeek usa una subclase ligera del agente `claude-code` integrado (fuerza el
endpoint del proxy y descarta el token OAuth que el agente integrado volvería a acuñar), así
que toma `--agent-import-path` en lugar de `-a claude-code`.

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

#### DeepSeek L1 — solo división

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

#### DeepSeek L2 — + negociación

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

#### DeepSeek L3 — + conciencia pasiva

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

La inyección compartida del proxy (que cambia el backend del LLM heredando toda la lógica
multiagente, los scripts de arranque y la protección de reanudación) vive en
`multi_agent/deepseek_proxy.py`; la subclase de la línea base B0 es
`multi_agent/claude_code_deepseek.py`.

### Reanudar un job cancelado o fallido

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
harbor job resume -p results/qa/<job-name> -f CancelledError -f RuntimeError
```

### Monitorización en vivo (opcional, en otra terminal)

```bash
bash multi_agent/monitor_coral_log.sh   # renders coral://state from the running container
```

---

## 🧪 Puntuación

Cada ensayo escribe la respuesta del equipo en `<trial>/agent/answer.txt`. Puntúala con el juez
LLM del benchmark:

```bash
source .env
python3 verify_local.py <task-id> <trial-dir>
# e.g.
python3 verify_local.py task-6905333b74f22949d97ba998 \
  results/qa/divneg-ba998/task-6905333b74f22949d97ba998__XXXXX
```

Esto escribe `<trial>/verifier/reward.txt` (1 solo cuando pasan todas las rúbricas) y
`evaluation_results.json` (puntuaciones por rúbrica). Ejecuta `pip install openai` si falta.

### Estructura de salida de un ensayo

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

## 📊 Resultados

Resultados completos en SWE-Atlas QnA (124 tareas, 1.306 rúbricas). Las filas de categoría dan
las tareas resueltas, con el tamaño de la categoría entre paréntesis. Dentro de cada columna de
modelo, todas las configuraciones usan el mismo harness y los mismos ajustes.

`B0` = un solo Claude Code · `L1` = 4× Claude Code + división del trabajo · `L2` = L1 +
negociación · `L3` = L2 + conciencia pasiva (AgentRadio).

**Opus 4.6**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| Arquitectura y diseño de sistemas (44) | 15 | 13 | 24 | **30** |
| Análisis de causa raíz (37) | 9 | 16 | 18 | **20** |
| Incorporación al código (28) | 11 | 12 | 14 | **18** |
| Seguridad (11) | 4 | **7** | **7** | **7** |
| Integración de API y librerías (4) | 1 | 1 | 1 | **2** |
| **Tareas resueltas (124)** | 40 | 49 | 64 | **77** |
| **Precisión por tarea (%)** | 32,3 | 39,5 | 51,6 | **62,1** |
| **Tasa de aprobación de rúbricas (%)** | 84,2 | 86,1 | 91,3 | **93,1** |

**DeepSeek V4 Pro**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| Arquitectura y diseño de sistemas (44) | 14 | 13 | 17 | **24** |
| Análisis de causa raíz (37) | 11 | 13 | 15 | **18** |
| Incorporación al código (28) | 7 | 8 | 10 | **13** |
| Seguridad (11) | 4 | 4 | 6 | **7** |
| Integración de API y librerías (4) | 0 | 0 | 1 | **1** |
| **Tareas resueltas (124)** | 36 | 39 | 49 | **63** |
| **Precisión por tarea (%)** | 29,0 | 31,4 | 39,5 | **50,8** |
| **Tasa de aprobación de rúbricas (%)** | 81,2 | 83,7 | 85,9 | **90,2** |

**L3 frente a L2, McNemar exacto sobre resultados de tareas emparejadas** — Opus 4.6: gana 15,
pierde 2, p = 0,0023. DeepSeek V4 Pro: gana 17, pierde 3, p = 0,0026.

El análisis a nivel de rúbrica muestra que la ganancia de la conciencia pasiva crece con la
dificultad de la tarea, coherente con la corrección a mitad de camino como mecanismo subyacente.

---

## 🛠️ Solución de problemas

- **Errores 401 a mitad de ejecución** — la instantánea del token OAuth caducó. Refréscala
  (ver arriba) y luego `harbor job resume -p results/qa/<job-name> -f NonZeroAgentExitCodeError`.
- **`claude: not found` en coral-server.log** — los scripts de arranque exportan
  `PATH="$HOME/.local/bin:$PATH"`; comprueba que Claude Code se instaló dentro del contenedor.
- **Tareas basadas en Alpine** — algunas tareas usan imágenes Alpine; los adaptadores lo
  detectan automáticamente e instalan un JDK compatible con Alpine.
- **Inspeccionar la comunicación** —
  `grep "sent message\|created thread" <trial>/agent/coral-server.log | sed 's/\x1b\[[0-9;]*m//g'`

---

## 🙏 Agradecimientos

Los datos de las tareas provienen del benchmark
[SWE-Atlas QnA](https://github.com/scaleapi/SWE-Atlas) (dataset de harbor
`scale-ai/swe-atlas-qna`) de Scale AI. Las ejecuciones se orquestan con
[Harbor](https://github.com/laude-institute/harbor) sobre [Modal](https://modal.com).

---

## 📚 Cita

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

## 📄 Licencia

Publicado bajo la [Licencia Apache 2.0](LICENSE).

---

Desarrollado en Coral AI Labs, SnT — Université du Luxembourg, King's College London y la
University of Hull.
