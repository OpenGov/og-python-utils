import re

def chain_sub_regexes(phrase, *regex_sub_pairs):
    '''
    Allow for a series of regex substitutions to occur

    chain_sub_regexes('test ok', (' ', '_'), ('k$', 'oo'))
    # => 'test_ooo'
    '''
    for regex, substitution in regex_sub_pairs:
        if isinstance(regex, basestring):
            regex = re.compile(regex)
        phrase = regex.sub(substitution, phrase)
    return phrase
