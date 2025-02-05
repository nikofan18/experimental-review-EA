import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.transforms
from matplotlib import ticker as mticker
from matplotlib.ticker import StrMethodFormatter, NullFormatter


# choose baseline method [RDGCN, RREA(semi)]
baseline_method = "MTransE"

data = pd.read_excel("performances_and_statistics.xlsx", skiprows=0)
Y = {}
for i in range(3, 36, 4):
    Y[data.columns[i]] = data[data.columns[i]][:8]

performance = pd.DataFrame(Y)
performance_baseline = performance[baseline_method + " MRR"]
performance_sub = performance.sub(performance_baseline, axis=0)
performance_sub = performance_sub.divide(performance_baseline, axis=0)
performance_sub.drop([baseline_method + " MRR"], axis=1, inplace=True)

X = {}
data_time = pd.read_excel("rev_time2.xlsx", skiprows=0)
for i in range(0, 18, 2):
    X[data_time.columns[i]] = (data_time[data_time.columns[i]][:8] + data_time[data_time.columns[i + 1]][:8])

exec_time = pd.DataFrame(X)
exec_baseline = exec_time[baseline_method + " train"]
exec_sub = exec_time.sub(exec_baseline, axis=0)
exec_sub = exec_sub.divide(exec_baseline, axis=0)
exec_sub.drop([baseline_method + " train"], axis=1, inplace=True)

fig = plt.figure(figsize=(7, 7))

markers = ["^", "D", "s", "P", "*", "o", "x", "p"]
colors = ["orange", "red", "maroon", "deepskyblue", "blue", "springgreen", "mediumseagreen", "darkgreen", "pink"]
counter = 0
first = 0
second = 0
third = 0
forth = 0
plt.axhline(y=0, color='black', linestyle='-')
plt.axvline(x=0, color='black', linestyle='-')
for col in performance_sub.columns:
    for i in range(0, 8):
        xx = performance_sub[col.split(" ")[0] + " MRR"][i]
        yy = exec_sub[col.split(" ")[0] + " train"][i]

        if xx == -1 or yy == -1:
            continue

        if xx >= 0 and yy > 0:
            first += 1
        elif xx <= 0 and yy > 0:
            second += 1
        elif xx <= 0 and yy < 0:
            third += 1
        elif xx >= 0 and yy < 0:
            forth += 1
        if i == 0:
            plt.scatter(performance_sub[col.split(" ")[0] + " MRR"][i], exec_sub[col.split(" ")[0] + " train"][i],
                        marker=markers[counter], label=col.split(" ")[0], color=colors[i])
        else:
            plt.scatter(performance_sub[col.split(" ")[0] + " MRR"][i], exec_sub[col.split(" ")[0] + " train"][i],
                        marker=markers[counter], color=colors[i])
    counter += 1
handles, labels = plt.gca().get_legend_handles_labels()

a = mpatches.Patch(color='red', label='D_W_15K_V1')
b = mpatches.Patch(color='maroon', label='D_W_15K_V2')
c = mpatches.Patch(color='deepskyblue', label='D_Y_15K_V1')
d = mpatches.Patch(color='blue', label='D_Y_15K_V2')
e = mpatches.Patch(color='orange', label='BBC_DB')
f = mpatches.Patch(color='springgreen', label='imdb-tmdb')
g = mpatches.Patch(color='mediumseagreen', label='imdb-tvdb')
h = mpatches.Patch(color='darkgreen', label='tmdb-tvdb')
handles.append(a)
handles.append(b)
handles.append(c)
handles.append(d)
handles.append(e)
handles.append(f)
handles.append(g)
handles.append(h)
legend = plt.legend(handles=handles, fontsize=7, ncol=6, loc="upper center", bbox_to_anchor=(0.49, 1.13))
for i in range(8):
    legend.legendHandles[i].set_color("black")

plt.xlabel('(MRR_Method - MRR_' + baseline_method + ') / MRR_' + baseline_method + ')')
plt.ylabel('(ET_Method - ET_' + baseline_method + ') / ET_' + baseline_method)
plt.xscale('symlog')

plt.autoscale(False)

if baseline_method == "BERT_INT":
    plt.xlim([-1.1, 1.3])

plt.fill_between([0, 200], 0, 800, alpha=0.3, color="tab:gray")
plt.fill_between([0, -200], 0, 80, alpha=0.3, color="tab:green")
plt.fill_between([0, -200], 0, -20, alpha=0.3, color="tab:gray")
plt.fill_between([0, 200], 0, -20, alpha=0.3, color="tab:red")

if baseline_method == "RREA(semi)":
    plt.text(0.85, 0.32, str(first) + ' points', fontsize=10)
    plt.text(-0.85, 0.32, str(second) + ' points', fontsize=10)
    plt.text(-0.8, -0.5, str(third) + ' points', fontsize=10)
    plt.text(0.85, -0.5, str(forth) + ' points', fontsize=10)
elif baseline_method == "RDGCN":
    plt.text(2.85, 7.92, str(first) + ' points', fontsize=10)
    plt.text(-2.85, 7.89, str(second) + ' points', fontsize=10)
    plt.text(-2.1, -1, str(third) + ' points', fontsize=10)
    plt.text(0.85, -1, str(forth) + ' points', fontsize=10)
elif baseline_method == "BERT_INT":
    plt.text(0.55, 2.65, str(first) + ' points', fontsize=10)
    plt.text(-0.65, 2.65, str(second) + ' points', fontsize=10)
    plt.text(-0.7, -0.5, str(third) + ' points', fontsize=10)
    plt.text(0.55, -0.5, str(forth) + ' points', fontsize=10)

print("Points: " + str(first) + " " + str(second) + " " + str(third) + " " + str(forth))

dx = 26/72.; dy = 0/72. 
offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
ax = plt.gca()
for label in ax.xaxis.get_majorticklabels():
    label.set_transform(label.get_transform() + offset)
    break

# plt.show()
plt.savefig("./test_trade_offs" + baseline_method + ".png")
