"""Zone fill boundary vs items of a different net class (and vs other zones): must be >= 2.0 mm across classes, >= 0.2 same class."""
import re,math,json,fnmatch,sys
B=sys.argv[1]; PRO=sys.argv[2]; b=open(B).read()
pats=json.load(open(PRO))['net_settings'].get('netclass_patterns') or []
def cls(n):
    for x in pats:
        if fnmatch.fnmatch(n,x['pattern']): return x['netclass']
    return 'Default'
# items (reuse parser from geom-audit, simplified to point sets along edges)
pts=[]  # (layer, net, x, y, radius)  radius = half-width/pad half-extent approx
for m in re.finditer(r'\(footprint "([^"]+)"(.*?)\n\t\)\n', b, re.S):
    body=m.group(2); ref=re.search(r'\(property "Reference" "([^"]+)"',body).group(1)
    at=re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',body); fx,fy,fr=float(at.group(1)),float(at.group(2)),float(at.group(3) or 0)
    for p in re.finditer(r'\(pad "([^"]*)" (\w+) (\w+)\n\t\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)\n\t\t\t\(size ([-\d.]+) ([-\d.]+)\)(.*?)\n\t\t\)',body,re.S):
        px,py,pa,sx,sy=float(p.group(4)),float(p.group(5)),float(p.group(6) or 0),float(p.group(7)),float(p.group(8))
        net=re.search(r'\(net "([^"]*)"\)',p.group(9)); net=net.group(1) if net else ''
        if not net or net.startswith('unconnected-'): continue
        layers=re.search(r'\(layers ([^)]*)\)',p.group(9)).group(1)
        a=math.radians(-fr); ax=fx+px*math.cos(a)-py*math.sin(a); ay=fy+px*math.sin(a)+py*math.cos(a)
        w,h=(sy,sx) if round(pa)%180==90 else (sx,sy)
        lay=['F.Cu','B.Cu'] if '*.Cu' in layers else [l for l in ('F.Cu','B.Cu') if l in layers]
        # sample pad outline
        for L in lay:
            for k in range(13):
                t=k/12
                for (x,y) in ((ax-w/2+w*t,ay-h/2),(ax-w/2+w*t,ay+h/2),(ax-w/2,ay-h/2+h*t),(ax+w/2,ay-h/2+h*t)): pts.append((L,net,'pad %s.%s'%(ref,p.group(1)),x,y,0))
for m in re.finditer(r'\(segment\n\t\t\(start ([-\d.]+) ([-\d.]+)\)\n\t\t\(end ([-\d.]+) ([-\d.]+)\)\n\t\t\(width ([-\d.]+)\)\n\t\t\(layer "([^"]+)"\)\n\t\t\(net "([^"]+)"\)',b):
    x1,y1,x2,y2,w=map(float,m.groups()[:5]); n=max(2,int(math.hypot(x2-x1,y2-y1)/0.1)+1)
    for k in range(n): pts.append((m.group(6),m.group(7),'track',x1+(x2-x1)*k/(n-1),y1+(y2-y1)*k/(n-1),w/2))
for m in re.finditer(r'\(via\n\t\t\(at ([-\d.]+) ([-\d.]+)\)\n\t\t\(size ([-\d.]+)\)[^)]*\)\n\t\t\(layers "[^"]+" "[^"]+"\)\n\t\t\(net "([^"]+)"\)',b):
    x,y,s=map(float,m.groups()[:3])
    for L in ('F.Cu','B.Cu'): pts.append((L,m.group(4),'via',x,y,s/2))
# zone fill boundary points
zp=[]
for m in re.finditer(r'\(zone\n\t\t\(net "([^"]+)"\)(.*?)\n\t\)\n',b,re.S):
    for fp in re.finditer(r'\(filled_polygon\n\t\t\t\(layer "([^"]+)"\)(.*?)\n\t\t\)',m.group(2),re.S):
        poly=[(float(x),float(y)) for x,y in re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)',fp.group(2))]
        for (ax,ay),(bx,by) in zip(poly,poly[1:]+poly[:1]):
            n=max(1,int(math.hypot(bx-ax,by-ay)/0.1))
            for k in range(n): zp.append((fp.group(1),m.group(1),ax+(bx-ax)*k/n,ay+(by-ay)*k/n))
grid={}
for L,net,x,y in zp: grid.setdefault((L,int(x),int(y)),[]).append((net,x,y))
viol={}
for L,net,what,x,y,r in pts:
    c=cls(net)
    for dx in range(-3,4):
        for dy in range(-3,4):
            for znet,zx,zy in grid.get((L,int(x)+dx,int(y)+dy),()):
                if znet==net: continue
                need=2.0 if cls(znet)!=c else 0.2
                d=math.hypot(x-zx,y-zy)-r
                if d<need-0.02:
                    key=(L,what,net,znet); viol[key]=min(viol.get(key,9),round(d,3))
print('item sample points:',len(pts),' zone boundary points:',len(zp),' violations:',len(viol))
cross=[(k,v) for k,v in viol.items() if cls(k[2])!=cls(k[3])]
print("CROSS-CLASS (2 mm rule) violations:",len(cross))
for k,v in sorted(cross,key=lambda kv:kv[1]): print('  ',v,k)
