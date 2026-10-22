"""Publication figures for the manuscript, in manuscript order (Figures 1–7).

Regenerate all seven by running: python run_analysis.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter
from . import SUBJECTS, SUBJECT_NAMES, ORIGINAL_ASSUMED_SCORES

NAVY="#1B2A4A"
TEAL="#2A9D8F"
GREY="#808080"
CORAL="#E76F51"
GOLD="#C49527"

def _style():
    plt.rcParams.update({
      "font.family":"serif","font.size":10,"axes.titlesize":12,
      "axes.labelsize":10,"figure.dpi":300,
      "axes.spines.top":False,"axes.spines.right":False,
      "axes.grid":False
    })

def _save(fig,outdir,filename):
    os.makedirs(outdir,exist_ok=True)
    path=os.path.join(outdir,filename)
    fig.tight_layout()
    fig.savefig(path,dpi=300,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    return path

def plot_sample_composition(n_students=30,n_teachers=5,output_dir="results/figures"):
    _style()
    fig,ax=plt.subplots(figsize=(7,4.5))
    sizes=[n_students,n_teachers]
    labels=[f"Students (n={n_students})",f"Teachers (n={n_teachers})"]
    wedges,_=ax.pie(sizes,startangle=90,colors=[NAVY,TEAL],wedgeprops={"width":0.4,"edgecolor":"white"})
    ax.text(0,0,f"{sum(sizes)}\\nRespondents",ha="center",va="center",fontsize=13,weight="bold")
    ax.legend(wedges,labels,loc="center left",bbox_to_anchor=(1.02,.5),frameon=False)
    ax.set_title("Survey Composition by Respondent Group")
    return _save(fig,output_dir,"figure_1_sample_composition.png")

def generate_workflow_diagram(output_dir="results/figures"):
    _style()
    fig,ax=plt.subplots(figsize=(7.5,6.7))
    ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis("off")
    steps=[
      ("Survey rating inputs","35 records; five subjects"),
      ("Validate ratings","Check scores and respondent IDs"),
      ("Exhaustive scoring","35 x 120 = 4,200 combinations"),
      ("Optimize and verify","Individual and group minima; tests"),
      ("Report outputs","Tables, figures, sensitivity analyses")
    ]
    for i,(title,desc) in enumerate(steps):
        y=0.88-i*0.185
        from matplotlib.patches import FancyBboxPatch
        box=FancyBboxPatch((.12,y-.063),.76,.126,boxstyle="round,pad=0.012",facecolor="#EFF5F6",edgecolor=NAVY,linewidth=1.3)
        ax.add_patch(box)
        ax.text(.15,y+.022,title,ha="left",va="center",color=NAVY,weight="bold",fontsize=10)
        ax.text(.15,y-.022,desc,ha="left",va="center",color="#444444",fontsize=9)
        if i<4: ax.annotate("",xy=(.5,y-.105),xytext=(.5,y-.069),arrowprops=dict(arrowstyle="-|>",color=TEAL,lw=2))
    ax.set_title("Python Computational Workflow")
    return _save(fig,output_dir,"figure_2_computational_workflow.png")

def plot_difficulty_means(stats,output_dir="results/figures"):
    _style()
    fig,ax=plt.subplots(figsize=(9,4.8))
    x=np.arange(5);w=.24
    students=[stats["students"][s]["mean"] for s in SUBJECTS]
    teachers=[stats["teachers"][s]["mean"] for s in SUBJECTS]
    assumed=[ORIGINAL_ASSUMED_SCORES[s] for s in SUBJECTS]
    ax.bar(x-w,students,w,color=NAVY,label="Students (n=30)")
    ax.bar(x,teachers,w,color=TEAL,label="Teachers (n=5)")
    ax.bar(x+w,assumed,w,color=GOLD,label="Khanna [1] assumed scores")
    ax.set_xticks(x,["Mathematics","Physics","Chemistry","Computer Science","English"],rotation=12)
    ax.set_ylim(0,5.35);ax.set_ylabel("Mean difficulty rating (1–5)")
    ax.grid(axis="y",alpha=.18);ax.set_axisbelow(True)
    ax.legend(frameon=False,ncol=3,loc="upper center",bbox_to_anchor=(.5,-.13))
    ax.set_title("Difficulty Ratings: Respondents and Original Assumptions")
    return _save(fig,output_dir,"figure_3_difficulty_means.png")

def plot_aggregate_scores(group_results,output_dir="results/figures"):
    _style()
    r=group_results["combined"]
    vals=[r.mean_baseline,r.mean_selected,r.mean_minimum]
    fig,ax=plt.subplots(figsize=(7.6,4.3))
    bars=ax.bar(range(3),vals,color=[GREY,NAVY,TEAL],width=.55)
    ax.set_xticks(range(3),["Baseline","Khanna [1] selected","Combined-group minimum"])
    ax.set_ylabel("Mean model score per respondent");ax.set_ylim(0,max(vals)*1.18)
    for b,v in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,v+.5,f"{v:.2f}",ha="center",weight="bold")
    ax.set_title("Comparison of Mean Scheduling Scores Across All Respondents")
    return _save(fig,output_dir,"figure_4_mean_scheduling_scores.png")

def plot_score_reductions(group_results,output_dir="results/figures"):
    _style()
    keys=["students","teachers","combined"];labs=["Students","Teachers","Combined"]
    selected=[100*(group_results[k].baseline_score-group_results[k].selected_score)/group_results[k].baseline_score for k in keys]
    minimum=[group_results[k].reduction_pct for k in keys]
    x=np.arange(3);w=.32
    fig,ax=plt.subplots(figsize=(7.8,4.4))
    b1=ax.bar(x-w/2,selected,w,color=NAVY,label="Khanna [1] selected")
    b2=ax.bar(x+w/2,minimum,w,color=TEAL,label="Group minimum")
    for b in list(b1)+list(b2):
       h=b.get_height();ax.text(b.get_x()+b.get_width()/2,h+.12,f"{h:.2f}%",ha="center",fontsize=9)
    ax.set_ylim(0,10);ax.set_xticks(x,labs);ax.set_ylabel("Reduction from baseline (%)")
    ax.legend(frameon=False,ncol=2,loc="upper center",bbox_to_anchor=(.5,-.1))
    ax.set_title("Baseline-Relative Model Score Reductions")
    return _save(fig,output_dir,"figure_5_score_reductions.png")

def plot_rating_distribution(stats,output_dir="results/figures"):
    _style()
    ratings=[2,3,4,5]
    counts=np.array([[stats["combined"][s]["frequencies"].get(v,0) for v in ratings] for s in SUBJECTS])
    fig,ax=plt.subplots(figsize=(7.6,4.7))
    im=ax.imshow(counts,cmap="Blues",aspect="auto",vmin=0,vmax=max(1,int(counts.max())))
    ax.set_xticks(range(4),ratings);ax.set_yticks(range(5),["Mathematics","Physics","Chemistry","Computer Science","English"])
    ax.set_xlabel("Reported difficulty rating");ax.set_title("Distribution of Survey Difficulty Ratings Across Subjects")
    for i in range(5):
      for j in range(4):
        v=int(counts[i,j]);ax.text(j,i,str(v),ha="center",va="center",color="white" if v>counts.max()*.57 else NAVY,fontsize=10)
    fig.colorbar(im,ax=ax,label="Number of respondents")
    return _save(fig,output_dir,"figure_6_rating_distribution.png")

def plot_individual_gaps(individual_results,output_dir="results/figures"):
    _style()
    gaps=Counter(r.optimality_gap for r in individual_results)
    xx=list(range(0,max(gaps)+1));vv=[gaps.get(i,0) for i in xx]
    fig,ax=plt.subplots(figsize=(7.8,4.3))
    bars=ax.bar(xx,vv,color=[TEAL if x==0 else NAVY for x in xx],width=.72)
    ax.set_xticks(xx);ax.set_xlabel("Optimality gap: selected score minus individual minimum")
    ax.set_ylabel("Number of respondents");ax.set_ylim(0,max(vv)*1.2)
    for b,v in zip(bars,vv):ax.text(b.get_x()+b.get_width()/2,v+.16,str(v),ha="center")
    ax.set_title("Individual Optimality Gaps Across 35 Rating Records")
    return _save(fig,output_dir,"figure_7_individual_optimality_gaps.png")

def generate_all_figures(stats,group_results,individual_results,output_dir="results/figures"):
    return [
       plot_sample_composition(30,5,output_dir),
       generate_workflow_diagram(output_dir),
       plot_difficulty_means(stats,output_dir),
       plot_aggregate_scores(group_results,output_dir),
       plot_score_reductions(group_results,output_dir),
       plot_rating_distribution(stats,output_dir),
       plot_individual_gaps(individual_results,output_dir),
    ]
