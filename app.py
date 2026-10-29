
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="OBSCURA — Aura RNG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html = r"""
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;background:#080807;color:#eee6d5;font-family:Arial,sans-serif}
button,input{font:inherit}
button{cursor:pointer}
#app{max-width:1200px;margin:auto;padding:18px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 0 20px;border-bottom:1px solid #302b22}
.logo{font-size:23px;font-weight:900;letter-spacing:6px}
.logo small{display:block;font-size:9px;color:#9b8c72;letter-spacing:4px;margin-top:7px}
button{background:#151410;color:#e9dfcd;border:1px solid #41392a;border-radius:4px;padding:12px 15px;font-size:11px;letter-spacing:2px}
button:hover{border-color:#c6a76d}
button:disabled{opacity:.45;cursor:wait}
button.gold{background:#c3a36a;color:#100e09;border-color:#c3a36a;font-weight:bold}
button.active{background:#c3a36a;color:#100e09}
.scene{position:relative;height:500px;margin-top:16px;overflow:hidden;background:#050605;border:1px solid #393226;isolation:isolate}
canvas{position:absolute;inset:0;width:100%;height:100%}
#world{z-index:0}
.center{position:absolute;inset:0;z-index:1;display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;padding:18px;pointer-events:none}
.kicker{font-size:10px;letter-spacing:6px;color:#b9a27a}
#name{font-size:clamp(30px,7vw,72px);font-weight:900;letter-spacing:3px;margin-top:20px;overflow-wrap:anywhere}
#sub{font-size:11px;letter-spacing:3px;color:#c2b49b;margin-top:14px}
#hint{font-size:10px;letter-spacing:3px;color:#847b6b;margin-top:32px}
#event{display:none;position:absolute;inset:0;z-index:5;align-items:center;justify-content:center;text-align:center;flex-direction:column;overflow:hidden;background:#030303}
#event.show{display:flex}
#eventCanvas{z-index:0}
.eventText{position:relative;z-index:2;padding:18px}
#eventLabel{font-size:10px;letter-spacing:6px;color:#c6ad7b}
#eventName{font-size:clamp(36px,9vw,94px);font-weight:1000;letter-spacing:3px;margin-top:25px;overflow-wrap:anywhere;text-shadow:0 0 45px currentColor}
#eventSub{font-size:11px;letter-spacing:3px;color:#d4c8ae;margin-top:20px}
#flash{position:absolute;inset:0;background:#f2e4c8;opacity:0;z-index:8;pointer-events:none}
#intro{position:absolute;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;background:#030303;overflow:hidden;transition:opacity 1s}
#introCanvas{z-index:0}
.introText{z-index:2;position:relative;padding:18px}
#introTitle{font-size:clamp(34px,8vw,80px);font-weight:1000;letter-spacing:9px;opacity:0}
#introSub{font-size:10px;letter-spacing:5px;color:#bba579;margin-top:20px;opacity:0}
#introProgress{height:2px;background:#2b261c;width:min(270px,65vw);margin-top:35px;overflow:hidden}
#introBar{height:100%;width:0;background:#c6a76d}
.controls{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:9px;margin-top:12px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:12px}
.stat,.panel{background:#10100e;border:1px solid #2c2922;padding:15px}
.stat label{font-size:9px;letter-spacing:3px;color:#9b907e}
.stat strong{display:block;font-size:19px;margin-top:8px;overflow-wrap:anywhere}
.section{margin-top:30px;border-top:1px solid #302b22;padding-top:20px}
.section h2{font-size:12px;letter-spacing:4px}
.index{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}
.card{background:linear-gradient(145deg,#171611,#0b0b09);border:1px solid #373024;padding:14px;min-height:125px;cursor:pointer;position:relative;overflow:hidden}
.card:hover{border-color:#c6a76d;transform:translateY(-2px)}
.card.locked{filter:saturate(.25)}
.tier{font-size:9px;letter-spacing:2px;color:#a99a81}
.auraName{font-size:15px;font-weight:900;margin-top:23px}
.odds{font-size:10px;color:#a69b87;margin-top:8px}
.replay{font-size:9px;letter-spacing:2px;color:#d1b27a;margin-top:12px}
.panel{margin-top:12px}
.panel h2{margin-top:0}
.codeRow{display:flex;gap:8px;margin-top:12px}
.codeRow input{min-width:0;flex:1;background:#080807;color:#eee6d5;border:1px solid #48402e;padding:13px;outline:none}
.codeRow input:focus{border-color:#c6a76d}
#message{font-size:11px;color:#c6b58f;min-height:17px;margin-top:10px}
.note{font-size:10px;line-height:1.8;color:#81796c}
footer{text-align:center;font-size:9px;letter-spacing:4px;color:#6f6656;padding:30px 0 12px}
@media(max-width:650px){
 #app{padding:11px}.scene{height:430px}
 .controls{grid-template-columns:1fr 1fr}
 .controls .gold{grid-column:span 2}
 .index{grid-template-columns:repeat(2,minmax(0,1fr))}
 .stats{gap:5px}.stat{padding:10px}.stat strong{font-size:15px}
 .codeRow{flex-wrap:wrap}.codeRow button{width:100%}
}
</style>
</head>
<body>
<div id="app">
<header>
 <div class="logo">OBSCURA<small>AN ATLAS OF THE IMPOSSIBLE</small></div>
 <div>
  <button id="rollTab" class="active">ROLL</button>
  <button id="indexTab">AURA INDEX</button>
 </div>
</header>

<main id="rollPage">
 <div class="scene" id="scene">
  <canvas id="world"></canvas>
  <div class="center">
   <div class="kicker" id="kicker">BEYOND THE ORDINARY</div>
   <div id="name">OBSCURA</div>
   <div id="sub">EVERYTHING BEGINS IN DARKNESS</div>
   <div id="hint">PREPARE TO DISCOVER THE UNKNOWN</div>
  </div>
  <div id="event">
   <canvas id="eventCanvas"></canvas>
   <div class="eventText">
    <div id="eventLabel">REALITY IS SHIFTING</div>
    <div id="eventName"></div>
    <div id="eventSub"></div>
   </div>
  </div>
  <div id="intro">
   <canvas id="introCanvas"></canvas>
   <div class="introText">
    <div class="kicker">AN UNKNOWN WORLD</div>
    <div id="introTitle">OBSCURA</div>
    <div id="introSub">YOUR DESTINY HAS NOT BEEN WRITTEN</div>
    <div id="introProgress"><div id="introBar"></div></div>
   </div>
  </div>
  <div id="flash"></div>
 </div>

 <div class="controls">
  <button class="gold" id="rollBtn" disabled>✦ &nbsp; ROLL</button>
  <button id="autoBtn">AUTO: OFF</button>
  <button id="openIndex">OPEN INDEX ↗</button>
 </div>
 <div class="stats">
  <div class="stat"><label>TOTAL ROLLS</label><strong id="rollCount">0</strong></div>
  <div class="stat"><label>RAREST DISCOVERY</label><strong id="best">—</strong></div>
  <div class="stat"><label>DISCOVERED</label><strong id="discovered">0 / 16</strong></div>
 </div>
 <p class="note">Discoveries are saved in this browser when local storage is available.</p>
</main>

<section class="section" id="indexPage" style="display:none">
 <h2>✦ THE AURA INDEX</h2>
 <p class="note">Undiscovered auras are hidden. Select a discovered aura to replay its animation.</p>
 <div class="index" id="index"></div>
 <button id="backBtn" style="margin-top:14px">← BACK TO ROLL</button>
</section>

<section class="panel">
 <h2>✦ SECRET CODES</h2>
 <p class="note">Enter a secret code to unlock hidden discoveries.</p>
 <form id="codeForm">
  <div class="codeRow">
   <input id="codeInput" placeholder="ENTER CODE..." autocomplete="off" maxlength="40">
   <button type="submit">REDEEM CODE</button>
  </div>
 </form>
 <div id="message" aria-live="polite"></div>
</section>
<footer>OBSCURA · EVERY DISCOVERY HAS A STORY</footer>
</div>

<script>
(() => {
"use strict";

const AURAS = [
 {id:"ash",name:"ASHEN",odds:2,color:"#b8b0a0",tier:"COMMON",time:5000},
 {id:"tide",name:"ABYSSAL TIDE",odds:8,color:"#347e83",tier:"UNCOMMON",time:5000},
 {id:"blood",name:"RED HARVEST",odds:40,color:"#9e302b",tier:"RARE",time:5500},
 {id:"moss",name:"HOLLOW GARDEN",odds:100,color:"#73845a",tier:"RARE",time:5500},
 {id:"glass",name:"BROKEN GLASS",odds:250,color:"#a5b8bd",tier:"EPIC",time:6000},
 {id:"sun",name:"DYNASTY OF GOLD",odds:500,color:"#c49a50",tier:"EPIC",time:6000},
 {id:"ember",name:"EMBER CROWN",odds:1000,color:"#c76b3d",tier:"LEGENDARY",time:6500},
 {id:"eclipse",name:"BLACK ECLIPSE",odds:2500,color:"#8d7770",tier:"LEGENDARY",time:7000},
 {id:"winter",name:"LAST WINTER",odds:7500,color:"#c2d1d0",tier:"MYTHIC",time:7500},
 {id:"saint",name:"PALE SAINT",odds:25000,color:"#e3ddc7",tier:"MYTHIC",time:8000},
 {id:"null",name:"NULL SOVEREIGN",odds:100000,color:"#9d80a5",tier:"TRANSCENDENT",time:8500},
 {id:"marrow",name:"MARROW KING",odds:150000,color:"#c3b9a6",tier:"TRANSCENDENT",time:8500},
 {id:"starless",name:"STARLESS SEA",odds:300000,color:"#7a899e",tier:"COSMIC",time:9000},
 {id:"seraph",name:"FALLEN SERAPH",odds:500000,color:"#bd927c",tier:"COSMIC",time:9500},
 {id:"origin",name:"THE FIRST LIGHT",odds:1000000,color:"#f1e4b7",tier:"IMPOSSIBLE",time:10000},
 {id:"end",name:"THE END OF ALL",odds:1000000,color:"#ffffff",tier:"ETERNAL",time:10000}
];

const $=id=>document.getElementById(id);
const world=$("world"),ctx=world.getContext("2d");
const ec=$("eventCanvas"),ex=ec.getContext("2d");
const ic=$("introCanvas"),ix=ic.getContext("2d");
const scene=$("scene");
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;

let W=1,H=1,D=1,stars=[],particles=[],rings=[];
let rolling=false,auto=false,introDone=false,rollTotal=0;
let inventory={},best=null,current=null,sequence=null;
let token=0,flash=0,last=performance.now(),introStart=performance.now();
let autoTimer=null;

function load(){
 try{
  const d=JSON.parse(localStorage.getItem("obscura-save-v2")||"null");
  if(d&&typeof d==="object"){
   if(d.inventory&&typeof d.inventory==="object")inventory=d.inventory;
   if(Number.isFinite(d.rollTotal))rollTotal=d.rollTotal;
   if(typeof d.best==="string")best=AURAS.find(a=>a.id===d.best)||null;
  }
 }catch(e){}
}
function save(){
 try{localStorage.setItem("obscura-save-v2",JSON.stringify({
  inventory,rollTotal,best:best?best.id:null
 }));}catch(e){}
}
load();

function resize(){
 D=Math.min(devicePixelRatio||1,2);
 const r=scene.getBoundingClientRect();W=Math.max(1,r.width);H=Math.max(1,r.height);
 for(const [c,w,h,context] of [[world,W,H,ctx],[ec,W,H,ex],[ic,W,H,ix]]){
  c.width=Math.round(w*D);c.height=Math.round(h*D);
  context.setTransform(D,0,0,D,0,0);
 }
 stars=Array.from({length:230},()=>({
  x:Math.random()*W,y:Math.random()*H,z:.15+Math.random(),p:Math.random()*6.28
 }));
}
addEventListener("resize",resize);resize();

function color(hex,a){
 const n=parseInt(hex.slice(1),16);
 return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`;
}
function burst(x,y,col,n,power=1){
 for(let i=0;i<n;i++){
  const a=Math.random()*Math.PI*2,s=(.5+Math.random()*5)*power;
  particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,
   life:35+Math.random()*75,size:.5+Math.random()*3,col});
 }
}
function addRing(col,speed=3){
 rings.push({r:5,speed,life:65,max:65,col,rot:Math.random()*6.28});
}
function toast(s){
 $("message").textContent=s;
}
function render(){
 $("rollCount").textContent=rollTotal.toLocaleString();
 $("discovered").textContent=Object.keys(inventory).filter(k=>inventory[k]).length+" / "+AURAS.length;
 $("best").textContent=best?best.name:"—";
 $("best").style.color=best?best.color:"#eee6d5";
 const root=$("index");root.innerHTML="";
 for(const a of AURAS){
  const owned=!!inventory[a.id];
  const card=document.createElement("div");card.className="card"+(owned?"":" locked");
  const tier=document.createElement("div");tier.className="tier";tier.textContent=owned?a.tier:"UNDISCOVERED";
  const name=document.createElement("div");name.className="auraName";name.textContent=owned?a.name:"???";
  if(owned)name.style.color=a.color;
  const odds=document.createElement("div");odds.className="odds";odds.textContent="1 IN "+a.odds.toLocaleString();
  const replay=document.createElement("div");replay.className="replay";replay.textContent=owned?"↻ REPLAY ANIMATION":"LOCKED";
  card.append(tier,name,odds,replay);
  card.onclick=()=>{
   if(!owned){toast("Deze aura is nog niet ontdekt.");return;}
   showPage("roll");playReveal(a,true);
  };
  root.appendChild(card);
 }
}
function showPage(p){
 const roll=p==="roll";
 $("rollPage").style.display=roll?"block":"none";
 $("indexPage").style.display=roll?"none":"block";
 $("rollTab").classList.toggle("active",roll);
 $("indexTab").classList.toggle("active",!roll);
}
$("rollTab").onclick=()=>showPage("roll");
$("indexTab").onclick=()=>showPage("index");
$("openIndex").onclick=()=>showPage("index");
$("backBtn").onclick=()=>showPage("roll");

function choose(){
 // Inverse odds weights: the rarest aura has a very small probability.
 const weights=AURAS.map(a=>1/a.odds);
 let r=Math.random()*weights.reduce((x,y)=>x+y,0);
 for(let i=0;i<AURAS.length;i++){r-=weights[i];if(r<=0)return AURAS[i];}
 return AURAS[0];
}
function setBusy(v){
 rolling=v;
 $("rollBtn").disabled=v||!introDone;
 $("rollBtn").textContent=v?"✧ REVEAL IN PROGRESS":"✦  ROLL";
}
function roll(){
 if(rolling||!introDone)return;
 const a=choose();
 rollTotal++;
 inventory[a.id]=(inventory[a.id]||0)+1;
 if(!best||a.odds>best.odds)best=a;
 save();render();
 playReveal(a,false);
}
$("rollBtn").onclick=roll;
$("autoBtn").onclick=()=>{
 auto=!auto;
 $("autoBtn").textContent=auto?"AUTO: ON":"AUTO: OFF";
 if(auto&&!rolling&&introDone)roll();
 if(!auto&&autoTimer){clearTimeout(autoTimer);autoTimer=null;}
};

function playReveal(a,replay){
 if(rolling)return;
 const myToken=++token;
 current=a;setBusy(true);
 $("event").classList.add("show");
 // Important: canvases were hidden before this point. Recalculate their size.
 resize();
 $("eventLabel").textContent="AN UNKNOWN PRESENCE APPROACHES";
 $("eventName").textContent="";
 $("eventSub").textContent="ENERGY CONVERGENCE";
 $("eventName").style.color=a.color;
 $("event").style.background="#030303";
 sequence={a,start:performance.now(),duration:reduced?1200:a.time,
  token:myToken,replay,done:false,stage:-1};
 burst(W/2,H/2,a.color,90,1.3);addRing(a.color,4);
 requestAnimationFrame(updateSequence);
}
function complete(s){
 if(s.done)return;s.done=true;
 $("eventLabel").textContent=s.replay?"DISCOVERY REPLAYED":"THE VEIL HAS BEEN LIFTED";
 $("eventName").textContent=s.a.name;
 $("eventSub").textContent="1 IN "+s.a.odds.toLocaleString()+" · "+s.a.tier;
 $("event").style.background=
  "radial-gradient(ellipse at center,"+color(s.a.color,.16)+",#030303 70%)";
 flash=s.a.odds>=100000?.9:.35;
 burst(W/2,H/2,s.a.color,s.a.odds>=100000?550:200,
  s.a.odds>=100000?3:1.5);
 for(let i=0;i<(s.a.odds>=100000?16:6);i++)addRing(s.a.color,s.a.odds>=100000?8:4);
 $("eventName").animate([
  {opacity:0,transform:"scale(.05)",filter:"blur(20px)"},
  {opacity:1,transform:"scale(1.12)",filter:"blur(0)",offset:.75},
  {opacity:1,transform:"scale(1)"}
 ],{duration:900,easing:"cubic-bezier(.12,.8,.2,1)"});
 $("kicker").textContent=s.a.tier+" DISCOVERED";
 $("name").textContent=s.a.name;$("name").style.color=s.a.color;
 $("sub").textContent="1 IN "+s.a.odds.toLocaleString()+" · "+s.a.tier;
 $("hint").textContent="DISCOVERY RECORDED";
 render();save();

 // A guaranteed cleanup path: the next roll cannot remain locked.
 setTimeout(()=>{
  if(s.token!==token)return;
  $("event").classList.remove("show");
  setBusy(false);
  if(auto){
   autoTimer=setTimeout(()=>{autoTimer=null;if(auto&&!rolling)roll();},350);
  }
 },s.replay?1300:1500);
}
function updateSequence(now){
 const s=sequence;
 if(!s||s.done||s.token!==token)return;
 const p=Math.min(1,(now-s.start)/s.duration);
 const a=s.a;
 let label,sub;
 if(p<.2){label="SOMETHING STIRS IN THE DARK";sub="SIGNAL DETECTED";}
 else if(p<.48){label="THE BOUNDARIES ARE BREAKING";sub="ENERGY CONVERGENCE";}
 else if(p<.76){label=a.odds>=100000?"AN IMPOSSIBLE PRESENCE":"A NEW PRESENCE";sub="REALITY IS BECOMING UNSTABLE";}
 else{label="FINAL SEQUENCE";sub="PREPARE FOR REVELATION";}
 $("eventLabel").textContent=label;$("eventSub").textContent=sub;
 for(let i=0;i<2+Math.floor(p*9);i++){
  const angle=Math.random()*Math.PI*2;
  const r=(.1+Math.random()*.55)*Math.min(W,H);
  const x=W/2+Math.cos(angle)*r,y=H/2+Math.sin(angle)*r;
  particles.push({x,y,vx:(W/2-x)*(.012+p*.025),
   vy:(H/2-y)*(.012+p*.025),life:24+Math.random()*35,
   size:1+Math.random()*3,col:a.color});
 }
 if(Math.random()<.25)addRing(a.color,2+p*7);
 if(p>=1){complete(s);return;}
 requestAnimationFrame(updateSequence);
}

function draw(now){
 const dt=Math.min(2,(now-last)/16.67||1);last=now;
 ctx.clearRect(0,0,W,H);
 const t=now*.001,cx=W/2,cy=H/2;
 const bg=ctx.createRadialGradient(cx,cy,1,cx,cy,Math.max(W,H)*.8);
 bg.addColorStop(0,"#17140e");bg.addColorStop(.45,"#0b0b09");bg.addColorStop(1,"#020202");
 ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);

 // Moving star field
 for(const s of stars){
  const x=(s.x+t*4*s.z)%W;
  const y=s.y+Math.sin(t*.3+s.p)*5;
  ctx.globalAlpha=.2+s.z*.45;ctx.fillStyle=s.z>.85?"#e5d2a5":"#bcb5a7";
  ctx.beginPath();ctx.arc(x,y,s.z*1.3,0,6.283);ctx.fill();
 }
 ctx.globalAlpha=1;

 // Opening sequence: seven seconds of slowly unfolding light.
 const elapsed=now-introStart;
 const intro=Math.min(1,elapsed/(reduced?1000:7000));
 ix.clearRect(0,0,W,H);
 ix.fillStyle="#030303";ix.fillRect(0,0,W,H);
 for(let i=0;i<85;i++){
  const a=i*2.399+t*.07;
  const r=(intro*intro)*Math.min(W,H)*.48*(i/85);
  ix.fillStyle=color("#c5a66b",.1+intro*.4);
  ix.beginPath();ix.arc(W/2+Math.cos(a)*r,H/2+Math.sin(a)*r,1+(i%3),0,6.283);ix.fill();
 }
 ix.save();ix.translate(W/2,H/2);ix.rotate(-.1);
 const seam=2+intro*W*.8;
 const grad=ix.createLinearGradient(-seam/2,0,seam/2,0);
 grad.addColorStop(0,"#c6a76b00");grad.addColorStop(.45,"#c6a76b77");
 grad.addColorStop(.5,"#fff0c9");grad.addColorStop(.55,"#c6a76b77");
 grad.addColorStop(1,"#c6a76b00");
 ix.fillStyle=grad;ix.fillRect(-seam/2,-H,seam,H*2);ix.restore();

 if(!introDone){
  $("introTitle").style.opacity=String(Math.max(0,Math.min(1,(intro-.25)*2)));
  $("introSub").style.opacity=String(Math.max(0,Math.min(1,(intro-.48)*2)));
  $("introBar").style.width=(intro*100)+"%";
  if(intro>=1){
   introDone=true;
   $("intro").style.opacity="0";
   setTimeout(()=>{$("intro").style.display="none";setBusy(false);},1000);
  }
 }

 // Permanent background aura ambience.
 if(current){
  const col=current.color;
  ctx.fillStyle=ctx.createRadialGradient(cx,cy,1,cx,cy,Math.min(W,H)*.45);
  const g=ctx.createRadialGradient(cx,cy,1,cx,cy,Math.min(W,H)*.45);
  g.addColorStop(0,color(col,.13));g.addColorStop(1,color(col,0));
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.save();ctx.translate(cx,cy);
  for(let i=0;i<4;i++){
   ctx.rotate(t*(i%2?-.18:.2));ctx.strokeStyle=color(col,.3+i*.08);
   ctx.beginPath();ctx.ellipse(0,0,65+i*20,22+i*9,0,0,6.283);ctx.stroke();
  }
  ctx.restore();
 }

 // Shared particles and expanding rings.
 for(let i=particles.length-1;i>=0;i--){
  const p=particles[i];p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vx*=Math.pow(.99,dt);p.vy*=Math.pow(.99,dt);p.life-=dt;
  if(p.life<=0){particles.splice(i,1);continue;}
  ctx.globalAlpha=Math.min(1,p.life/18);ctx.fillStyle=p.col;
  ctx.shadowColor=p.col;ctx.shadowBlur=8;
  ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,6.283);ctx.fill();
 }
 ctx.shadowBlur=0;
 for(let i=rings.length-1;i>=0;i--){
  const r=rings[i];r.r+=r.speed*dt;r.life-=dt;
  if(r.life<=0){rings.splice(i,1);continue;}
  ctx.globalAlpha=r.life/r.max;ctx.strokeStyle=r.col;
  ctx.lineWidth=1.4;ctx.beginPath();
  ctx.ellipse(cx,cy,r.r,r.r*.42,Math.sin(t)*.3,0,6.283);ctx.stroke();
 }
 ctx.globalAlpha=1;
 if(flash>0){
  $("flash").style.opacity=String(flash);flash*=.78;
  if(flash<.015){flash=0;$("flash").style.opacity="0";}
 }

 // Full-screen reveal background effects.
 if($("event").classList.contains("show")){
  ex.clearRect(0,0,W,H);
  const s=sequence;
  if(s){
   const p=Math.min(1,(now-s.start)/s.duration);
   const a=s.a;
   const eg=ex.createRadialGradient(W/2,H/2,1,W/2,H/2,
    Math.min(W,H)*(.1+p*.8));
   eg.addColorStop(0,color(a.color,.22));eg.addColorStop(1,"#030303");
   ex.fillStyle=eg;ex.fillRect(0,0,W,H);
   for(let i=0;i<12;i++){
    const rr=((p*1.3+i/12)%1)*Math.max(W,H)*.7;
    ex.strokeStyle=color(a.color,(1-rr/(Math.max(W,H)*.8))*.4);
    ex.beginPath();ex.arc(W/2,H/2,rr,0,6.283);ex.stroke();
   }
   ex.save();ex.translate(W/2,H/2);ex.rotate(t*.2);
   const points=a.odds>=100000?18:10,outer=15+p*110;
   ex.beginPath();
   for(let i=0;i<points*2;i++){
    const angle=i*Math.PI/points,rr=i%2===0?outer:outer*.25;
    const x=Math.cos(angle)*rr,y=Math.sin(angle)*rr;
    if(i===0)ex.moveTo(x,y);else ex.lineTo(x,y);
   }
   ex.closePath();ex.strokeStyle=color(a.color,.8);ex.lineWidth=1.5;ex.stroke();
   ex.restore();
  }
 }
 requestAnimationFrame(draw);
}

render();
setBusy(true);
requestAnimationFrame(draw);

$("codeForm").addEventListener("submit",e=>{
 e.preventDefault();
 const code=$("codeInput").value.trim().toLowerCase();
 if(code==="unlock_all"){
  for(const a of AURAS)inventory[a.id]=Math.max(1,inventory[a.id]||0);
  save();render();toast("UNLOCK ALL: alle aura's zijn ontgrendeld!");
  $("codeInput").value="";
 }else if(code===""){
  toast("Vul eerst een code in.");
 }else{
  toast("Ongeldige code.");
 }
});
})();
</script>
</body>
</html>
"""

components.html(html, height=1550, scrolling=True)
