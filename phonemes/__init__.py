from . import consonants, vowels, metaclasses


def isPhoneme(s):
    """Returns True iff s is a phoneme represented in this system"""
    return consonants.isConsonant(s) or vowels.isVowel(s)
