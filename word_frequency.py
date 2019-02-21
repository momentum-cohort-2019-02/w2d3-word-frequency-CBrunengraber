import collections
import string

STOP_WORDS = [
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'i', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'were',
    'will', 'with'
]

seneca_falls = ['when', 'course', 'human', 'events', 'becomes', 'necessary', 'one', 'portion', 'family', 'man', 'assume', 'among', 'people', 'earth', 'position', 'different', 'which', 'they', 'have', 'hitherto', 'occupied', 'but', 'one', 'which', 'laws', 'nature', 'natures', 'god', 'entitle', 'them', 'decent', 'respect', 'opinions', 'mankind', 'requires', 'they', 'should', 'declare', 'causes', 'impel', 'them', 'such', 'course', 'we', 'hold', 'these', 'truths', 'selfevident', 'all', 'men', 'women', 'created', 'equal', 'they', 'endowed', 'their', 'creator', 'certain', 'inalienable', 'rights', 'among', 'these', 'life', 'liberty', 'pursuit', 'happiness', 'secure', 'these', 'rights', 'governments', 'instituted', 'deriving', 'their', 'just', 'powers', 'consent', 'governed', 'whenever', 'any', 'form', 'government', 'becomes', 'destructive', 'these', 'ends', 'right', 'those', 'who', 'suffer', 'refuse', 'allegiance', 'insist', 'upon', 'institution', 'new', 'government', 'laying', 'foundation', 'such', 'principles', 'organizing', 'powers', 'such', 'form', 'them', 'shall', 'seem', 'most', 'likely', 'effect', 'their', 'safety', 'happiness', 'prudence', 'indeed', 'dictate', 'governments', 'long', 'established', 'should', 'not', 'changed', 'light', 'transient', 'causes', 'accordingly', 'all', 'experience', 'hath', 'shown', 'mankind', 'more', 'disposed', 'suffer', 'while', 'evils', 'sufferable', 'than', 'right', 'themselves', 'abolishing', 'forms', 'which', 'they', 'accustomed', 'but', 'when', 'long', 'train', 'abuses', 'usurpations', 'pursuing', 'invariably', 'same', 'object', 'evinces', 'design', 'reduce', 'them', 'under', 'absolute', 'despotism', 'their', 'duty', 'throw', 'off', 'such', 'government', 'provide', 'new', 'guards', 'their', 'future', 'security', 'such', 'been', 'patient', 'sufferance', 'women', 'under', 'this', 'government', 'such', 'now', 'necessity', 'which', 'constrains', 'them', 'demand', 'equal', 'station', 'which', 'they', 'entitled', 'history', 'mankind', 'history', 'repeated', 'injuries', 'usurpations', 'part', 'man', 'toward', 'woman', 'having', 'direct', 'object', 'establishment', 'absolute', 'tyranny', 'over', 'her', 'prove', 'this', 'let', 'facts', 'submitted', 'candid', 'world', 'history', 'mankind', 'history', 'repeated', 'injuries', 'usurpations', 'part', 'man', 'toward', 'woman', 'having', 'direct', 'object', 'establishment', 'absolute', 'tyranny', 'over', 'her', 'prove', 'this', 'let', 'facts', 'submitted', 'candid', 'world', 'never', 'permitted', 'her', 'exercise', 'her', 'inalienable', 'right', 'elective', 'franchise', 'compelled', 'her', 'submit', 'laws', 'formation', 'which', 'she', 'had', 'no', 'voice', 'withheld', 'her', 'rights', 'which', 'given', 'most', 'ignorant', 'degraded', 'menboth', 'natives', 'foreigners', 'having', 'deprived', 'her', 'this', 'first', 'right', 'citizen', 'elective', 'franchise', 'thereby', 'leaving', 'her', 'without', 'representation', 'halls', 'legislation',
                'oppressed', 'her', 'all', 'sides', 'made', 'her', 'if', 'married', 'eye', 'law', 'civilly', 'dead', 'taken', 'her', 'all', 'right', 'property', 'even', 'wages', 'she', 'earns', 'made', 'her', 'morally', 'irresponsible', 'being', 'she', 'can', 'commit', 'many', 'crimes', 'impunity', 'provided', 'they', 'done', 'presence', 'her', 'husband', 'covenant', 'marriage', 'she', 'compelled', 'promise', 'obedience', 'her', 'husband', 'becoming', 'all', 'intents', 'purposes', 'her', 'masterthe', 'law', 'giving', 'him', 'power', 'deprive', 'her', 'her', 'liberty', 'administer', 'chastisement', 'so', 'framed', 'laws', 'divorce', 'what', 'shall', 'proper', 'causes', 'case', 'separation', 'whom', 'guardianship', 'children', 'shall', 'given', 'wholly', 'regardless', 'happiness', 'womenthe', 'law', 'all', 'cases', 'going', 'upon', 'false', 'supposition', 'supremacy', 'man', 'giving', 'all', 'power', 'into', 'his', 'hands', 'after', 'depriving', 'her', 'all', 'rights', 'married', 'woman', 'if', 'single', 'owner', 'property', 'taxed', 'her', 'support', 'government', 'which', 'recognizes', 'her', 'only', 'when', 'her', 'property', 'can', 'made', 'profitable', 'monopolized', 'nearly', 'all', 'profitable', 'employments', 'those', 'she', 'permitted', 'follow', 'she', 'receives', 'but', 'scanty', 'remuneration', 'closes', 'against', 'her', 'all', 'avenues', 'wealth', 'distinction', 'which', 'considers', 'most', 'honorable', 'himself', 'teacher', 'theology', 'medicine', 'or', 'law', 'she', 'not', 'known', 'denied', 'her', 'facilities', 'obtaining', 'thorough', 'education', 'all', 'colleges', 'being', 'closed', 'against', 'her', 'allows', 'her', 'church', 'well', 'state', 'but', 'subordinate', 'position', 'claiming', 'apostolic', 'authority', 'her', 'exclusion', 'ministry', 'some', 'exceptions', 'any', 'public', 'participation', 'affairs', 'church', 'created', 'false', 'public', 'sentiment', 'giving', 'world', 'different', 'code', 'morals', 'men', 'women', 'which', 'moral', 'delinquencies', 'which', 'exclude', 'women', 'society', 'not', 'only', 'tolerated', 'but', 'deemed', 'little', 'account', 'man', 'usurped', 'prerogative', 'jehovah', 'himself', 'claiming', 'his', 'right', 'assign', 'her', 'sphere', 'action', 'when', 'belongs', 'her', 'conscience', 'her', 'god', 'endeavored', 'every', 'way', 'could', 'destroy', 'her', 'confidence', 'her', 'own', 'powers', 'lessen', 'her', 'selfrespect', 'make', 'her', 'willing', 'lead', 'dependent', 'abject', 'life', 'now', 'view', 'this', 'entire', 'disfranchisement', 'onehalf', 'people', 'this', 'country', 'their', 'social', 'religious', 'degradationin', 'view', 'unjust', 'laws', 'above', 'mentioned', 'because', 'women', 'do', 'feel', 'themselves', 'aggrieved', 'oppressed', 'fraudulently', 'deprived', 'their', 'most', 'sacred', 'rights', 'we', 'insist', 'they', 'have', 'immediate', 'admission', 'all', 'rights', 'privileges', 'which', 'belong', 'them', 'citizens', 'united', 'states']


from collections import Counter
counts = Counter(seneca_falls)

print (counts)


def normalize_text(text):
    """
    Given a text, lowercases it, removes all punctuation, 
    and replaces all whitespace with normal spaces. Multiple whitespace will
    be compressed into a single space.
    """
    text = text.casefold()
    valid_chars = string.ascii_letters + string.whitespace + string.digits

    # Remove all punctuation
    new_text = ""
    for char in text:
        if char in valid_chars:
            new_text += char

    text = new_text
    text = text.replace("\n", " ")
    return text


def print_word_freq(filename):
    """Read in `filename` and print out the frequency of words in that file."""
    with open(filename) as file:
        text = file.read()

    text = normalize_text(text)
    words = []
    for word in text.split(" "):
        if word != '' and word not in STOP_WORDS:
            words.append(word)

    print(words)


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Get the word frequency in a text file.')
    parser.add_argument('file', help='file to read')
    args = parser.parse_args()

    file = Path(args.file)
    if file.is_file():
        print_word_freq(file)
    else:
        print(f"{file} does not exist!")
        exit(1)
