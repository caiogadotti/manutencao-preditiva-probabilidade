import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
C1,C2,INK,MUT="#0F766E","#F59E0B","#1E293B","#64748B"
f,ax=plt.subplots(figsize=(6,4)); ax.set_xlim(0,3.45); ax.set_ylim(0.45,3.4); ax.axis("off"); ax.invert_yaxis()
cel={(0,0):"0,60",(0,1):"0,10",(1,0):"0,12",(1,1):"0,18"}
for (i,j),t in cel.items():
    dest=(i,j)==(1,1)
    ax.add_patch(Rectangle((1+j,1+i),1,1,fc=C2 if dest else "#E6F2F1",ec="white",lw=3))
    ax.text(1.5+j,1.5+i,t,ha="center",va="center",fontsize=22,weight="bold",color=INK)
for k,t in enumerate(["0,70","0,30"]):
    ax.text(3.2,1.5+k,t,ha="center",va="center",fontsize=16,color=C1,weight="bold")
for k,t in enumerate(["0,72","0,28"]):
    ax.text(1.5+k,3.15,t,ha="center",va="center",fontsize=16,color=C1,weight="bold")
ax.text(3.2,0.8,"P(X)",ha="center",fontsize=13,color=MUT); ax.text(0.55,3.15,"P(Y)",ha="center",va="center",fontsize=13,color=MUT)
for k,t in enumerate(["Temp.\nnormal","Temp.\nalta"]): ax.text(1.5+k,0.75,t,ha="center",va="center",fontsize=13)
for k,t in enumerate(["Vibração\nnormal","Vibração\nalta"]): ax.text(0.55,1.5+k,t,ha="center",va="center",fontsize=13)
plt.tight_layout(); plt.savefig("graficos/conjunta.png",dpi=200)
