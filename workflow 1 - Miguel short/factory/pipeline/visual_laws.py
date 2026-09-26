"""Measure declared connectors and completed emphasis in the emitted page.

Raster ink collisions still require the independent frame review. These checks
cover measurable SVG/CSS geometry rather than treating a declared exception as proof.
"""
CHECK_JS = r"""() => {
 const errors=[]; const tl=window.__timelines?.main;
 const originalTime=tl?.time?.();
 const clips=[...document.querySelectorAll('#root > [data-start][data-duration]')];
 const originalVisibility=clips.map(el=>el.style.visibility);
 const seekVisible=(at)=>{
   tl.seek(at,false);
   for(const el of clips){
     const start=Number(el.dataset.start),duration=Number(el.dataset.duration);
     el.style.visibility=at>=start-.01&&at<start+duration-.01?'visible':'hidden';
   }
 };
 try {
 const add=(el,msg)=>errors.push({type:'visual_contract',severity:'error',elements:[el.id||el.tagName],detail:msg,from:0,to:0});
 const nodes=[...document.querySelectorAll('[data-connect-to],[data-emphasis],.connector,.arrow')];
 for (const el of nodes) {
   const isConnector=el.matches('[data-connect-to],.connector,.arrow');
   const targetId=isConnector?el.dataset.connectTo:el.dataset.emphasisTarget;
   const target=targetId&&document.getElementById(targetId.replace(/^#/,''));
   if(!target){add(el,'Declare an existing target ID for every connector/emphasis');continue}
   const at=Number(el.dataset.checkAt);
   if(!el.dataset.checkAt||!Number.isFinite(at)||at<0||!tl||at>=tl.duration()) {add(el,'Declare data-check-at at the completed visible state');continue}
   seekVisible(at);
   const visible=(node)=>{let op=1;for(let n=node;n;n=n.parentElement){const c=getComputedStyle(n);if(c.display==='none'||c.visibility==='hidden')return false;op*=Number(c.opacity)}return op>.1};
   if(!visible(el)||!visible(target)){add(el,'Completed check state hides the mark or its target');continue}
   const b=target.getBoundingClientRect(),r=el.getBoundingClientRect();
   if(isConnector){
     const side=el.dataset.anchorSide;
     const fraction=el.dataset.anchorFraction === undefined ? 0.5 : Number(el.dataset.anchorFraction);
     if(!['left','right','top','bottom'].includes(side)||!Number.isFinite(fraction)||fraction<0||fraction>1){add(el,'Declare target anchor side and fraction');continue}
     const path=el.getTotalLength?el:el.querySelector('path,line,polyline');
     let end;
     if(path?.getTotalLength){
       const q=path.getPointAtLength(path.getTotalLength()),m=path.getScreenCTM();
       end=new DOMPoint(q.x,q.y).matrixTransform(m);
       const head=el.querySelector('path.shead,path.ahead,path[data-connector-head]');
       if(head){
         // The shaft stops at the arrowhead base; the painted tip is the endpoint.
         const number='(-?\\d+(?:\\.\\d+)?)';
         const pattern=new RegExp('^\\s*M\\s*'+number+'[ ,]+'+number+'\\s*L\\s*'+number+'[ ,]+'+number+'\\s*L\\s*'+number+'[ ,]+'+number+'\\s*Z?\\s*$','i');
         const points=head.getAttribute('d')?.match(pattern);
         if(!points){add(el,'Arrowhead needs a measurable triangle tip');continue}
         const h=head.getScreenCTM(),hc=getComputedStyle(head);
         if(((hc.fill==='none'||hc.fill==='rgba(0, 0, 0, 0)')&&(hc.stroke==='none'||Number(hc.strokeOpacity)<=.1||parseFloat(hc.strokeWidth)<=0))||Number(hc.opacity)<=.1){add(el,'Completed arrowhead is not painted');continue}
         const before=path.getPointAtLength(Math.max(0,path.getTotalLength()-.1));
         const prev=new DOMPoint(before.x,before.y).matrixTransform(m);
         const dx=end.x-prev.x,dy=end.y-prev.y;
         if(Math.hypot(dx,dy)<.00001){add(el,'Arrow shaft has no measurable final direction');continue}
         const vertices=[1,3,5].map(i=>new DOMPoint(Number(points[i]),Number(points[i+1])).matrixTransform(h));
         end=vertices.reduce((best,v)=>v.x*dx+v.y*dy>best.x*dx+best.y*dy?v:best);
       }
     } else {
       // CSS connectors are measured from their painted bar or triangle tip.
       // Rotated/skewed shapes need a separate geometry implementation.
       let axisAligned=true;
       for(let n=el;n;n=n.parentElement){const tr=getComputedStyle(n).transform;
         if(tr!=='none'){const m=new DOMMatrix(tr);if(Math.abs(m.b)>.00001||Math.abs(m.c)>.00001||m.a<=0||m.d<=0)axisAligned=false}}
       const head=el.querySelector('.ahead'),c=getComputedStyle(el);
       const solid=(color)=>color!=='transparent'&&color!=='rgba(0, 0, 0, 0)';
       if(axisAligned&&head){
         const hc=getComputedStyle(head),clip=hc.clipPath;
         const points=clip.startsWith('polygon(')?clip.slice(8,-1).split(',').map(p=>p.trim().match(/^([\d.]+)%\s+([\d.]+)%$/)):[];
         if(solid(hc.backgroundColor)&&points.length===3&&points.every(Boolean)){
           const xy=points.map(p=>[Number(p[1])/100,Number(p[2])/100]);
           // The two vertices of the triangle base share x or y; the third is its tip.
           let tip=null;
           for(let i=0;i<3;i++){const other=xy.filter((_,j)=>j!==i);
             if((other[0][0]===other[1][0]&&xy[i][0]!==other[0][0])||
                (other[0][1]===other[1][1]&&xy[i][1]!==other[0][1]))tip=xy[i]}
           if(tip){const h=head.getBoundingClientRect();end={x:h.left+tip[0]*h.width,y:h.top+tip[1]*h.height}}
         }
       } else if(axisAligned&&!el.children.length&&solid(c.backgroundColor)&&Math.max(r.width,r.height)>=2*Math.min(r.width,r.height)){
         if(r.width>r.height&&['left','right'].includes(side))end={x:side==='left'?r.right:r.left,y:r.top+r.height/2};
         if(r.height>r.width&&['top','bottom'].includes(side))end={x:r.left+r.width/2,y:side==='top'?r.bottom:r.top};
       }
       if(!end){add(el,'Connector needs a measurable SVG path/line or supported painted CSS bar/triangle');continue}
     }
     const anchor=side==='left'?[b.left,b.top+b.height*fraction]:side==='right'?[b.right,b.top+b.height*fraction]:side==='top'?[b.left+b.width*fraction,b.top]:[b.left+b.width*fraction,b.bottom];
     const distance=Math.hypot(end.x-anchor[0],end.y-anchor[1]);
     if(distance>4)add(el,`Connector misses its target anchor by ${distance.toFixed(2)}px (maximum 4px)`);
   } else {
     const kind=el.dataset.emphasis;
     if(kind==='ring'){add(el,'Circular emphasis is disallowed by the current visual standard');continue}
     for(const p of [el,...el.querySelectorAll('path,line,rect,polyline,circle,ellipse')]){
       const c=getComputedStyle(p),d=c.strokeDasharray;
       if(d&&d!=='none'&&Math.abs(parseFloat(c.strokeDashoffset)||0)>.5)add(el,'Completed emphasis still has an unfinished stroke');
     }
     // INK IS WHAT PAINTS, NOT WHAT THE WRAPPER'S COMPUTED STYLE SAYS (2026-09-06):
     // a DIV wrapping a stroked SVG reports stroke 'none' and a borderTopColor equal
     // to its inherited text colour, so the old wrapper-only read flagged a teal SVG
     // box over navy text as same-colour.  Collect the colours of the VISIBLE painted
     // pieces (SVG strokes/fills with width, painted CSS borders, and for highlights
     // the background; for the target also its own text colour) on both sides.
     const solidC=(v)=>!!v&&v!=='none'&&v!=='transparent'&&v!=='rgba(0, 0, 0, 0)';
     const SHAPES='path,line,rect,polyline,polygon,circle,ellipse';
     // opts.fill: count SVG fills as ink (the target's own drawing); an emphasis
     // stroke/box/border only paints its STROKE or painted CSS border, so the
     // shape's unchanged fill (paper behind a purple border) is not its ink.
     // opts.exclude: a subtree to ignore, so an emphasis nested INSIDE its own
     // target is never compared with itself (run-16 Plants, 2026-09-06).
     const painted=(root,opts)=>{
       const inks=new Set();let widths=[];
       const consider=(n)=>{
         if(opts.exclude&&(n===opts.exclude||opts.exclude.contains(n)))return;
         if(!visible(n))return;
         const s=getComputedStyle(n);
         if(n instanceof SVGElement){
           if(!n.matches(SHAPES))return;
           const sw=parseFloat(s.strokeWidth)||0;
           if(solidC(s.stroke)&&sw>0){inks.add(s.stroke);widths.push(sw)}
           if(opts.fill&&solidC(s.fill))inks.add(s.fill);
         } else {
           const bw=parseFloat(s.borderTopWidth)||0;
           if(solidC(s.borderTopColor)&&bw>0&&s.borderTopStyle!=='none'){inks.add(s.borderTopColor);widths.push(bw)}
           if(opts.background&&solidC(s.backgroundColor))inks.add(s.backgroundColor);
           if(opts.text&&solidC(s.color)&&[...n.childNodes].some(t=>t.nodeType===3&&t.textContent.trim()))inks.add(s.color);
         }
       };
       consider(root);root.querySelectorAll('*').forEach(consider);
       return {inks,width:widths.length?Math.max(...widths):0};
     };
     const mine=painted(el,{background:kind==='highlight',text:false,fill:kind==='highlight'});
     const theirs=painted(target,{background:false,text:true,fill:true,exclude:el});
     if(!mine.inks.size){add(el,'Emphasis paints no visible ink (no stroked/filled shape, painted border or highlight fill)');continue}
     if(kind==='box'){
       const gaps=[b.left-r.left,r.right-b.right,b.top-r.top,r.bottom-b.bottom];
       if(Math.min(...gaps)-mine.width/2<4)add(el,'Emphasis box needs at least 4px clearance from the target bounds');
     }
     const shared=[...mine.inks].filter(x=>theirs.inks.has(x));
     if(shared.length)add(el,'Emphasis uses the same color as its target ink ('+shared.join(', ')+')');
   }
 }
 return errors;
 } finally {
   if(tl&&Number.isFinite(originalTime))tl.seek(originalTime,false);
   clips.forEach((el,i)=>{el.style.visibility=originalVisibility[i]});
 }
}"""


def enforce_no_exemptions(page):
    """Production geometry may not opt logos or annotations out of measurement."""
    page.evaluate("""() => document.querySelectorAll('[data-overlap-ok],[data-glyph-ok]').forEach(el=>{
        el.removeAttribute('data-overlap-ok');el.removeAttribute('data-glyph-ok');
    })""")
