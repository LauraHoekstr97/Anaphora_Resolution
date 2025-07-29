import os
import ast
import re
import jsonlines
from Helper_functions import retrieve_anaphors_with_their_antecedents, search_sentence_number, recipe_details

# Cleans up + formats gpt output - Experiment 1
def formatting_experiment1(results_folder_name, doc_key):
    # Gets corresponding GPT output for this recipe, using doc_key search.
    file_path_folder_results = os.path.join('Results', results_folder_name, f'{doc_key}.txt')
    with open(file_path_folder_results, 'r') as file:
        raw_gpt_output = file.read()

    # Removes code block markers and whitespace
    stripped = raw_gpt_output.strip().removeprefix("```python").removesuffix(
        "```").strip()

    # Removes last, unfinished/broken list of lists in GPT output - there are symbols missing probably due to GPT seeming to be stuck in and thrown out a loop.
    # For now only needed for experiment 1 - gpt3.5

    correct_lists = re.findall(r"\[([^\[\]]+?)](?=,|\s*$)", stripped)  # Gets all lists which are not broken.
    stripped = "[" + ", ".join(f"[{correct_list}]" for correct_list in correct_lists) + "]" # Reconstructs the list again.

    # Parses the string into Python literal expressions.
    literals = ast.literal_eval(stripped)  # Parses the string into Python literal expressions.

    return literals

# Cleans up + formats gpt output - Experiment 2
def formatting_experiment2(results_folder_name, doc_key):
    file_path_folder_results = os.path.join('Results', results_folder_name, f'{doc_key}.jsonlines')
    with jsonlines.open(file_path_folder_results, 'r') as results_file:
        raw_gpt_output = results_file.read()

    labels = ('Coreference', 'Transformed', 'Ingredient_without_state_change_associated',
                          'Ingredient_with_state_change_associated')

    # Stores all GPT its predictions
    predictions = []

    # Goes over all predicted antecedents
    for label in labels:
        relations = raw_gpt_output.get(label)
        if relations:
            for relation in relations:
                anaphor, anaphor_sentence_number = relation[0] # Collects anaphor information
                string_predicted_antecedents = relation[1]
                predicted_antecedents = ast.literal_eval(string_predicted_antecedents) # Convert from string to literal.


                # Wraps it in a list if it is a single antecedent/a single list. - To make the next code work for one and also for more antecedents.
                if isinstance(predicted_antecedents[0], list):
                    items = predicted_antecedents
                else:
                    items = [predicted_antecedents]

                # Collects all information of each predicted antecedent.
                for item in items:
                    antecedent, antecedent_sentence_number, pred_label = item

                    # Stores it in preferred format for comparison.
                    predictions.append([anaphor, anaphor_sentence_number, antecedent, antecedent_sentence_number, pred_label])

    # Format: [anaphor, anaphor sentence number, predicted antecedent, predicted antecedent sentence number, predicted label]
    return predictions

# Turns data into same format as gpt results + returns doc_key which is used to retrieve the GPT results corresponding to the same recipe.
def formatting_reciperef(recipe):

    # 1. COLLECTS THE RECIPE DETAILS
    doc_key, coreference, transformed, ingredient_without_state_change_associated, ingredient_with_state_change_associated, all_sentences, sentence_spans_ex, sentence_input_format_gpt = recipe_details(recipe)

    relations = {
        'Coreference': coreference,
        'Transformed': transformed,
        'Ingredient_without_state_change_associated': ingredient_without_state_change_associated,
        'Ingredient_with_state_change_associated': ingredient_with_state_change_associated
    }

    # 2. EXPECTED OUTPUT - IN SAME FORMAT AS THE EXPERIMENTS.
    # To store the expected outputs
    expected_output_list = []

    # Includes every relation type in the training data.
    for label, relations in relations.items():
        anaphors_with_their_antecedents = retrieve_anaphors_with_their_antecedents(all_sentences, relations)

        for i, anaphor_antecedent_pair in enumerate(anaphors_with_their_antecedents):
            # Collecting information that needs to be included in the prompt.
            anaphor_ex = anaphor_antecedent_pair[0]
            span_anaphor_ex = relations[i][0]
            sentence_num_anaphor_ex = search_sentence_number(sentence_spans_ex, span_anaphor_ex)

            antecedent_ex = anaphor_antecedent_pair[1]
            span_antecedent_ex = relations[i][1]
            sentence_num_antecedent_ex = search_sentence_number(sentence_spans_ex, span_antecedent_ex)

            # Adds the expected output to the list.
            expected_output_list.append([anaphor_ex[0], sentence_num_anaphor_ex, antecedent_ex[0], sentence_num_antecedent_ex, label])

    return doc_key, expected_output_list