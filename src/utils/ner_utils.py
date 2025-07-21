def clean_ner_output(ner_results):
    """
    Cleans and merges entity tokens into meaningful entity strings.
    """
    cleaned = []
    temp = {}
    for entity in ner_results:
        word = entity["word"].replace("##", "")
        entity_type = entity["entity_group"]
        if temp and temp["entity_group"] == entity_type:
            temp["word"] += word if entity["word"].startswith("##") else " " + word
        else:
            if temp:
                cleaned.append(temp)
            temp = {"word": word, "entity_group": entity_type}
    if temp:
        cleaned.append(temp)
    return cleaned
