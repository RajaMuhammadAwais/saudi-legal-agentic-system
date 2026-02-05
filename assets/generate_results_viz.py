import matplotlib.pyplot as plt
import pandas as pd
import json

# Load the bilingual test results
with open('bilingual_test_results.json', 'r') as f:
    data = json.load(f)

results = data['results']
df = pd.DataFrame([
    {
        'Scenario': r['scenario_id'],
        'Language': r['language'],
        'Time (s)': float(r['execution_time'].replace('s', '')),
        'Confidence': r['result']['confidence']
    } for r in results
])

# Set up the plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar plot for Execution Time
color = 'tab:blue'
ax1.set_xlabel('Scenario ID')
ax1.set_ylabel('Execution Time (s)', color=color)
bars = ax1.bar(df['Scenario'], df['Time (s)'], color=color, alpha=0.6, label='Execution Time')
ax1.tick_params(axis='y', labelcolor=color)

# Second axis for Confidence
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Confidence Score', color=color)
line = ax2.plot(df['Scenario'], df['Confidence'], color=color, marker='o', linewidth=2, label='Confidence')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 1.1)

# Add titles and legend
plt.title('Saudi Legal Agentic System: Bilingual Test Results', fontsize=14)
fig.tight_layout()

# Save the plot
plt.savefig('test_results_visualization.png', dpi=300)
print("Visualization saved as test_results_visualization.png")
