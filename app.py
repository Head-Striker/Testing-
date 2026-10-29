
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
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 0 16px;border-bottom:1px solid #302b22}
.nav{display:flex;gap:7px;flex-wrap:wrap}
.nav button{min-width:105px}
.page{min-height:calc(100vh - 110px)}
#codesPage{display:none}
#codesPage .panel{margin-top:24px}
#rollPage .scene{height:min(58vh,560px);min-height:360px}
#event{position:fixed;inset:0;width:100vw;height:100vh;height:100dvh}
#eventCanvas{width:100%;height:100%}
#eventName{max-width:96vw}
@media(max-width:650px){.nav{width:100%}.nav button{flex:1;min-width:0;padding:11px 8px;letter-spacing:1px}#rollPage .scene{height:54vh;min-height:330px}}
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
#event{display:none;position:fixed;inset:0;width:100vw;height:100vh;z-index:99999;align-items:center;justify-content:center;text-align:center;flex-direction:column;overflow:hidden;background:#030303;opacity:0;transition:opacity .1s ease}
#event.show{display:flex;opacity:1}
#event.fade-out{opacity:0}
#eventLabel,#eventSub{display:none!important}
.scene.revealing > .center{visibility:hidden}
#event{background:#030303}
#eventName{line-height:1.05;text-wrap:balance}
#introTitle{ text-shadow:0 0 35px #c6a76d,0 0 90px #c6a76d55; transform:translateY(12px) scale(.94); transition:transform 1.2s,opacity 1s}
#introSub{transition:opacity 1s}
#introProgress{box-shadow:0 0 18px #c6a76d55}
.scene.revealing #event{background:#030303}
#eventCanvas{z-index:0}
.eventText{position:relative;z-index:2;padding:18px;max-width:100vw}
#eventName{font-size:clamp(36px,8vw,110px);font-weight:1000;letter-spacing:3px;line-height:1.05;margin:0;padding:0 5vw;overflow-wrap:anywhere;text-wrap:balance;text-shadow:0 0 45px currentColor}
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
 <nav class="nav" aria-label="Main navigation">
  <button id="rollTab" class="active">ROLLING</button>
  <button id="indexTab">INDEX</button>
  <button id="codesTab">CODES</button>
 </nav>
</header>

<main id="rollPage" class="page">
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
    <div class="kicker">REALITY // INITIALIZING</div>
    <div id="introTitle">OBSCURA</div>
    <div id="introSub">THE VEIL IS OPENING</div>
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
  <div class="stat"><label>DISCOVERED</label><strong id="discovered">0 / 26</strong></div>
 </div>
 <p class="note">Discoveries are saved in this browser when local storage is available.</p>
</main>

<section class="section page" id="indexPage" style="display:none">
 <h2>✦ THE AURA INDEX</h2>
 <p class="note">Undiscovered auras are hidden. Select a discovered aura to replay its animation.</p>
 <div class="index" id="index"></div>
 <button id="backBtn" style="margin-top:14px">← BACK TO ROLL</button>
</section>

<section class="page" id="codesPage" style="display:none">
 <div class="panel">
 <h2>✦ SECRET CODES</h2>
 <p class="note">Enter a secret code to unlock hidden discoveries.</p>
 <form id="codeForm">
  <div class="codeRow">
   <input id="codeInput" placeholder="ENTER CODE..." autocomplete="off" maxlength="40">
   <button type="submit">REDEEM CODE</button>
  </div>
 </form>
 <div id="message" aria-live="polite"></div>
 </div>
</section>
<footer>OBSCURA · EVERY DISCOVERY HAS A STORY</footer>
</div>

<script>
(() => {
"use strict";

const AURAS = [
 {id:"ash",name:"ASHEN",odds:2,color:"#b8b0a0",tier:"COMMON",time:900,style:"ash"},
 {id:"tide",name:"ABYSSAL TIDE",odds:8,color:"#347eae",tier:"UNCOMMON",time:1200,style:"tide"},
 {id:"blood",name:"RED HARVEST",odds:40,color:"#d32f3f",tier:"RARE",time:1600,style:"blood"},
 {id:"moss",name:"HOLLOW GARDEN",odds:100,color:"#73845a",tier:"RARE",time:1800,style:"moss"},
 {id:"glass",name:"BROKEN GLASS",odds:250,color:"#a5dce8",tier:"EPIC",time:2200,style:"glass"},
 {id:"sun",name:"DYNASTY OF GOLD",odds:500,color:"#e8b94f",tier:"EPIC",time:2400,style:"sun"},
 {id:"ember",name:"EMBER CROWN",odds:1000,color:"#ff642e",tier:"LEGENDARY",time:2900,style:"ember"},
 {id:"eclipse",name:"BLACK ECLIPSE",odds:2500,color:"#9c78b7",tier:"LEGENDARY",time:3200,style:"eclipse"},
 {id:"winter",name:"LAST WINTER",odds:7500,color:"#c2f4ff",tier:"MYTHIC",time:3800,style:"winter"},
 {id:"saint",name:"PALE SAINT",odds:25000,color:"#fff0ce",tier:"MYTHIC",time:4200,style:"saint"},
 {id:"null",name:"NULL SOVEREIGN",odds:100000,color:"#b67bff",tier:"TRANSCENDENT",time:5000,style:"null"},
 {id:"marrow",name:"MARROW KING",odds:150000,color:"#d6c4a8",tier:"TRANSCENDENT",time:5300,style:"marrow"},
 {id:"starless",name:"STARLESS SEA",odds:300000,color:"#7a9dff",tier:"COSMIC",time:6000,style:"starless"},
 {id:"seraph",name:"FALLEN SERAPH",odds:500000,color:"#ffb6d5",tier:"COSMIC",time:6500,style:"seraph"},
 {id:"origin",name:"THE FIRST LIGHT",odds:1000000,color:"#fff5b7",tier:"IMPOSSIBLE",time:7500,style:"origin"},
 {id:"end",name:"THE END OF ALL",odds:2000000,color:"#ffffff",tier:"ETERNAL",time:8000,style:"end"},
 {id:"storm",name:"THUNDER VEIL",odds:120,color:"#7b9dff",tier:"RARE",time:1900,style:"storm"},
 {id:"crystal",name:"PRISMATIC HEART",odds:350,color:"#ff8de1",tier:"EPIC",time:2300,style:"crystal"},
 {id:"phantom",name:"PHANTOM STEP",odds:800,color:"#9b8cff",tier:"EPIC",time:2500,style:"phantom"},
 {id:"inferno",name:"INFERNAL ENGINE",odds:1800,color:"#ff4c16",tier:"LEGENDARY",time:3000,style:"inferno"},
 {id:"moon",name:"MOONVEIL",odds:6000,color:"#b8c8ff",tier:"MYTHIC",time:3600,style:"moon"},
 {id:"venom",name:"VENOM BLOOM",odds:14000,color:"#74ff91",tier:"MYTHIC",time:4000,style:"venom"},
 {id:"oracle",name:"THE ORACLE",odds:60000,color:"#ffdc8a",tier:"TRANSCENDENT",time:4700,style:"oracle"},
 {id:"rift",name:"RIFT WALKER",odds:180000,color:"#ff70e8",tier:"TRANSCENDENT",time:5500,style:"rift"},
 {id:"nebula",name:"NEBULA WRAITH",odds:400000,color:"#8e78ff",tier:"COSMIC",time:6200,style:"nebula"},
 {id:"zenith",name:"ZENITH ZERO",odds:1500000,color:"#d7ffff",tier:"ETERNAL",time:7800,style:"zenith"}
];

const $=id=>document.getElementById(id);
const world=$("world"),ctx=world.getContext("2d");
const ec=$("eventCanvas"),ex=ec.getContext("2d");
const ic=$("introCanvas"),ix=ic.getContext("2d");
const scene=$("scene");
// Move the reveal layer out of the scene stacking context so it can cover the whole viewport.
document.body.appendChild($("event"));
const reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;

let W=1,H=1,EW=1,EH=1,D=1,stars=[],particles=[],rings=[];
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
 for(const [c,w,h,context] of [[world,W,H,ctx],[ic,W,H,ix]]){
  c.width=Math.round(w*D);c.height=Math.round(h*D);
  context.setTransform(D,0,0,D,0,0);
 }
 const fullscreen=$("event").classList.contains("show");
 EW=Math.max(1,fullscreen?window.innerWidth:W);EH=Math.max(1,fullscreen?window.innerHeight:H);
 ec.width=Math.round(EW*D);ec.height=Math.round(EH*D);ex.setTransform(D,0,0,D,0,0);
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
   showPage("roll");
   window.scrollTo({top:0,behavior:"instant"});
   playReveal(a,true);
  };
  root.appendChild(card);
 }
}
function showPage(p){
 const pages={roll:"rollPage",index:"indexPage",codes:"codesPage"};
 for(const [key,id] of Object.entries(pages)) $(id).style.display=key===p?(key==="roll"?"block":"block"):"none";
 $("rollTab").classList.toggle("active",p==="roll");
 $("indexTab").classList.toggle("active",p==="index");
 $("codesTab").classList.toggle("active",p==="codes");
 // Keep navigation predictable: changing tabs always returns to the top of the app.
 window.scrollTo({top:0,behavior:"instant"});
}
$("rollTab").onclick=()=>showPage("roll");
$("indexTab").onclick=()=>showPage("index");
$("codesTab").onclick=()=>showPage("codes");
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
 scene.classList.add("revealing");
 const eventLayer=$("event");
 eventLayer.classList.remove("fade-out");
 eventLayer.style.opacity="0";
 eventLayer.classList.add("show");
 // Expand the reveal canvas to the full visible viewport.
 resize();
 requestAnimationFrame(()=>{eventLayer.style.opacity="1";});
 $("eventLabel").textContent="AN UNKNOWN PRESENCE APPROACHES";
 $("eventName").textContent="";
 $("eventSub").textContent="ENERGY CONVERGENCE";
 $("eventName").style.color=a.color;
 $("event").style.background="#030303";
 sequence={a,start:performance.now(),duration:reduced?Math.min(900,a.time):a.time,
  token:myToken,replay,done:false,stage:-1};
 burst(W/2,H/2,a.color,a.odds>=100000?180:45,a.odds>=100000?2:0.8);addRing(a.color,a.odds>=100000?7:2);
 requestAnimationFrame(updateSequence);
}
function complete(s){
 if(s.done)return;s.done=true;
 // During the reveal there are no extra captions; only the final aura name appears.
 $("eventName").textContent=s.a.name;
 $("event").style.background=
  "radial-gradient(ellipse at center,"+color(s.a.color,.16)+",#030303 70%)";
 flash=s.a.odds>=100000?.8:(s.a.odds>=1000?.35:.12);
 burst(W/2,H/2,s.a.color,s.a.odds>=100000?420:(s.a.odds>=1000?150:55),
  s.a.odds>=100000?2.8:(s.a.odds>=1000?1.5:.7));
 for(let i=0;i<(s.a.odds>=100000?14:(s.a.odds>=1000?6:2));i++)addRing(s.a.color,s.a.odds>=100000?7:(s.a.odds>=1000?4:2));
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
  const eventLayer=$("event");
  eventLayer.classList.add("fade-out");
  eventLayer.style.opacity="0";
  // Fade the full-screen reveal away over 100 ms, exposing the start screen.
  setTimeout(()=>{
   if(s.token!==token)return;
   eventLayer.classList.remove("show","fade-out");
   eventLayer.style.opacity="";
   scene.classList.remove("revealing");
   resize();
   setBusy(false);
   if(auto){autoTimer=setTimeout(()=>{autoTimer=null;if(auto&&!rolling)roll();},350);}
  },100);
 },s.replay?1300:1500);
}
function updateSequence(now){
 const s=sequence;
 if(!s||s.done||s.token!==token)return;
 const p=Math.min(1,(now-s.start)/s.duration),a=s.a;
 if(p<.28){$("eventLabel").textContent="ANOMALY DETECTED";$("eventSub").textContent="REALITY IS RESPONDING";}
 else if(p<.62){$("eventLabel").textContent=a.odds>=100000?"A COSMIC PRESENCE AWAKENS":"AURA FORMING";$("eventSub").textContent="ENERGY CONVERGENCE";}
 else{$("eventLabel").textContent="REVEAL IMMINENT";$("eventSub").textContent="PREPARE FOR DISCOVERY";}
 const amount=a.odds>=100000?8:(a.odds>=1000?5:2);
 for(let i=0;i<amount;i++){
  const angle=Math.random()*Math.PI*2;
  const r=(.1+Math.random()*.55)*Math.min(W,H);
  const x=W/2+Math.cos(angle)*r,y=H/2+Math.sin(angle)*r;
  particles.push({x,y,vx:(W/2-x)*(.009+p*.035),vy:(H/2-y)*(.009+p*.035),life:18+Math.random()*30,size:1+Math.random()*(a.odds>=1000?3:1.5),col:a.color});
 }
 if(Math.random()<(a.odds>=100000?.6:.18))addRing(a.color,(a.odds>=1000?5:2)+p*5);
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

 // Cinematic 8-second intro: collapsing star field, rotating sigils and a portal opening.
 const elapsed=now-introStart;
 const intro=Math.min(1,elapsed/(reduced?900:8000));
 ix.clearRect(0,0,W,H);ix.fillStyle="#020204";ix.fillRect(0,0,W,H);
 const portal=Math.max(0,Math.min(1,(intro-.12)/.78));
 const pulse=1+Math.sin(t*2.2)*.035;
 ix.save();ix.translate(W/2,H/2);ix.rotate(t*.12);
 for(let ring=0;ring<5;ring++){
  const rr=(Math.min(W,H)*(.08+portal*.44*(ring/5+.15)))*pulse;
  ix.beginPath();ix.ellipse(0,0,rr,rr*(.52+ring*.07),0,0,Math.PI*2);
  ix.strokeStyle=color(ring%2?"#8e6ee8":"#d9bd7b",.18+portal*.45);ix.lineWidth=ring===0?2:1;ix.stroke();
 }
 for(let i=0;i<96;i++){
  const a=i*2.399+t*(i%2?.08:-.04),r=(Math.min(W,H)*(.04+portal*.47))*((i%17+1)/18);
  const x=Math.cos(a)*r,y=Math.sin(a)*r;
  ix.fillStyle=color(i%3===0?"#fff0c9":"#bda7ff",.18+portal*.72);
  ix.beginPath();ix.arc(x,y,(i%5===0?2.1:0.8)+portal,0,Math.PI*2);ix.fill();
 }
 // Bright vertical rift that opens near the end of the intro.
 const seam=(2+Math.pow(portal,2)*W*.9);
 const grad=ix.createLinearGradient(-seam/2,0,seam/2,0);
 grad.addColorStop(0,"rgba(190,160,255,0)");grad.addColorStop(.43,"rgba(198,167,109,.2)");
 grad.addColorStop(.5,"rgba(255,250,226,.95)");grad.addColorStop(.57,"rgba(198,167,109,.2)");grad.addColorStop(1,"rgba(190,160,255,0)");
 ix.fillStyle=grad;ix.fillRect(-seam/2,-H,seam,H*2);ix.restore();
 // Lens-flare beam sweeps across the portal.
 ix.save();ix.translate(W/2,H/2);ix.rotate(-.18+Math.sin(t*.45)*.12);
 const beamW=W*(.1+intro*.9),beam=ix.createLinearGradient(-beamW/2,0,beamW/2,0);
 beam.addColorStop(0,"rgba(255,220,150,0)");beam.addColorStop(.5,"rgba(255,238,190,"+(intro*.18)+")");beam.addColorStop(1,"rgba(255,220,150,0)");
 ix.fillStyle=beam;ix.fillRect(-beamW/2,-H*.6,beamW,H*1.2);ix.restore();

 if(!introDone){
  $("introTitle").style.opacity=String(Math.max(0,Math.min(1,(intro-.18)*2)));
  $("introTitle").style.transform="translateY("+(12-intro*12)+"px) scale("+(.94+intro*.06)+")";
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

 // Aura-specific reveal effects: each style has its own silhouette/motion language.
 if($("event").classList.contains("show")){
  ex.clearRect(0,0,EW,EH);
  const s=sequence;
  if(s){
   const p=Math.min(1,(now-s.start)/s.duration),a=s.a,cx2=EW/2,cy2=EH/2,limit=Math.min(EW,EH)*.46;
   // Opaque backdrop fills the screen and prevents duplicate text from the start screen.
   ex.fillStyle="#030306";ex.fillRect(0,0,EW,EH);
   const glow=ex.createRadialGradient(cx2,cy2,1,cx2,cy2,limit*(.35+p*.8));
   glow.addColorStop(0,color(a.color,.2+p*.22));glow.addColorStop(1,"rgba(0,0,0,0)");
   ex.fillStyle=glow;ex.fillRect(0,0,EW,EH);
   // Rare and ultra-rare auras get full-screen multicolour streaks, not just a centered symbol.
   if(a.odds>=1000){
    const palette=a.odds>=100000?[a.color,"#ffffff","#8e78ff","#54e7ff","#ff70d6","#ffd66b"]:[a.color,"#ffffff","#68e7ff","#ff78c8"];
    const streakCount=a.odds>=100000?42:20;
    ex.save();ex.globalCompositeOperation="lighter";
    for(let i=0;i<streakCount;i++){
     const lane=(i*97.31+(i%3)*41)%EH;
     const speed=(a.odds>=100000?520:360)+(i%7)*55;
     const travel=(now/1000*speed+i*137)%(EW+360)-180;
     const y=(lane+Math.sin(t*1.7+i*2.1)*EH*.07+EH)%(EH);
     const len=(a.odds>=100000?180:100)+(i%5)*38;
     const col=palette[i%palette.length];
     ex.strokeStyle=color(col,a.odds>=100000?.78:.5);ex.lineWidth=i%6===0?2.4:1;
     ex.shadowColor=col;ex.shadowBlur=a.odds>=100000?16:8;
     ex.beginPath();ex.moveTo(travel-len,y+Math.sin(t*2+i)*28);ex.lineTo(travel,y);ex.lineTo(travel+len*.12,y+Math.cos(t*1.4+i)*8);ex.stroke();
    }
    ex.shadowBlur=0;
    // Chromatic diagonal cuts sweep across the entire screen on the rarest rolls.
    if(a.odds>=100000){
     for(let j=0;j<7;j++){
      const offset=((t*(240+j*27)+j*EW/7)%(EW+EH))-EH*.25;
      ex.strokeStyle=color(palette[(j+2)%palette.length],.22);ex.lineWidth=1+(j%3);
      ex.beginPath();ex.moveTo(offset,0);ex.lineTo(offset-EH*.65,EH);ex.stroke();
     }
    }
    ex.restore();
   }
   ex.save();ex.translate(cx2,cy2);
   const spin=t*(a.odds>=100000?-.65:.35),style=a.style;
   ex.strokeStyle=color(a.color,.8);ex.fillStyle=color(a.color,.16);ex.lineWidth=1.5;
   const line=(x1,y1,x2,y2,alpha=1)=>{ex.globalAlpha=alpha;ex.beginPath();ex.moveTo(x1,y1);ex.lineTo(x2,y2);ex.stroke();ex.globalAlpha=1;};
   const polygon=(n,r1,r2,rot=0)=>{ex.beginPath();for(let i=0;i<n*2;i++){const an=rot+i*Math.PI/n,rr=i%2===0?r1:r2,x=Math.cos(an)*rr,y=Math.sin(an)*rr;if(i===0)ex.moveTo(x,y);else ex.lineTo(x,y);}ex.closePath();ex.stroke();};
   const circle=(r,alpha=1)=>{ex.globalAlpha=alpha;ex.beginPath();ex.arc(0,0,r,0,Math.PI*2);ex.stroke();ex.globalAlpha=1;};
   if(style==="ash"){
    for(let i=0;i<34;i++){const an=i*2.4+t*(.2+i%2*.15),r=limit*(.1+((i*17+p*90)%100)/120);ex.fillStyle=color(a.color,.7);ex.beginPath();ex.arc(Math.cos(an)*r,Math.sin(an)*r,1+(i%3),0,7);ex.fill();}
   }else if(style==="tide"){
    for(let i=0;i<7;i++){ex.beginPath();for(let j=0;j<=90;j++){const an=j/90*Math.PI*2,r=limit*(.12+i*.1)+Math.sin(an*4+t*2+i)*9;const x=Math.cos(an+t*.2)*r,y=Math.sin(an+t*.2)*r;if(j===0)ex.moveTo(x,y);else ex.lineTo(x,y);}ex.stroke();}
   }else if(style==="blood"||style==="inferno"){
    for(let i=0;i<42;i++){const an=i*2.399+t*(style==="inferno"?1.4:.5),r=limit*(.15+((i*13+p*80)%100)/120);line(Math.cos(an)*r,Math.sin(an)*r,Math.cos(an)*Math.max(0,r-18-p*50),Math.sin(an)*Math.max(0,r-18-p*50),.8);}
    polygon(8,limit*(.2+p*.35),limit*.12,spin);
   }else if(style==="moss"||style==="venom"){
    for(let i=0;i<12;i++){const an=i*Math.PI/6+spin,r=limit*(.15+p*.3);ex.beginPath();ex.ellipse(Math.cos(an)*r*.35,Math.sin(an)*r*.35,limit*.09,limit*.23,an,0,Math.PI*2);ex.stroke();}
   }else if(style==="glass"||style==="crystal"){
    for(let i=0;i<13;i++){const an=i*2.399+spin,r=limit*(.15+(i%4)*.13);ex.beginPath();ex.moveTo(Math.cos(an)*r,Math.sin(an)*r);ex.lineTo(Math.cos(an+.22)*(r+20+p*25),Math.sin(an+.22)*(r+20+p*25));ex.lineTo(Math.cos(an-.17)*(r+8),Math.sin(an-.17)*(r+8));ex.closePath();ex.stroke();}
   }else if(style==="sun"||style==="saint"||style==="oracle"||style==="origin"){
    for(let i=0;i<48;i++){const an=i*Math.PI/24+spin,inner=limit*(.12+(i%3)*.035),outer=limit*(.35+p*.45);line(Math.cos(an)*inner,Math.sin(an)*inner,Math.cos(an)*outer,Math.sin(an)*outer,.3+(i%3)*.2);}
    circle(limit*(.18+p*.2));circle(limit*(.32+p*.25),.55);polygon(12,limit*(.3+p*.15),limit*.22,spin);
   }else if(style==="ember"){
    for(let i=0;i<26;i++){const an=i*2.4+t*.7,r=limit*(.15+((i*11+p*120)%100)/130);ex.beginPath();ex.moveTo(Math.cos(an)*r,Math.sin(an)*r);ex.quadraticCurveTo(Math.cos(an+.5)*(r+18),Math.sin(an+.5)*(r+18),Math.cos(an+.15)*(r+38+p*25),Math.sin(an+.15)*(r+38+p*25));ex.stroke();}
    polygon(3,limit*(.25+p*.3),limit*.1,spin);
   }else if(style==="eclipse"||style==="null"||style==="end"||style==="rift"){
    circle(limit*(.12+p*.12),1);ex.fillStyle="#030306";ex.beginPath();ex.arc(0,0,limit*(.1+p*.13),0,7);ex.fill();
    for(let i=0;i<5;i++){ex.save();ex.rotate(spin*(i%2?-1:1)+i);ex.beginPath();ex.ellipse(0,0,limit*(.22+i*.055),limit*(.08+i*.018),0,0,Math.PI*2);ex.stroke();ex.restore();}
    polygon(10,limit*(.3+p*.25),limit*.16,spin);
   }else if(style==="winter"||style==="moon"){
    for(let i=0;i<8;i++){const an=i*Math.PI/4+spin,r=limit*(.12+p*.25);line(Math.cos(an)*r*.2,Math.sin(an)*r*.2,Math.cos(an)*r,Math.sin(an)*r);line(Math.cos(an)*r*.65,Math.sin(an)*r*.65,Math.cos(an+.28)*r*.8,Math.sin(an+.28)*r*.8);line(Math.cos(an)*r*.65,Math.sin(an)*r*.65,Math.cos(an-.28)*r*.8,Math.sin(an-.28)*r*.8);}
    circle(limit*(.22+p*.22));
   }else if(style==="marrow"||style==="phantom"){
    for(let i=0;i<9;i++){const an=i*Math.PI*2/9+spin,r=limit*(.2+p*.2);ex.beginPath();ex.ellipse(Math.cos(an)*r*.5,Math.sin(an)*r*.5,limit*.1,limit*.27,an,0,Math.PI*2);ex.stroke();}
    polygon(9,limit*(.28+p*.16),limit*.08,-spin);
   }else if(style==="starless"||style==="nebula"||style==="zenith"){
    for(let i=0;i<7;i++){ex.save();ex.rotate(spin*(i%2?-.6:1)+i*.4);ex.beginPath();ex.ellipse(0,0,limit*(.12+i*.045),limit*(.08+i*.025),0,0,Math.PI*2);ex.stroke();ex.restore();}
    for(let i=0;i<65;i++){const an=i*2.399+t*.08,r=limit*(.08+((i*29)%100)/120);ex.fillStyle=color(a.color,.35+(i%4)*.15);ex.fillRect(Math.cos(an)*r,Math.sin(an)*r,1.5,1.5);}
   }else if(style==="seraph"){
    for(let side of [-1,1]){ex.save();ex.scale(side,1);ex.beginPath();ex.moveTo(0,0);ex.bezierCurveTo(limit*.12,-limit*.05,limit*.18,-limit*.6,limit*.55,-limit*.42);ex.bezierCurveTo(limit*.38,-limit*.15,limit*.25,limit*.08,0,0);ex.stroke();for(let i=1;i<7;i++)line(limit*.06*i,-limit*.06*i,limit*.08*i,-limit*(.12+i*.045));ex.restore();}
    circle(limit*.16);
   }else if(style==="storm"){
    for(let i=0;i<7;i++){const an=i*.9+t*.2;ex.beginPath();ex.moveTo(Math.cos(an)*limit*.1,Math.sin(an)*limit*.1);for(let j=1;j<7;j++){const r=limit*(.1+j*.07),aa=an+(Math.random()-.5)*.55;ex.lineTo(Math.cos(aa)*r,Math.sin(aa)*r);}ex.stroke();}
   }else{
    circle(limit*(.2+p*.2));polygon(8,limit*(.3+p*.2),limit*.1,spin);
   }
   // Tiny sparks drift outward for every aura, but the main shape is unique.
   const sparks=a.odds>=100000?36:12;
   for(let i=0;i<sparks;i++){const an=i*2.399+t*(i%2?.25:-.18),r=limit*(.15+((i*19+p*70)%100)/115);ex.fillStyle=color(a.color,.5);ex.beginPath();ex.arc(Math.cos(an)*r,Math.sin(an)*r,1+(i%3),0,Math.PI*2);ex.fill();}
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

components.html(html, height=900, scrolling=True)
