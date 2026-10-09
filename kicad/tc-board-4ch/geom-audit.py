"""Independent geometric audit: min copper distance between items of different nets.
Pads as rectangles/circles, tracks as capsules, vias as circles. Threshold 0.2 mm same class, 2.0 mm across island classes."""
import re,math,json,fnmatch,sys
from collections import defaultdict
B=sys.argv[1]; PRO=sys.argv[2]
b=open(B).read()
pro=json.load(open(PRO)); pats=pro['net_settings'].get('netclass_patterns') or []
def cls(n):
    for x in pats:
        if fnmatch.fnmatch(n,x['pattern']): return x['netclass']
    return 'Default'
items=[]  # (kind, layer, net, geom)
for m in re.finditer(r'\(footprint "([^"]+)"(.*?)\n\t\)\n', b, re.S):
    body=m.group(2); ref=re.search(r'\(property "Reference" "([^"]+)"',body).group(1)
    at=re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',body); fx,fy,fr=float(at.group(1)),float(at.group(2)),float(at.group(3) or 0)
    for p in re.finditer(r'\(pad "([^"]*)" (\w+) (\w+)\n\t\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)\n\t\t\t\(size ([-\d.]+) ([-\d.]+)\)(.*?)\n\t\t\)',body,re.S):
        px,py,pa,sx,sy=float(p.group(4)),float(p.group(5)),float(p.group(6) or 0),float(p.group(7)),float(p.group(8))
        net=re.search(r'\(net "([^"]*)"\)',p.group(9)); net=net.group(1) if net else ''
        layers=re.search(r'\(layers ([^)]*)\)',p.group(9)).group(1)
        a=math.radians(-fr); ax=fx+px*math.cos(a)-py*math.sin(a); ay=fy+px*math.sin(a)+py*math.cos(a)
        w,h=(sy,sx) if round(pa)%180==90 else (sx,sy)
        if round(pa)%90: w=h=max(sx,sy)  # odd angle: conservative circle-ish box
        lay=['F.Cu','B.Cu'] if '*.Cu' in layers else [l for l in ('F.Cu','B.Cu') if l in layers]
        shape=p.group(3)
        for L in lay: items.append(('pad %s.%s'%(ref,p.group(1)),L,net,('rect',ax,ay,w,h) if shape!='circle' else ('circ',ax,ay,max(w,h)/2)))
for m in re.finditer(r'\(segment\n\t\t\(start ([-\d.]+) ([-\d.]+)\)\n\t\t\(end ([-\d.]+) ([-\d.]+)\)\n\t\t\(width ([-\d.]+)\)\n\t\t\(layer "([^"]+)"\)\n\t\t\(net "([^"]+)"\)',b):
    x1,y1,x2,y2,w=map(float,m.groups()[:5]); items.append(('track',m.group(6),m.group(7),('seg',x1,y1,x2,y2,w/2)))
for m in re.finditer(r'\(via\n\t\t\(at ([-\d.]+) ([-\d.]+)\)\n\t\t\(size ([-\d.]+)\)[^)]*\)\n\t\t\(layers "[^"]+" "[^"]+"\)\n\t\t\(net "([^"]+)"\)',b):
    x,y,s=map(float,m.groups()[:3])
    for L in ('F.Cu','B.Cu'): items.append(('via',L,m.group(4),('circ',x,y,s/2)))
def pt_seg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L2=dx*dx+dy*dy
    t=0 if L2==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L2)); return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
def rect_pt(x,y,w,h,px,py):  # distance from point to axis-aligned rect
    dx=max(x-w/2-px,0,px-(x+w/2)); dy=max(y-h/2-py,0,py-(y+h/2)); return math.hypot(dx,dy)
def dist(g1,g2):
    k1,k2=g1[0],g2[0]
    if k1=='seg' and k2!='seg': g1,g2=g2,g1; k1,k2=k2,k1
    if k1=='circ' and k2=='circ': return math.hypot(g1[1]-g2[1],g1[2]-g2[2])-g1[3]-g2[3]
    if k1=='circ' and k2=='seg': return pt_seg(g1[1],g1[2],*g2[1:5])-g1[3]-g2[5]
    if k1=='rect' and k2=='circ': return rect_pt(g1[1],g1[2],g1[3],g1[4],g2[1],g2[2])-g2[3]
    if k1=='circ' and k2=='rect': return rect_pt(g2[1],g2[2],g2[3],g2[4],g1[1],g1[2])-g1[3]
    if k1=='rect' and k2=='rect':
        dx=max(g1[1]-g1[3]/2-(g2[1]+g2[3]/2),0,g2[1]-g2[3]/2-(g1[1]+g1[3]/2)); dy=max(g1[2]-g1[4]/2-(g2[2]+g2[4]/2),0,g2[2]-g2[4]/2-(g1[2]+g1[4]/2)); return math.hypot(dx,dy)
    if k1=='rect' and k2=='seg':  # sample the segment
        x1,y1,x2,y2,r=g2[1:]; n=max(2,int(math.hypot(x2-x1,y2-y1)/0.05)+1)
        return min(rect_pt(g1[1],g1[2],g1[3],g1[4],x1+(x2-x1)*k/(n-1),y1+(y2-y1)*k/(n-1)) for k in range(n))-r
    if k1=='seg' and k2=='seg':
        x1,y1,x2,y2,r1=g1[1:]; x3,y3,x4,y4,r2=g2[1:]
        d=min(pt_seg(x1,y1,x3,y3,x4,y4),pt_seg(x2,y2,x3,y3,x4,y4),pt_seg(x3,y3,x1,y1,x2,y2),pt_seg(x4,y4,x1,y1,x2,y2))
        # crossing check
        def ccw(ax,ay,bx,by,cx,cy): return (cy-ay)*(bx-ax)>(by-ay)*(cx-ax)
        if ccw(x1,y1,x3,y3,x4,y4)!=ccw(x2,y2,x3,y3,x4,y4) and ccw(x1,y1,x2,y2,x3,y3)!=ccw(x1,y1,x2,y2,x4,y4): d=0
        return d-r1-r2
def bbox(g):
    if g[0]=='circ': return (g[1]-g[3],g[2]-g[3],g[1]+g[3],g[2]+g[3])
    if g[0]=='rect': return (g[1]-g[3]/2,g[2]-g[4]/2,g[1]+g[3]/2,g[2]+g[4]/2)
    return (min(g[1],g[3])-g[5],min(g[2],g[4])-g[5],max(g[1],g[3])+g[5],max(g[2],g[4])+g[5])
viol=[]
by_layer=defaultdict(list)
for it in items: by_layer[it[1]].append(it)
for L,lst in by_layer.items():
    bb=[bbox(it[3]) for it in lst]
    for i in range(len(lst)):
        for j in range(i+1,len(lst)):
            a,c=lst[i],lst[j]
            if a[2]==c[2]: continue
            if a[2].startswith('unconnected-') or c[2].startswith('unconnected-'): continue
            if not a[2] or not c[2]: continue
            ca,cc=cls(a[2]),cls(c[2])
            need=0.2 if ca==cc else 2.0
            if ('ISO' in ca or 'ISO' in cc) and ca!=cc: need=2.0
            if bb[i][0]-need>bb[j][2] or bb[j][0]-need>bb[i][2] or bb[i][1]-need>bb[j][3] or bb[j][1]-need>bb[i][3]: continue
            d=dist(a[3],c[3])
            if d<need-1e-6: viol.append((round(d,3),need,L,a[0],a[2],c[0],c[2]))
viol.sort()
print('items:',len(items),' violations below threshold:',len(viol))
for v in viol[:40]: print('  ',v)
