<p align="center">
  <img src="main.png" alt="AgentRadio — الوعي السلبي لوكلاء البرمجة" width="100%">
</p>

<h1 align="center">📻 AgentRadio</h1>

<h3 align="center">الوعي السلبي للتعاون متعدد الوكلاء في المهام طويلة الأمد — أربعة وكلاء برمجة يواصلون العمل <b>بينما</b> يستمعون</h3>

<p align="center">
  <a href="https://arxiv.org/abs/2607.28430"><img src="https://img.shields.io/badge/Paper-arXiv-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="البحث"></a>
  <a href="https://github.com/Coral-Protocol/AgentRadio"><img src="https://img.shields.io/badge/Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white" alt="الرخصة: Apache 2.0"></a>
</p>

<p align="center">
  <a href="https://github.com/scaleapi/SWE-Atlas"><img src="https://img.shields.io/badge/Benchmark-SWE--Atlas_QnA-0E9B9B?style=for-the-badge&logo=github&logoColor=white" alt="المعيار"></a>
  <a href="https://github.com/laude-institute/harbor"><img src="https://img.shields.io/badge/Orchestration-Harbor-4B32C3?style=for-the-badge&logo=github&logoColor=white" alt="Harbor"></a>
  <a href="https://modal.com"><img src="https://img.shields.io/badge/Compute-Modal-7FEE64?style=for-the-badge&logo=modal&logoColor=black" alt="Modal"></a>
</p>

<p align="center">
  <a href="https://discord.gg/GSHKNXF8U"><img src="https://img.shields.io/badge/Discord-Join-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://github.com/Coral-Protocol"><img src="https://img.shields.io/badge/Coral_Protocol-Org-FF5C8A?style=for-the-badge&logo=github&logoColor=white" alt="Coral Protocol"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <b>العربية</b>
</p>

<p align="center" dir="rtl">
  <i>امنح أربعة وكلاء برمجة قناة راديو مشتركة. يقتسمون العمل، ويتفاوضون على الخطة، ويواصلون بثّ
  اكتشافاتهم <b>أثناء</b> عملهم — لأن الاستماع يعمل كمهمة في الخلفية بدلاً من أن يسرق دورًا كاملاً.</i>
</p>

<div dir="rtl">

يحتوي هذا المستودع على الشيفرة والبيانات اللازمة لإعادة إنتاج تجارب البحث
<i>AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration</i>
(<a href="https://arxiv.org/abs/2607.28430">arXiv:2607.28430</a>).

</div>

### 🏆 بروتوكول واحد، أربعة وكلاء — بزيادة 29.8 نقطة على الوكيل المفرد

| التهيئة | ما الذي تضيفه | الدقة (Opus 4.6) | الدقة (DeepSeek V4 Pro) |
|---|---|:---:|:---:|
| **B0** وكيل مفرد | — | 32.3 % | 29.0 % |
| **B1** أفضل ستة تشغيلات مفردة | ميزانية 6× بلا تنسيق | 37.9 % | 31.4 % |
| **L1** أربعة وكلاء + تقسيم | تقسيم العمل | 39.5 % | 31.4 % |
| **L2** + تفاوض | تخطيط مشترك + مراجعة متبادلة (استقبال حاجب) | 51.6 % | 39.5 % |
| **L3** + وعي سلبي (**AgentRadio**) | ‏`wait_for_mention` في الخلفية | **62.1 %** | **50.8 %** |

<div dir="rtl">

الانتقال من L2 إلى L3 يغيّر <b>فقط</b> نمط التواصل. فهو يربح 15 مهمة ويخسر 2 مع Opus 4.6
(اختبار مكنمار الدقيق، p = 0.0023)، ويربح 17 ويخسر 3 مع DeepSeek (‏p = 0.0026). أربعة وكلاء من
Opus 4.6 تحت AgentRadio (‏62.1 %) يتفوقون على أقوى نتيجة لوكيل مفرد في لوحة الصدارة، وهي
Claude Code مع الإصدار الأحدث Opus 4.8 (‏57.2 %).

</div>

← <a href="#results">النتائج الكاملة</a> · <a href="https://arxiv.org/abs/2607.28430">البحث</a> · <a href="#running">شغّلها بنفسك</a>

## 📣 الأخبار

<div dir="rtl">

<ul>
<li><b>2026-08</b> — تناولت <a href="https://venturebeat.com/">VentureBeat</a> مشروع AgentRadio في مقال بعنوان <a href="https://venturebeat.com/orchestration/four-ai-agents-coordinating-in-real-time-outperformed-claude-opus-4-8-on-enterprise-coding-tasks">«أربعة وكلاء ذكاء اصطناعي يتنسّقون في الوقت الحقيقي يتفوّقون على Claude Opus 4.8 في مهام البرمجة المؤسسية»</a>. 📰</li>
<li><b>2026-07</b> — نُشر بحث AgentRadio على <a href="https://arxiv.org/abs/2607.28430">arXiv</a>. 🎉</li>
<li><b>2026-07</b> — إتاحة الشيفرة والمحوِّلات والإعداد الكامل لمهام SWE-Atlas QnA الـ 124 كمصدر مفتوح. 🚀</li>
</ul>

</div>

## 💡 لماذا AgentRadio

<div dir="rtl">

<ul>
<li><b>التواصل لم يعد يكلّف خطوة عمل</b> — تعمل <code>wait_for_mention</code> كمهمة في خلفية الـ harness،
فتظهر رسالة الزميل عند حدّ الخطوة التالية بدلاً من استهلاك دور كامل. لم يعد على الوكيل أن يختار
بين العمل والاستماع.</li>
<li><b>التصحيح في منتصف التنفيذ</b> — في الأنظمة الحاجبة لا يصل الاكتشاف إلى الزميل قبل حدّ المرحلة
التالية. أما مع الوعي السلبي فيصل فورًا، فيدمجه الزميل في المهمة الجارية بالفعل.</li>
<li><b>بلا تعديل على الـ harness</b> — كل ما يلزم هو القدرة على تشغيل أمر صدفة في الخلفية، وهو ما
توفّره بالفعل بيئات البرمجة الشائعة. يأتي AgentRadio كخادم رسائل مستقل بالإضافة إلى ثلاثة
سكربتات صدفة خفيفة.</li>
<li><b>بلا استدعاءات إضافية للنموذج</b> — المراقِب عملية نظام تشغيل عادية وليس خطوة وكيل. الرموز
(tokens) الإضافية الوحيدة التي يدفعها الوكيل هي الرسائل التي تظهر فعليًا.</li>
<li><b>مستقل عن النموذج</b> — البروتوكول نفسه والموجّهات وسكربتات الإقلاع تعمل على Claude Opus 4.6
وعلى DeepSeek-V4-Pro عبر وسيط ترجمة LiteLLM.</li>
<li><b>سُلّم استئصال نظيف</b> — يعزل التسلسل B0 ← L1 ← L2 ← L3 أثر تقسيم العمل والتفاوض والوعي
السلبي طبقةً طبقة، بإعدادات harness متطابقة.</li>
</ul>

</div>

## 🧩 كيف يعمل

### العمليات الأولية الثلاث

<div dir="rtl">

يوفّر AgentRadio ثلاث عمليات لكل وكيل:

</div>

| العملية الأولية | السلوك |
|---|---|
| `create_thread(name, participants)` | يفتح محادثة مسمّاة على خادم الرسائل ويعيد معرّفها. |
| `send_message(thread, content, mentions)` | يضيف رسالة إلى خيط ويعود فورًا، سواء أكان أحد يستمع أم لا. ويمكنه الإشارة إلى وكلاء بعينهم بعلامة @. |
| `wait_for_mention(timeout)` | يحجب التنفيذ حتى تصل رسالة تُشير إلى المُستدعي، ثم يعيدها مع لقطة كاملة لكل الخيوط، فلا يحتاج المُستدعي إلى قراءة ثانية لإعادة بناء السياق. |

<div dir="rtl">

لا تتخذ هذه الطبقة موقفًا بشأن <i>متى</i> يستمع الوكيل. فموضع تشغيل <code>wait_for_mention</code> هو درجة
الحرية الوحيدة التي تفصل بين نمطي التواصل:

<ul>
<li><b>في المقدمة</b> ← <i>استقبال حاجب</i>. يتوقف الوكيل عن العمل كي يستمع، فكل رسالة يسمعها تكلّفه
خطوة عمل. وهذا هو خط الأساس L2.</li>
<li><b>مهمة في الخلفية</b> ← <i>وعي سلبي</i>. يواصل الوكيل العمل، وتظهر أي إشارة عند حدّ الخطوة
التالية دون إنفاق أي خطوة على الاستماع. وهذا هو L3، أي AgentRadio الكامل.</li>
</ul>

كل ما عدا ذلك — العمليات الأولية والخيوط والبروتوكول — يبقى ثابتًا. وهذا الفارق بمقدار «بِت واحد»
هو تحديدًا ما تعزله التجارب.

</div>

### بروتوكول المراحل الخمس

<div dir="rtl">

ينفّذ أربعة وكلاء بروتوكولًا ثابتًا لتقسيم العمل والتفاوض. ويؤدي agent-1 دورًا إضافيًا بوصفه
<b>المُجمِّع</b>: فهو يفتح خيوط التخطيط وسجل العمل والإجابة النهائية، ويتحكم بكل انتقال — إذ لا
تنتهي أي مرحلة إلا بعد أن يجمع موافقة صريحة من كل وكيل.

<ol>
<li><b>P1 · الاستكشاف</b> — يبدأ كل وكيل مراقِبه في الخلفية، ويستكشف المستودع باستقلالية، ويصوغ
الأسئلة الفرعية التي يراها. ولا يُرسَل شيء في هذه المرحلة.</li>
<li><b>P2 · التقسيم</b> — يفتح المُجمِّع خيط تخطيط. يجمع الوكلاء اكتشافاتهم، ويتفاوضون على تقسيم
الأسئلة الفرعية، ويراجعونه حتى يوافق الجميع.</li>
<li><b>P3 · التنفيذ</b> — يعمل كل وكيل على أسئلته الفرعية. ويؤدي أي اكتشاف إلى نشر فوري في سجل
العمل: اكتشاف يمسّ زميلًا، أو تناقض مع الخطة المتفق عليها، أو عقبة، أو طريق مسدود تم التخلي عنه.</li>
<li><b>P4 · المراجعة</b> — يبثّ كل وكيل اكتشافاته مع الأدلة في خيط نتائجه الخاص. وينشر المراجعون
التعارضات الواقعية والأدلة الضعيفة والملاحظات غير المذكورة، ويمكنهم إعادة سؤال فرعي إلى P3.</li>
<li><b>P5 · التسليم</b> — يؤلّف المُجمِّع الإجابة النهائية من النتائج المعتمدة، ويبثّ المسودة لجولة
موافقات أخيرة، ثم يسلّمها.</li>
</ol>

في الاستقبال الحاجب تُنفَّذ المراحل الخمس نفسها دون تغيير، لكن التشارك الحي في P3 يختفي: فسماع
رسالة يكلّف انتظارًا في المقدمة، فيصمت الوكلاء أثناء العمل، ولا يمكن لاكتشاف أن يصل إلى زميل قبل P4.

</div>

## 🗂️ بنية المستودع

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

<div dir="rtl">

يحتوي كل مجلد مهمة تحت <code>data/qa/</code> على التعليمات، وبيئة التنفيذ المثبّتة، ومجموعة معايير
التقييم التي يستخدمها المدقّق.

</div>

---

## 📦 الإعداد

<div dir="rtl">

تُنفَّذ التشغيلات داخل حاويات Docker على <a href="https://modal.com">Modal</a>، بتنسيق من
<a href="https://github.com/laude-institute/harbor">Harbor</a>. مهمة واحدة = حاوية واحدة تُشغّل خادم
الرسائل بالإضافة إلى أربعة وكلاء Claude Code.

</div>

### 1. Docker Desktop

<div dir="rtl">

ثبّته من https://www.docker.com/products/docker-desktop/ وتحقّق منه بالأمر <code>docker run hello-world</code>.

</div>

### 2. uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Harbor (مثبّت على 0.6.4)

<div dir="rtl">

إصدارات Harbor الأحدث (‏0.7 فما فوق) تتضمّن تغييرات كاسرة في الواجهة البرمجية تجعل هذه المحوِّلات
تفشل. ثبّت الإصدارات:

</div>

| المكوّن | الإصدار الصالح |
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

<div dir="rtl">

تحتاج إلى <b>اشتراك Claude Max</b> للوكلاء. ويحتاج المدقّق إضافةً إلى <b>مفتاح واجهة برمجة من Anthropic</b>.

</div>

### 6. ملف JAR الخاص بخادم الرسائل

<div dir="rtl">

يُستضاف ملف JAR بحجم 106 ميغابايت بوصفه أثرًا مجهول المصدر (فهو أكبر من أن يوضع في مستودع git).
المعامل <code>confirm=t</code> يتخطى صفحة فحص الملفات الكبيرة كي يحصل <code>curl</code> على الملف الثنائي مباشرة:

</div>

```bash
curl -L -o multi_agent/coral-server.jar \
  "https://drive.usercontent.google.com/download?id=17b40_1kXFrAC0pnN8w_7PPY13O7pYVke&export=download&confirm=t"
```

<div dir="rtl">

ترفع المحوِّلات هذا الملف إلى كل حاوية مهمة. ولا يلزم تشغيل أي شيء محليًا، ومن ثمّ لا حاجة إلى JDK محلي.

</div>

### 7. مساعد الرمز المميّز وملف ‎.env

```bash
cp run_config/qa/claude-token ~/.local/bin/claude-token
chmod +x ~/.local/bin/claude-token
cp .env.example .env      # then fill in your Anthropic API key
```

### قبل كل تشغيل: جدّد رمز OAuth

<div dir="rtl">

يتناوب رمز OAuth الخاص بـ Claude Code. وتحصل كل حاوية على لقطة ثابتة عند الإقلاع، والرمز المنتهي
يُنهي الوكلاء الأربعة جميعًا بخطأ 401 في منتصف التشغيل. جدّده قبل كل جلسة:

</div>

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

<a id="running"></a>

## ⚡ تشغيل التهيئات الأربع

<div dir="rtl">

تُنفَّذ كل الأوامر من جذر المستودع بعد <code>source .env</code>. ومعرّفات المهام هي أسماء المجلدات تحت
<code>data/qa/</code> (كرّر <code>-i</code> للتجميع، أو احذفه كليًا لتشغيل المهام الـ 124 جميعها).
والمعامل <code>-n</code> هو عدد المهام المتزامنة (مهمة واحدة = أربعة وكلاء في L1–L3).

</div>

### B0 — وكيل مفرد (خط الأساس)

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

### L1 — أربعة وكلاء + تقسيم العمل

<div dir="rtl">

يستكشف agent-1 لفترة وجيزة، ثم يقسّم السؤال، ويحلّ كل وكيل نصيبه باستقلالية. وتُدمج الإجابات دون مراجعة.

</div>

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

### L2 — + تفاوض (استقبال حاجب)

<div dir="rtl">

البروتوكول الكامل بمراحله الخمس — استكشاف مشترك، وتقسيم متفاوض عليه حتى الإجماع، وتنفيذ حيّ،
ومراجعة متبادلة، وتسليم مُجمَّع — لكن مع تشغيل <code>wait_for_mention</code> في <b>المقدمة</b>، فيتوقف
الوكلاء عن العمل كي يستمعوا.

</div>

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

### L3 — + وعي سلبي (AgentRadio الكامل)

<div dir="rtl">

البروتوكول نفسه، لكن <code>wait_for_mention</code> يعمل بوصفه <b>مهمة في الخلفية</b>: يواصل الوكلاء
العمل وتظهر الرسائل بين الخطوات. ولا يحصل Claude Code على أي إعداد MCP — إذ يمرّ كل التواصل عبر
أغلفة الصدفة الخفيفة في <code>passive_scripts/</code>.

</div>

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

<div dir="rtl">

يغلّف <code>run_config/qa/run_passive_multi_agent.sh</code> الأمر نفسه بوصفه مشغّلًا دفعيًا، بوظيفة
harbor واحدة لكل معرّف مهمة.

</div>

---

## 🔀 التشغيل باستخدام DeepSeek-V4-Pro

<div dir="rtl">

يمكن تشغيل التهيئات متعددة الوكلاء (‏L1–L3) بوكلاء <b>DeepSeek-V4-Pro</b> بدلاً من Opus 4.6، بما
يعيد إنتاج عمود DeepSeek في جدول النتائج. البروتوكول والموجّهات وسكربتات الإقلاع وحارس الاستئناف
كلها متطابقة، ولا يتغيّر سوى الواجهة الخلفية للنموذج.

لا يتحدث Claude Code سوى واجهة Anthropic Messages، بينما يُقدَّم DeepSeek عبر OpenRouter (المتوافقة
مع OpenAI فقط). ونجسر بينهما بـ<b>وسيط ترجمة LiteLLM مُستضاف مرة واحدة على Modal</b>. ولا تثبّت
حاويات المهام أي شيء — إذ توجّه <code>ANTHROPIC_BASE_URL</code> فقط إلى العنوان العام للوسيط.

أما مدقّق معايير التقييم فلم يتغيّر: فهو ما زال يستخدم حَكَم Anthropic لديك
(<code>OPENAI_API_KEY</code> / <code>EVAL_MODEL</code>). و DeepSeek هو الواجهة الخلفية <i>للوكيل</i> فقط.

</div>

### إعداد الوسيط لمرة واحدة

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

<div dir="rtl">

يبقى الوسيط دافئًا (<code>min_containers=1</code>)؛ ولا تُعِد نشره إلا بعد تعديله. ولإيقاف الفوترة
عند الخمول: <code>modal app stop deepseek-litellm-proxy</code> (ويعيده أمر <code>modal deploy</code> لاحقًا).

</div>

### L1 / L2 / L3 مع DeepSeek

<div dir="rtl">

مطابقة لأوامر Opus أعلاه، لكن مسار الاستيراد يشير إلى محوِّل DeepSeek، ويوجّه
<code>-m "deepseek-v4-pro"</code> الطلبات عبر الوسيط. ويجب أن يكون <code>source .env</code> قد صدّر
<code>AGENTRADIO_PROXY_URL</code>. أما معرّفات المهام والتجميع بـ <code>-i</code> فيعملان تمامًا كما سبق.

</div>

#### DeepSeek B0 — وكيل مفرد (خط الأساس)

<div dir="rtl">

يستخدم خط أساس DeepSeek صنفًا فرعيًا خفيفًا من وكيل <code>claude-code</code> المدمج (يفرض نقطة نهاية
الوسيط ويتخلّص من رمز OAuth الذي كان الوكيل المدمج سيعيد إصداره)، ولذلك يأخذ
<code>--agent-import-path</code> بدلاً من <code>-a claude-code</code>.

</div>

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

#### DeepSeek L1 — تقسيم فقط

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

#### DeepSeek L2 — + تفاوض

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

#### DeepSeek L3 — + وعي سلبي

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

<div dir="rtl">

يوجد حَقن الوسيط المشترك (الذي يبدّل الواجهة الخلفية للنموذج مع وراثة كل منطق تعدّد الوكلاء
وسكربتات الإقلاع وحارس الاستئناف) في <code>multi_agent/deepseek_proxy.py</code>؛ أما الصنف الفرعي
لخط الأساس B0 فهو <code>multi_agent/claude_code_deepseek.py</code>.

</div>

### استئناف وظيفة أُلغيت أو أخفقت

```bash
source .env
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
harbor job resume -p results/qa/<job-name> -f CancelledError -f RuntimeError
```

### المراقبة الحيّة (اختياري، في طرفية منفصلة)

```bash
bash multi_agent/monitor_coral_log.sh   # renders coral://state from the running container
```

---

## 🧪 التقييم

<div dir="rtl">

تكتب كل تجربة إجابة الفريق في <code>&lt;trial&gt;/agent/answer.txt</code>. قيّمها بحَكَم النموذج اللغوي
الخاص بالمعيار:

</div>

```bash
source .env
python3 verify_local.py <task-id> <trial-dir>
# e.g.
python3 verify_local.py task-6905333b74f22949d97ba998 \
  results/qa/divneg-ba998/task-6905333b74f22949d97ba998__XXXXX
```

<div dir="rtl">

يكتب هذا الأمر <code>&lt;trial&gt;/verifier/reward.txt</code> (ويكون 1 فقط عندما تجتاز كل المعايير)
و<code>evaluation_results.json</code> (الدرجات لكل معيار). ونفّذ <code>pip install openai</code> إن لم تكن مثبتة.

</div>

### بنية مخرجات التجربة

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

<a id="results"></a>

## 📊 النتائج

<div dir="rtl">

النتائج الكاملة على SWE-Atlas QnA (‏124 مهمة، 1,306 معايير تقييم). تعطي صفوف الفئات عدد المهام
المحلولة، مع حجم الفئة بين قوسين. وداخل كل عمود نموذج، تستخدم جميع التهيئات الـ harness والإعدادات
نفسها.

<code>B0</code> = وكيل Claude Code مفرد · <code>L1</code> = ‏4× Claude Code + تقسيم العمل ·
<code>L2</code> = ‏L1 + تفاوض · <code>L3</code> = ‏L2 + وعي سلبي (AgentRadio).

</div>

**Opus 4.6**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| البنية وتصميم الأنظمة (44) | 15 | 13 | 24 | **30** |
| تحليل السبب الجذري (37) | 9 | 16 | 18 | **20** |
| التعرّف على قاعدة الشيفرة (28) | 11 | 12 | 14 | **18** |
| الأمن (11) | 4 | **7** | **7** | **7** |
| تكامل الواجهات والمكتبات (4) | 1 | 1 | 1 | **2** |
| **المهام المحلولة (124)** | 40 | 49 | 64 | **77** |
| **دقة المهام (%)** | 32.3 | 39.5 | 51.6 | **62.1** |
| **معدل اجتياز المعايير (%)** | 84.2 | 86.1 | 91.3 | **93.1** |

**DeepSeek V4 Pro**

| | B0 | L1 | L2 | L3 |
|---|:---:|:---:|:---:|:---:|
| البنية وتصميم الأنظمة (44) | 14 | 13 | 17 | **24** |
| تحليل السبب الجذري (37) | 11 | 13 | 15 | **18** |
| التعرّف على قاعدة الشيفرة (28) | 7 | 8 | 10 | **13** |
| الأمن (11) | 4 | 4 | 6 | **7** |
| تكامل الواجهات والمكتبات (4) | 0 | 0 | 1 | **1** |
| **المهام المحلولة (124)** | 36 | 39 | 49 | **63** |
| **دقة المهام (%)** | 29.0 | 31.4 | 39.5 | **50.8** |
| **معدل اجتياز المعايير (%)** | 81.2 | 83.7 | 85.9 | **90.2** |

<div dir="rtl">

<b>L3 مقابل L2، اختبار مكنمار الدقيق على نتائج المهام المزدوجة</b> — ‏Opus 4.6: يربح 15 ويخسر 2،
‏p = 0.0023. و DeepSeek V4 Pro: يربح 17 ويخسر 3، ‏p = 0.0026.

يُظهر التحليل على مستوى معايير التقييم أن مكسب الوعي السلبي يتزايد مع صعوبة المهمة، وهو ما يتسق
مع كون التصحيح في منتصف الطريق هو الآلية الكامنة وراءه.

</div>

---

## 🛠️ حلّ المشكلات

<div dir="rtl">

<ul>
<li><b>أخطاء 401 في منتصف التشغيل</b> — انتهت صلاحية لقطة رمز OAuth. جدّدها (انظر أعلاه) ثم نفّذ
<code>harbor job resume -p results/qa/&lt;job-name&gt; -f NonZeroAgentExitCodeError</code>.</li>
<li><b>‏<code>claude: not found</code> في coral-server.log</b> — تصدّر سكربتات الإقلاع
<code>PATH="$HOME/.local/bin:$PATH"</code>؛ تحقّق من أن Claude Code قد ثُبّت داخل الحاوية.</li>
<li><b>المهام المبنية على Alpine</b> — تستخدم بعض المهام صور Alpine؛ وتكتشف المحوِّلات ذلك تلقائيًا
وتثبّت JDK متوافقًا مع Alpine.</li>
<li><b>فحص التواصل</b> —
<code>grep "sent message\|created thread" &lt;trial&gt;/agent/coral-server.log | sed 's/\x1b\[[0-9;]*m//g'</code></li>
</ul>

</div>

---

## 🙏 شكر وتقدير

<div dir="rtl">

بيانات المهام مأخوذة من معيار <a href="https://github.com/scaleapi/SWE-Atlas">SWE-Atlas QnA</a>
(مجموعة بيانات harbor باسم <code>scale-ai/swe-atlas-qna</code>) من Scale AI. وتُنسَّق التشغيلات
بواسطة <a href="https://github.com/laude-institute/harbor">Harbor</a> على
<a href="https://modal.com">Modal</a>.

</div>

---

## 📚 الاستشهاد

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

## 📄 الرخصة

<div dir="rtl">

يُنشر بموجب <a href="LICENSE">رخصة Apache 2.0</a>.

</div>

---

<div dir="rtl">

طُوِّر في Coral AI Labs، و SnT — جامعة لوكسمبورغ، وكينغز كوليدج لندن، وجامعة هَل.

</div>
