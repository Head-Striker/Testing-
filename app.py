
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="OBSCURA — Aura RNG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility:hidden;}
    .stApp {background:#070707;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {border:0 !important;}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root {
 --bg:#070707; --panel:#10100f; --line:#34302a;
 --muted:#8f897f; --text:#eee7d8; --gold:#c6a66b;
}
* {box-sizing:border-box}
html,body {
 margin:0; padding:0; background:var(--bg); color:var(--text);
 font-family:Arial,Helvetica,sans-serif;
}
button {font:inherit;cursor:pointer}
button:focus-visible {outline:2px solid #d8bd83;outline-offset:3px}
#app {max-width:1250px;margin:auto;padding:22px}
header {
 display:flex;align-items:center;justify-content:space-between;
 gap:15px;padding:10px 0 22px;border-bottom:1px solid #292621;
}
.brand {font-size:21px;font-weight:900;letter-spacing:7px}
.brand small {
 display:block;color:#8d8271;font-size:9px;letter-spacing:4px;
 margin-top:7px;font-weight:500;
}
.nav {display:flex;gap:8px;flex-wrap:wrap}
.nav button,.btn {
 background:#151411;border:1px solid #3b362c;color:#e9dfcc;
 padding:12px 15px;border-radius:5px;font-size:11px;
 letter-spacing:2px;transition:.2s;
}
.nav button:hover,.btn:hover {border-color:#c4a56a;background:#211d16}
.nav button.active {background:#c5a56a;color:#100e09;border-color:#c5a56a}
.scene {
 position:relative;margin-top:17px;height:520px;overflow:hidden;
 border:1px solid #363026;background:#080908;isolation:isolate;
}
#world {position:absolute;inset:0;width:100%;height:100%}
.scene:after {
 content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
 background:linear-gradient(180deg,#07070733 0%,transparent 25%,
 #07070700 70%,#070707bb 100%);
}
.scene-content {
 position:absolute;z-index:3;inset:0;display:flex;
 align-items:center;justify-content:center;flex-direction:column;
 text-align:center;pointer-events:none;padding:18px;
}
.kicker {font-size:10px;letter-spacing:6px;color:#b3a58b}
#name {
 margin-top:17px;font-size:clamp(32px,7vw,76px);font-weight:900;
 letter-spacing:4px;line-height:1.05;color:#eee7d8;
 text-shadow:0 0 28px #c9b48a44;overflow-wrap:anywhere;
}
#sub {margin-top:16px;font-size:11px;letter-spacing:4px;color:#c1b7a5}
#hint {margin-top:36px;font-size:10px;letter-spacing:3px;color:#777166}
#flash {
 position:absolute;inset:0;z-index:5;background:#f8e9c5;
 opacity:0;pointer-events:none;
}
.full-event {
 position:absolute;inset:0;z-index:6;display:none;overflow:hidden;
 background:#030303;align-items:center;justify-content:center;
 flex-direction:column;text-align:center;padding:20px;
}
.full-event.show {display:flex}
#eventCanvas {position:absolute;inset:0;width:100%;height:100%}
.event-copy {position:relative;z-index:2;max-width:800px}
#eventLabel {font-size:10px;letter-spacing:7px;color:#b7a17a}
#eventName {
 font-size:clamp(40px,10vw,100px);font-weight:1000;
 letter-spacing:4px;line-height:1.05;margin-top:25px;
 text-shadow:0 0 55px currentColor;overflow-wrap:anywhere;
}
#eventSub {margin-top:22px;font-size:11px;letter-spacing:4px;color:#d4c7ad}
.controls {
 display:grid;grid-template-columns:1.5fr 1fr 1fr;
 gap:9px;margin-top:12px;
}
.btn {min-height:48px}
.btn.main {
 background:#c4a56b;color:#100e09;border-color:#c4a56b;
 font-weight:900;
}
.btn:disabled {opacity:.4;cursor:wait}
.metrics {display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:12px}
.metric {background:#10100e;border:1px solid #292720;padding:15px}
.metric label {font-size:9px;letter-spacing:3px;color:#8e8576}
.metric strong {display:block;margin-top:8px;font-size:22px;font-weight:700}
.section {
 margin-top:30px;border-top:1px solid #2d2923;padding-top:21px;
}
.section-title {
 display:flex;align-items:center;justify-content:space-between;
 gap:10px;flex-wrap:wrap;margin-bottom:15px;
}
.section-title h2 {font-size:12px;letter-spacing:4px;font-weight:700}
.section-title p {font-size:10px;letter-spacing:1px;color:#8b8376}
.index-grid {
 display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;
}
.card {
 position:relative;overflow:hidden;min-height:125px;
 padding:14px;background:linear-gradient(140deg,#151411,#0a0a09);
 border:1px solid #302c24;cursor:pointer;transition:.2s;
}
.card:hover {transform:translateY(-2px);border-color:#9b8050}
.card:before {
 content:"";position:absolute;right:-25px;top:-30px;
 width:90px;height:90px;border-radius:50%;
 background:var(--aura,#c5a56a);opacity:.09;filter:blur(20px);
}
.card .tier {font-size:9px;letter-spacing:2px;color:#968b79}
.card .aura-name {font-size:16px;font-weight:900;margin-top:22px}
.card .odds {font-size:10px;color:#a39a89;margin-top:7px}
.card.locked {filter:saturate(.25)}
.card.locked .aura-name {color:#8b857b;letter-spacing:3px}
.card .replay {font-size:9px;letter-spacing:2px;color:#c8ad78;margin-top:12px}
.card.locked .replay {color:#777166}
#toast {
 position:fixed;left:50%;bottom:18px;transform:translateX(-50%);
 z-index:30;background:#191711;border:1px solid #615036;
 padding:12px 18px;font-size:11px;letter-spacing:1px;display:none;
 max-width:90%;text-align:center;
}
.note {font-size:10px;color:#777166;line-height:1.8;margin-top:14px}
footer {
 text-align:center;margin:35px 0 12px;color:#696255;
 font-size:9px;letter-spacing:4px;
}
@media(max-width:680px) {
 #app {padding:12px}
 header {align-items:flex-start;flex-direction:column}
 .scene {height:430px}
 .index-grid {grid-template-columns:repeat(2,minmax(0,1fr))}
 .controls {grid-template-columns:1fr 1fr}
 .btn.main {grid-column:span 2}
 .metric {padding:11px}
 .metric strong {font-size:17px}
 .brand {font-size:18px}
}
@media(prefers-reduced-motion:reduce) {
 *,*:before,*:after {scroll-behavior:auto!important}
}
</style>
</head>
<body>
<div id="app">
<header>
 <div class="brand">OBSCURA<small>AN ATLAS OF THE IMPOSSIBLE</small></div>
 <nav class="nav">
  <button class="active" id="navRoll">ROLL</button>
  <button id="navIndex">AURA INDEX</button>
 </nav>
</header>

<main id="rollPage">
 <section class="scene" id="scene">
  <canvas id="world"></canvas>
  <div id="flash"></div>
  <div class="scene-content">
   <div class="kicker" id="kicker">BEYOND THE ORDINARY</div>
   <div id="name">OBSCURA</div>
   <div id="sub">EVERYTHING BEGINS IN DARKNESS</div>
   <div id="hint">PRESS ROLL TO OPEN THE UNKNOWN</div>
  </div>
  <div class="full-event" id="event">
   <canvas id="eventCanvas"></canvas>
   <div class="event-copy">
    <div id="eventLabel">THE VEIL HAS BEEN LIFTED</div>
    <div id="eventName"></div>
    <div id="eventSub"></div>
   </div>
  </div>
 </section>

 <div class="controls">
  <button class="btn main" id="rollBtn">✦ &nbsp; ROLL</button>
  <button class="btn" id="autoBtn">AUTO: OFF</button>
  <button class="btn" id="indexBtn">OPEN INDEX ↗</button>
 </div>

 <div class="metrics">
  <div class="metric"><label>TOTAL ROLLS</label><strong id="rollCount">0</strong></div>
  <div class="metric"><label>RAREST DISCOVERY</label><strong id="best">—</strong></div>
  <div class="metric"><label>DISCOVERED</label><strong id="discovered">0 / 8</strong></div>
 </div>
 <p class="note">Your discoveries are saved in this browser when storage is available. Odds are displayed as approximate rarity tiers.</p>
</main>

<section class="section" id="indexPage" style="display:none">
 <div class="section-title">
  <div><h2>THE AURA INDEX</h2><p>UNKNOWN THINGS DO NOT REVEAL THEIR NAMES.</p></div>
  <button class="btn" id="backBtn">← BACK TO ROLL</button>
 </div>
 <div class="index-grid" id="indexGrid"></div>
 <p class="note">Select an aura you have discovered to replay its reveal. Undiscovered auras remain hidden behind ???.</p>
</section>

<footer>OBSCURA / NO TWO DESTINIES ARE ALIKE</footer>
</div>
<div id="toast"></div>

<script>
(() => {
"use strict";

const AURAS = [
 {id:"ash", name:"ASHEN", odds:2, color:"#b8b0a0", tier:"COMMON",
  duration:1600, style:0},
 {id:"tide", name:"ABYSSAL TIDE", odds:8, color:"#347e83", tier:"UNCOMMON",
  duration:2200, style:1},
 {id:"blood", name:"RED HARVEST", odds:40, color:"#9e302b", tier:"RARE",
  duration:2800, style:2},
 {id:"sun", name:"DYNASTY OF GOLD", odds:250, color:"#c49a50", tier:"EPIC",
  duration:3500, style:3},
 {id:"eclipse", name:"BLACK ECLIPSE", odds:2500, color:"#8d7770", tier:"LEGENDARY",
  duration:4500, style:4},
 {id:"saint", name:"PALE SAINT", odds:25000, color:"#e3ddc7", tier:"MYTHIC",
  duration:5700, style:5},
 {id:"null", name:"NULL SOVEREIGN", odds:100000, color:"#9d80a5", tier:"TRANSCENDENT",
  duration:7200, style:6},
 {id:"origin", name:"THE FIRST LIGHT", odds:1000000, color:"#f1e4b7", tier:"IMPOSSIBLE",
  duration:9000, style:7}
];

const $ = id => document.getElementById(id);
const world = $("world"), ctx = world.getContext("2d");
const eventCanvas = $("eventCanvas"), ectx = eventCanvas.getContext("2d");
const scene = $("scene");
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

let W=0,H=0,EW=0,EH=0;
let particles=[], rings=[], stars=[], shards=[];
let rolling=false, auto=false, rollTotal=0, bestAura=null;
let inventory={}, currentAura=null, eventToken=0, toastTimer;
let introStart=performance.now(), introDone=false, lastFrame=performance.now();
let sequence=null;

function safeLoad(){
 try {
  const raw=localStorage.getItem("obscura-save-v1");
  if(raw){
   const d=JSON.parse(raw);
   if(d && typeof d==="object"){
    if(d.inventory && typeof d.inventory==="object")inventory=d.inventory;
    if(Number.isFinite(d.rollTotal))rollTotal=d.rollTotal;
    if(typeof d.best==="string")bestAura=AURAS.find(a=>a.id===d.best)||null;
   }
  }
 } catch(e) {}
}
function save(){
 try {
  localStorage.setItem("obscura-save-v1",JSON.stringify({
   inventory,rollTotal,best:bestAura?bestAura.id:null
  }));
 } catch(e) {}
}
safeLoad();

function resize(){
 const r=scene.getBoundingClientRect();
 const d=Math.min(devicePixelRatio||1,2);
 W=r.width;H=r.height;
 world.width=Math.max(1,Math.floor(W*d));
 world.height=Math.max(1,Math.floor(H*d));
 ctx.setTransform(d,0,0,d,0,0);
 const er=$("event").getBoundingClientRect();
 EW=er.width||W;EH=er.height||H;
 eventCanvas.width=Math.max(1,Math.floor(EW*d));
 eventCanvas.height=Math.max(1,Math.floor(EH*d));
 ectx.setTransform(d,0,0,d,0,0);
 stars=Array.from({length:180},()=>({
  x:Math.random()*W,y:Math.random()*H,
  z:Math.random(),p:Math.random()*6.28
 }));
}
addEventListener("resize",resize);
resize();

function toast(msg){
 const t=$("toast");
 t.textContent=msg;t.style.display="block";
 clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>t.style.display="none",2200);
}
function chooseAura(){
 // Weighted rarity selection. Rarity tiers are approximate.
 const weights=AURAS.map(a=>1/a.odds);
 const sum=weights.reduce((x,y)=>x+y,0);
 let n=Math.random()*sum;
 for(let i=0;i<AURAS.length;i++){
  n-=weights[i];
  if(n<=0)return AURAS[i];
 }
 return AURAS[0];
}
function hexRgb(hex){
 const n=parseInt(hex.slice(1),16);
 return [(n>>16)&255,(n>>8)&255,n&255];
}
function rgba(hex,a){
 const [r,g,b]=hexRgb(hex);
 return `rgba(${r},${g},${b},${a})`;
}
function burst(x,y,color,count,power=1){
 for(let i=0;i<count;i++){
  const a=Math.random()*Math.PI*2;
  const speed=(.5+Math.random()*5.5)*power;
  particles.push({
   x,y,vx:Math.cos(a)*speed,vy:Math.sin(a)*speed,
   life:45+Math.random()*65,max:110,
   size:.5+Math.random()*2.8,color,
   kind:Math.random()<.25?"shard":"dot",
   spin:Math.random()*6
  });
 }
}
function ring(color,r=8,speed=3,tilt=.4){
 rings.push({x:W/2,y:H/2,r,speed,life:70,max:70,color,tilt,
  angle:Math.random()*6.28});
}
function lineBurst(color,count){
 for(let i=0;i<count;i++){
  const x=W/2+(Math.random()-.5)*W*.9;
  const y=H/2+(Math.random()-.5)*H*.7;
  shards.push({x,y,life:10+Math.random()*22,color,
   vx:(W/2-x)*.05,vy:(H/2-y)*.05});
 }
}
function setAuraText(a){
 $("kicker").textContent=a.tier+" DISCOVERED";
 $("name").textContent=a.name;
 $("name").style.color=a.color;
 $("name").style.textShadow="0 0 35px "+rgba(a.color,.38);
 $("sub").textContent="1 IN "+a.odds.toLocaleString("en-US")+" · "+a.tier;
 $("hint").textContent="DISCOVERY RECORDED";
}
function renderMetrics(){
 $("rollCount").textContent=rollTotal.toLocaleString("en-US");
 $("best").textContent=bestAura?bestAura.name:"—";
 $("best").style.color=bestAura?bestAura.color:"#eee7d8";
 $("discovered").textContent=Object.keys(inventory).length+" / "+AURAS.length;
 renderIndex();
}
function renderIndex(){
 const root=$("indexGrid");
 root.innerHTML="";
 for(const a of AURAS){
  const owned=!!inventory[a.id];
  const card=document.createElement("div");
  card.className="card"+(owned?"":" locked");
  card.style.setProperty("--aura",a.color);
  const tier=document.createElement("div");
  tier.className="tier";
  tier.textContent=owned?a.tier:"UNDISCOVERED";
  const name=document.createElement("div");
  name.className="aura-name";
  name.textContent=owned?a.name:"???";
  if(owned)name.style.color=a.color;
  const odds=document.createElement("div");
  odds.className="odds";
  odds.textContent="1 IN "+a.odds.toLocaleString("en-US");
  const replay=document.createElement("div");
  replay.className="replay";
  replay.textContent=owned?"↻ REPLAY REVEAL":"LOCKED";
  card.append(tier,name,odds,replay);
  card.addEventListener("click",()=>{
   if(!owned){toast("This aura has not been discovered yet.");return;}
   showPage("roll");
   playReveal(a,true);
  });
  root.appendChild(card);
 }
}
function showPage(which){
 const isRoll=which==="roll";
 $("rollPage").style.display=isRoll?"block":"none";
 $("indexPage").style.display=isRoll?"none":"block";
 $("navRoll").classList.toggle("active",isRoll);
 $("navIndex").classList.toggle("active",!isRoll);
 if(!isRoll)renderIndex();
}
$("navRoll").onclick=()=>showPage("roll");
$("navIndex").onclick=()=>showPage("index");
$("indexBtn").onclick=()=>showPage("index");
$("backBtn").onclick=()=>showPage("roll");

function setBusy(value){
 rolling=value;
 $("rollBtn").disabled=value;
 $("rollBtn").textContent=value?"✧  THE VEIL IS OPENING":"✦  ROLL";
}

function roll(){
 if(rolling)return;
 const a=chooseAura();
 rollTotal++;
 inventory[a.id]=(inventory[a.id]||0)+1;
 if(!bestAura||a.odds>bestAura.odds)bestAura=a;
 save();
 renderMetrics();
 playReveal(a,false);
}
$("rollBtn").onclick=roll;

$("autoBtn").onclick=()=>{
 auto=!auto;
 $("autoBtn").textContent=auto?"AUTO: ON":"AUTO: OFF";
 if(auto&&!rolling)roll();
};

function playReveal(a,replay){
 if(rolling && !replay)return;
 const token=++eventToken;
 currentAura=a;
 setBusy(true);
 $("event").classList.add("show");
 $("eventName").textContent="";
 $("eventName").style.color=a.color;
 $("eventSub").textContent="";
 $("eventLabel").textContent=replay?"REPLAYING A DISCOVERY":"AN UNKNOWN PRESENCE APPROACHES";
 $("flash").style.opacity="0";
 $("event").style.background="#020202";
 sequence={
  token,a,replay,start:performance.now(),
  duration:reduceMotion?1000:a.duration,
  stage:0,done:false
 };
 // Build energy immediately; the main scene keeps moving underneath.
 burst(W/2,H/2,a.color,70,1.2);
 ring(a.color,10,4);
 if(a.odds>=2500)lineBurst(a.color,24);
 requestAnimationFrame(updateSequence);
}

function finishSequence(s){
 if(s.done)return;
 s.done=true;
 $("eventLabel").textContent=s.replay?"DISCOVERY REPLAYED":"THE VEIL HAS BEEN LIFTED";
 $("eventName").textContent=s.a.name;
 $("eventName").style.color=s.a.color;
 $("eventSub").textContent="1 IN "+s.a.odds.toLocaleString("en-US")+"  ·  "+s.a.tier;
 $("event").style.background=
  "radial-gradient(ellipse at center,"+rgba(s.a.color,.15)+",#030303 65%)";
 $("flash").style.opacity=s.a.odds>=2500?".9":".35";
 setTimeout(()=>{$("flash").style.opacity="0"},120);
 // Final impact, with longer shockwaves for rare auras.
 burst(EW/2,EH/2,s.a.color,s.a.odds>=2500?330:150,
  s.a.odds>=100000?3.4:s.a.odds>=2500?2:1);
 for(let i=0;i<(s.a.odds>=2500?12:5);i++)
  ring(s.a.color,8+i*6,s.a.odds>=2500?7:4,.25+i*.03);
 if(!reduceMotion){
  $("eventName").animate([
   {transform:"scale(.05)",filter:"blur(20px)",opacity:0},
   {transform:"scale(1.2)",filter:"blur(0)",opacity:1,offset:.7},
   {transform:"scale(1)",opacity:1}
  ],{duration:950,easing:"cubic-bezier(.12,.8,.2,1)"});
 }
 setAuraText(s.a);
 renderMetrics();
 // Keep the full-screen reveal visible for a dramatic pause.
 setTimeout(()=>{
  if(token!==eventToken)return;
  $("event").classList.remove("show");
  setBusy(false);
  if(auto) setTimeout(()=>{if(auto&&!rolling)roll()},450);
 },s.replay?1600:Math.min(3500,Math.max(1800,s.a.odds>=2500?3000:1800)));
}

function updateSequence(now){
 const s=sequence;
 if(!s||s.done||s.token!==eventToken)return;
 const elapsed=now-s.start;
 const p=Math.min(1,elapsed/s.duration);
 const a=s.a;
 // Each stage changes the whole atmosphere.
 if(p<.18){
  $("eventLabel").textContent="SOMETHING STIRS IN THE DARK";
  $("eventSub").textContent="SIGNAL DETECTED";
 }else if(p<.45){
  $("eventLabel").textContent="THE BOUNDARIES ARE BREAKING";
  $("eventSub").textContent="ENERGY CONVERGENCE  ·  "+Math.floor(p*100)+"%";
 }else if(p<.72){
  $("eventLabel").textContent=a.odds>=2500?"AN IMPOSSIBLE PRESENCE":"A NEW PRESENCE";
  $("eventSub").textContent="REALITY IS BECOMING UNSTABLE";
 }else{
  $("eventLabel").textContent="FINAL SEQUENCE";
  $("eventSub").textContent="PREPARE FOR REVELATION";
 }
 // More energy and faster rotation near the reveal.
 const amount=1+Math.floor(p*8);
 for(let i=0;i<amount;i++){
  const angle=Math.random()*Math.PI*2;
  const radius=(.15+Math.random()*.4)*Math.min(EW,EH);
  const x=EW/2+Math.cos(angle)*radius;
  const y=EH/2+Math.sin(angle)*radius;
  const speed=(.5+p*2.5)*(a.odds>=100000?1.6:1);
  particles.push({
   x,y,vx:(EW/2-x)*.015*speed,vy:(EH/2-y)*.015*speed,
   life:22+Math.random()*25,max:45,size:1+Math.random()*3,
   color:a.color,kind:"dot",spin:0
  });
 }
 if(p>.25 && Math.random()<.5)ring(a.color,10,2+p*8,.2);
 if(p>.5 && Math.random()<.25)lineBurst(a.color,a.odds>=2500?4:1);
 if(p>=1){finishSequence(s);return;}
 requestAnimationFrame(updateSequence);
}

function drawScene(now){
 ctx.clearRect(0,0,W,H);
 const t=now*.001;
 const cx=W/2,cy=H/2;
 const intro=Math.min(1,(now-introStart)/(reduceMotion?100:2300));
 // Dark opening atmosphere, slowly revealed.
 const vignette=ctx.createRadialGradient(cx,cy,5,cx,cy,Math.max(W,H)*.7);
 vignette.addColorStop(0,"#17150f");
 vignette.addColorStop(.4,"#0b0b09");
 vignette.addColorStop(1,"#030303");
 ctx.fillStyle=vignette;ctx.fillRect(0,0,W,H);
 // Moving stars, drifting toward the opening.
 for(const s of stars){
  const drift=intro<1?(1-intro)*15:2;
  const x=((s.x+(t*5*s.z))%W+W)%W;
  const y=((s.y+Math.sin(t*.3+s.p)*drift)%H+H)%H;
  ctx.globalAlpha=.15+s.z*.6;
  ctx.fillStyle=s.z>.85?"#e6d2a5":"#c5bba7";
  ctx.beginPath();ctx.arc(x,y,s.z*1.5+.2,0,Math.PI*2);ctx.fill();
 }
 ctx.globalAlpha=1;
 // Opening seam: the light splits the darkness.
 if(!introDone){
  const width=2+intro*W*.6;
  ctx.save();
  ctx.translate(cx,cy);
  ctx.rotate(-.12);
  const g=ctx.createLinearGradient(-width/2,0,width/2,0);
  g.addColorStop(0,"#c5a56a00");
  g.addColorStop(.45,"#c5a56a55");
  g.addColorStop(.5,"#f2e1b9");
  g.addColorStop(.55,"#c5a56a55");
  g.addColorStop(1,"#c5a56a00");
  ctx.fillStyle=g;
  ctx.fillRect(-width/2,-H,width,H*2);
  ctx.restore();
  if(intro>=1)introDone=true;
 }
 // Aura effects keep moving behind the reveal.
 const a=currentAura;
 if(a){
  const col=a.color;
  const rad=35+Math.sin(t*2)*4;
  const g=ctx.createRadialGradient(cx,cy,2,cx,cy,rad*4);
  g.addColorStop(0,rgba(col,.22));
  g.addColorStop(1,rgba(col,0));
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.save();ctx.translate(cx,cy);
  for(let i=0;i<4;i++){
   ctx.rotate(t*(i%2?-.18:.22));
   ctx.strokeStyle=rgba(col,.25+i*.09);
   ctx.lineWidth=i===2?2:1;
   ctx.beginPath();
   ctx.ellipse(0,0,rad*1.5+i*17,rad*.45+i*8,0,0,Math.PI*2);
   ctx.stroke();
  }
  ctx.restore();
  const orb=ctx.createRadialGradient(cx-rad*.3,cy-rad*.3,1,cx,cy,rad);
  orb.addColorStop(0,"#fff9e9");
  orb.addColorStop(.18,col);
  orb.addColorStop(1,rgba(col,0));
  ctx.fillStyle=orb;ctx.beginPath();ctx.arc(cx,cy,rad,0,Math.PI*2);ctx.fill();
 }
 // Ambient particles.
 for(let i=particles.length-1;i>=0;i--){
  const p=particles[i];
  p.x+=p.vx;p.y+=p.vy;p.vx*=.99;p.vy*=.99;p.life--;
  if(p.life<=0){particles.splice(i,1);continue;}
  ctx.globalAlpha=Math.min(1,p.life/20);
  ctx.fillStyle=p.color;
  ctx.shadowColor=p.color;ctx.shadowBlur=8;
  if(p.kind==="shard"){
   ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.spin+t);
   ctx.fillRect(-p.size/2,-p.size*2,p.size,p.size*4);
   ctx.restore();
  }else{
   ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();
  }
 }
 ctx.shadowBlur=0;
 // Shockwave rings.
 for(let i=rings.length-1;i>=0;i--){
  const r=rings[i];r.r+=r.speed;r.life--;
  if(r.life<=0){rings.splice(i,1);continue;}
  ctx.globalAlpha=r.life/r.max;
  ctx.strokeStyle=r.color;ctx.lineWidth=1.4;
  ctx.save();ctx.translate(r.x,r.y);ctx.rotate(r.angle);
  ctx.beginPath();ctx.ellipse(0,0,r.r,r.r*r.tilt,0,0,Math.PI*2);
  ctx.stroke();ctx.restore();
 }
 ctx.globalAlpha=1;
}
function drawEvent(now){
 ectx.clearRect(0,0,EW,EH);
 const s=sequence;
 if(!s)return;
 const a=s.a,t=now*.001;
 const elapsed=now-s.start;
 const p=Math.min(1,elapsed/s.duration);
 const cx=EW/2,cy=EH/2;
 // The entire event background changes color with the energy.
 const strength=a.odds>=100000?1:.6;
 const radius=Math.min(EW,EH)*(.1+p*.75);
 const g=ectx.createRadialGradient(cx,cy,1,cx,cy,radius);
 g.addColorStop(0,rgba(a.color,.12+Math.sin(t*3)*.04));
 g.addColorStop(.5,rgba(a.color,.04));
 g.addColorStop(1,"#030303");
 ectx.fillStyle=g;ectx.fillRect(0,0,EW,EH);
 // Slowly expanding concentric circles.
 for(let i=0;i<9;i++){
  const r=((p*1.4+i/9)%1)*Math.max(EW,EH)*.75;
  ectx.strokeStyle=rgba(a.color,(1-r/(Math.max(EW,EH)*.85))*.4);
  ectx.lineWidth=i%3===0?1.5:.6;
  ectx.beginPath();ectx.arc(cx,cy,r,0,Math.PI*2);ectx.stroke();
 }
 // Fracture lines converge into the center.
 const rays=a.odds>=100000?100:45;
 ectx.lineWidth=.7;
 for(let i=0;i<rays;i++){
  const ang=i*Math.PI*2/rays+t*.06;
  const r=Math.max(EW,EH)*(.22+p*.65);
  ectx.strokeStyle=rgba(a.color,.08+Math.random()*.16);
  ectx.beginPath();
  ectx.moveTo(cx+Math.cos(ang)*r,cy+Math.sin(ang)*r);
  ectx.lineTo(cx+Math.cos(ang+.08)*r*.65,cy+Math.sin(ang+.08)*r*.65);
  ectx.stroke();
 }
 // Central star/portal opens gradually.
 ectx.save();ectx.translate(cx,cy);ectx.rotate(t*.12);
 const points=a.odds>=100000?16:8;
 const outer=(15+p*100)*strength;
 const inner=outer*.3;
 ectx.beginPath();
 for(let i=0;i<points*2;i++){
  const angle=i*Math.PI/points;
  const r=i%2===0?outer:inner;
  const x=Math.cos(angle)*r,y=Math.sin(angle)*r;
  if(i===0)ectx.moveTo(x,y);else ectx.lineTo(x,y);
 }
 ectx.closePath();
 ectx.strokeStyle=rgba(a.color,.7);ectx.lineWidth=1.3;ectx.stroke();
 ectx.fillStyle=rgba(a.color,.07+p*.07);ectx.fill();
 ectx.restore();
 // Flash in the final instant.
 if(p>.88){
  ectx.fillStyle=rgba(a.color,(p-.88)*.65);
  ectx.fillRect(0,0,EW,EH);
 }
}
function frame(now){
 const dt=Math.min(50,now-lastFrame);lastFrame=now;
 drawScene(now);
 if($("event").classList.contains("show"))drawEvent(now);
 requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

// Dramatic opening title sequence.
setTimeout(()=>{
 if(introDone)return;
 $("kicker").textContent="WELCOME TO THE UNKNOWN";
 $("name").textContent="OBSCURA";
 $("name").style.color="#e8d7b3";
 $("sub").textContent="YOUR DESTINY HAS NOT BEEN WRITTEN";
 $("hint").textContent="A WORLD OF ONE-IN-A-MILLION DISCOVERIES";
 $("name").animate([
  {opacity:0,transform:"translateY(25px) scale(.92)",filter:"blur(10px)"},
  {opacity:1,transform:"translateY(0) scale(1)",filter:"blur(0)"}
 ],{duration:1300,easing:"cubic-bezier(.15,.8,.2,1)"});
},650);

renderMetrics();
$("name").style.color="#e8d7b3";
$("name").style.textShadow="0 0 32px #c5a56a33";
})();
</script>
</body>
</html>
"""

components.html(html, height=1250, scrolling=True)
