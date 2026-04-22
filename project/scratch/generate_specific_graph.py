import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Data for the specific models requested
data = {
    'Model': ['Random Forest', 'KNN', 'SVM', 'Logistic Regression'],
    'Accuracy': [0.9808, 0.9770, 0.9152, 0.9145],
    'Precision': [0.9808, 0.9770, 0.9148, 0.9142],
    'F1-Score': [0.9807, 0.9770, 0.9124, 0.9116]
}

df = pd.DataFrame(data)

# Set style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# Create long-form data for seaborn
df_melted = df.melt(id_vars='Model', var_name='Metric', value_name='Score')

# Plot
ax = sns.barplot(data=df_melted, x='Model', y='Score', hue='Metric', palette='viridis')

# Customize
plt.title('Fischer Detector: Specific Model Comparison', fontsize=16, pad=20)
plt.ylim(0.8, 1.0)  # Zoom in on the top section for clarity
plt.ylabel('Score (0.0 - 1.0)', fontsize=12)
plt.xlabel('Model Architecture', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Add values on top of bars
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.4f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points',
                   fontsize=9)

plt.tight_layout()

# Save
output_path = '/home/yashbansal/machinelearning/project/results/specific_model_comparison.png'
plt.savefig(output_path)
print(f"Graph successfully saved to: {output_path}")
