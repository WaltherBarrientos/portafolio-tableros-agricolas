import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
rng=np.random.default_rng(3)
import json
R=json.load(open("rows.json")); FINCAS=["LA ESPERANZA","SAN JOSÉ","EL MIRADOR","BUENAVISTA","LA PALMA"]
KG=sum(r["kr"] for r in R)
FC={"LA ESPERANZA":"#1F3B62","SAN JOSÉ":"#2A9D8F","EL MIRADOR":"#E9A23B","BUENAVISTA":"#5B7DB1","LA PALMA":"#8AB17D"}
NAVY="#1F3B62"; ACC="#2A9D8F"; ACC2="#E9A23B"; ACC3="#5B7DB1"; GRAY="#6B7280"; BG="#F4F6F9"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11})
M=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
def es(t): return t.replace(",","X").replace(".",",").replace("X",".")
def mill(x,_=None): return es(f"${x/1e6:,.0f}M")
def card(fig,x,y,w,h,title,val,sub,color):
    ax=fig.add_axes([x,y,w,h]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),1,1,boxstyle="round,pad=0,rounding_size=0.06",fc="white",ec="#E5E7EB",transform=ax.transAxes))
    ax.add_patch(FancyBboxPatch((0,0),0.03,1,boxstyle="square,pad=0",fc=color,ec=color,transform=ax.transAxes))
    ax.text(0.08,0.72,title,fontsize=11,color=GRAY,transform=ax.transAxes)
    ax.text(0.08,0.32,val,fontsize=22,weight="bold",color=NAVY,transform=ax.transAxes)
    ax.text(0.08,0.1,sub,fontsize=9.5,color=color,transform=ax.transAxes)
def panel(fig,rect,title,lx=0.1):
    bg=fig.add_axes(rect); bg.axis("off")
    bg.add_patch(FancyBboxPatch((0,0),1,1,boxstyle="round,pad=0,rounding_size=0.03",fc="white",ec="#E5E7EB",transform=bg.transAxes))
    x,y,w,h=rect
    bg.text(0.03,0.93,title,fontsize=12.5,weight="bold",color=NAVY,transform=bg.transAxes)
    ax=fig.add_axes([x+w*lx,y+h*0.12,w*(0.95-lx)-(0.06*w if 'costo por kg' in title else 0),h*0.7])
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB"); ax.spines["bottom"].set_color("#D1D5DB"); ax.tick_params(colors=GRAY)
    return ax
def header(fig,title,sub,filt="Año 2026  ·  Todas las fincas"):
    ax=fig.add_axes([0,0.9,1,0.1]); ax.axis("off"); ax.add_patch(plt.Rectangle((0,0),1,1,color=NAVY,transform=ax.transAxes))
    ax.text(0.02,0.55,title,fontsize=20,weight="bold",color="white",transform=ax.transAxes,va="center")
    ax.text(0.02,0.18,sub,fontsize=10.5,color="#C7D2E3",transform=ax.transAxes,va="center")
    ax.text(0.98,0.55,"2026",fontsize=18,weight="bold",color="white",transform=ax.transAxes,ha="right",va="center")
def footer(fig):
    fig.text(0.98,0.012,"Elaborado por Walther Barrientos – Analista de Datos",ha="right",fontsize=9,color=GRAY)

# ---------- Dashboard 1: costos agrícolas
fig=plt.figure(figsize=(16,9),dpi=120,facecolor=BG)
header(fig,"Tablero de Costos de Producción Agrícola","Seguimiento de costos por labor, lote y kilo producido · Fincas La Esperanza, San José, El Mirador, Buenavista y La Palma")
w=rng.normal(42000,6000,12)*(1+np.sin(np.arange(12)/1.9)*0.25); prod=np.round(w/w.sum()*KG).astype(int); prod[-1]+=KG-prod.sum()
labores={"Cosecha":0.31,"Fertilización":0.22,"Control fitosanitario":0.17,"Podas":0.12,"Riego":0.09,"Mantenimiento":0.09}
costo_mes=prod*rng.normal(1850,120,12)
tot_c=costo_mes.sum(); tot_p=prod.sum(); ingreso=tot_p*2650
card(fig,0.02,0.75,0.225,0.12,"Producción total",es(f"{tot_p:,.0f} kg"),"▲ 6,4 % vs 2025",ACC)
card(fig,0.265,0.75,0.225,0.12,"Costo total",mill(tot_c),"▼ 2,1 % vs presupuesto",ACC3)
card(fig,0.51,0.75,0.225,0.12,"Costo por kg",es(f"${tot_c/tot_p:,.0f}"),"Meta: $1.900 / kg",ACC2)
card(fig,0.755,0.75,0.225,0.12,"Margen bruto",es(f"{(ingreso-tot_c)/ingreso*100:,.1f} %"),"Precio prom. $2.650 / kg",ACC)
ax=panel(fig,[0.02,0.39,0.47,0.34],"Producción (t) y costo por kg mensual",lx=0.09)

ax.bar(M,prod/1000,color=ACC,width=0.6); ax.set_ylabel("Toneladas",color=GRAY)
ax2=ax.twinx(); ax2.plot(M,costo_mes/prod,color=ACC2,marker="o",lw=2.5); ax2.set_ylabel("$/kg",color=GRAY)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x,_:es(f"${x:,.0f}")));ax2.spines["top"].set_visible(False); ax2.tick_params(colors=GRAY)
ax=panel(fig,[0.51,0.39,0.47,0.34],"Costo por labor",lx=0.24)
lab=list(labores.items())[::-1]; vals=[tot_c*v for _,v in lab]
ax.barh([k for k,_ in lab],vals,color=ACC3); ax.xaxis.set_major_formatter(FuncFormatter(mill))
for i,v in enumerate(vals): ax.text(v,i,"  "+mill(v),va="center",fontsize=9.5,color=NAVY)
ax.set_xlim(0,max(vals)*1.22)
ax=panel(fig,[0.02,0.04,0.47,0.33],"Plan vs ejecución de labores por finca (%)")
fn=[f.title() for f in FINCAS]; ejec=[98,91,104,86,79]
cols=[ACC if e>=90 else ACC2 if e>=80 else "#D64545" for e in ejec]
ax.bar(fn,ejec,color=cols,width=0.55); ax.axhline(100,ls="--",color=GRAY,lw=1); ax.set_ylim(0,115)
for i,e in enumerate(ejec): ax.text(i,max(e,100)+2.5,f"{e}%",ha="center",fontsize=10,color=NAVY,weight="bold")
ax=panel(fig,[0.51,0.04,0.47,0.33],"Costo por hectárea por lote",lx=0.1)
lots=[r["l"] for r in R]; cha=np.array([tot_c*r["kr"]/KG/r["ha"]*rng.uniform(0.85,1.15) for r in R])
ax.bar(lots,cha,color=[FC[r["f"]] for r in R],width=0.65); ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:es(f"${x/1e6:,.0f}M")))
ax.tick_params(axis="x",labelsize=8.5,rotation=90)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=FC[f],label=f.title()) for f in FINCAS],frameon=False,fontsize=8.5,ncol=5,loc="upper center",bbox_to_anchor=(0.5,1.16),handlelength=1)
ax.axhline(cha.mean(),ls="--",color="#D64545",lw=1.3); ax.text(17.4,cha.mean()*1.03,"Promedio",color="#D64545",va="bottom",fontsize=9,ha="right",weight="bold")
footer(fig); fig.savefig("Tablero_Costos_Agricolas.png",facecolor=BG); plt.close(fig)

# ---------- Dashboard 2: ventas de cosecha
fig=plt.figure(figsize=(16,9),dpi=120,facecolor=BG)
header(fig,"Tablero de Ventas de Cosecha","Ventas por mes, finca, lote y destino · Fincas La Esperanza, San José, El Mirador, Buenavista y La Palma","Año 2026  ·  Todas las fincas")
kgv=np.round(prod*rng.uniform(0.93,0.98,12)); precio=rng.normal(2650,90,12); ventas=kgv*precio; meta=np.full(12,ventas.sum()/12*1.05)
card(fig,0.02,0.75,0.225,0.12,"Ventas año",mill(ventas.sum()),"▲ 11,2 % vs 2025",ACC)
card(fig,0.265,0.75,0.225,0.12,"Kg vendidos",es(f"{kgv.sum():,.0f}"),es(f"{kgv.sum()/KG*100:,.1f} % de lo cosechado"),ACC3)
card(fig,0.51,0.75,0.225,0.12,"Precio promedio / kg",es(f"${ventas.sum()/kgv.sum():,.0f}"),"Meta: $2.600 / kg",ACC2)
card(fig,0.755,0.75,0.225,0.12,"Cumplimiento meta",es(f"{ventas.sum()/meta.sum()*100:,.1f} %"),"Meta anual "+mill(meta.sum()),ACC)
ax=panel(fig,[0.02,0.39,0.47,0.34],"Ventas vs meta mensual")
ax.bar(M,ventas,color=ACC3,width=0.6,label="Ventas"); ax.plot(M,meta,color=ACC2,lw=2.5,label="Meta")
ax.yaxis.set_major_formatter(FuncFormatter(mill)); ax.legend(frameon=False,loc="upper center",bbox_to_anchor=(0.5,1.18),ncol=2)
ax=panel(fig,[0.51,0.39,0.47,0.34],"Ventas por finca",lx=0.2)
vf=sorted([(f,sum(r["kr"] for r in R if r["f"]==f)/KG*ventas.sum()) for f in FINCAS],key=lambda x:x[1])
ax.barh([f.title() for f,_ in vf],[v for _,v in vf],color=[FC[f] for f,_ in vf]); ax.xaxis.set_major_formatter(FuncFormatter(mill)); ax.set_xlim(0,vf[-1][1]*1.22)
for i,(_,v) in enumerate(vf): ax.text(v,i,"  "+mill(v),va="center",fontsize=9.5,color=NAVY)
ax=panel(fig,[0.02,0.04,0.47,0.33],"Participación por destino")
z=["Exportación","Nacional","Industria","Mercado local"]; zp=[46,28,17,9]
ax.axis("off"); a2=fig.add_axes([0.06,0.06,0.22,0.27])
a2.pie(zp,colors=[NAVY,ACC3,ACC,ACC2],startangle=90,wedgeprops=dict(width=0.38,edgecolor="white"))
for i,(n,p) in enumerate(zip(z,zp)):
    fig.text(0.30,0.27-i*0.045,f"■ {n}: {p} %",color=[NAVY,ACC3,ACC,ACC2][i],fontsize=12,weight="bold")
ax=panel(fig,[0.51,0.04,0.47,0.33],"Top 8 lotes por ventas")
top=sorted(R,key=lambda r:-r["kr"])[:8]; tv=[r["kr"]/KG*ventas.sum() for r in top]
ax.bar([r["l"] for r in top],tv,color=[FC[r["f"]] for r in top],width=0.6); ax.yaxis.set_major_formatter(FuncFormatter(mill)); ax.set_ylim(0,max(tv)*1.2)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=FC[f],label=f.title()) for f in FINCAS],frameon=False,fontsize=8.5,ncol=5,loc="upper center",bbox_to_anchor=(0.5,1.16),handlelength=1)
for i,v in enumerate(tv): ax.text(i,v+max(tv)*0.03,mill(v),ha="center",fontsize=9.5,color=NAVY,weight="bold")
footer(fig); fig.savefig("Tablero_Ventas_Cosecha.png",facecolor=BG); plt.close(fig)
print("ok")
