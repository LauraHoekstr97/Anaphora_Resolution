# Anaphora Resolution (Master-Thesis - 2025)

This repository contains code for the **anaphora resolution** experiments using GPT models.
The experiments utilise the RecipeRef data from the [RecipeRef dataset](#data).

---

## 🤖 Overview of the Experiments

### **Experiment 1: Anaphor Detection**
- Task: Identifying **anaphors** in the recipe(s).
- The model identifies the **anaphors** from raw recipe.
- Results file format:
- Evaluation format: ``` [anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label] ```

### **Experiment 2: Relation Detection**
- Task: Given an anaphor, predicting the **antecedent**.
- The **anaphor is provided**, and the model predicts the **antecedent**.
- Results file format:
- Evaluation format: ``` [anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label] ```

### **Experiment 3: Full Anaphora Resolution** - not available (yet)
- Task: Anaphora resolution — both **detecting anaphors** and **identifying their antecedents**.
- This experiment involves both tasks: anaphor detection and relations detection.
- The model identifies the **anaphors** and their **antecedents** from the recipe.
- Data format:
- Evaluation format: ``` [anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label] ```

## 💻 Running the Experiments

1. **Choose the experiment to run**:
   - For **Experiment 1 & 3**, run the `Experiment1_3.py` file.
   - For **Experiment 2**, run the `Experiment2.py` file.

2. **Select the GPT model**:
   - Inside the corresponding experiment file, **uncomment the lines** related to the GPT model you want to use.

---

## 📊 Evaluation

- To evaluate the experiment results, run the `Evaluation.py` file.
- Inside the evaluation file, **uncomment the lines** of the experiment(s)/results you want to evaluate.

---

## 📂 Code Files

- **Main files**:
  - `Experiment 1 & 3 - Anaphor Detection & Anaphora Resolution.py` - for experiment 1 (and possibly experiment 3)
  - `Experiment 2 - Relation Detection.py` — for Experiment 2
  - `Evaluation.py` — for result evaluation

- **Supporting files**: All other code and files are utilities used by the three main files above.
- Helper_functions.py
- Post_processing_and_formatting.py
- Example with multiple antecedents.txt
- GPT Task description - Experiment 1&3.txt
- GPT Task description - Experiment 2.txt

**Folders**
- Results: This folder... consist and updates...
- Results:

---

## 👩🏻‍🍳🍳 Data

- The RecipeRef data is from **RecipeRef**.  
  📖 Reference: [Include citation here]

---

## 🧷 Data & Output Formats

### **Postprocessed Data Format**
```
[anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label]
```


