import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
rng=np.random.default_rng(8)
BG="#0F1B2D"; PAN="#16263D"; TX="#E6EDF7"; MU="#8FA3BF"; GRID="#24385A"
C1="#38BDF8"; C2="#F59E0B"; C3="#34D399"; C4="#F87171"; C5="#A78BFA"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"text.color":TX,"axes.labelcolor":MU,"xtick.color":MU,"ytick.color":MU})
M=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
def es(t): return t.replace(",","X").replace(".",",").replace("X",".")
def mill(x,_=None): return es(f"${x/1e6:,.0f}M")
def panel(rect,title,lx=0.08,ly=0.12,h=0.7):
    bg=fig.add_axes(rect); bg.axis("off")
    bg.add_patch(FancyBboxPatch((0,0),1,1,boxstyle="round,pad=0,rounding_size=0.03",fc=PAN,ec=GRID,transform=bg.transAxes))
    bg.text(0.03,0.92,title,fontsize=12.5,weight="bold",color=TX,transform=bg.transAxes)
    x,y,w,hh=rect; ax=fig.add_axes([x+w*lx,y+hh*ly,w*(0.95-lx),hh*h]); ax.set_facecolor(PAN)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    for s in ["left","bottom"]: ax.spines[s].set_color(GRID)
    return ax
def card(x,title,val,sub,col,up=True):
    ax=fig.add_axes([x,0.755,0.152,0.115]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),1,1,boxstyle="round,pad=0,rounding_size=0.08",fc=PAN,ec=col,lw=1.6,transform=ax.transAxes))
    ax.text(0.08,0.74,title,fontsize=10.5,color=MU,transform=ax.transAxes)
    ax.text(0.08,0.36,val,fontsize=20,weight="bold",color=TX,transform=ax.transAxes)
    ax.text(0.08,0.11,sub,fontsize=9.5,color=C3 if up else C4,transform=ax.transAxes)
ing=rng.normal(520e6,45e6,12)*(1+np.arange(12)*0.012); cv=ing*rng.uniform(0.58,0.62,12); gop=ing*rng.uniform(0.2,0.24,12)
uti=ing-cv-gop; I,CV,GO,U=ing.sum(),cv.sum(),gop.sum(),uti.sum(); imp=U*0.35; UN=U-imp
flujo=uti*rng.uniform(0.7,1.2,12)-rng.normal(15e6,8e6,12); cartera=812e6
fig=plt.figure(figsize=(16,9),dpi=120,facecolor=BG)
fig.text(0.02,0.94,"Tablero Financiero · Pyme Comercial",fontsize=22,weight="bold",color=TX)
fig.text(0.02,0.905,"Estado de resultados, flujo de caja, cartera y presupuesto en una sola vista",fontsize=11,color=MU)
fig.text(0.98,0.935,"2026",fontsize=20,weight="bold",color=C1,ha="right")
cards=[("Ingresos",mill(I),"▲ 12,4 % vs 2025",C1,True),("Utilidad neta",mill(UN),"▲ 9,1 % vs 2025",C3,True),
("Margen neto",es(f"{UN/I*100:,.1f} %"),"Meta: 10 %",C5,True),("Flujo de caja neto",mill(flujo.sum()),"▲ 6 meses positivos seguidos",C2,True),
("Cartera por cobrar",mill(cartera),"▼ 14 % vencida > 60 días",C4,False),("Días de cartera","47 días","Meta: 45 días",C1,False)]
for i,c in enumerate(cards): card(0.02+i*0.161,*c)
# ingresos gastos utilidad
ax=panel([0.02,0.40,0.55,0.33],"Ingresos, costos y utilidad operacional por mes",lx=0.09)
x=np.arange(12); ax.bar(x-0.2,ing,0.38,color=C1,label="Ingresos"); ax.bar(x+0.2,cv+gop,0.38,color=MU,alpha=0.55,label="Costos + gastos")
ax.plot(x,uti,color=C2,lw=2.8,marker="o",label="Utilidad operacional"); ax.set_xticks(x,M)
ax.yaxis.set_major_formatter(FuncFormatter(mill)); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False,ncol=3,loc="upper center",bbox_to_anchor=(0.5,1.17),fontsize=9.5,labelcolor=TX)
# waterfall
ax=panel([0.59,0.40,0.39,0.33],"Estado de resultados (cascada)",lx=0.12)
st=[("Ingresos",I),("Costo ventas",-CV),("Gastos op.",-GO),("Impuestos",-imp),("Utilidad neta",UN)]
cum=0
for i,(n,v) in enumerate(st):
    if i in (0,4): b,hgt,col=0,v,(C1 if i==0 else C3)
    else: b,hgt,col=cum+v,-v,C4
    ax.bar(i,hgt,bottom=b,color=col,width=0.6)
    ax.text(i,b+hgt+I*0.02,mill(abs(v)),ha="center",fontsize=9.5,color=TX,weight="bold")
    if i<4: cum = v if i==0 else cum+v
ax.set_xticks(range(5),[s[0] for s in st],fontsize=9.5); ax.yaxis.set_major_formatter(FuncFormatter(mill))
ax.set_ylim(0,I*1.15); ax.grid(axis="y",color=GRID,lw=0.6); ax.set_axisbelow(True)
# cartera
ax=panel([0.02,0.04,0.30,0.33],"Cartera por antigüedad",lx=0.2)
ed=["0–30 días","31–60 días","61–90 días","> 90 días"]; pv=np.array([0.58,0.28,0.09,0.05])*cartera
ax.barh(ed[::-1],pv[::-1],color=[C4,C2,C5,C3]); ax.xaxis.set_major_formatter(FuncFormatter(mill)); ax.set_xlim(0,pv.max()*1.35); ax.set_xticks([0,200e6,400e6,600e6])
for i,v in enumerate(pv[::-1]): ax.text(v,i,"  "+mill(v)+es(f"  ({v/cartera*100:,.0f} %)"),va="center",fontsize=9.5,color=TX)
# presupuesto
ax=panel([0.34,0.04,0.33,0.33],"Gastos: real vs. presupuesto",lx=0.1)
rub=["Nómina","Arriendo","Mercadeo","Logística","Servicios"]; pres=np.array([620,180,140,210,90])*1e6; real=pres*np.array([0.98,1.0,1.18,1.07,0.93])
xx=np.arange(5); ax.bar(xx-0.2,pres,0.38,color=MU,alpha=0.55,label="Presupuesto"); ax.bar(xx+0.2,real,0.38,color=[C4 if r>p else C3 for r,p in zip(real,pres)],label="Real")
for i,(r,p) in enumerate(zip(real,pres)): ax.text(i+0.2,r+pres.max()*0.03,es(f"{(r/p-1)*100:+.0f}%"),ha="center",fontsize=9,color=C4 if r>p else C3,weight="bold")
ax.set_xticks(xx,rub,fontsize=9.5); ax.yaxis.set_major_formatter(FuncFormatter(mill)); ax.set_ylim(0,pres.max()*1.2)
ax.legend(frameon=False,fontsize=9,loc="upper right",labelcolor=TX)
# flujo acumulado
ax=panel([0.69,0.04,0.29,0.33],"Flujo de caja acumulado",lx=0.14)
acc=np.cumsum(flujo); ax.plot(M,acc,color=C3,lw=2.8); ax.fill_between(range(12),acc,color=C3,alpha=0.18)
ax.yaxis.set_major_formatter(FuncFormatter(mill)); ax.tick_params(axis="x",labelsize=8.5); ax.grid(axis="y",color=GRID,lw=0.6)
ax.text(11,acc[-1]*1.04,mill(acc[-1]),ha="right",color=C3,weight="bold",fontsize=10.5)
fig.text(0.98,0.012,"Elaborado por Walther Barrientos – Analista de Datos",ha="right",fontsize=9,color=MU)
fig.savefig("Tablero_Financiero_Pyme.png",facecolor=BG); print("ok")
