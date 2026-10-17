(function(){
  var b=document.querySelector('.menu-btn'), n=document.getElementById('nav');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
})();
(function(){
  var m=document.querySelector('.marquee'); if(!m) return;
  var tr=m.querySelector('.track'), sl=m.parentNode;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SPEED=32, GAP=32, x=0, P=1, last=0, hover=false, drag=null, idleUntil=0, anim=null, vel=0, moved=false;
  function period(){P=(tr.scrollWidth+GAP)/2||1;}
  function wrap(){x=((x%P)+P)%P;}
  function paint(){tr.style.transform='translate3d('+(-x)+'px,0,0)';}
  function step(){var c=tr.querySelector('.pcard');return c?c.getBoundingClientRect().width+GAP:300;}
  function hold(ms){idleUntil=performance.now()+ms;}
  function loop(t){
    var dt=last?Math.min(t-last,64)/1000:0; last=t;
    if(anim){var k=Math.min(1,(t-anim.t0)/anim.d);var e=1-Math.pow(1-k,3);x=anim.from+anim.by*e;if(k>=1)anim=null;}
    else if(!drag&&Math.abs(vel)>5){x+=vel*dt;vel*=Math.pow(0.04,dt);}
    else if(!drag&&!hover&&!reduce&&t>idleUntil){x+=SPEED*dt;}
    wrap();paint();requestAnimationFrame(loop);
  }
  m.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')hover=true;});
  m.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')hover=false;});
  m.addEventListener('pointerdown',function(e){
    if(e.button!==0)return; anim=null;vel=0;moved=false;
    drag={id:e.pointerId,sx:e.clientX,sy:e.clientY,x0:x,lx:e.clientX,lt:performance.now(),axis:null};
  });
  m.addEventListener('pointermove',function(e){
    if(!drag||e.pointerId!==drag.id)return;
    var dx=e.clientX-drag.sx, dy=e.clientY-drag.sy;
    if(!drag.axis){if(Math.abs(dx)<6&&Math.abs(dy)<6)return;drag.axis=Math.abs(dx)>Math.abs(dy)?'x':'y';
      if(drag.axis==='x'){m.setPointerCapture(e.pointerId);m.classList.add('dragging');}}
    if(drag.axis!=='x'){drag=null;return;}
    moved=true; var now=performance.now();
    vel=-(e.clientX-drag.lx)/Math.max(1,(now-drag.lt))*1000; drag.lx=e.clientX; drag.lt=now;
    x=drag.x0-dx; wrap();
  });
  function end(e){if(!drag||(e&&e.pointerId!==drag.id))return;
    if(performance.now()-drag.lt>80)vel=0; vel=Math.max(-3000,Math.min(3000,vel));
    drag=null;m.classList.remove('dragging');hold(3000);}
  m.addEventListener('pointerup',end);m.addEventListener('pointercancel',end);
  m.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false;}},true);
  function go(dir){vel=0;anim={from:x,by:dir*step(),t0:performance.now(),d:450};hold(4000);}
  var pv=sl.querySelector('.sl-btn.prev'), nx=sl.querySelector('.sl-btn.next');
  if(pv)pv.addEventListener('click',function(){go(-1);});
  if(nx)nx.addEventListener('click',function(){go(1);});
  m.addEventListener('focusin',function(e){var c=e.target.closest('.pcard');if(!c)return;
    hold(6000);anim=null;x=c.offsetLeft-24;wrap();});
  window.addEventListener('resize',period);
  period();requestAnimationFrame(loop);
})();
