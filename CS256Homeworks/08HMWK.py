import matplotlib.pyplot as plt
import os
fig = plt.figure(figsize=(7,5))
names = ["Avinash", "Dan", "Michelle", "Sally"]
scores =[89,78,93, 57]
scores2=[95,85,87,78]
positions =[0, 1, 2, 3]
positions2 = [0.3, 1.3, 2.3, 3.3]
positions3 = [0.15, 1.15, 2.15, 3.15]

plt.bar(positions, scores, width=0.3, color="g")
plt.bar(positions2, scores2, width=0.3)
plt.title("Michael Vincent Rayo")
plt.xticks(positions3, names)
downloads_path = os.path.expanduser("/Users/mvrayo-mini/Downloads")
# plt.savefig("my_plot.png", dpi=300, bbox_inches="tight")
# plt.savefig("grades.png")
# plt.savefig(os.path.join(downloads_path, "my_plot.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(downloads_path, "grades.png"))
plt.show()
