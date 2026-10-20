import os
from ebooklib import epub

book = epub.EpubBook()
book.set_identifier('daily-english-reading-lesson-01')
book.set_title('Lesson 01: The 15-Minute Morning Reset')
book.set_language('zh-CN')
book.add_author('Daily English Reading Tutor')

# CSS Style
style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    line-height: 1.8;
    color: #1f2937;
    padding: 10px 14px;
}

h1, h2, h3, h4 {
    color: #111827;
    font-weight: 700;
}

h1 { font-size: 1.5rem; margin-bottom: 0.5rem; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; }
h2 { font-size: 1.25rem; margin-top: 1.5rem; margin-bottom: 0.8rem; color: #1d4ed8; }
h3 { font-size: 1.1rem; margin-top: 1.2rem; margin-bottom: 0.6rem; color: #374151; }

.passage {
    font-family: Georgia, Cambria, "Times New Roman", serif;
    font-size: 1.08rem;
    line-height: 2.1;
    margin: 1rem 0;
    padding: 14px 18px;
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
}

.passage p {
    margin-bottom: 1.2rem;
}
.passage p:last-child {
    margin-bottom: 0;
}

/* Syntax Dissection Visual Lines (Clean, no brackets, pure styling) */
.s { border-bottom: 2px solid #2563eb; }
.v { border-bottom: 2px solid #059669; font-weight: 600; }
.o { border-bottom: 2px solid #7c3aed; }
.adv { border-bottom: 1.5px dashed #d97706; }
.part { border-bottom: 1.5px dotted #0891b2; }
.clause { border-bottom: 1.5px dashed #64748b; }

/* Legend Box */
.legend-box {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 16px;
    font-size: 0.88rem;
    line-height: 1.8;
}

.legend-item {
    display: inline-block;
    margin-right: 12px;
}

/* Card */
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 14px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.card-sentence {
    font-family: Georgia, serif;
    font-size: 1.05rem;
    line-height: 1.9;
    color: #0f172a;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px dashed #e2e8f0;
}

.card-backbone {
    font-size: 0.92rem;
    font-weight: 600;
    color: #1e40af;
    margin-bottom: 8px;
}

.card-detail {
    font-size: 0.88rem;
    color: #475569;
    line-height: 1.7;
}

.card-detail-item {
    margin: 4px 0;
}

.card-detail-item b {
    color: #1e293b;
}

/* Vocabulary Item */
.vocab-item {
    margin: 16px 0;
    padding: 12px 14px;
    background: #f8fafc;
    border-left: 3px solid #10b981;
    border-radius: 0 6px 6px 0;
}
.vocab-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #065f46;
}
.vocab-meta {
    font-size: 0.85rem;
    color: #64748b;
    margin: 2px 0 6px 0;
}
.vocab-def {
    font-size: 0.92rem;
    color: #334155;
    margin-bottom: 6px;
}
.vocab-example {
    font-size: 0.88rem;
    color: #475569;
    font-style: italic;
    background: #ffffff;
    padding: 6px 10px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

.bilingual-pair {
    margin: 14px 0;
    padding: 12px 14px;
    border-bottom: 1px solid #e2e8f0;
}
.bilingual-en {
    font-family: Georgia, serif;
    font-size: 1.02rem;
    line-height: 1.8;
    color: #1e293b;
    margin-bottom: 6px;
}
.bilingual-zh {
    font-size: 0.92rem;
    line-height: 1.7;
    color: #475569;
}
'''

default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
book.add_item(default_css)

# Chapter 1: Introduction & Blind Reading
c1 = epub.EpubHtml(title='1. 原文导读（沉浸盲读版）', file_name='chap_01.xhtml', lang='zh-CN')
c1.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>1. 原文导读（沉浸盲读版）</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>Lesson 01: The 15-Minute Morning Reset</h1>
    <p><b>建议难度</b>：CEFR B1-B2 · <b>预计用时</b>：10-15分钟</p>
    
    <h2>读前思考 (Warm-up)</h2>
    <p><i>What is the very first thing you do after turning off your alarm in the morning? Do you usually check your phone right away?</i></p>

    <h2>沉浸盲读全文</h2>
    <p style="font-size: 0.9rem; color: #64748b;">💡 建议第一遍不查词、不分心，顺畅通读，抓住文章整体大意：</p>
    
    <div class="passage">
        <p>Most of us start our day <b>in a rush</b>, <b>reaching for</b> our phones before our feet even touch the floor. We <b>scroll through</b> unread messages, skim social media headlines, and immediately let other people's priorities <b>dictate</b> our mood.</p>
        <p>However, adopting a simple "15-minute reset" can fundamentally transform how your workday <b>unfolds</b>. Instead of <b>diving straight into</b> your inbox, dedicate the first quarter-hour of your morning to intentional calm. You might brew a cup of coffee without screens nearby, stretch by an open window, or <b>jot down</b> three realistic goals for the day.</p>
        <p>Neuroscientists suggest that our brains are particularly impressionable right after waking up. When you protect this brief window from digital noise, you give yourself space to prioritize what truly matters. It is not about waking up at 5 a.m. or building an elaborate routine; it is simply about <b>taking ownership of</b> the start of your day before the world demands your attention.</p>
    </div>
</body>
</html>
'''
c1.add_item(default_css)
book.add_item(c1)

# Chapter 2: Syntax Dissection (Pure CSS Underlines)
c2 = epub.EpubHtml(title='2. 句法透视精读（无括号·视觉划线版）', file_name='chap_02.xhtml', lang='zh-CN')
c2.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>2. 句法透视精读（无括号·视觉划线版）</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>2. 英文原文（句法透视精读版）</h1>
    
    <div class="legend-box">
        <b>💡 句法视觉透视指引（100%纯英文，零括号干扰）：</b><br/>
        <span class="legend-item"><span class="s">主语 (S)</span> 蓝实线</span>
        <span class="legend-item"><span class="v">谓语动词 (V)</span> 绿实线加粗</span>
        <span class="legend-item"><span class="o">宾语/表语 (O/P)</span> 紫实线</span>
        <span class="legend-item"><span class="adv">状语修饰</span> 橙色虚线</span>
        <span class="legend-item"><span class="part">伴随/定语</span> 青色点线</span>
        <span class="legend-item"><span class="clause">从句边界</span> 灰虚线</span>
    </div>

    <div class="passage">
        <p>
            <span class="s">Most of us</span>
            <span class="v">start</span>
            <span class="o">our day</span>
            <span class="adv">in a rush</span>,
            <span class="part">reaching for our phones</span>
            <span class="clause">before our feet even touch the floor</span>.
            <span class="s">We</span>
            <span class="v">scroll through</span>
            <span class="o">unread messages</span>,
            <span class="v">skim</span>
            <span class="o">social media headlines</span>, and
            <span class="adv">immediately</span>
            <span class="v">let</span>
            <span class="o">other people's priorities</span>
            <span class="part">dictate our mood</span>.
        </p>

        <p>
            <span class="adv">However</span>,
            <span class="s">adopting a simple "15-minute reset"</span>
            <span class="adv">fundamentally</span>
            <span class="v">can transform</span>
            <span class="o">how your workday unfolds</span>.
            <span class="adv">Instead of diving straight into your inbox</span>,
            <span class="v">dedicate</span>
            <span class="o">the first quarter-hour of your morning</span>
            <span class="adv">to intentional calm</span>.
            <span class="s">You</span>
            <span class="v">might brew</span>
            <span class="o">a cup of coffee</span>
            <span class="adv">without screens nearby</span>,
            <span class="v">stretch</span>
            <span class="adv">by an open window</span>, or
            <span class="v">jot down</span>
            <span class="o">three realistic goals for the day</span>.
        </p>

        <p>
            <span class="s">Neuroscientists</span>
            <span class="v">suggest</span>
            <span class="o">that our brains are particularly impressionable right after waking up</span>.
            <span class="clause">When you protect this brief window from digital noise</span>,
            <span class="s">you</span>
            <span class="v">give</span>
            <span class="o">yourself</span>
            <span class="o">space</span>
            <span class="part">to prioritize what truly matters</span>.
            <span class="s">It</span>
            <span class="v">is not about</span>
            <span class="o">waking up at 5 a.m. or building an elaborate routine</span>;
            <span class="s">it</span>
            <span class="adv">simply</span>
            <span class="v">is about</span>
            <span class="o">taking ownership of the start of your day</span>
            <span class="clause">before the world demands your attention</span>.
        </p>
    </div>
</body>
</html>
'''
c2.add_item(default_css)
book.add_item(c2)

# Chapter 3: Sentence-by-Sentence Breakdown Cards
c3 = epub.EpubHtml(title='3. 逐句句法骨架与修饰深度解剖', file_name='chap_03.xhtml', lang='zh-CN')
c3.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>3. 逐句句法骨架与修饰深度解剖</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>3. 逐句句法骨架与修饰深度解剖</h1>
    <p style="font-size: 0.9rem; color: #64748b;">剥离修饰层级，看清地道英语的句法脊梁：</p>

    <!-- Sentence 1 -->
    <div class="card">
        <div class="card-sentence">
            <span class="s">Most of us</span> <span class="v">start</span> <span class="o">our day</span> <span class="adv">in a rush</span>, <span class="part">reaching for our phones</span> <span class="clause">before our feet even touch the floor</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：主语 Most of us ➔ 谓语 start ➔ 宾语 our day</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 方式状语</b>：in a rush（介词短语修饰 start，描绘匆忙慌乱状态）</div>
            <div class="card-detail-item"><b>✂️ 伴随状语</b>：reaching for our phones（现在分词短语作伴随，与开启一天同时发生）</div>
            <div class="card-detail-item"><b>✂️ 时间从句</b>：before our feet even touch the floor（时间状语从句，描写脚还没踩到地板的瞬间）</div>
        </div>
    </div>

    <!-- Sentence 2 -->
    <div class="card">
        <div class="card-sentence">
            <span class="s">We</span> <span class="v">scroll through</span> <span class="o">unread messages</span>, <span class="v">skim</span> <span class="o">social media headlines</span>, and <span class="adv">immediately</span> <span class="v">let</span> <span class="o">other people's priorities</span> <span class="part">dictate our mood</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：主语 We ➔ 谓语 1 scroll through ➔ 谓语 2 skim ➔ 谓语 3 let</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 并列结构</b>：动词短语三连动，生动勾勒现代人醒后的自动化动作</div>
            <div class="card-detail-item"><b>✂️ 宾语补足语</b>：dictate our mood（使役动词 let 的省略 to 不定式短语，说明情绪被外界摆布）</div>
        </div>
    </div>

    <!-- Sentence 3 -->
    <div class="card">
        <div class="card-sentence">
            <span class="adv">However</span>, <span class="s">adopting a simple "15-minute reset"</span> <span class="adv">fundamentally</span> <span class="v">can transform</span> <span class="o">how your workday unfolds</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：动名词主语 adopting... ➔ 谓语 can transform ➔ 宾语从句 how your workday unfolds</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 逻辑副词</b>：However（转折衔接）· fundamentally（程度副词修饰 transform）</div>
            <div class="card-detail-item"><b>✂️ 宾语从句</b>：how 引导的名词性从句，从句内 workday 为主语，unfolds 为谓语动词</div>
        </div>
    </div>

    <!-- Sentence 4 -->
    <div class="card">
        <div class="card-sentence">
            <span class="adv">Instead of diving straight into your inbox</span>, <span class="v">dedicate</span> <span class="o">the first quarter-hour of your morning</span> <span class="adv">to intentional calm</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：祈使句省略主语 you ➔ 谓语 dedicate ➔ 宾语 the first quarter-hour...</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 让步状语</b>：Instead of diving straight into your inbox（介词短语作状语）</div>
            <div class="card-detail-item"><b>✂️ 句型搭配</b>：dedicate A to B（把 A 留给/奉献给 B）</div>
        </div>
    </div>

    <!-- Sentence 5 -->
    <div class="card">
        <div class="card-sentence">
            <span class="s">You</span> <span class="v">might brew</span> <span class="o">a cup of coffee</span> <span class="adv">without screens nearby</span>, <span class="v">stretch</span> <span class="adv">by an open window</span>, or <span class="v">jot down</span> <span class="o">three realistic goals for the day</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：主语 You ➔ 情态动词 might 统领并列动词 brew、stretch 与 jot down</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 伴随修饰</b>：without screens nearby（介词短语修饰喝咖啡）</div>
            <div class="card-detail-item"><b>✂️ 地点状语</b>：by an open window（修饰拉伸）</div>
        </div>
    </div>

    <!-- Sentence 6 -->
    <div class="card">
        <div class="card-sentence">
            <span class="s">Neuroscientists</span> <span class="v">suggest</span> <span class="o">that our brains are particularly impressionable right after waking up</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：主语 Neuroscientists ➔ 谓语 suggest ➔ 宾语从句 that...</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 宾语从句内部</b>：our brains（主）+ are（系）+ impressionable（表）+ right after waking up（时间状语）</div>
        </div>
    </div>

    <!-- Sentence 7 -->
    <div class="card">
        <div class="card-sentence">
            <span class="clause">When you protect this brief window from digital noise</span>, <span class="s">you</span> <span class="v">give</span> <span class="o">yourself</span> <span class="o">space</span> <span class="part">to prioritize what truly matters</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：主语 you ➔ 双宾谓语 give ➔ 间宾 yourself ➔ 直宾 space</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 时间条件从句</b>：When 引导，内含 protect A from B（保护 A 免受 B 干扰）</div>
            <div class="card-detail-item"><b>✂️ 后置定语</b>：不定式 to prioritize what truly matters 修饰 space</div>
        </div>
    </div>

    <!-- Sentence 8 -->
    <div class="card">
        <div class="card-sentence">
            <span class="s">It</span> <span class="v">is not about</span> <span class="o">waking up at 5 a.m. or building an elaborate routine</span>; <span class="s">it</span> <span class="adv">simply</span> <span class="v">is about</span> <span class="o">taking ownership of the start of your day</span> <span class="clause">before the world demands your attention</span>.
        </div>
        <div class="card-backbone">🦴 核心主干：对仗句型 It is not about A ; it is simply about B</div>
        <div class="card-detail">
            <div class="card-detail-item"><b>✂️ 介词宾语对仗</b>：并列动名词 waking up... or building... 与 taking ownership of...</div>
            <div class="card-detail-item"><b>✂️ 拟人化从句</b>：before the world demands your attention（在世界索取你的注意力之前）</div>
        </div>
    </div>
</body>
</html>
'''
c3.add_item(default_css)
book.add_item(c3)

# Chapter 4: Vocabulary
c4 = epub.EpubHtml(title='4. 核心词汇与地道搭配', file_name='chap_04.xhtml', lang='zh-CN')
c4.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>4. 核心词汇与地道搭配</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>4. 核心词汇与地道搭配</h1>

    <div class="vocab-item">
        <div class="vocab-title">1. in a rush</div>
        <div class="vocab-meta">/ɪn ə rʌʃ/ · 介词短语</div>
        <div class="vocab-def"><b>释义</b>：仓促地、匆匆忙忙地（= in a hurry）。常与 start the day, leave the house 搭配。</div>
        <div class="vocab-example">"I was in such a rush this morning that I forgot my laptop charger."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">2. reach for sth</div>
        <div class="vocab-meta">/riːtʃ fɔːr/ · 短语动词</div>
        <div class="vocab-def"><b>释义</b>：伸手去够、伸手去拿。常用于下意识动作：reach for the phone / mug / wallet。</div>
        <div class="vocab-example">"He reached for his phone as soon as he heard the notification chime."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">3. dictate</div>
        <div class="vocab-meta">/dɪkˈteɪt/ · 及物动词</div>
        <div class="vocab-def"><b>释义</b>：左右、支配、决定（情绪、结果、方向）。常见搭配 dictate terms / dictate your mood。</div>
        <div class="vocab-example">"Don't let a bad morning meeting dictate the rest of your day."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">4. unfold</div>
        <div class="vocab-meta">/ʌnˈfəʊld/ · 动词</div>
        <div class="vocab-def"><b>释义</b>：（事件、一天）展开、呈现、一步步发展。常说 how the day unfolds。</div>
        <div class="vocab-example">"Let's see how the situation unfolds before making a final decision."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">5. dive into sth (dive straight into)</div>
        <div class="vocab-meta">/daɪv ˈɪntuː/ · 短语动词</div>
        <div class="vocab-def"><b>释义</b>：一头扎进、立即全力投入。比 start 更生动传神。</div>
        <div class="vocab-example">"Let's skip the small talk and dive straight into the code review."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">6. jot down</div>
        <div class="vocab-meta">/dʒɒt daʊn/ · 短语动词</div>
        <div class="vocab-def"><b>释义</b>：随手记下、匆匆写下（简短要点）。比 write down 更轻量随意。</div>
        <div class="vocab-example">"Let me jot down your email address so I don't forget it."</div>
    </div>

    <div class="vocab-item">
        <div class="vocab-title">7. take ownership of</div>
        <div class="vocab-meta">/teɪk ˈəʊnəʃɪp ɒv/ · 动词短语</div>
        <div class="vocab-def"><b>释义</b>：掌控、承担起……的责任、主动主导。职场高频表达。</div>
        <div class="vocab-example">"Great engineers take full ownership of their projects from start to finish."</div>
    </div>
</body>
</html>
'''
c4.add_item(default_css)
book.add_item(c4)

# Chapter 5: Bilingual Reference
c5 = epub.EpubHtml(title='5. 全文中英双语对照与文化小贴士', file_name='chap_05.xhtml', lang='zh-CN')
c5.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>5. 全文中英双语对照与文化小贴士</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>5. 全文中英双语对照</h1>

    <div class="bilingual-pair">
        <div class="bilingual-en">Most of us start our day in a rush, reaching for our phones before our feet even touch the floor. We scroll through unread messages, skim social media headlines, and immediately let other people's priorities dictate our mood.</div>
        <div class="bilingual-zh">我们大多数人都在匆忙中开始新的一天，双脚还没踩到地板，手就已经伸向了手机。我们刷着未读消息，扫一眼社交媒体头条，立刻让别人的琐事左右了自己的情绪。</div>
    </div>

    <div class="bilingual-pair">
        <div class="bilingual-en">However, adopting a simple "15-minute reset" can fundamentally transform how your workday unfolds. Instead of diving straight into your inbox, dedicate the first quarter-hour of your morning to intentional calm. You might brew a cup of coffee without screens nearby, stretch by an open window, or jot down three realistic goals for the day.</div>
        <div class="bilingual-zh">然而，建立一个简单的“15分钟晨间重置”，就能从根本上改变你整个工作日的展开方式。与其一头扎进收件箱，不如把清晨的最初一刻钟留给从容平静。你可以冲一杯咖啡，身边不放任何屏幕；可以在开着的窗边伸展一下身体；或者随手写下今天三个切实可行的目标。</div>
    </div>

    <div class="bilingual-pair">
        <div class="bilingual-en">Neuroscientists suggest that our brains are particularly impressionable right after waking up. When you protect this brief window from digital noise, you give yourself space to prioritize what truly matters. It is not about waking up at 5 a.m. or building an elaborate routine; it is simply about taking ownership of the start of your day before the world demands your attention.</div>
        <div class="bilingual-zh">神经科学家指出，我们的大脑在刚睡醒时极易受到外界刺激影响。当你守护好这短暂的一小段时间、远离数字噪音时，你就为自己留出了辨明真正要事的空间。这并不是要求你早上 5 点起床，或是制定一套繁琐的仪式；这仅仅是让你在这个世界向你索取注意力之前，先拿回属于自己一天的掌控权。</div>
    </div>

    <h2>💡 语境与避坑小贴士</h2>
    <p><b>quarter-hour vs. 15 minutes</b>：在日常口语和书面语中，英美人士极其习惯使用 <i>a quarter of an hour</i> 或 <i>quarter-hour</i> 来表达 15 分钟，就像用 <i>half an hour</i> 表达半小时一样普遍。</p>
    <p><b>中式英语避坑</b>：随手记笔记时，避免总是说 <i>write it on paper</i>，使用地道的短语动词 <b>jot down</b> 会让你的英语立刻鲜活起来。</p>
</body>
</html>
'''
c5.add_item(default_css)
book.add_item(c5)

# Chapter 6: Exercises
c6 = epub.EpubHtml(title='6. 随堂互动练习与参考答案', file_name='chap_06.xhtml', lang='zh-CN')
c6.content = '''
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>6. 随堂互动练习与参考答案</title>
    <link rel="stylesheet" href="style/default.css" type="text/css" />
</head>
<body>
    <h1>6. 随堂互动练习</h1>

    <h2>练习 1：阅读理解 (Comprehension)</h2>
    <p>According to the passage, why does the author suggest avoiding your phone or inbox during the first 15 minutes of the morning?</p>

    <h2>练习 2：选词填空 (Cloze)</h2>
    <p>从 <i>(in a rush / dive into / jot down / dictate)</i> 中选择合适短语填空：</p>
    <ol>
        <li>Don't let temporary frustration ________ your long-term career choices.</li>
        <li>She was ________ because her morning meeting started in five minutes.</li>
    </ol>

    <h2>练习 3：句型仿写 (Sentence Making)</h2>
    <p>使用句型 <b>give yourself space to + 动词原形</b> 写一个与你生活相关的句子。</p>

    <hr style="margin: 24px 0; border: none; border-top: 1px dashed #cbd5e1;" />

    <h2>💡 参考答案</h2>
    <p><b>练习 1</b>：Because our brains are very impressionable right after waking up, and checking phones immediately lets digital noise and other people's priorities dictate our mood.</p>
    <p><b>练习 2</b>：1. dictate · 2. in a rush</p>
    <p><b>练习 3（参考）</b>：<i>Taking a weekend break gives you space to reflect on what truly matters in your life.</i></p>
</body>
</html>
'''
c6.add_item(default_css)
book.add_item(c6)

# Table of Contents
book.toc = (
    c1,
    c2,
    c3,
    c4,
    c5,
    c6
)

# Spine
book.spine = ['nav', c1, c2, c3, c4, c5, c6]

# Add Navigation Files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Write EPUB file
output_path = 'english_reading_lesson_01.epub'
epub.write_epub(output_path, book, {})
print(f"Successfully generated {output_path}")
