# drift-cognition-training
<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Drift Cognition Series — Explosive Safety Training</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Epilogue:ital,wght@0,300;0,400;0,700;0,900;1,300&display=swap');

:root {
–bg: #08090b;
–surface: #0e1014;
–border: #1c2028;
–border2: #252b35;
–text: #dde3ec;
–mid: #7a8494;
–muted: #3d4452;
–accent: #bf3228;
–warn: #c97c20;
–green: #277a50;
–mono: ‘DM Mono’, monospace;
–head: ‘Epilogue’, sans-serif;
}

- { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
background: var(–bg);
color: var(–text);
font-family: var(–head);
min-height: 100vh;
overflow-x: hidden;
}

/* NOISE TEXTURE */
body::after {
content: ‘’;
position: fixed;
inset: 0;
background-image: url(“data:image/svg+xml,%3Csvg viewBox=‘0 0 256 256’ xmlns=‘http://www.w3.org/2000/svg’%3E%3Cfilter id=‘noise’%3E%3CfeTurbulence type=‘fractalNoise’ baseFrequency=‘0.9’ numOctaves=‘4’ stitchTiles=‘stitch’/%3E%3C/filter%3E%3Crect width=‘100%25’ height=‘100%25’ filter=‘url(%23noise)’ opacity=‘0.035’/%3E%3C/svg%3E”);
pointer-events: none;
z-index: 0;
}

/* TOP LINE */
.top-rule {
height: 2px;
background: linear-gradient(90deg, var(–accent) 0%, var(–warn) 50%, transparent 100%);
}

/* NAV */
nav {
position: relative;
z-index: 10;
display: flex;
justify-content: space-between;
align-items: center;
padding: 20px 48px;
border-bottom: 1px solid var(–border);
}

.nav-mark {
font-family: var(–mono);
font-size: 11px;
letter-spacing: 0.3em;
color: var(–muted);
text-transform: uppercase;
}

.nav-mark span { color: var(–accent); }

.nav-links {
display: flex;
gap: 32px;
list-style: none;
}

.nav-links a {
font-family: var(–mono);
font-size: 10px;
letter-spacing: 0.2em;
color: var(–mid);
text-decoration: none;
text-transform: uppercase;
transition: color 0.15s;
}

.nav-links a:hover { color: var(–text); }

/* HERO */
.hero {
position: relative;
z-index: 1;
padding: 100px 48px 80px;
max-width: 1100px;
margin: 0 auto;
display: grid;
grid-template-columns: 1fr auto;
gap: 60px;
align-items: end;
}

.hero-eyebrow {
font-family: var(–mono);
font-size: 10px;
letter-spacing: 0.4em;
color: var(–accent);
text-transform: uppercase;
margin-bottom: 20px;
display: flex;
align-items: center;
gap: 12px;
}

.eyebrow-line {
width: 40px;
height: 1px;
background: var(–accent);
}

h1 {
font-family: var(–head);
font-weight: 900;
font-size: clamp(56px, 9vw, 112px);
line-height: 0.88;
letter-spacing: -0.04em;
text-transform: uppercase;
color: var(–text);
margin-bottom: 32px;
}

h1 em {
display: block;
font-style: normal;
color: var(–accent);
-webkit-text-stroke: 1px var(–accent);
color: transparent;
}

.hero-desc {
font-size: 16px;
color: var(–mid);
line-height: 1.7;
font-weight: 300;
max-width: 520px;
margin-bottom: 40px;
}

.hero-actions {
display: flex;
gap: 12px;
flex-wrap: wrap;
}

.btn-primary {
display: inline-block;
background: var(–accent);
color: #fff;
font-family: var(–mono);
font-size: 11px;
letter-spacing: 0.2em;
text-transform: uppercase;
padding: 14px 28px;
text-decoration: none;
transition: background 0.15s;
}

.btn-primary:hover { background: #a82820; }

.btn-secondary {
display: inline-block;
background: transparent;
border: 1px solid var(–border2);
color: var(–mid);
font-family: var(–mono);
font-size: 11px;
letter-spacing: 0.2em;
text-transform: uppercase;
padding: 14px 28px;
text-decoration: none;
transition: all 0.15s;
}

.btn-secondary:hover { border-color: var(–mid); color: var(–text); }

.hero-stat-block {
display: flex;
flex-direction: column;
gap: 24px;
padding-bottom: 8px;
}

.hero-stat {
text-align: right;
padding-bottom: 20px;
border-bottom: 1px solid var(–border);
}

.hero-stat:last-child { border-bottom: none; padding-bottom: 0; }

.hs-num {
font-family: var(–head);
font-weight: 900;
font-size: 48px;
line-height: 1;
letter-spacing: -0.04em;
color: var(–text);
}

.hs-label {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.3em;
color: var(–muted);
text-transform: uppercase;
margin-top: 4px;
}

/* DIVIDER */
.section-divider {
max-width: 1100px;
margin: 0 auto;
padding: 0 48px;
display: flex;
align-items: center;
gap: 20px;
}

.divider-label {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.4em;
color: var(–muted);
text-transform: uppercase;
white-space: nowrap;
}

.divider-line {
flex: 1;
height: 1px;
background: var(–border);
}

/* MODULES SECTION */
.modules-section {
position: relative;
z-index: 1;
max-width: 1100px;
margin: 48px auto 0;
padding: 0 48px 80px;
}

.modules-grid {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 2px;
margin-top: 32px;
}

.mod-card {
background: var(–surface);
border: 1px solid var(–border);
padding: 28px;
text-decoration: none;
color: inherit;
display: block;
position: relative;
overflow: hidden;
transition: border-color 0.2s, background 0.2s;
}

.mod-card.live:hover {
border-color: var(–accent);
background: #111318;
}

.mod-card.upcoming {
opacity: 0.45;
cursor: default;
}

.mod-card::before {
content: attr(data-id);
position: absolute;
bottom: -16px;
right: 12px;
font-family: var(–head);
font-weight: 900;
font-size: 88px;
color: rgba(255,255,255,0.025);
line-height: 1;
pointer-events: none;
letter-spacing: -0.05em;
}

.card-top {
display: flex;
justify-content: space-between;
align-items: flex-start;
margin-bottom: 16px;
}

.card-id {
font-family: var(–mono);
font-size: 10px;
letter-spacing: 0.2em;
color: var(–muted);
}

.card-status {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.15em;
padding: 3px 8px;
text-transform: uppercase;
}

.s-live { background: rgba(39,122,80,0.15); color: var(–green); }
.s-next { background: rgba(201,124,32,0.15); color: var(–warn); }
.s-plan { background: rgba(61,68,82,0.3); color: var(–muted); }

.card-title {
font-family: var(–head);
font-weight: 700;
font-size: 20px;
color: var(–text);
letter-spacing: -0.02em;
margin-bottom: 8px;
line-height: 1.2;
}

.card-desc {
font-size: 12px;
color: var(–mid);
line-height: 1.6;
font-weight: 300;
margin-bottom: 20px;
}

.card-type {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.2em;
color: var(–muted);
text-transform: uppercase;
border-top: 1px solid var(–border);
padding-top: 14px;
}

.card-arrow {
display: inline-block;
margin-left: 8px;
transition: transform 0.15s;
color: var(–accent);
}

.mod-card.live:hover .card-arrow { transform: translateX(4px); }

/* DOCTRINE SECTION */
.doctrine-section {
position: relative;
z-index: 1;
background: var(–surface);
border-top: 1px solid var(–border);
border-bottom: 1px solid var(–border);
padding: 80px 48px;
}

.doctrine-inner {
max-width: 1100px;
margin: 0 auto;
display: grid;
grid-template-columns: 1fr 1fr;
gap: 80px;
align-items: center;
}

.doctrine-label {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.4em;
color: var(–accent);
text-transform: uppercase;
margin-bottom: 20px;
}

.doctrine-quote {
font-family: var(–head);
font-weight: 900;
font-size: 36px;
line-height: 1.1;
letter-spacing: -0.03em;
color: var(–text);
margin-bottom: 24px;
}

.doctrine-body {
font-size: 14px;
color: var(–mid);
line-height: 1.8;
font-weight: 300;
}

.loop-visual {
display: flex;
flex-direction: column;
gap: 2px;
}

.loop-step {
display: flex;
align-items: center;
gap: 16px;
padding: 14px 18px;
border: 1px solid var(–border);
background: var(–bg);
transition: background 0.15s;
}

.loop-step:hover { background: #111318; }

.loop-n {
font-family: var(–mono);
font-size: 10px;
color: var(–muted);
width: 24px;
flex-shrink: 0;
}

.loop-name {
font-family: var(–head);
font-weight: 700;
font-size: 14px;
flex: 1;
text-transform: uppercase;
letter-spacing: 0.03em;
}

.loop-step:nth-child(1) .loop-name { color: var(–green); }
.loop-step:nth-child(2) .loop-name { color: #8ab87a; }
.loop-step:nth-child(3) .loop-name { color: var(–warn); }
.loop-step:nth-child(4) .loop-name { color: #b85020; }
.loop-step:nth-child(5) .loop-name { color: var(–accent); }

.loop-tag {
font-family: var(–mono);
font-size: 9px;
color: var(–muted);
letter-spacing: 0.1em;
}

.interrupt-flag {
margin-top: 8px;
padding: 10px 18px;
background: rgba(39,122,80,0.08);
border: 1px solid rgba(39,122,80,0.25);
font-family: var(–mono);
font-size: 10px;
color: var(–green);
letter-spacing: 0.15em;
}

/* FOOTER */
footer {
position: relative;
z-index: 1;
padding: 40px 48px;
display: flex;
justify-content: space-between;
align-items: center;
border-top: 1px solid var(–border);
max-width: 100%;
}

.footer-mark {
font-family: var(–head);
font-weight: 900;
font-size: 18px;
letter-spacing: -0.03em;
color: var(–muted);
}

.footer-mark span { color: var(–accent); }

.footer-links {
display: flex;
gap: 28px;
list-style: none;
}

.footer-links a {
font-family: var(–mono);
font-size: 9px;
letter-spacing: 0.2em;
color: var(–muted);
text-decoration: none;
text-transform: uppercase;
transition: color 0.15s;
}

.footer-links a:hover { color: var(–text); }

.footer-copy {
font-family: var(–mono);
font-size: 9px;
color: var(–muted);
letter-spacing: 0.15em;
}

@media (max-width: 900px) {
nav { padding: 16px 24px; }
.nav-links { display: none; }
.hero { padding: 60px 24px 48px; grid-template-columns: 1fr; }
.hero-stat-block { flex-direction: row; justify-content: flex-start; }
.hero-stat { text-align: left; padding-bottom: 0; border-bottom: none; padding-right: 24px; border-right: 1px solid var(–border); }
.hero-stat:last-child { border-right: none; }
.hs-num { font-size: 32px; }
.section-divider, .modules-section { padding-left: 24px; padding-right: 24px; }
.modules-grid { grid-template-columns: 1fr; }
.doctrine-section { padding: 48px 24px; }
.doctrine-inner { grid-template-columns: 1fr; gap: 40px; }
footer { padding: 24px; flex-direction: column; gap: 20px; text-align: center; }
.footer-links { flex-wrap: wrap; justify-content: center; }
}
</style>

</head>
<body>

<div class="top-rule"></div>

<nav>
  <div class="nav-mark">DRIFT<span>.</span>COGNITION</div>
  <ul class="nav-links">
    <li><a href="#modules">Modules</a></li>
    <li><a href="#doctrine">Doctrine</a></li>
    <li><a href="drift-training-index.html">Full Index</a></li>
  </ul>
</nav>

<section class="hero">
  <div>
    <div class="hero-eyebrow"><span class="eyebrow-line"></span>Explosive Safety Training Program</div>
    <h1>Drift<em>Cognition</em>Series</h1>
    <p class="hero-desc">The cognitive skill that separates a technician from a strategist. Sensing invisible degradation before it becomes a hazard — the doctrine that will save lives in 2030–2050.</p>
    <div class="hero-actions">
      <a href="drift-cognition-training.html" class="btn-primary">Start DC-04 →</a>
      <a href="drift-training-index.html" class="btn-secondary">View Full Index</a>
    </div>
  </div>
  <div class="hero-stat-block">
    <div class="hero-stat">
      <div class="hs-num">8</div>
      <div class="hs-label">Total Modules</div>
    </div>
    <div class="hero-stat">
      <div class="hs-num">4</div>
      <div class="hs-label">Cognitive Layers</div>
    </div>
    <div class="hero-stat">
      <div class="hs-num">5</div>
      <div class="hs-label">Loop Stages</div>
    </div>
  </div>
</section>

<div class="section-divider">
  <span class="divider-label">Training Modules</span>
  <span class="divider-line"></span>
</div>

<section class="modules-section" id="modules">
  <div class="modules-grid">

```
<a href="drift-cognition-training.html" class="mod-card live" data-id="04">
  <div class="card-top">
    <div class="card-id">DC-04</div>
    <div class="card-status s-live">● Live</div>
  </div>
  <div class="card-title">Drift Cognition</div>
  <div class="card-desc">Four cognitive layers · Drift Loop · Red Flag signatures · Competency check with immediate feedback</div>
  <div class="card-type">Core Doctrine <span class="card-arrow">→</span></div>
</a>

<div class="mod-card upcoming" data-id="05">
  <div class="card-top">
    <div class="card-id">DC-05</div>
    <div class="card-status s-next">◐ Next</div>
  </div>
  <div class="card-title">Drift Pattern Library</div>
  <div class="card-desc">Deep reference for all six drift type signatures · Field identification exercises · Case matching</div>
  <div class="card-type">Pattern Recognition</div>
</div>

<div class="mod-card upcoming" data-id="06">
  <div class="card-top">
    <div class="card-id">DC-06</div>
    <div class="card-status s-plan">○ Planned</div>
  </div>
  <div class="card-title">Tacit Knowledge Capture</div>
  <div class="card-desc">January Capture Plan · Expert knowledge extraction · Structured handoff before rotation</div>
  <div class="card-type">Core Doctrine</div>
</div>

<div class="mod-card upcoming" data-id="07">
  <div class="card-top">
    <div class="card-id">DC-07</div>
    <div class="card-status s-plan">○ Planned</div>
  </div>
  <div class="card-title">AI Risk Reasoning</div>
  <div class="card-desc">GenAI hazard modeling · Teaching the agent Drift Cognition · Human-AI safety loop design</div>
  <div class="card-type">AI Integration</div>
</div>

<div class="mod-card upcoming" data-id="08">
  <div class="card-top">
    <div class="card-id">DC-08</div>
    <div class="card-status s-plan">○ Planned</div>
  </div>
  <div class="card-title">Consequence Mapping</div>
  <div class="card-desc">Second and third-order simulations · Cascading failure scenarios · Minden case study</div>
  <div class="card-type">Pattern Recognition</div>
</div>

<div class="mod-card upcoming" data-id="09+">
  <div class="card-top">
    <div class="card-id">DC-09–11</div>
    <div class="card-status s-plan">○ Planned</div>
  </div>
  <div class="card-title">Field & Integration</div>
  <div class="card-desc">Contractor Transparency · Leadership Handoff Safety · GenAI Agent Integration</div>
  <div class="card-type">Field Application + AI</div>
</div>
```

  </div>
</section>

<section class="doctrine-section" id="doctrine">
  <div class="doctrine-inner">
    <div>
      <div class="doctrine-label">Core Doctrine</div>
      <div class="doctrine-quote">"Systems fail slowly, then all at once."</div>
      <div class="doctrine-body">
        Drift Cognition is the mental skill that separates a technician from a strategist, and a safe installation from a future headline.<br><br>
        It is the ability to detect invisible degradation — shortcuts becoming normal, documentation becoming ritual, assumptions replacing verification — before any single failure becomes catastrophic.<br><br>
        Future warrants and safety officers must carry this skill in their heads, not just their checklists.
      </div>
    </div>
    <div>
      <div class="loop-visual">
        <div class="loop-step">
          <div class="loop-n">01</div>
          <div class="loop-name">Deviation</div>
          <div class="loop-tag">A shortcut enters the system</div>
        </div>
        <div class="loop-step">
          <div class="loop-n">02</div>
          <div class="loop-name">Normalization</div>
          <div class="loop-tag">"This is fine"</div>
        </div>
        <div class="loop-step">
          <div class="loop-n">03</div>
          <div class="loop-name">Institutionalization</div>
          <div class="loop-tag">"This is how we do it"</div>
        </div>
        <div class="loop-step">
          <div class="loop-n">04</div>
          <div class="loop-name">Blindness</div>
          <div class="loop-tag">Original standard is forgotten</div>
        </div>
        <div class="loop-step">
          <div class="loop-n">05</div>
          <div class="loop-name">☠ Catastrophe</div>
          <div class="loop-tag">System collapses</div>
        </div>
        <div class="interrupt-flag">▶ INTERRUPT AT STAGE 01 OR 02 — NOT AFTER</div>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="footer-mark">DRIFT<span>.</span>COGNITION</div>
  <ul class="footer-links">
    <li><a href="drift-cognition-training.html">DC-04 Module</a></li>
    <li><a href="drift-training-index.html">Training Index</a></li>
    <li><a href="notion-template.md">Notion Template</a></li>
  </ul>
  <div class="footer-copy">Explosive Safety Training · 2026</div>
</footer>

</body>
</html>