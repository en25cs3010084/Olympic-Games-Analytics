import matplotlib.pyplot as plt
import pandas as pd

# ---------------- DATA ----------------

df = pd.DataFrame({
    "Country": ["Australia", "China", "France", "Germany", "Great Britain", "Hungary",
                "Italy", "Japan", "Netherlands", "ROC", "Russia", "South Korea", "United States"],
    "Gold":    [64, 190, 70, 65, 100, 5, 50, 60, 22, 20, 56, 40, 200],
    "Silver":  [68, 126, 67, 65, 107, 7, 49, 50, 22, 28, 58, 40, 195],
    "Bronze":  [77, 122, 76, 67, 102, 6, 64, 59, 26, 23, 70, 35, 178],
})
# df = pd.read_csv("olympics.csv")   # columns: Country, Gold, Silver, Bronze
df["Total"] = df[["Gold", "Silver", "Bronze"]].sum(axis=1)
# Screenshot ke Total chart ke exact numbers (ROC us chart me nahi hai)
exact_total = {"Australia": 209, "China": 438, "France": 213, "Germany": 197,
               "Great Britain": 309, "Hungary": 18, "Italy": 163, "Japan": 169,
               "Netherlands": 70, "Russia": 184, "South Korea": 115, "United States": 573}
df["Total"] = df["Country"].map(exact_total).fillna(df["Total"])

short = lambda c: {"Australia": "Aust..", "China": "China", "France": "Fran..", "Germany": "Ger..",
                   "Great Britain": "Grea..", "Hungary": "Hun..", "Italy": "Italy", "Japan": "Japan",
                   "Netherlands": "Net..", "ROC": "ROC", "Russia": "Russ..",
                   "South Korea": "Sout..", "United States": "Unit.."}[c]

COL = {"Australia": "#4e79a7", "China": "#a0cbe8", "France": "#f28e2b", "Germany": "#ffbe7d",
       "Great Britain": "#59a14f", "Hungary": "#8cd17d", "Italy": "#b6992d", "Japan": "#f1ce63",
       "Netherlands": "#499894", "ROC": "#86bcb6", "Russia": "#e15759",
       "South Korea": "#ff9d9a", "United States": "#59595e"}

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig = plt.figure(figsize=(10, 17))
fig.suptitle("Olympics Games Analytics: Medal Treands\n& Country Performance",
             x=0.06, ha="left", fontsize=20, y=0.985)
gs = fig.add_gridspec(4, 1, hspace=0.55, top=0.92, bottom=0.04, left=0.1, right=0.95)

# ---------- 1) Total Olympic Medals by Country ----------
t = df[df.Country != "ROC"]
ax = fig.add_subplot(gs[0])
b = ax.bar([short(c) for c in t.Country], t.Total, color=[COL[c] for c in t.Country])
ax.bar_label(b, padding=2)
ax.set_title("Total Olympic Medals by Country", loc="left", fontsize=15)
ax.set_ylabel("Total")

# ---------- 2) Gold Medals by Country (Bronze | Gold panels) ----------
sub = gs[1].subgridspec(1, 2, wspace=0.05)
a1, a2 = fig.add_subplot(sub[0]), fig.add_subplot(sub[1], sharey=None)
y = range(len(df))
a1.barh(y, df.Bronze, color="#59a89c"); a1.set_xlabel("Bronze")
g = a2.barh(y, df.Gold, color="#e8914f"); a2.set_xlabel("Gold")
a2.bar_label(g, padding=3)
for a in (a1, a2):
    a.set_ylim(len(df) - 0.5, -0.5)
a1.set_yticks(list(y)); a1.set_yticklabels(df.Country)
a2.set_yticks([])
a1.set_title("Gold Medals by Country", loc="left", fontsize=15)

# ---------- 3) Silver Medals by Country (Bronze vs Silver, per country) ----------
sub = gs[2].subgridspec(1, len(df), wspace=0.0)
fig.text(0.1, gs[2].get_position(fig).y1 + 0.012, "Silver Medals by Country", fontsize=15)
ymax = max(df.Bronze.max(), df.Silver.max()) * 1.15
for i, r in df.iterrows():
    a = fig.add_subplot(sub[i])
    bars = a.bar(["Br..", "Sil.."], [r.Bronze, r.Silver], color=["#4e79a7", "#e15759"])
    a.bar_label(bars, labels=[f"{r.Bronze:.1f}", ""], rotation=90, padding=2, fontsize=8)
    a.set_ylim(0, ymax)
    a.set_title(short(r.Country), fontsize=8)
    a.tick_params(axis="x", rotation=90, labelsize=7)
    if i: a.set_yticks([]); a.spines["left"].set_visible(False)
    else: a.set_ylabel("Value")

# ---------- 4) Bronze Medals by Country ----------
bz = df[df.Country != "Hungary"]
ax = fig.add_subplot(gs[3])
b = ax.bar([short(c) for c in bz.Country], bz.Bronze, color=[COL[c] for c in bz.Country])
ax.bar_label(b, padding=2)
ax.set_title("Bronze Medals by Country", loc="left", fontsize=15)
ax.set_ylabel("Bronze")

fig.savefig("olympics_dashboard.png", dpi=150)
plt.show()