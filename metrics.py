import matplotlib.pyplot as plt

# Evaluation steps or iterations (e.g., 1 to 5)
iterations = [1, 2, 3, 4, 5]

# Sample data — replace these with your real values
english = {
    'accuracy': [87, 88.5, 89.2, 90.1, 90.5],
    'precision': [85, 86.2, 87.5, 88.3, 88.9],
    'recall': [86.5, 87.8, 89, 90.2, 90.4]
}
hindi = {
    'accuracy': [86.5, 88, 89.1, 89.9, 90.2],
    'precision': [84, 85.6, 86.9, 87.8, 88.3],
    'recall': [85.7, 87, 88.6, 89.1, 89.9]
}
tamil = {
    'accuracy': [85.9, 87.4, 88.8, 89.3, 89.7],
    'precision': [83.5, 84.9, 86.4, 87.1, 87.6],
    'recall': [84.8, 86.2, 87.7, 88.4, 89]
}

# Create a line chart for each metric
metrics = ['accuracy', 'precision', 'recall']
colors = {'english': 'blue', 'hindi': 'green', 'tamil': 'red'}

for metric in metrics:
    plt.figure(figsize=(10, 5))
    plt.plot(iterations, english[metric], marker='o', label='English', color=colors['english'])
    plt.plot(iterations, hindi[metric], marker='o', label='Hindi', color=colors['hindi'])
    plt.plot(iterations, tamil[metric], marker='o', label='Tamil', color=colors['tamil'])
    
    plt.title(f"{metric.capitalize()} over Evaluation Iterations")
    plt.xlabel("Iteration")
    plt.ylabel(f"{metric.capitalize()} (%)")
    plt.ylim(80, 95)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
