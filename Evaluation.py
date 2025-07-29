# Error analysis
import pandas as pd
from Helper_functions import grouped_by_label
from Post_processing_and_formatting import *

# Compares the model its predicted results with the expected results.
def comparing_results(results_folder_name, experiment=None):
    # Imports the official test data (with the expected output)
    with jsonlines.open('Data/Test.english.jsonlines', 'r') as RecipeRef_test_file:
        input_recipes = [input_recipe for input_recipe in RecipeRef_test_file]

    # Saves all the results
    results_experiment = []

    # Compares for every recipe the expected output with the GPT model output
    for recipe in input_recipes:

    # 1. COLLECTING ALL RECIPE INFORMATION
        # Turns test data into same format as gpt results for comparison + gets doc_key which is used to retrieve the GPT results corresponding to the same recipe.
        doc_key, expected_output  = formatting_reciperef(recipe)

    # 2. POST PROCESSING & FORMAT
        # Formatting function depends on the experiment
        if experiment == 'Experiment 1':
            cleaned_gpt_results = formatting_experiment1(results_folder_name, doc_key)
        elif experiment == 'Experiment 2':
            cleaned_gpt_results = formatting_experiment2(results_folder_name, doc_key)
        else:
            cleaned_gpt_results = None
            print(f'No experiment given as parameter, please do so!')

        # Groups output by anaphoric relation
        gpt_output_grouped_by_label = grouped_by_label(cleaned_gpt_results)
        expected_output_grouped_by_label = grouped_by_label(expected_output)

    # 3. ANALYSING RESULTS
        labels = ('Coreference','Transformed','Ingredient_without_state_change_associated','Ingredient_with_state_change_associated')

        # Gets the results for this specific label
        for label in labels:
            predicted = gpt_output_grouped_by_label.get(label, [])  # returns empty set when label does not exist.
            expected = expected_output_grouped_by_label.get(label, [])

            # Evaluation depends on experiment.
            # Format: [anaphor, sentence number of anaphor, antecedent, sentence number of antecedent, label]

            # Experiment 1 = anaphor detection, so evaluating x[0] and x[1]
            if experiment == 'Experiment 1':
                # Only comparing the anaphor prediction results.
                predicted_set = set((x[0], x[1]) for x in predicted)
                expected_set = set((x[0], x[1]) for x in expected)

            # Experiment 2 = relation detection, so evaluating x[2] and x[3].
            else:
                # Comparing the antecedent (relation) prediction results.
                predicted_set = set((x[2], x[3]) for x in predicted)
                expected_set = set((x[2], x[3]) for x in expected)

            # Collects TP (True Positives), FPs (False Negatives) and FPs (False Positives)
            tp = predicted_set & expected_set # GPT correctly identifies anaphor.
            fp = predicted_set - expected_set # GPT predicts an anaphor, but it is not an anaphor.
            fn = expected_set - predicted_set # GPT fails to identify the anaphor.

            # Stored the results + examples
            results_experiment.append({
                'doc_key': doc_key,
                'label': label,
                'TP': len(tp),
                'FP': len(fp),
                'FN': len(fn),
                'TP_examples': list(tp),
                'FP_examples': list(fp),
                'FN_examples': list(fn),
            })

    return results_experiment

# Collects total TPs, FPs, FNs per label_type and calculates precision, recall and F1 scores (and prints them).
def calculate_metrics(results_df, experiment_name):
    # All labels in the dataset
    labels = ('Coreference', 'Transformed', 'Ingredient_without_state_change_associated', 'Ingredient_with_state_change_associated')

    # Introduces results in the terminal
    print(f'Results {experiment_name}:')

    # For each label in the dataset...
    for label in labels:
        # ...collects and prints total TPs, FPs and FNs (over all the recipes).
        tp = ((results_df[results_df['label'] == label])['TP']).sum()
        fp = ((results_df[results_df['label'] == label])['FP']).sum()
        fn = ((results_df[results_df['label'] == label])['FN']).sum()

        # ... calculates Precision, Recall and F1
        # NOTE! dividing by 0 is not possible, therefore first checks if 0 in the if statement.
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        # Prints the found results
        print(f'{label}: TP: {tp}, FP: {fp}, FN: {fn}, Precision: {precision*100}, Recall: {recall*100}, F1: {f1*100}')
    print(f'\n')


# ------ EXPERIMENT RESULTS EVALUATION ---------

# Results Experiment 1 - Anaphor Prediction - GPT4.1
results_experiment1_df = pd.DataFrame(comparing_results('Experiment 1 - GPT4.1', 'Experiment 1')) # Retrieves evaluation information and directly puts it in Pandas dataframe for easy analysis.
calculate_metrics(results_experiment1_df, 'Experiment 1 - Anaphor Prediction - GPT4.1') # Prints the results'''

# Results Experiment 2 - Relation Detection - GPT4.1
'''results_experiment1_df = pd.DataFrame(comparing_results('Experiment 2 - GPT4.1', 'Experiment 2')) # Retrieves evaluation information and directly puts it in Pandas dataframe for easy analysis.
calculate_metrics(results_experiment1_df, 'Experiment 2 - Anaphor Relation Detection - GPT4.1') # Prints the results'''

# Results Experiment 1 - Anaphor Prediction - GPT3.5
'''results_experiment1_df = pd.DataFrame(comparing_results('Experiment 1 - GPT3.5', 'Experiment 1')) # Retrieves evaluation information and directly puts it in Pandas dataframe for easy analysis.
calculate_metrics(results_experiment1_df, 'Experiment 1 - Anaphor Prediction - GPT3.5') # Prints the results '''

# Results Experiment 2 - Relation Detection - GPT3.5
'''results_experiment1_df = pd.DataFrame(comparing_results('Experiment 2 - GPT3.5', 'Experiment 2')) # Retrieves evaluation information and directly puts it in Pandas dataframe for easy analysis.
calculate_metrics(results_experiment1_df, 'Experiment 2 - Anaphor Relation Detection - GPT3.5') # Prints the results'''