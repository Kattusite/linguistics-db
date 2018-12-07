import json, const

# ref. https://en.wikipedia.org/wiki/Distinctive_feature
# ref. https://gawron.sdsu.edu/intro/course_core/lectures/phonology.htm

METACLASSES = {

    const.DICT: {
        "complex consonant": COMPLEX_CONSONANTS,
        "stridents": STRIDENTS,
        "sibilant": SIBILANTS,

        "labial": LABIALS,

        "voiced": VOICED,
        "unvoiced": UNVOICED,

        "sonorant": SONORANTS,
        "obstruents": OBSTRUENTS,

        "consonantal": CONSONANTALS,
        "vocalic": VOCALIC,

        "syllabic": SYLLABIC,
        "nonsyllabic": NONSYLLABIC,

        "continuant": CONTINUANT,
        "noncontinuant": NONCONTINUANT,
    },
    const.MULTI: True
}
