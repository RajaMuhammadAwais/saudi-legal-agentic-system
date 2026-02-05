import matplotlib.pyplot as plt
from matplotlib import rcParams

# Use a font that supports Arabic
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans Arabic', 'Arial']

terminal_output = """
ubuntu@sandbox:~/saudi-legal-agentic-system $ ls -la
total 360
drwxrwxr-x  4 ubuntu ubuntu   4096 Feb  5 00:45 .
drwxr-x--- 14 ubuntu ubuntu   4096 Feb  5 00:47 ..
drwxrwxr-x  8 ubuntu ubuntu   4096 Feb  5 00:45 .git
-rw-rw-r--  1 ubuntu ubuntu   5490 Feb  5 00:42 README.md
-rw-rw-r--  1 ubuntu ubuntu   5775 Feb  5 00:42 bilingual_test_results.json
-rw-rw-r--  1 ubuntu ubuntu 105375 Feb  5 00:32 saudi_labor_law.txt
-rw-rw-r--  1 ubuntu ubuntu   7580 Feb  5 00:35 saudi_legal_lightning.py
-rw-r--r--  1 ubuntu ubuntu   2745 Feb  5 00:41 test_bilingual_scenarios.py

ubuntu@sandbox:~/saudi-legal-agentic-system $ python3 test_bilingual_scenarios.py
--- Starting Bilingual Test Suite (4 scenarios) ---
[Scenario EN_LABOR_01] Language: English
Query: What are the specific conditions for a valid non-compete clause...
Triage: DEEP | Plan generated.
Lightning Execution Time: 10.40s
--- [Self-Improvement] Analyzing performance... ---
Self-Improvement: Learned new tip - Enhance the LegalExtractor...
Completed in 11.45s with confidence 1.0

[Scenario AR_LABOR_01] Language: Arabic
Query: ما هي شروط الاستقالة في نظام العمل السعودي...
Triage: FAST | Plan generated.
Lightning Execution Time: 7.82s
--- [Self-Improvement] Analyzing performance... ---
Self-Improvement: Learned new tip - The Synthesizer should segment...
Completed in 9.03s with confidence 0.95

--- All tests completed. Results saved to bilingual_test_results.json ---
"""

fig, ax = plt.subplots(figsize=(12, 8))
# Note: Matplotlib's text rendering for Arabic is limited without additional libraries like arabic_reshaper,
# but using a compatible font will at least show the characters.
ax.text(0.01, 0.99, terminal_output, fontsize=10, verticalalignment='top', transform=ax.transAxes)
ax.set_axis_off()
plt.title("Local Environment & Test Execution Screenshot", fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('local_env_screenshot.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Terminal screenshot saved as local_env_screenshot.png")
