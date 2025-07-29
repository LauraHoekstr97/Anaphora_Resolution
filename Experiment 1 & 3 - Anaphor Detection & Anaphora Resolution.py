import jsonlines
import os
from tqdm import tqdm
from openai import OpenAI
from Helper_functions import recipe_details
from Post_processing_and_formatting import formatting_reciperef

# GPT model set-up with personal API key
with open("C:/Users/Laura/Documents/1. Thesis/1. Experimentation/GPT_key_uni.txt", 'r') as key_file:
    my_key = key_file.read()
client = OpenAI(api_key = my_key)

# FEW SHOT TEXT - Constructs the text used in the prompt that shows the examples.
def build_examples_for_few_shot():
    few_shot_prompt = "Examples with answers:\n\n"

    with jsonlines.open("Data/Train.english.jsonlines", 'r') as RecipeRef_train_file:
        recipes_ex = [recipe for recipe in RecipeRef_train_file]

    # 1. COLLECTS THE RECIPE DETAILS
    for recipe_index, recipe_ex in enumerate(recipes_ex):
        doc_key, coreference, transformed, ingredient_without_state_change_associated, ingredient_with_state_change_associated, all_sentences, sentence_spans_ex, sentence_input_format_gpt = recipe_details(recipe_ex)

        # 2. BUILDS PROMPT TEXT

        # Includes the recipe == numbered sentences
        few_shot_prompt += f"Recipe:\n"
        lines = [f"{index + 1}. {sentence}" for index, sentence in enumerate(sentence_input_format_gpt)]
        few_shot_prompt += "\n".join(lines) + "\n\n"

        # Adds the description of the expected output format.
        few_shot_prompt+= "Output in Python list format:\n"

        # 3. ADDS EXPECTED OUTPUT
        # Turns expected output data in GPT format.
        doc_key, expected_output = formatting_reciperef(recipe_ex)
        # Adds the examples to the task
        few_shot_prompt += f"{expected_output}\n\n"

    return few_shot_prompt

# PROMPT - Constructs the prompt.
def build_the_prompt(recipe, few_shot_text):
    # 1. TASK DESCRIPTION
    # Gets the task description from te txt file.
    with (open("GPT Task description - Experiment 1&3.txt", 'r', encoding='utf-8') as task_file):
        task_description = task_file.read()
        cleaned_task_description = task_description.replace('\n', ' ') # Turns \n into white spaces (so the .txt itself can remain readable).

    # 2. RECIPE TO BE SOLVED
    doc_key, coreference, transformed, ingredient_without_state_change_associated, ingredient_with_state_change_associated, all_sentences, sentence_spans_ex, sentence_input_format_gpt = recipe_details(recipe)
    task = "Task for you to answer:\n\n"

    # Includes the recipe == numbered sentences
    task += f"Recipe:\n"
    lines = [f"{index + 1}. {sentence}" for index, sentence in enumerate(sentence_input_format_gpt)]
    task += "\n".join(lines) + "\n\n"

    # Adds the que for the model to solve the anaphora for the given recipe.
    task+= "Output in Python list format:\n\n"

    # 3. FINAL PROMPT (WITH FEW SHOT ADDED)
    final_prompt = f"{cleaned_task_description}\n\n{few_shot_text}\n{task}"

    return final_prompt

# GPT MODEL - GPT model environment.
def gpt_model(input_prompt, model_type):
    response = client.chat.completions.create(
        model= model_type,
        messages=[{"role": "user", "content": input_prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# EXPERIMENT - runs experiment
def experimentation_environment(recipe, few_shot_text, results_folder_name, gpt_model_type):
    doc_key = recipe['doc_key']

    # 1. EXPERIMENT
    prompt = build_the_prompt(recipe, few_shot_text) # Creates the prompt.
    results = gpt_model(prompt, gpt_model_type) # Runs the model with the recipe.

    # 2. SAVING THE RESULTS

    # 2.1. Creates a new results file.
    result_file_name = doc_key + '.txt'  # The file name correspond with the doc_key of the recipe.
    file_path_results = os.path.join('Results', results_folder_name, result_file_name)

    # 2.2. Writes the corresponding results to the file.
    with open(file_path_results, "w") as result_file:
        result_file.write(results)


# ------------ RUN EXPERIMENT -----------------------------

# EXPERIMENT - Runs experiment on given test settings and saves the results a corresponding file. (So that when the model stops at least able to check until which recipe the results are there/saved.)
with jsonlines.open('Data/Test.english.jsonlines', 'r') as RecipeRef_dev_file:
    test_recipes = [input_recipe for input_recipe in RecipeRef_dev_file]

# Constructs the few shot text. - done outside the experiment and prompt function, since it only needs to be constructed once. Because stays the same throughout the whole experiment.
few_shot = build_examples_for_few_shot()

# Loops through all recipes for which the model needs to solve the anaphora.
# Uncomment below to run experiment/gpt model!
for test_recipe in tqdm(test_recipes, desc="Recipe Progress"):
    # Experiment 1 - GPT3.5
    '''experimentation_environment(test_recipe, few_shot, "Experiment 1 - GPT4.1", "gpt-4.1-2025-04-14")'''
    # Experiment 1 - GPT3.5
    '''experimentation_environment(test_recipe, few_shot, "Experiment 1 - GPT3.5", "gpt-3.5-turbo-0125")'''