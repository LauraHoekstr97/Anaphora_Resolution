# Anaphora Resolution (Master-Thesis - 2025)

***This repository contains code for anaphora resolution experiments on recipes using GPT-based models.***

---  

## 🤖 Overview of the Experiments

### **Experiment 1: Anaphor Detection**
Task: Identify the anaphors in the recipe(s).  
The *recipe* and *prompt* are provided, and the model predicts the *anaphors*.

### **Experiment 2: Relation Detection**
Task: Given an anaphor, identify the antecedent(s) within the recipe.  
The *recipe*, *anaphor* and *prompt* are provided, and the model predicts the *antecedent*.

### **Experiment 3: Anaphora Resolution** - not available (yet)
Task: Anaphora resolution — both *identifying anaphors* and *identifying their antecedents*.  
The *recipe* and the *prompt* are provided, and the model predicts the *anaphoric relations*.

---  

## 🚀 Running the Experiments

1. **Choose the experiment to run**:  
   For *experiment 1 & 3*, run the `Experiment 1 & 3 - Anaphor Detection & Anaphora Resolution.py` file.  
   For *experiment 2*, run the `Experiment 2 - Relation Detection.py` file.

2. **Select the GPT model**:
   Inside the corresponding experiment file, *uncomment the lines* related to the GPT model you want to use.  

***Note***: The results, the GPT outputs, are already available in the results folder, so it's not necessary to run the experiment code to access them. Thus, you can skip Step 1 if preferred.

---

## 📊 Evaluation
To evaluate the experiment results, run the `Evaluation.py` file.  
Inside the evaluation file, *uncomment the lines* of the experiment(s) you want to evaluate.  

*Format* after post-processing and formatting: ``` [anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label] ```

---

## 📂 Code Files
**Main files**:
  - `Experiment 1 & 3 - Anaphor Detection & Anaphora Resolution.py` — for experiment 1 (and possibly experiment 3).
  - `Experiment 2 - Relation Detection.py` — for experiment 2.
  - `Evaluation.py` — for result evaluation.

**Supporting files**: All other code and files are utilities used by the three main files above.
- `Helper_functions.py` — Contains small functions that are used frequently throughout the project.
- `Post_processing_and_formatting.py` — Contains functions to standardise all outputs into a consistent format, to enable comparison.
  
- `Example with multiple antecedents.txt` — Contains an extra example used in the few-shot prompt of experiment 2.
- `GPT Task description - Experiment 1&3.txt` — The task description of experiment 1 (and 3).
- `GPT Task description - Experiment 2.txt` — The task description of experiment 2.

**Folders**
- `Results`: Contains the experiment results (and gets automatically updated) when the experiment code is run. The subfolders correspond to the experiment and the GPT model used.
- `Data`: Contains the training (used for few-shot) and test datasets used in the experiments. The data is sourced from RecipeRef (add citation).
---

## 👩🏻‍🍳🍳 Data  
The data used for these experiments consists of annotated recipe texts from the RecipeRef corpus:   
- RecipeRef is from and described in : [What does it take to bake a cake?](https://aclanthology.org/2022.findings-acl.275/) by Fang et al. (2022)
- RecipeRef can be found at: [RecipeRef GitHub repository](https://github.com/biaoyanf/RecipeRef/tree/main/data)
---



