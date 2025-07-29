import itertools
from collections import defaultdict

# Retrieves useful information of the recipe, contained in the dataset, for creating the prompt
def recipe_details(recipe):
    doc_key = recipe['doc_key']
    sentences = recipe['sentences']
    coreference = recipe.get('Coreference')
    transformed = recipe.get('Transformed')
    ingredient_without_state_change_associated = recipe.get('Ingredient_without-state-change_associated')
    ingredient_with_state_change_associated = recipe.get('Ingredient_with-state-change_associated')
    all_sentences = list(itertools.chain(*sentences))

    # Turns all sentences into readable sentences for GPT input.
    sentence_input_format_gpt = []
    for sentence in sentences:
        sentence_input_format_gpt.append((" ".join(sentence)).replace(' .', '.').replace(' ,', ','))

    # full_recipe = " ".join(all_sentences)
    # full_recipe_clean = full_recipe.replace(' .', '.').replace(' ,', ',')

    # Collecting the word index range (span) of each sentence within the recipe. For usage GPT. To help match the GPT output.
    sentence_spans = defaultdict(list)  # Default_dict so sentence 1 matches with key 1. (because with a list sentence 1 would match with index 0, which might turn be confusing and might turn into minor mistakes later on)
    counter_span = 0

    for i, sentence in enumerate(sentences):
        sentence_number = i + 1
        span = [counter_span, counter_span + len(sentence) - 1]
        sentence_spans[sentence_number] = span

        counter_span += len(sentence)  # Updating counter_span to index of the first word of the next sentence.

    '''print(f"Recipe entry: {recipe}")
    # Use to find position (e.g. of words that corefer).
    print(f"Full recipe: {all_sentences}")
    print(f"Use as LLM input: {sentence_input_format_gpt}")
    # Use to check GPT its output.
    print(f"Span_dict: {sentence_spans}")'''

    return (doc_key, coreference, transformed, ingredient_without_state_change_associated,
            ingredient_with_state_change_associated, all_sentences, sentence_spans, sentence_input_format_gpt)

# Returns words corresponding to given spans (corresponding to words locations).
def retrieve_words_given_spans(input_spans, sentences):
    corresponding_words = []

    for span in input_spans:
        words_per_span = []
        begin_span = span[0]
        end_span = span[1] + 1

        for i in range(begin_span, end_span):
            words_per_span.append(sentences[i])

        joined_words = " ".join(words_per_span)
        corresponding_words.append(joined_words)

    return corresponding_words

# Retrieves the anaphor with their antecedent.
def retrieve_anaphors_with_their_antecedents(sentences, references):
    anaphor_antecedent_pair = []

    for referring_pair in references:
        anaphor = retrieve_words_given_spans(referring_pair[0], sentences)
        antecedent = retrieve_words_given_spans(referring_pair[1], sentences)
        anaphor_antecedent_pair.append([anaphor, antecedent])

    # Returns a list of the anaphors and their corresponding antecedents.
    return anaphor_antecedent_pair

# Finds sentence number given a span.
def search_sentence_number(sentence_spans, mention_span):
    start_mention = mention_span[0][0]
    end_mention = mention_span[0][1]

    for sentence_number, span in sentence_spans.items():
        start, end = span
        if start <= start_mention and end_mention <= end:
            return sentence_number

    # print(f"sentence number not found for mention span: {mention_span}")
    return None # if no matching sentence is found

# Checks whether the output is in the expected format
'''def is_single_list(output):
    single_list = isinstance(output, list) and all(not isinstance(elem, list) for elem in output)
    return single_list'''

# Sort the output by anaphoric label
def grouped_by_label(data):
    data_grouped_by_label = defaultdict(list)
    for result in data:
        label = result[4]  # label is stored at index 4.
        data_grouped_by_label[label].append(result)

    return data_grouped_by_label

