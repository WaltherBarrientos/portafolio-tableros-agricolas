exec(open("costos_y_ventas.py").read().split("# ---------- Dashboard 1")[0])
from matplotlib.patches import Patch
rng=np.random.default_rng(21)
trab={"LA ESPERANZA":22,"SAN JOSÉ":34,"EL MIRADOR":14,"BUENAVISTA":19,"LA PALMA":41}
T=sum(trab.values())
lab={"Cosecha":0.38,"Podas":0.16,"Fertilización":0.14,"Control fitosanitario":0.13,"Riego":0.09,"Mantenimiento":0.10}
jor_mes=np.round(rng.normal(T*22,60,12)*(1+np.sin(np.arange(12)/1.9)*0.08))
JT=jor_mes.sum(); VJ=78000
fig=plt.figure(figsize=(16,9),dpi=120,facecolor=BG)
header(fig,"Tablero de Recursos Humanos y Jornales","Personal, jornales, nómina y rendimiento · Fincas La Esperanza, San José, El Mirador, Buenavista y La Palma")
card(fig,0.02,0.75,0.18,0.12,"Trabajadores activos",str(T),"▲ 8 vs 2025",ACC)
card(fig,0.215,0.75,0.18,0.12,"Jornales año",es(f"{JT:,.0f}"),es(f"{JT/12:,.0f} promedio / mes"),ACC3)
card(fig,0.41,0.75,0.18,0.12,"Costo nómina",mill(JT*VJ),"Jornal: $78.000",ACC2)
card(fig,0.605,0.75,0.18,0.12,"Ausentismo","3,8 %","Meta: < 4 %",ACC)
card(fig,0.80,0.75,0.18,0.12,"Rotación","6,2 %","▼ 1,1 pts vs 2025",ACC3)
# jornales por labor por mes stacked
ax=panel(fig,[0.02,0.39,0.47,0.34],"Jornales por labor y mes")
cols=[NAVY,ACC,ACC2,ACC3,"#8AB17D","#B0B7C3"]; bot=np.zeros(12)
for (k,v),c in zip(lab.items(),cols):
    vals=jor_mes*v*rng.uniform(0.85,1.15,12); ax.bar(M,vals,bottom=bot,color=c,width=0.65,label=k); bot+=vals
ax.legend(frameon=False,fontsize=8.5,ncol=6,loc="upper center",bbox_to_anchor=(0.5,1.17),handlelength=1)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:es(f"{x:,.0f}")))
# nómina por finca
ax=panel(fig,[0.51,0.39,0.47,0.34],"Costo de nómina por finca",lx=0.2)
nf=sorted([(f,trab[f]/T*JT*VJ) for f in FINCAS],key=lambda x:x[1])
ax.barh([f.title() for f,_ in nf],[v for _,v in nf],color=[FC[f] for f,_ in nf]); ax.xaxis.set_major_formatter(FuncFormatter(mill)); ax.set_xlim(0,nf[-1][1]*1.3)
for i,(f,v) in enumerate(nf): ax.text(v,i,"  "+mill(v)+f"  ·  {trab[f]} trab.",va="center",fontsize=9.5,color=NAVY)
# rendimiento kg/jornal por lote
ax=panel(fig,[0.02,0.04,0.47,0.33],"Rendimiento de cosecha por lote (kg / jornal)",lx=0.09)
rv=[r["rop"] for r in R]; ax.bar([r["l"] for r in R],rv,color=[FC[r["f"]] for r in R],width=0.65)
ax.tick_params(axis="x",labelsize=8.5,rotation=90); m=np.mean(rv); ax.axhline(m,ls="--",color="#D64545",lw=1.3)
ax.text(17.4,m*1.03,"Promedio "+es(f"{m:,.0f}"),color="#D64545",ha="right",va="bottom",fontsize=9,weight="bold")
ax.legend(handles=[Patch(color=FC[f],label=f.title()) for f in FINCAS],frameon=False,fontsize=8.5,ncol=5,loc="upper center",bbox_to_anchor=(0.5,1.16),handlelength=1)
# ausentismo por motivo donut
ax=panel(fig,[0.51,0.04,0.47,0.33],"Ausentismo por motivo"); ax.axis("off")
mot=["Incapacidad médica","Permiso personal","Calamidad","Injustificada"]; mp=[52,24,14,10]
a2=fig.add_axes([0.55,0.06,0.22,0.27]); c4=[NAVY,ACC3,ACC,ACC2]
a2.pie(mp,colors=c4,startangle=90,wedgeprops=dict(width=0.38,edgecolor="white"))
a2.text(0,0,"3,8 %",ha="center",va="center",fontsize=16,weight="bold",color=NAVY)
for i,(n,p) in enumerate(zip(mot,mp)): fig.text(0.79,0.27-i*0.045,f"■ {n}: {p} %",color=c4[i],fontsize=11.5,weight="bold")
footer(fig); fig.savefig("Tablero_RRHH_Jornales.png",facecolor=BG); print("ok")
