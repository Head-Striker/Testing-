
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AURA RNG",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html = r"""
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing:border-box; }
body {
    margin:0; background:#050610; color:white;
    font-family:Arial,Helvetica,sans-serif;
}
button { font-family:inherit; cursor:pointer; }
.game {
    max-width:1100px; margin:auto; padding:18px;
}
.top {
    display:flex; align-items:center; justify-content:space-between;
    gap:12px; flex-wrap:wrap; margin-bottom:15px;
}
.logo { font-size:25px; font-weight:900; letter-spacing:5px; }
.pill {
    border:1px solid #303654; border-radius:30px;
    background:#111429; padding:10px 15px; color:#aab6ff;
    font-size:12px; letter-spacing:1px;
}
.arena {
    position:relative; height:460px; overflow:hidden;
    border-radius:22px; border:1px solid #252b50;
    background:
      radial-gradient(ellipse at 50% 50%,#18163d 0%,#090a1b 45%,#03040b 100%);
    isolation:isolate;
}
#fx {
    position:absolute; inset:0; width:100%; height:100%;
}
.arena:after {
    content:""; position:absolute; inset:0; pointer-events:none;
    background:linear-gradient(180deg,transparent 65%,#050610 100%);
}
.center {
    position:absolute; z-index:2; inset:0;
    display:flex; align-items:center; justify-content:center;
    flex-direction:column; pointer-events:none; text-align:center;
}
#eyebrow {
    font-size:11px; letter-spacing:5px; color:#939bc9;
    margin-bottom:18px;
}
#result {
    font-size:clamp(34px,7vw,70px); font-weight:1000;
    letter-spacing:2px; line-height:1.05;
    text-shadow:0 0 28px currentColor;
    transition:color .15s;
}
#rarity {
    margin-top:13px; font-size:13px; letter-spacing:4px;
    color:#c6c8e8;
}
#status {
    margin-top:22px; color:#8f96c2; font-size:12px;
    letter-spacing:3px;
}
.flash {
    position:absolute; z-index:3; inset:0; pointer-events:none;
    background:white; opacity:0;
}
.controls {
    display:grid; grid-template-columns:1fr 1fr 1fr;
    gap:10px; margin-top:14px;
}
.action {
    border:1px solid #303654; border-radius:13px;
    background:#12152a; color:#e7eaff; padding:16px 8px;
    font-size:13px; font-weight:800; transition:.2s;
}
.action:hover { border-color:#a1aaff; transform:translateY(-2px); }
.primary {
    background:linear-gradient(110deg,#7554ff,#b74cff);
    border:0; box-shadow:0 0 28px #794aff35;
}
.action:disabled { opacity:.5; cursor:wait; transform:none; }
.panels {
    display:grid; grid-template-columns:1fr 1fr;
    gap:14px; margin-top:16px;
}
.panel {
    background:#0c0e1d; border:1px solid #222744;
    border-radius:16px; padding:16px; min-width:0;
}
.panel h3 {
    margin:0 0 13px; font-size:12px; letter-spacing:3px;
    color:#aab2e9;
}
.inventory {
    display:flex; flex-wrap:wrap; gap:7px; min-height:35px;
}
.item {
    border:1px solid #313754; border-radius:9px;
    padding:8px 10px; background:#15182c; font-size:12px;
}
.item b { display:block; margin-bottom:4px; }
.item small { color:#a8aecb; }
.muted { color:#737b9f; font-size:12px; line-height:1.7; }
.stats {
    display:flex; gap:12px; flex-wrap:wrap; margin-top:12px;
}
.stat { flex:1; min-width:85px; background:#101326;
    border-radius:12px; padding:12px; }
.stat small { color:#9299bd; font-size:10px; letter-spacing:1px; }
.stat div { font-size:21px; font-weight:900; margin-top:5px; }
.odds { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
.odds div {
    display:flex; align-items:center; gap:8px; font-size:12px;
    background:#121529; padding:10px; border-radius:9px;
}
.dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
.odds span:last-child { margin-left:auto; color:#a5acce; }
.footer { text-align:center; color:#515a7e; font-size:10px;
    letter-spacing:2px; padding:22px 0 8px; }
@keyframes pulse {
    0%,100% { transform:scale(1); }
    50% { transform:scale(1.045); }
}
.pulsing { animation:pulse .65s infinite; }
@media(max-width:600px) {
    .arena { height:390px; }
    .controls { grid-template-columns:1fr 1fr; }
    .controls .primary { grid-column:span 2; }
    .panels { grid-template-columns:1fr; }
    .logo { font-size:20px; }
}
</style>
</head>
<body>
<div class="game">
    <div class="top">
        <div class="logo">✦ AURA RNG</div>
        <div class="pill">REALITY IS RANDOM</div>
    </div>

    <div class="arena" id="arena">
        <canvas id="fx"></canvas>
        <div class="flash" id="flash"></div>
        <div class="center">
            <div id="eyebrow">DISCOVER YOUR DESTINY</div>
            <div id="result">READY?</div>
            <div id="rarity">PRESS ROLL TO BEGIN</div>
            <div id="status">✧ INFINITE POSSIBILITIES ✧</div>
        </div>
    </div>

    <div class="controls">
        <button class="action primary" id="roll">✦  ROLL AURA</button>
        <button class="action" id="auto">↻  AUTO: OFF</button>
        <button class="action" id="clear">⌫  CLEAR INVENTORY</button>
    </div>

    <div class="stats">
        <div class="stat"><small>TOTAL ROLLS</small><div id="count">0</div></div>
        <div class="stat"><small>BEST AURA</small><div id="best">—</div></div>
        <div class="stat"><small>COLLECTED</small><div id="collected">0</div></div>
    </div>

    <div class="panels">
        <div class="panel">
            <h3>✧ YOUR COLLECTION</h3>
            <div id="inventory" class="inventory">
                <div class="muted">Your journey starts here...</div>
            </div>
        </div>
        <div class="panel">
            <h3>✧ AURA INDEX</h3>
            <div id="odds" class="odds"></div>
            <p class="muted">Odds are illustrative. Each roll is random.
            Progress is stored for this open browser session only.</p>
        </div>
    </div>
    <div class="footer">AURA RNG · UNLEASH THE UNKNOWN</div>
</div>

<script>
(() => {
"use strict";

const AURAS = [
 {name:"COMMON", chance:50, color:"#b9c5dd", power:1},
 {name:"BLUE FLAME", chance:25, color:"#16b9ff", power:2},
 {name:"CRIMSON", chance:13, color:"#ff365f", power:3},
 {name:"THUNDER", chance:7, color:"#bb6cff", power:4},
 {name:"CELESTIAL", chance:3.5, color:"#ffce52", power:5},
 {name:"VOID", chance:1.3, color:"#ff4be7", power:6},
 {name:"INFINITY", chance:0.2, color:"#ffffff", power:7}
];

const $ = id => document.getElementById(id);
const canvas = $("fx");
const ctx = canvas.getContext("2d");
const arena = $("arena");

let W=0, H=0, rolling=false, auto=false, rollCount=0;
let inventory={}, particles=[], rings=[], bolts=[];
let aura=null, start=0, revealAt=0, lastTime=0;
let shake=0, flash=0, stars=[];
let bestPower=0, currentRoll=0;
let reducedMotion=window.matchMedia(
 "(prefers-reduced-motion: reduce)"
).matches;

function resize(){
 const r=arena.getBoundingClientRect();
 const d=Math.min(window.devicePixelRatio||1,2);
 W=r.width; H=r.height;
 canvas.width=Math.round(W*d);
 canvas.height=Math.round(H*d);
 ctx.setTransform(d,0,0,d,0,0);
 stars=Array.from({length:100},()=>({
  x:Math.random()*W,y:Math.random()*H,
  r:Math.random()*1.5+.3,p:Math.random()*6.28
 }));
}
window.addEventListener("resize",resize);
resize();

function pickAura(){
 let n=Math.random()*100;
 for(const a of AURAS){
  n-=a.chance;
  if(n<=0)return a;
 }
 return AURAS[0];
}

function addBurst(x,y,color,n,power=1){
 for(let i=0;i<n;i++){
  const ang=Math.random()*Math.PI*2;
  const speed=(1+Math.random()*5)*power;
  particles.push({
   x,y,vx:Math.cos(ang)*speed,vy:Math.sin(ang)*speed,
   life:45+Math.random()*50,max:95,
   size:1+Math.random()*3,color
  });
 }
}

function makeRing(color,r=10,speed=4){
 rings.push({
  x:W/2,y:H/2+12,r,life:65,max:65,
  speed,color,rotation:Math.random()*6.28
 });
}

function makeBolt(color){
 const pts=[];
 let x=W/2+(Math.random()-.5)*70;
 let y=H/2-35;
 pts.push([x,y]);
 while(y<H*.8){
  x+=(Math.random()-.5)*75;
  y+=12+Math.random()*25;
  pts.push([x,y]);
 }
 bolts.push({pts,color,life:9});
}

function weightedRarity(){
 const a=pickAura();
 return a;
}

function updateUI(a){
 $("result").textContent=a.name;
 $("result").style.color=a.color;
 $("rarity").textContent="CHANCE  ·  1 IN "+Math.max(1,
 Math.round(100/a.chance)).toLocaleString("en-US");
 $("status").textContent=a.power>=6
  ?"✦ AN EXTRAORDINARY DISCOVERY ✦"
  :"✧ A NEW ENERGY AWAKENS ✧";
 $("count").textContent=rollCount.toLocaleString();
 $("collected").textContent=Object.keys(inventory).length;
 $("best").textContent=bestPower ? AURAS.find(
  x=>x.power===bestPower).name : "—";
}

function updateInventory(a){
 inventory[a.name]=(inventory[a.name]||0)+1;
 const root=$("inventory");
 root.innerHTML="";
 const items=Object.keys(inventory).sort((x,y)=>
  AURAS.find(a=>a.name===y).power-
  AURAS.find(a=>a.name===x).power
 );
 for(const name of items){
  const found=AURAS.find(a=>a.name===name);
  const el=document.createElement("div");
  el.className="item";
  el.style.borderColor=found.color+"88";
  el.innerHTML="";
  const b=document.createElement("b");
  b.textContent=found.name;
  b.style.color=found.color;
  const small=document.createElement("small");
  small.textContent="× "+inventory[name];
  el.append(b,small);
  root.appendChild(el);
 }
}

function reveal(a){
 aura=a;
 rolling=false;
 $("roll").disabled=false;
 $("roll").textContent="✦  ROLL AGAIN";
 $("result").classList.remove("pulsing");
 updateUI(a);
 updateInventory(a);
 if(a.power>bestPower)bestPower=a.power;

 // Dramatic reveal
 const rare=a.power>=5;
 flash=rare?0.95:0.5;
 shake=rare?20:8;
 addBurst(W/2,H/2,a.color,rare?260:120,rare?2.1:1.25);
 for(let i=0;i<(rare?8:4);i++)
  makeRing(a.color,10+i*5,rare?7:4);
 for(let i=0;i<(rare?18:7);i++)makeBolt(a.color);
 if(rare && !reducedMotion){
  $("result").animate([
   {transform:"scale(.2) rotate(-8deg)",filter:"blur(12px)"},
   {transform:"scale(1.2) rotate(2deg)",filter:"blur(0)"},
   {transform:"scale(1)",filter:"blur(0)"}
  ],{duration:700,easing:"cubic-bezier(.1,.8,.2,1)"});
 }
 if(auto) setTimeout(()=>{if(auto&&!rolling)roll();},650);
}

function roll(){
 if(rolling)return;
 rolling=true;
 currentRoll++;
 start=performance.now();
 revealAt=start+(reducedMotion?700:2600);
 aura=null;
 $("roll").disabled=true;
 $("roll").textContent="✧  ROLLING...";
 $("result").textContent="???";
 $("result").style.color="#d8d9ff";
 $("rarity").textContent="ENERGY ACCUMULATING";
 $("status").textContent="✦ DESTINY IS FORMING ✦";
 $("result").classList.add("pulsing");

 rollCount++;
 $("count").textContent=rollCount.toLocaleString();

 // Build up energy around the center
 for(let i=0;i<5;i++)makeRing("#7e75ff",10+i*8,4+i);
 addBurst(W/2,H/2,"#b4a4ff",90,1.2);
}

$("roll").addEventListener("click",roll);

$("auto").addEventListener("click",()=>{
 auto=!auto;
 $("auto").textContent=auto?"↻  AUTO: ON":"↻  AUTO: OFF";
 $("auto").style.borderColor=auto?"#aa8cff":"";
 if(auto&&!rolling)roll();
});

$("clear").addEventListener("click",()=>{
 if(rolling)return;
 inventory={};
 bestPower=0;
 $("inventory").innerHTML=
 '<div class="muted">Your collection has been cleared.</div>';
 $("collected").textContent="0";
 $("best").textContent="—";
});

document.addEventListener("keydown",e=>{
 if(e.code==="Space" && !rolling &&
    !["INPUT","TEXTAREA"].includes(document.activeElement.tagName)){
  e.preventDefault();roll();
 }
});

for(const a of AURAS){
 const el=document.createElement("div");
 const dot=document.createElement("span");
 dot.className="dot";
 dot.style.background=a.color;
 dot.style.boxShadow="0 0 9px "+a.color;
 const name=document.createElement("b");
 name.textContent=a.name;
 name.style.color=a.color;
 const odds=document.createElement("span");
 odds.textContent="1 in "+Math.round(100/a.chance);
 el.append(dot,name,odds);
 $("odds").appendChild(el);
}

function draw(now){
 const dt=Math.min(2,(now-lastTime)/16.67||1);
 lastTime=now;

 ctx.clearRect(0,0,W,H);
 ctx.save();
 if(shake>0.2 && !reducedMotion){
  ctx.translate((Math.random()-.5)*shake,(Math.random()-.5)*shake);
  shake*=.88;
 }else shake=0;

 // Starfield
 for(const s of stars){
  ctx.globalAlpha=.3+.4*Math.sin(now*.001+s.p);
  ctx.fillStyle="#cbd0ff";
  ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();
 }
 ctx.globalAlpha=1;

 const cx=W/2,cy=H/2+10;
 const col=aura?aura.color:"#8e7aff";
 const t=now*.001;
 const energy=rolling?1+Math.sin(t*9)*.17:1;

 // Ambient glow
 const glow=ctx.createRadialGradient(cx,cy,2,cx,cy,
  (aura?aura.power*40:100)*energy);
 glow.addColorStop(0,(aura?aura.color:"#776bff")+"55");
 glow.addColorStop(1,"#090a1b00");
 ctx.fillStyle=glow;
 ctx.fillRect(0,0,W,H);

 // Rotating magical circles
 if(rolling || aura){
  const strength=aura?aura.power:3;
  for(let k=0;k<3;k++){
   ctx.save();
   ctx.translate(cx,cy);
   ctx.rotate(t*(k%2?-.45:.55)*(k+1));
   ctx.strokeStyle=col;
   ctx.globalAlpha=.35+k*.12;
   ctx.lineWidth=k===1?2:1;
   ctx.beginPath();
   ctx.ellipse(0,0,(38+strength*8+k*17)*energy,
    (17+strength*3+k*8)*energy,0,0,Math.PI*2);
   ctx.stroke();
   for(let i=0;i<8+k*2;i++){
    const ang=i*Math.PI*2/(8+k*2);
    const rx=(38+strength*8+k*17)*energy;
    const ry=(17+strength*3+k*8)*energy;
    ctx.fillStyle=col;
    ctx.beginPath();
    ctx.arc(Math.cos(ang)*rx,Math.sin(ang)*ry,2+k*.5,0,Math.PI*2);
    ctx.fill();
   }
   ctx.restore();
  }
 }

 // Main energy orb
 if(rolling || aura){
  const strength=aura?aura.power:3;
  const rad=(rolling?28:22)+strength*3;
  const gradient=ctx.createRadialGradient(cx-rad*.3,cy-rad*.3,1,
   cx,cy,rad*energy);
  gradient.addColorStop(0,"#ffffff");
  gradient.addColorStop(.18,col);
  gradient.addColorStop(.55,col+"aa");
  gradient.addColorStop(1,col+"00");
  ctx.globalAlpha=.95;
  ctx.fillStyle=gradient;
  ctx.beginPath();ctx.arc(cx,cy,rad*energy,0,Math.PI*2);
  ctx.fill();

  // Orbiting sparks
  for(let i=0;i<Math.min(40,10+strength*4);i++){
   const ang=t*(i%2?1:-1)*(1+i%4)+i*2.4;
   const dist=rad+12+(i%5)*9;
   const x=cx+Math.cos(ang)*dist;
   const y=cy+Math.sin(ang)*dist*.58;
   ctx.globalAlpha=.4+.6*Math.abs(Math.sin(t*3+i));
   ctx.fillStyle=i%4===0?"#ffffff":col;
   ctx.beginPath();
   ctx.arc(x,y,i%4===0?2.5:1.5,0,Math.PI*2);
   ctx.fill();
  }
 }
 ctx.globalAlpha=1;

 // Explosion particles
 for(let i=particles.length-1;i>=0;i--){
  const p=particles[i];
  p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vx*=Math.pow(.985,dt);p.vy*=Math.pow(.985,dt);
  p.vy+=.025*dt;p.life-=dt;
  if(p.life<=0){particles.splice(i,1);continue;}
  ctx.globalAlpha=Math.min(1,p.life/22);
  ctx.fillStyle=p.color;
  ctx.shadowColor=p.color;ctx.shadowBlur=10;
  ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();
 }
 ctx.shadowBlur=0;

 // Expanding shockwave rings
 for(let i=rings.length-1;i>=0;i--){
  const r=rings[i];
  r.r+=r.speed*dt;r.life-=dt;
  if(r.life<=0){rings.splice(i,1);continue;}
  ctx.save();ctx.translate(r.x,r.y);
  ctx.rotate(r.rotation);ctx.globalAlpha=r.life/r.max;
  ctx.strokeStyle=r.color;ctx.lineWidth=2;
  ctx.beginPath();
  ctx.ellipse(0,0,r.r,r.r*.4,0,0,Math.PI*2);
  ctx.stroke();
  ctx.restore();
 }

 // Lightning arcs
 for(let i=bolts.length-1;i>=0;i--){
  const b=bolts[i];b.life-=dt;
  if(b.life<=0){bolts.splice(i,1);continue;}
  ctx.globalAlpha=Math.min(1,b.life/3);
  ctx.strokeStyle=b.color;ctx.lineWidth=2+Math.random()*2;
  ctx.shadowColor=b.color;ctx.shadowBlur=15;
  ctx.beginPath();
  b.pts.forEach((p,j)=>{
   if(j===0)ctx.moveTo(p[0],p[1]);else ctx.lineTo(p[0],p[1]);
  });
  ctx.stroke();ctx.shadowBlur=0;
 }
 ctx.globalAlpha=1;
 ctx.restore();

 if(flash>0){
  $("flash").style.opacity=String(flash);
  flash*=.78;
  if(flash<.015){flash=0;$("flash").style.opacity="0";}
 }

 if(rolling && now>=revealAt){
  reveal(weightedRarity());
 }
 requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
})();
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=True)
