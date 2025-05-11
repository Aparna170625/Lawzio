import matplotlib.pyplot as plt

# Iteration steps (replace with actual steps like epochs or tests if needed)
iterations = [1, 2, 3, 4, 5]

# Sample Precision and Recall values (replace with real values)
english = {
    'precision': [85, 86.2, 87.5, 88.3, 88.9],
    'recall':    [86.5, 87.8, 89.0, 90.2, 90.4]
}
hindi = {
    'precision': [84, 85.6, 86.9, 87.8, 88.3],
    'recall':    [85.7, 87.0, 88.6, 89.1, 89.9]
}
tamil = {
    'precision': [83.5, 84.9, 86.4, 87.1, 87.6],
    'recall':    [84.8, 86.2, 87.7, 88.4, 89.0]
}

# Plot Precision
plt.figure(figsize=(10, 5))
plt.plot(iterations, english['precision'], marker='o', label='English', color='blue')
plt.plot(iterations, hindi['precision'], marker='o', label='Hindi', color='green')
plt.plot(iterations, tamil['precision'], marker='o', label='Tamil', color='red')

plt.title("Precision over Evaluation Iterations")
plt.xlabel("Iteration")
plt.ylabel("Precision (%)")
plt.ylim(80, 95)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Plot Recall
plt.figure(figsize=(10, 5))
plt.plot(iterations, english['recall'], marker='o', label='English', color='blue')
plt.plot(iterations, hindi['recall'], marker='o', label='Hindi', color='green')
plt.plot(iterations, tamil['recall'], marker='o', label='Tamil', color='red')

plt.title("Recall over Evaluation Iterations")
plt.xlabel("Iteration")
plt.ylabel("Recall (%)")
plt.ylim(80, 95)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
