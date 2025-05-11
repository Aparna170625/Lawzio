import matplotlib.pyplot as plt
import numpy as np


languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Marathi', 'Kannada', 'Bengali', 'Gujarati', 'Malayalam', 'Punjabi']


precision = [0.91, 0.88, 0.86, 0.85, 0.84, 0.83, 0.825, 0.815, 0.80, 0.785]
recall    = [0.90, 0.87, 0.85, 0.83, 0.82, 0.825, 0.815, 0.805, 0.79, 0.77]
f1_score  = [0.905, 0.875, 0.855, 0.84, 0.83, 0.827, 0.82, 0.807, 0.785, 0.765]

x = np.arange(len(languages))  # the label locations
width = 0.25  # the width of the bars

# Create the plot
fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width, precision, width, label='Precision', color='orange')
bars2 = ax.bar(x, recall, width, label='Recall', color='gold')
bars3 = ax.bar(x + width, f1_score, width, label='F1-Score', color='deeppink')

# Labels and Title
ax.set_xlabel('Language')
ax.set_ylabel('Score')
ax.set_title('Model Performance Across Indian Languages')
ax.set_xticks(x)
ax.set_xticklabels(languages)
ax.set_ylim([0.70, 1.00])
ax.legend()

# Grid
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
