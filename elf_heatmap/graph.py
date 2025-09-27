import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

stages = [
    "(small) GCC out of the box",
    "(smaller) GCC without the standard library",
    "(tiny) NASM out of the box",
    "(insy) NASM with explicit Linker Script",
    "insy + strip",
    "insy + strip + sstrip"
]

sizes = [15784, 8816, 4648, 584, 352, 138]
percentages = [size / sizes[0] * 100 for size in sizes]

# Create segments for gradient
points = np.array([range(len(stages)), percentages]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create a colormap
cmap = plt.get_cmap('viridis')
norm = plt.Normalize(0, len(segments))

lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=2)
lc.set_array(np.arange(len(segments)))

fig, ax = plt.subplots(figsize=(10, 6))
ax.add_collection(lc)

# Plot points on top
ax.plot(range(len(stages)), percentages, 'o', color='black')

# Annotate points with actual sizes
for i, (perc, size) in enumerate(zip(percentages, sizes)):
    ax.text(i, perc + 2, f"{size} B", ha='center', va='bottom', fontsize=9)

ax.set_xticks(range(len(stages)))
ax.set_xticklabels(stages, rotation=30, ha='right')
ax.set_ylim(0, 110)
ax.set_ylabel("Size (% of original)")
ax.set_title("Binary Size Reduction Across Stages")
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
