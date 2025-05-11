import matplotlib.pyplot as plt

# X-axis labels (languages)
languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Marathi',
             'Kannada', 'Bengali', 'Gujarati', 'Malayalam', 'Punjabi']

# Sample values based on your image (visually estimated)
precision = [0.91, 0.88, 0.86, 0.84, 0.83, 0.82, 0.81, 0.80, 0.79, 0.77]
recall    = [0.90, 0.87, 0.85, 0.83, 0.82, 0.81, 0.80, 0.79, 0.78, 0.76]
f1_score  = [0.905, 0.875, 0.855, 0.835, 0.825, 0.815, 0.805, 0.795, 0.785, 0.765]

# Create line chart
plt.figure(figsize=(12, 6))

plt.plot(languages, precision, marker='o', label='Precision', color='blue', linewidth=2)
plt.plot(languages, recall, marker='o', label='Recall', color='red', linewidth=2)
plt.plot(languages, f1_score, marker='o', label='F1-Score', color='green', linewidth=2)

plt.title('Model Performance Metrics Across Indian Languages')
plt.xlabel('Language')
plt.ylabel('Score')
plt.ylim(0.7, 1.0)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
