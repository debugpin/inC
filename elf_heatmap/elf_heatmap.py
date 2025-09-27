import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from elftools.elf.elffile import ELFFile

if len(sys.argv) < 2:
    print(f"Usage: python3 {sys.argv[0]} <ELF binary>")
    sys.exit(1)

elf_path = sys.argv[1]

# Open ELF binary and keep file open during processing
with open(elf_path, 'rb') as f:
    elf = ELFFile(f)

    # Collect section names and sizes
    sections = []
    sizes = []
    for section in elf.iter_sections():
        sections.append(section.name)
        sizes.append(section['sh_size'])

    print(sections)
    print(sizes)

# Convert sizes to numpy array
sizes = np.array(sizes)
sizes_normalized = sizes / sizes.max() if sizes.max() != 0 else sizes

# Convert sizes to human-readable labels (bytes)
labels = [f"{s}" for s in sizes]

# Plot the heatmap
plt.figure(figsize=(12, 2))
sns.heatmap([sizes_normalized], annot=[labels], fmt="", yticklabels=[''], xticklabels=sections, cmap="Reds")
plt.title(f"ELF Section Size Heatmap: {elf_path}")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
