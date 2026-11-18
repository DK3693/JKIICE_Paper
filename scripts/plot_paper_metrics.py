"""Generate portfolio visuals using aggregate metrics reported in the manuscript.

This is a companion visualization utility. It does not reconstruct raw sensor data,
train models, or reproduce the original event-level analysis.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

STATES = ['Baseline', 'Elevated', 'High']
COUNTS = [2153, 819, 713]
RATIOS = [58.43, 22.23, 19.35]  # Reported values, rounding may sum to 100.01%.
TRANSITIONS = np.array([[.78,.15,.07],[.40,.35,.25],[.20,.29,.51]])

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.titlesize': 16, 'axes.labelsize': 12,
    'xtick.labelsize': 11, 'ytick.labelsize': 11,
    'savefig.facecolor':'white', 'figure.facecolor': 'white'
})

fig, ax = plt.subplots(figsize=(8,4.6), dpi=150)
colors = ['#315b91','#35b4a4','#edb06e']
bars = ax.bar(STATES, RATIOS, color=colors, width=0.52, zorder=3)
ax.set_ylim(0, 70)
ax.set_ylabel('Share of valid 5-min bins (%)')
ax.set_title('Activity State Distribution', loc='left', fontweight='bold', pad=17)
ax.grid(axis='y', alpha=0.15, zorder=0)
for b, r, count in zip(bars, RATIOS, COUNTS):
    ax.text(b.get_x()+b.get_width()/2, r+1.4, f'{r:.2f}%\n(n={count:,})', ha='center', va='bottom', fontweight='medium')
for spine in ('top','right'): ax.spines[spine].set_visible(False)
fig.tight_layout(pad=2)
fig.savefig(ASSETS/'activity_states.png', dpi=220, bbox_inches='tight')
plt.close(fig)

fig, ax = plt.subplots(figsize=(7,5.8), dpi=150)
im = ax.imshow(TRANSITIONS, cmap='Blues', vmin=0, vmax=1)
ax.set_xticks(range(3), STATES)
ax.set_yticks(range(3), STATES)
ax.set_xlabel('Next state')
ax.set_ylabel('Current state')
ax.set_title('Activity State Transition Matrix', loc='left', fontweight='bold', pad=20)
for i in range(3):
    for j in range(3):
        v=TRANSITIONS[i,j]
        ax.text(j,i,f'{v:.2f}', ha='center', va='center', fontsize=16, fontweight='bold', color='white' if v>=.48 else '#18304e')
cb=fig.colorbar(im,ax=ax,shrink=.76,pad=.04)
cb.set_label('Transition probability')
fig.tight_layout(pad=2)
fig.savefig(ASSETS/'state_transition_matrix.png',dpi=220,bbox_inches='tight')
plt.close(fig)

# Compact overview image featuring only measured / manuscript-reported summary metrics.
fig = plt.figure(figsize=(13.4,6.5), dpi=150)
fig.patch.set_facecolor('#f5f8fc')
fig.text(.055,.91,'SMARTWATCH ACTIVITY ANALYSIS',fontsize=13,color='#377a8f',fontweight='bold')
fig.text(.055,.85,'Results at a glance',fontsize=25,color='#16253d',fontweight='bold')
labels=[('28','collection days'),('14','baseline days'),('3,685','valid 5-min bins'),('91.39%','valid-data ratio')]
for i,(v,lbl) in enumerate(labels):
    x=.058 + i*.23
    fig.text(x,.73,v,fontsize=25,color='#173359',fontweight='bold')
    fig.text(x,.67,lbl,fontsize=10,color='#506078')
fig.text(.055,.57,'ACTIVITY DISTRIBUTION',fontsize=12,color='#16253d',fontweight='bold')
ax=fig.add_axes([.055,.18,.54,.32],facecolor='#f5f8fc')
for i,(s,p,c) in enumerate(zip(STATES,RATIOS,colors)):
    ax.barh(i,p,color=c,height=.46)
    ax.text(p+1.1,i,f'{p:.2f}%',va='center',color='#16253d',fontweight='bold')
ax.set_xlim(0,80)
ax.set_yticks(range(3),STATES)
ax.invert_yaxis()
ax.set_xlabel('Share of valid bins (%)')
ax.xaxis.grid(True,alpha=.11)
ax.set_axisbelow(True)
for sp in ax.spines.values(): sp.set_visible(False)
ax.tick_params(axis='y',length=0)
fig.text(.65,.58,'PHYSIOLOGICAL CHECK',fontsize=12,color='#16253d',fontweight='bold')
for y,v,lbl in [(.48,'≈ 0.285','Activity proxy–HR correlation'),(.34,'13.27 min','Mean observed HR recovery'),(.20,'124','Recovery events identified')]:
    fig.text(.65,y,v,fontsize=22,color='#173359',fontweight='bold')
    fig.text(.65,y-.045,lbl,fontsize=10,color='#506078')
fig.text(.055,.055,'Single-participant research case study  •  HR reserved for physiological cross-checks',fontsize=10,color='#6d7b8d')
fig.savefig(ASSETS/'results_overview.png',dpi=220,bbox_inches='tight')
plt.close(fig)
print('Generated metrics charts in', ASSETS)
