/* Automatically generated by selectors.py. DO NOT EDIT! */
var SELECTORS_DICT = {
    "agreement-selector": {
        "dict": {
            "ergative/absolutive": [],
            "nominative/accusative": [],
            "none": [
                "doesn't have",
                "none"
            ],
            "other": [
                "other",
                "some other",
                "other sort"
            ]
        },
        "html id": "agreement-selector",
        "mode": "pick one",
        "multi": false,
        "popover prefix": "a-lbox-popover",
        "reply": "have %s agreement",
        "reply vars": [
            "sel"
        ],
        "select name": "Agreement:",
        "select what": "agreement"
    },
    "case-selector": {
        "dict": {
            "ergative/absolutive": [],
            "nominative/accusative": [],
            "none": [
                "doesn't have",
                "none"
            ],
            "other": [
                "other",
                "some other",
                "other sort"
            ]
        },
        "html id": "case-selector",
        "mode": "pick one",
        "multi": false,
        "popover prefix": "c-lbox-popover",
        "reply": "have %s case",
        "reply vars": [
            "sel"
        ],
        "select name": "Case:",
        "select what": "case"
    },
    "complex-consonants-selector": {
        "bool body": "Complex Consonants",
        "dict": null,
        "html id": "complex-consonants-selector",
        "mode": "boolean",
        "multi": null,
        "popover prefix": null,
        "reply": "contain complex consonants",
        "reply vars": null,
        "select name": "Has complex consonants",
        "select what": null
    },
    "consonant-articulation-selector": {
        "dict": {
            "manners": [],
            "places": []
        },
        "html id": "consonant-articulation-selector",
        "mode": "pick multi",
        "multi": false,
        "popover prefix": "ca-lbox-popover",
        "reply": "contain %s %s %s of consonant articulation",
        "reply vars": [
            "mode",
            "k",
            "sel"
        ],
        "select name": "Has articulation features:",
        "select what": "articulation type"
    },
    "consonant-class-selector": {
        "dict": null,
        "html id": "consonant-class-selector",
        "mode": "pick class",
        "multi": null,
        "popover prefix": "ccbox-popover",
        "reply": "contain %s %s of %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Contains consonant class:",
        "select what": "natural classes"
    },
    "formation-freq-selector": {
        "dict": {
            "equal affixation and other": [
                "affixation and other"
            ],
            "equal prefixing and suffixing": [
                "prefixing and suffixing"
            ],
            "exclusively isolating": [
                "exclusively isolating",
                "purely isolating"
            ],
            "exclusively non-affixal": [],
            "exclusively prefixing": [],
            "exclusively suffixing": [],
            "mostly isolating": [],
            "mostly non-affixal": [],
            "mostly prefixing": [],
            "mostly suffixing": []
        },
        "html id": "formation-freq-selector",
        "mode": "pick one",
        "multi": false,
        "popover prefix": "ff-lbox-popover",
        "reply": "use %s strategies to form words",
        "reply vars": [
            "sel"
        ],
        "select name": "Word formation frequency:",
        "select what": "frequency"
    },
    "headedness-selector": {
        "dict": {
            "consistently head-final": [],
            "consistently head-initial": [],
            "mixed headedness": [],
            "mostly head-final": [],
            "mostly head-initial": []
        },
        "html id": "headedness-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "h-lbox-popover",
        "reply": "are %s %s of %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Headedness:",
        "select what": "headedness"
    },
    "ipa-consonant-selector": {
        "dict": null,
        "html id": "ipa-consonant-selector",
        "mode": "pick k ipa",
        "multi": null,
        "popover prefix": "ipacbox-popover",
        "reply": "contain %s %s of %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Contains consonant:",
        "select what": "consonants"
    },
    "ipa-vowel-selector": {
        "dict": null,
        "html id": "ipa-vowel-selector",
        "mode": "pick k ipa",
        "multi": null,
        "popover prefix": "ipavbox-popover",
        "reply": "contain %s %s of %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Contains vowel:",
        "select what": "vowels"
    },
    "metaclass-selector": {
        "dict": {
            "consonantal": [
                "b",
                "b\u02b0",
                "c",
                "c\u02b0",
                "d",
                "dz",
                "d\u0292",
                "d\u02b0",
                "f",
                "g",
                "g\u02b0",
                "k",
                "k\u02b0",
                "l",
                "m",
                "n",
                "p",
                "p\u02b0",
                "q",
                "q\u02b0",
                "r",
                "s",
                "t",
                "ts",
                "t\u0283",
                "t\u02b0",
                "v",
                "x",
                "z",
                "\u00e7",
                "\u00f0",
                "\u0127",
                "\u014b",
                "\u0234",
                "\u0256",
                "\u0256\u02b0",
                "\u025f",
                "\u025f\u02b0",
                "\u0262",
                "\u0262\u02b0",
                "\u0263",
                "\u026c",
                "\u026e",
                "\u0271",
                "\u0272",
                "\u0273",
                "\u0274",
                "\u0278",
                "\u0279",
                "\u027b",
                "\u027d",
                "\u027e",
                "\u0280",
                "\u0281",
                "\u0282",
                "\u0283",
                "\u0288",
                "\u0288\u02b0",
                "\u028b",
                "\u028e",
                "\u0290",
                "\u0292",
                "\u0295",
                "\u0299",
                "\u029d",
                "\u029f",
                "\u03b2",
                "\u03b8",
                "\u03c7",
                "\u2c71"
            ],
            "continuant": [
                "a",
                "e",
                "f",
                "h",
                "i",
                "j",
                "l",
                "o",
                "r",
                "s",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
                "\u00e6",
                "\u00e7",
                "\u00f0",
                "\u00f8",
                "\u0127",
                "\u0153",
                "\u0234",
                "\u0250",
                "\u0251",
                "\u0252",
                "\u0254",
                "\u0258",
                "\u0259",
                "\u025b",
                "\u025c",
                "\u025e",
                "\u0263",
                "\u0264",
                "\u0265",
                "\u0266",
                "\u0268",
                "\u026a",
                "\u026f",
                "\u0270",
                "\u0275",
                "\u0276",
                "\u0278",
                "\u0279",
                "\u027a",
                "\u027b",
                "\u027d",
                "\u027e",
                "\u0280",
                "\u0281",
                "\u0282",
                "\u0283",
                "\u0289",
                "\u028a",
                "\u028c",
                "\u028e",
                "\u028f",
                "\u0290",
                "\u0292",
                "\u0295",
                "\u029d",
                "\u029f",
                "\u03b2",
                "\u03b8",
                "\u03c7"
            ],
            "noncontinuant": [
                "b",
                "b\u02b0",
                "c",
                "c\u02b0",
                "d",
                "dz",
                "d\u0292",
                "d\u02b0",
                "g",
                "g\u02b0",
                "k",
                "k\u02b0",
                "m",
                "n",
                "p",
                "p\u02b0",
                "q",
                "q\u02b0",
                "t",
                "ts",
                "t\u0283",
                "t\u02b0",
                "\u014b",
                "\u0256",
                "\u0256\u02b0",
                "\u025f",
                "\u025f\u02b0",
                "\u0262",
                "\u0262\u02b0",
                "\u026c",
                "\u026e",
                "\u0271",
                "\u0272",
                "\u0273",
                "\u0274",
                "\u0288",
                "\u0288\u02b0",
                "\u028b",
                "\u0294",
                "\u0299",
                "\u2c71"
            ],
            "nonsyllabic": [
                "b",
                "b\u02b0",
                "c",
                "c\u02b0",
                "d",
                "dz",
                "d\u0292",
                "d\u02b0",
                "f",
                "g",
                "g\u02b0",
                "h",
                "j",
                "k",
                "k\u02b0",
                "p",
                "p\u02b0",
                "q",
                "q\u02b0",
                "s",
                "t",
                "ts",
                "t\u0283",
                "t\u02b0",
                "v",
                "w",
                "x",
                "z",
                "\u00e7",
                "\u00f0",
                "\u0127",
                "\u0256",
                "\u0256\u02b0",
                "\u025f",
                "\u025f\u02b0",
                "\u0262",
                "\u0262\u02b0",
                "\u0263",
                "\u0266",
                "\u026c",
                "\u026e",
                "\u0270",
                "\u0278",
                "\u0282",
                "\u0283",
                "\u0288",
                "\u0288\u02b0",
                "\u028b",
                "\u0290",
                "\u0292",
                "\u0294",
                "\u0295",
                "\u0299",
                "\u029d",
                "\u03b2",
                "\u03b8",
                "\u03c7",
                "\u2c71"
            ],
            "obstruents": [
                "b",
                "b\u02b0",
                "c",
                "c\u02b0",
                "d",
                "dz",
                "d\u0292",
                "d\u02b0",
                "f",
                "g",
                "g\u02b0",
                "h",
                "k",
                "k\u02b0",
                "p",
                "p\u02b0",
                "q",
                "q\u02b0",
                "s",
                "t",
                "ts",
                "t\u0283",
                "t\u02b0",
                "v",
                "x",
                "z",
                "\u00e7",
                "\u00f0",
                "\u0127",
                "\u0256",
                "\u0256\u02b0",
                "\u025f",
                "\u025f\u02b0",
                "\u0262",
                "\u0262\u02b0",
                "\u0263",
                "\u0266",
                "\u026c",
                "\u026e",
                "\u0278",
                "\u0282",
                "\u0283",
                "\u0288",
                "\u0288\u02b0",
                "\u028b",
                "\u0290",
                "\u0292",
                "\u0294",
                "\u0295",
                "\u0299",
                "\u029d",
                "\u03b2",
                "\u03b8",
                "\u03c7",
                "\u2c71"
            ],
            "sonorant": [
                "a",
                "e",
                "i",
                "j",
                "l",
                "m",
                "n",
                "o",
                "r",
                "u",
                "w",
                "y",
                "\u00e6",
                "\u00f8",
                "\u014b",
                "\u0153",
                "\u0234",
                "\u0250",
                "\u0251",
                "\u0252",
                "\u0254",
                "\u0258",
                "\u0259",
                "\u025b",
                "\u025c",
                "\u025e",
                "\u0264",
                "\u0265",
                "\u0268",
                "\u026a",
                "\u026f",
                "\u0270",
                "\u0271",
                "\u0272",
                "\u0273",
                "\u0274",
                "\u0275",
                "\u0276",
                "\u0279",
                "\u027a",
                "\u027b",
                "\u027d",
                "\u027e",
                "\u0280",
                "\u0281",
                "\u0289",
                "\u028a",
                "\u028c",
                "\u028e",
                "\u028f",
                "\u029f"
            ],
            "syllabic": [
                "a",
                "e",
                "i",
                "l",
                "m",
                "n",
                "o",
                "r",
                "u",
                "y",
                "\u00e6",
                "\u00f8",
                "\u014b",
                "\u0153",
                "\u0234",
                "\u0250",
                "\u0251",
                "\u0252",
                "\u0254",
                "\u0258",
                "\u0259",
                "\u025b",
                "\u025c",
                "\u025e",
                "\u0264",
                "\u0268",
                "\u026a",
                "\u026f",
                "\u0271",
                "\u0272",
                "\u0273",
                "\u0274",
                "\u0275",
                "\u0276",
                "\u0279",
                "\u027a",
                "\u027b",
                "\u027d",
                "\u027e",
                "\u0280",
                "\u0281",
                "\u0289",
                "\u028a",
                "\u028c",
                "\u028e",
                "\u028f",
                "\u029f"
            ],
            "vocalic": [
                "a",
                "e",
                "h",
                "i",
                "j",
                "o",
                "u",
                "w",
                "y",
                "\u00e6",
                "\u00f8",
                "\u0153",
                "\u0250",
                "\u0251",
                "\u0252",
                "\u0254",
                "\u0258",
                "\u0259",
                "\u025b",
                "\u025c",
                "\u025e",
                "\u0264",
                "\u0265",
                "\u0266",
                "\u0268",
                "\u026a",
                "\u026f",
                "\u0270",
                "\u0275",
                "\u0276",
                "\u0289",
                "\u028a",
                "\u028c",
                "\u028f",
                "\u0294"
            ],
            "voiced": [
                "a",
                "b",
                "b\u02b0",
                "d",
                "dz",
                "d\u0292",
                "d\u02b0",
                "e",
                "g",
                "g\u02b0",
                "i",
                "j",
                "l",
                "m",
                "n",
                "o",
                "r",
                "u",
                "v",
                "w",
                "y",
                "z",
                "\u00e6",
                "\u00f0",
                "\u00f8",
                "\u014b",
                "\u0153",
                "\u0234",
                "\u0250",
                "\u0251",
                "\u0252",
                "\u0254",
                "\u0256",
                "\u0256\u02b0",
                "\u0258",
                "\u0259",
                "\u0259",
                "\u025b",
                "\u025c",
                "\u025e",
                "\u025f",
                "\u025f\u02b0",
                "\u0262",
                "\u0262\u02b0",
                "\u0263",
                "\u0264",
                "\u0266",
                "\u0268",
                "\u026a",
                "\u026e",
                "\u026f",
                "\u0270",
                "\u0271",
                "\u0272",
                "\u0273",
                "\u0274",
                "\u0275",
                "\u0276",
                "\u0279",
                "\u027b",
                "\u027d",
                "\u027e",
                "\u0280",
                "\u0281",
                "\u0289",
                "\u028a",
                "\u028b",
                "\u028c",
                "\u028e",
                "\u028f",
                "\u0290",
                "\u0292",
                "\u0295",
                "\u0299",
                "\u029d",
                "\u029f",
                "\u03b2",
                "\u2c71"
            ],
            "voiceless": [
                "c",
                "c\u02b0",
                "f",
                "h",
                "k",
                "k\u02b0",
                "p",
                "p\u02b0",
                "q",
                "q\u02b0",
                "s",
                "t",
                "ts",
                "t\u0283",
                "t\u02b0",
                "x",
                "\u00e7",
                "\u0127",
                "\u026c",
                "\u0278",
                "\u0282",
                "\u0283",
                "\u0288",
                "\u0288\u02b0",
                "\u0294",
                "\u03b8",
                "\u03c7"
            ]
        },
        "html id": "metaclass-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "mc-lbox-popover",
        "reply": "have %s %s phoneme that is %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Contains metaclass:",
        "select what": "metaclasses"
    },
    "morphological-selector": {
        "dict": {
            "agglutinating": [],
            "analytic": [
                "analytic",
                "not isolating"
            ],
            "fusional": [],
            "isolating": [],
            "polysynthetic": []
        },
        "html id": "morphological-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "m-lbox-popover",
        "reply": "use %s %s of the morphological types %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Morphological type:",
        "select what": "morphological type"
    },
    "placeholder-selector": {
        "bool body": "Select a trait from the dropdown menu to start submitting queries!",
        "html id": "placeholder-selector",
        "mode": "no query",
        "select name": "Select trait..."
    },
    "stress-selector": {
        "bool body": "Predictable Stress",
        "dict": null,
        "html id": "stress-selector",
        "mode": "boolean",
        "multi": null,
        "popover prefix": null,
        "reply": "have stress",
        "reply vars": null,
        "select name": "Has stress",
        "select what": null
    },
    "syllable-selector": {
        "dict": {
            "C coda": [
                "CVC",
                "VC"
            ],
            "C onset": [
                "CV"
            ],
            "CC coda": [
                "VCC"
            ],
            "CC onset": [
                "CCV"
            ],
            "CCC coda": [
                "VCCC"
            ],
            "CCC onset": [
                "CCCV"
            ],
            "CCCC coda": [
                "VCCCC"
            ],
            "CCCC onset": [
                "CCCCV"
            ],
            "V": [
                "V"
            ]
        },
        "html id": "syllable-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "s-lbox-popover",
        "reply": "use %s %s of the syllable structures %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Allows syllable structure:",
        "select what": "syllables"
    },
    "tone-selector": {
        "bool body": "Tone (Including \"Pitch Accent\")",
        "dict": null,
        "html id": "tone-selector",
        "mode": "boolean",
        "multi": null,
        "popover prefix": null,
        "reply": "have tone",
        "reply vars": null,
        "select name": "Has tone",
        "select what": null
    },
    "vowel-class-selector": {
        "dict": null,
        "html id": "vowel-class-selector",
        "mode": "pick class",
        "multi": null,
        "popover prefix": "vcbox-popover",
        "reply": "contain %s %s of %s",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Contains vowel class:",
        "select what": "natural classes"
    },
    "word-formation-selector": {
        "dict": {
            "affixation": [
                "affixation",
                "prefixation or suffixation"
            ],
            "compounding": [],
            "conversion": [],
            "infixation": [],
            "internal change": [],
            "prefixation": [],
            "purely isolating": [
                "none",
                "purely isolating"
            ],
            "reduplication": [],
            "root-and-pattern": [],
            "stress or tone shift": [],
            "suffixation": [],
            "suppleton": []
        },
        "html id": "word-formation-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "wf-lbox-popover",
        "reply": "use %s %s of %s to form words",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Word formation strategy:",
        "select what": "word formation"
    },
    "word-order-selector": {
        "dict": {
            "OSV": [],
            "OVS": [],
            "SOV": [],
            "SVO": [],
            "VOS": [],
            "VSO": [],
            "free": [
                "no basic",
                "none",
                "free"
            ]
        },
        "html id": "word-order-selector",
        "mode": "pick multi",
        "multi": true,
        "popover prefix": "wo-lbox-popover",
        "reply": "have %s %s of %s word orders",
        "reply vars": [
            "mode",
            "k",
            "selList"
        ],
        "select name": "Basic word order:",
        "select what": "word order"
    }
};
