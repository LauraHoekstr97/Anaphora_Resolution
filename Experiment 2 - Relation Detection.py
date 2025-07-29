# Setting up experiment environment
from openai import OpenAI
import os
import jsonlines
import json
from tqdm import tqdm
from collections import defaultdict
from Helper_functions import recipe_details, retrieve_anaphors_with_their_antecedents, search_sentence_number

# GPT model set-up with personal API key
with open("C:/Users/Laura/Documents/1. Thesis/1. Experimentation/GPT_key_uni.txt", 'r') as key_file:
    my_key = key_file.read()
client = OpenAI(api_key = my_key)

# FEW SHOT TEXT - Constructs the text used in the prompt that shows the examples.
def build_examples_for_few_shot():
    few_shot_prompt = "Examples with answers:\n"

    with jsonlines.open('Data/Train2.english.jsonlines', 'r') as RecipeRef_train_file:
        recipes_ex = [recipe for recipe in RecipeRef_train_file]

    # 1. COLLECTS THE RECIPE DETAILS
    for recipe_ex in recipes_ex:
        doc_key, coreference, transformed, ingredient_without_state_change_associated, ingredient_with_state_change_associated, all_sentences, sentence_spans_ex, sentence_input_format_gpt = recipe_details(recipe_ex)

        relations = {
            'Coreference': coreference,
            'Transformed': transformed,
            'Ingredient_without_state_change_associated': ingredient_without_state_change_associated,
            'Ingredient_with_state_change_associated': ingredient_with_state_change_associated
        }

    # 2. BUILDS PROMPT TEXT
        # Includes every relation type in the training data.
        for label, relations in relations.items():
            anaphors_with_their_antecedents = retrieve_anaphors_with_their_antecedents(all_sentences, relations)

            # Includes every relation in the training data.
            for i, anaphor_antecedent_pair in enumerate(anaphors_with_their_antecedents):
                # Collecting information that needs to be included in the prompt.
                anaphor_ex = anaphor_antecedent_pair[0]
                span_anaphor_ex = relations[i][0]
                sentence_num_anaphor_ex = search_sentence_number(sentence_spans_ex, span_anaphor_ex)

                # Building prompt text.
                anaphora_task_ex = f"Recipe:\n"

                # Adds the sentences in which to find the antecedent.
                lines = [f"{index + 1}. {sentence}" for index, sentence in enumerate(sentence_input_format_gpt[0:sentence_num_anaphor_ex])]  # Gets sentences from index 0 to sentence_number-1 and formats it with sentence numbering.
                anaphora_task_ex += "\n".join(lines) + "\n"

                # Adds the anaphora for which the antecedent needs to be found.
                anaphora_task_ex += f"Analyze this anaphor which appears in the last sentence of the given recipe:\n{anaphor_ex}\n"

                # Adds the description of the expected output format.
                anaphora_task_ex += "Output in Python list format:\n"

        # 3. ADDS EXPECTED OUTPUT
                antecedent_ex = anaphor_antecedent_pair[1]
                span_antecedent_ex = relations[i][1]
                sentence_num_antecedent_ex = search_sentence_number(sentence_spans_ex, span_antecedent_ex)
                anaphora_task_ex += f"['{antecedent_ex[0]}', {sentence_num_antecedent_ex}, '{label}']"

                few_shot_prompt += f"\n{[anaphora_task_ex]}\n"

    # 4. ADDS EXAMPLE WITH MULTIPLE ANTECEDENTS
    # Hardcoding this part, since only one example is needed - and to avoid complex code.
    # Example is: Ingredient_with-state-change_associated": [[[[147, 148]], [[142, 144]]], [[[147, 148]], [[140, 140]]]
    with (open("Example with multiple antecedents.txt", 'r', encoding='utf-8') as example_file):
        example_with_multiple_antecedents = example_file.read()
        few_shot_prompt += f"\n{example_with_multiple_antecedents}\n"

    return few_shot_prompt

# PROMPT - Constructs the prompt.
def building_the_prompt(recipe_gpt_format, few_shot_text, anaphor_to_be_solved, sentence_number_anaphora):

    # 1. TASK DESCRIPTION - Gets the task description from the txt file.
    with (open("GPT Task description - Experiment 2.txt", 'r', encoding='utf-8') as task_file):
        task_description = task_file.read()
        cleaned_task_description = task_description.replace('\n', ' ') # Turns \n into white spaces (so the .txt itself can remain readable).

    # 2. TASK - creates the specific anaphora task that need to be solved by the model.
        anaphora_task_text = "Task for you to answer:\n\nSentences:\n"

        # Adds the sentences in which the model needs to find the antecedent.
        lines = [f"{index + 1}. {sentence}" for index, sentence in enumerate(recipe_gpt_format[0:sentence_number_anaphora])]  # Gets sentences from index 0 to sentence_number-1 and formats it with sentence numbering.
        anaphora_task_text += "\n".join(lines) + "\n"

        # Adds the anaphora for which the model needs to find the antecedent.
        anaphora_task_text += f"Analyze this anaphor which appears in the last sentence of the given recipe:\n'{anaphor_to_be_solved[0]}'\n"

        # Adds the expected output format which the model needs to use for its output.
        anaphora_task_text += "Output in Python list format:"

    # 3. CONSTRUCTING - Constructs the final prompt.
    # Building the few shot prompt (task description + examples + anaphora task)
    constructed_prompt = (f"{cleaned_task_description}\n"
                          f"\n{few_shot_text}"
                          f"\n{anaphora_task_text}")

    # 4. PROMPT - Returns the final prompt
    return constructed_prompt

# GPT MODEL - GPT model environment.
def gpt_model(input_prompt, model_type):
    response = client.chat.completions.create(
        model=model_type,
        messages=[{"role": "user", "content": input_prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()

# ANAPHORA TASK - Runs experiment for every anaphor gold mention within the recipe.
def experimentation_environment(recipe, few_shot_text, results_folder_name, gpt_model_type):
    # 1. COLLECTS THE RECIPE DETAILS
    key, coref, trans, ingredient_no_state_change, ingredient_state_change, recipe_sentences, sentence_spans, input_format_gpt = recipe_details(recipe)

    relations = {
        'Coreference': coref,
        'Transformed': trans,
        'Ingredient_without_state_change_associated': ingredient_no_state_change,
        'Ingredient_with_state_change_associated': ingredient_state_change
    }

    # 2. RELATION DETECTION TASK - for every gold anaphor mention.
    relation_results = defaultdict(list)  # For collecting the results per relation. Using relation key.
    tested_anaphors = set() # For checking if anaphor is already covered in earlier prompts (== anaphor with multiple antecedents).

    # Includes every relation type in the training data.
    for label, relation in relations.items():
        # Only if this relation exists in this recipe.
        if relation is not None:
            words_given_spans = retrieve_anaphors_with_their_antecedents(recipe_sentences, relation)

            # Testing every anaphor antecedent pair (of the relation type).
            for i, anaphor_antecedent_pair in enumerate(words_given_spans):
                # 1. BUILDING PROMPT

                # Collecting all information that needs to be included in the prompt.
                anaphor = anaphor_antecedent_pair[0]
                span_anaphor = relation[i][0]
                sentence_num_anaphor = search_sentence_number(sentence_spans, span_anaphor)
                anaphor_information = f'{anaphor[0]}', sentence_num_anaphor

                # Only makes prompt for anaphors that have not been seen before and skips over it if this anaphor is a duplicate (due too having multiple antecedents).
                if anaphor_information not in tested_anaphors:
                    # Adds the new anaphor to the set
                    tested_anaphors.add(anaphor_information)

                    # Builds the prompt for this anaphor antecedent pair.
                    prompt = building_the_prompt(input_format_gpt, few_shot_text, anaphor, sentence_num_anaphor)

                    # 2. RUNS GPT MODEL + SAVES THE OUTPUT
                    gpt_output = gpt_model(prompt, gpt_model_type)  # output format: [antecedent, sentence number, label].

                    # 3. SAVES GIVEN ANAPHOR + GPT OUTPUT in a dict
                    # Output format: [(anaphor, anaphor sentence number), gpt_output]
                    relation_results[label].append([anaphor_information, gpt_output])

    # format: label: [[(anaphor, anaphor sentence number), (gpt output)], [...]]
    relation_results_with_doc_key = {'doc_key': key, **relation_results}

    # 5. SAVES RESULTS IN A FILE.

    # 5.1. Creates a new results file for the recipe.
    result_file_name = key + '.jsonlines'  # The file name correspond with the doc_key of the recipe.
    file_path_results = os.path.join('Results', results_folder_name, result_file_name)

    # 5.2 Writes the corresponding results to the file.
    with open(file_path_results, "w") as result_file:
        json.dump(relation_results_with_doc_key, result_file)


# ---------- RUN EXPERIMENT ENVIRONMENT ----------

# Runs the experiment
with jsonlines.open('Data/Test.english.jsonlines', 'r') as RecipeRef_data_file:
    test_recipes = [recipe for recipe in RecipeRef_data_file] # Stores recipes in a list for easy accessibility.

few_shot = build_examples_for_few_shot()

# Loops through all recipes for which the model needs to do relation detection.
# Uncomment below to run experiment/gpt model!
for test_recipe in tqdm(test_recipes, desc="Processing Recipes"):
    # Experiment 2 - GPT3.5
    '''experimentation_environment(test_recipe, few_shot,
                                "Experiment 2 - GPT4.1", "gpt-4.1-2025-04-14")'''
    # Experiment 2 - GPT3.5
    '''experimentation_environment(test_recipe, few_shot,
                                "Experiment 2 - GPT3.5", "gpt-3.5-turbo-0125")'''