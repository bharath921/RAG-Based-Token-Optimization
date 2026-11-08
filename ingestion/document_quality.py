def normalize_text(text):
    """
    Normalize whitespace in extracted PDF text.
    """

    normalized_text = " ".join(text.split())

    return normalized_text


sample_text = "   Artificial Intelligence\n\n  is    transforming healthcare. "

result = normalize_text(sample_text)

print(result)