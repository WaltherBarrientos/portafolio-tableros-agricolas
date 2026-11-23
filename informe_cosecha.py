import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly
from shapely.geometry import Point, MultiPoint, Polygon, box
from shapely.ops import unary_union, voronoi_diagram
rng=np.random.default_rng(11)
G="#1B5233"; OR="#E8742E"; BG="white"
def es(x,d=0):
    s=f"{x:,.{d}f}"; return s.replace(",","X").replace(".",",").replace("X",".")
farms={"LA ESPERANZA":("LE",3),"SAN JOSÉ":("SJ",4),"EL MIRADOR":("EM",2),"BUENAVISTA":("BV",3),"LA PALMA":("LP",6)}
rows=[]
for f,(c,n) in farms.items():
    for i in range(1,n+1):
        ha=rng.uniform(6,22); arb=int(ha*rng.uniform(380,520)); pron=int(ha*rng.uniform(4000,13000))
        cum=rng.uniform(0.55,1.2) if c=="LP" else rng.uniform(0.82,1.22)
        kr=int(pron*cum); jor=round(kr/rng.uniform(250,540),1)
        rows.append(dict(f=f,l=f"{c}{i}",kr=kr,jor=jor,kha=kr/ha,rop=kr/jor,pron=pron,cum=kr/pron,kab=kr/arb,ha=ha))
KR=sum(r["kr"] for r in rows); PR=sum(r["pron"] for r in rows); JOR=sum(r["jor"] for r in rows); HA=sum(r["ha"] for r in rows)
fig=plt.figure(figsize=(16,9.25),dpi=120,facecolor=BG)
# sidebar
sb=fig.add_axes([0.015,0.03,0.12,0.94]); sb.axis("off"); sb.add_patch(Rectangle((0,0),1,1,color=G,transform=sb.transAxes))
k=[(es(KR/PR*100,2)+" %","% CUMPLIMIENTO"),(es(PR),"TOTAL PRONOSTICADO"),(es(KR),"KILOS REALES"),(es(KR/JOR,2),"RENDIMIENTO OPERARIO"),(es(KR/HA,2),"KILOS_POR_HA")]
for i,(v,t) in enumerate(k):
    y=0.89-i*0.19
    sb.text(0.5,y,v,ha="center",color=OR,fontsize=15,weight="bold",transform=sb.transAxes)
    sb.text(0.5,y-0.04,t,ha="center",color=OR,fontsize=9,weight="bold",transform=sb.transAxes)
fig.text(0.41,0.915,"INFORME GENERAL DE COSECHA 2026",ha="center",color=OR,fontsize=21)
# table detail
def table(rect,title,head,data,widths,total,fs=8.6):
    ax=fig.add_axes(rect); ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
    n=len(data)+3; h=1/n
    ax.add_patch(Rectangle((0,1-h),1,h,color=G)); ax.text(0.5,1-h/2,title,ha="center",va="center",color=OR,fontsize=12)
    xs=np.cumsum([0]+widths)
    for j,hd in enumerate(head): ax.text(xs[j]+0.01,1-1.5*h,hd,va="center",fontsize=fs,color="#222")
    ax.plot([0,1],[1-2*h,1-2*h],color="#2E75B6",lw=1)
    for i,r in enumerate(data):
        y=1-(2.5+i)*h
        if i%2==1: ax.add_patch(Rectangle((0,y-h/2),1,h,color="#EFEFEF",lw=0))
        for j,v in enumerate(r):
            ax.text(xs[j+1]-0.01 if j>=2 or len(head)==4 and j>=1 else xs[j]+0.01,y,v,va="center",fontsize=fs,ha="right" if (j>=2 or (len(head)==4 and j>=1)) else "left")
    y=1-(2.5+len(data))*h; ax.plot([0,1],[y+h/2,y+h/2],color="#2E75B6",lw=1)
    for j,v in enumerate(total):
        ax.text(xs[j+1]-0.01 if j>=1 else xs[j]+0.01,y,v,va="center",fontsize=fs,weight="bold",ha="right" if j>=1 else "left")
    for x in xs[1:-1]: ax.plot([x,x],[0,1-h],color="#BBBBBB",lw=0.6)
hd=["FINCA","LOTE","K. REALES","JORNALES","K_POR_HA","R.OPERARIO","PRONOSTICO","% CUMPLIM.","Kg POR ARBOL"]
w=[0.13,0.07,0.1,0.1,0.1,0.11,0.12,0.13,0.14]
data=[[r["f"],r["l"],es(r["kr"]),es(r["jor"],1),es(r["kha"],2),es(r["rop"],2),es(r["pron"]),es(r["cum"]*100,2)+" %",es(r["kab"],2)] for r in rows]
tot=["Total","",es(KR),es(JOR,1),es(KR/HA,2),es(KR/JOR,2),es(PR),es(KR/PR*100,2)+" %",es(sum(r['kr'] for r in rows)/sum(int(r['kr']/r['kab']) for r in rows),2)]
table([0.14,0.33,0.535,0.55],"Detallado",hd,data,w,tot)
# farm table
fd=[]
for f in farms:
    rr=[r for r in rows if r["f"]==f]; a=sum(r["kr"] for r in rr); p=sum(r["pron"] for r in rr); fd.append((f,a,p))
fd.sort(key=lambda x:-x[1])
table([0.14,0.04,0.27,0.25],"KG por Finca",["FINCA","K REALES","K ESTIMADO","% CUMPLIMIENTO"],
      [[f,es(a),es(p),es(a/p*100,2)+" %"] for f,a,p in fd],[0.3,0.22,0.22,0.26],["Total",es(KR),es(PR),es(KR/PR*100,2)+" %"])
# top 3
top=sorted(rows,key=lambda r:-r["kha"])[:3]; top=[top[1],top[0],top[2]]
tx=fig.add_axes([0.43,0.26,0.245,0.035]); tx.axis("off"); tx.add_patch(Rectangle((0,0),1,1,color=G,transform=tx.transAxes))
tx.text(0.5,0.5,"MEJORES 3 LOTES EN PRODUCCION/HA",ha="center",va="center",color=OR,fontsize=11.5,transform=tx.transAxes)
ax=fig.add_axes([0.44,0.06,0.225,0.17]); ax.axis("off")
v=[r["kha"] for r in top]; ax.bar(range(3),v,color=G,width=0.75); ax.set_ylim(0,max(v)*1.25)
for i,r in enumerate(top):
    ax.text(i,r["kha"]+max(v)*0.04,es(r["kha"]),ha="center",color=OR,fontsize=10,weight="bold")
    ax.text(i,-max(v)*0.1,r["l"],ha="center",fontsize=10,weight="bold")
# map
mt=fig.add_axes([0.695,0.905,0.29,0.045]); mt.axis("off"); mt.add_patch(Rectangle((0,0),1,1,color=G,transform=mt.transAxes))
mt.text(0.5,0.5,"Concentración de Kg por Lote",ha="center",va="center",color=OR,fontsize=15,transform=mt.transAxes)
mp=fig.add_axes([0.70,0.04,0.285,0.84]); mp.axis("off"); mp.set_aspect("equal")
centers={"LA ESPERANZA":(2.0,8.9),"SAN JOSÉ":(4.3,6.6),"EL MIRADOR":(6.1,9.0),"BUENAVISTA":(1.4,4.6),"LA PALMA":(3.9,2.0)}
sizes={"LA ESPERANZA":1.1,"SAN JOSÉ":1.5,"EL MIRADOR":1.1,"BUENAVISTA":1.15,"LA PALMA":1.7}
kmax=max(r["kr"] for r in rows); kmin=min(r["kr"] for r in rows)
from matplotlib.colors import LinearSegmentedColormap
cmap=LinearSegmentedColormap.from_list("agro",["#D9E8A6","#C9C23A","#93A82A","#4E7A23","#1B5233"])
for f,(c,n) in farms.items():
    cx,cy=centers[f]; s=sizes[f]
    ang=np.sort(rng.uniform(0,2*np.pi,22)); rad=s*(1+0.35*np.sin(ang*rng.integers(2,4)+rng.uniform(0,6)))*rng.uniform(0.8,1.15,22)
    blob=Polygon([(cx+r*np.cos(a)*1.15,cy+r*np.sin(a)*0.9) for a,r in zip(ang,rad)]).buffer(0)
    if blob.geom_type!="Polygon": blob=max(blob.geoms,key=lambda g:g.area)
    minx,miny,maxx,maxy=blob.bounds
    pts=[]
    while len(pts)<n:
        p=Point(rng.uniform(minx,maxx),rng.uniform(miny,maxy))
        if blob.contains(p) and all(p.distance(q)>s*0.6 for q in pts): pts.append(p)
    vor=voronoi_diagram(MultiPoint(pts),envelope=box(minx-1,miny-1,maxx+1,maxy+1))
    lots=[r for r in rows if r["f"]==f]
    for cell in vor.geoms:
        g=cell.intersection(blob)
        idx=[i for i,p in enumerate(pts) if cell.contains(p)][0]
        r=lots[idx]; t=(r["kr"]-kmin)/(kmax-kmin)
        geoms=[g] if g.geom_type=="Polygon" else list(g.geoms)
        for gg in geoms:
            mp.add_patch(MPoly(np.array(gg.exterior.coords),fc=cmap(t),ec="white",lw=1.2))
        rp=g.representative_point(); mp.text(rp.x,rp.y,r["l"],color=OR,fontsize=9.5,weight="bold",ha="center",va="center")
mp.set_xlim(-0.6,7.6); mp.set_ylim(-0.4,10.9)
lg=fig.add_axes([0.73,0.045,0.22,0.012]); lg.imshow(np.linspace(0,1,100)[None,:],aspect="auto",cmap=cmap); lg.set_yticks([]); lg.set_xticks([0,99]); lg.set_xticklabels([es(kmin)+" kg",es(kmax)+" kg"],fontsize=8.5,color="#444")
for sp in lg.spines.values(): sp.set_visible(False)
fig.savefig("Informe_Cosecha_Portafolio.png",facecolor=BG)
import json; json.dump(rows,open("rows.json","w"))
print("ok",len(rows))
