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
        "mode": "pick k",
        "multi": false,
        "popover prefix": "ca-lbox-popover",
        "reply": "contain %s %s %s of consonant articulation",
        "reply vars": [
            "mode",
            "k",
            "selList"
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
        "reply": "use %s to form words",
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
                "p",
                "b",
                "t",
                "d",
                "\u0288",
                "\u0256",
                "c",
                "\u025f",
                "k",
                "g",
                "q",
                "\u0262",
                "p\u02b0",
                "b\u02b0",
                "t\u02b0",
                "d\u02b0",
                "\u0288\u02b0",
                "\u0256\u02b0",
                "c\u02b0",
                "\u025f\u02b0",
                "k\u02b0",
                "g\u02b0",
                "q\u02b0",
                "\u0262\u02b0",
                "m",
                "\u0271",
                "n",
                "\u0273",
                "\u0272",
                "\u014b",
                "\u0274",
                "\u0299",
                "r",
                "\u0280",
                "\u2c71",
                "\u027e",
                "\u027d",
                "\u0278",
                "\u03b2",
                "f",
                "v",
                "\u03b8",
                "\u00f0",
                "s",
                "z",
                "\u0283",
                "\u0292",
                "\u0282",
                "\u0290",
                "\u00e7",
                "\u029d",
                "x",
                "\u0263",
                "\u03c7",
                "\u0281",
                "\u0127",
                "\u0295",
                "ts",
                "dz",
                "t\u0283",
                "d\u0292",
                "\u026c",
                "\u026e",
                "\u028b",
                "\u0279",
                "\u027b",
                "l",
                "\u0234",
                "\u028e",
                "\u029f"
            ],
            "continuant": [
                "\u0258",
                "r",
                "\u0280",
                "s",
                "\u0278",
                "e",
                "\u00f8",
                "\u03c7",
                "\u0275",
                "\u028e",
                "\u028f",
                "\u00e7",
                "\u025e",
                "\u0250",
                "\u0234",
                "\u0281",
                "\u0127",
                "\u0264",
                "\u029d",
                "f",
                "\u028a",
                "\u0259",
                "\u0268",
                "\u027e",
                "\u0290",
                "\u027a",
                "x",
                "v",
                "z",
                "w",
                "\u0295",
                "\u03b8",
                "\u0292",
                "i",
                "\u0276",
                "\u027b",
                "j",
                "u",
                "\u0254",
                "\u0270",
                "\u025c",
                "l",
                "\u0279",
                "\u028c",
                "\u0263",
                "\u0282",
                "\u03b2",
                "\u025b",
                "\u026f",
                "o",
                "\u0252",
                "\u00e6",
                "\u029f",
                "\u00f0",
                "\u0153",
                "a",
                "h",
                "\u0251",
                "\u0283",
                "\u0266",
                "\u0289",
                "\u026a",
                "y",
                "\u027d",
                "\u0265"
            ],
            "noncontinuant": [
                "p",
                "b",
                "t",
                "d",
                "\u0288",
                "\u0256",
                "c",
                "\u025f",
                "k",
                "g",
                "q",
                "\u0262",
                "\u0294",
                "p\u02b0",
                "b\u02b0",
                "t\u02b0",
                "d\u02b0",
                "\u0288\u02b0",
                "\u0256\u02b0",
                "c\u02b0",
                "\u025f\u02b0",
                "k\u02b0",
                "g\u02b0",
                "q\u02b0",
                "\u0262\u02b0",
                "m",
                "\u0271",
                "n",
                "\u0273",
                "\u0272",
                "\u014b",
                "\u0274",
                "\u0299",
                "\u2c71",
                "ts",
                "dz",
                "t\u0283",
                "d\u0292",
                "\u026c",
                "\u026e",
                "\u028b"
            ],
            "nonsyllabic": [
                "p",
                "b",
                "t",
                "d",
                "\u0288",
                "\u0256",
                "c",
                "\u025f",
                "k",
                "g",
                "q",
                "\u0262",
                "\u0294",
                "p\u02b0",
                "b\u02b0",
                "t\u02b0",
                "d\u02b0",
                "\u0288\u02b0",
                "\u0256\u02b0",
                "c\u02b0",
                "\u025f\u02b0",
                "k\u02b0",
                "g\u02b0",
                "q\u02b0",
                "\u0262\u02b0",
                "\u0299",
                "\u2c71",
                "\u0278",
                "\u03b2",
                "f",
                "v",
                "\u03b8",
                "\u00f0",
                "s",
                "z",
                "\u0283",
                "\u0292",
                "\u0282",
                "\u0290",
                "\u00e7",
                "\u029d",
                "x",
                "\u0263",
                "\u03c7",
                "\u0127",
                "\u0295",
                "h",
                "\u0266",
                "ts",
                "dz",
                "t\u0283",
                "d\u0292",
                "\u026c",
                "\u026e",
                "\u028b",
                "j",
                "\u0270",
                "w"
            ],
            "obstruents": [
                "p",
                "b",
                "t",
                "d",
                "\u0288",
                "\u0256",
                "c",
                "\u025f",
                "k",
                "g",
                "q",
                "\u0262",
                "\u0294",
                "p\u02b0",
                "b\u02b0",
                "t\u02b0",
                "d\u02b0",
                "\u0288\u02b0",
                "\u0256\u02b0",
                "c\u02b0",
                "\u025f\u02b0",
                "k\u02b0",
                "g\u02b0",
                "q\u02b0",
                "\u0262\u02b0",
                "\u0299",
                "\u2c71",
                "\u0278",
                "\u03b2",
                "f",
                "v",
                "\u03b8",
                "\u00f0",
                "s",
                "z",
                "\u0283",
                "\u0292",
                "\u0282",
                "\u0290",
                "\u00e7",
                "\u029d",
                "x",
                "\u0263",
                "\u03c7",
                "\u0127",
                "\u0295",
                "h",
                "\u0266",
                "ts",
                "dz",
                "t\u0283",
                "d\u0292",
                "\u026c",
                "\u026e",
                "\u028b"
            ],
            "sonorant": [
                "\u0258",
                "r",
                "\u0280",
                "e",
                "\u028e",
                "\u00f8",
                "\u0275",
                "\u028f",
                "\u025e",
                "\u0250",
                "\u0234",
                "\u0271",
                "\u0281",
                "\u0264",
                "\u028a",
                "\u0259",
                "\u0268",
                "\u027e",
                "\u027a",
                "\u0272",
                "w",
                "i",
                "\u0274",
                "\u0276",
                "j",
                "\u027b",
                "u",
                "\u0254",
                "\u0270",
                "\u025c",
                "l",
                "\u0279",
                "\u014b",
                "\u028c",
                "n",
                "\u026f",
                "\u0252",
                "\u025b",
                "o",
                "\u00e6",
                "\u029f",
                "m",
                "\u0273",
                "\u0153",
                "a",
                "\u0251",
                "\u0289",
                "\u026a",
                "y",
                "\u027d",
                "\u0265"
            ],
            "syllabic": [
                "\u0258",
                "r",
                "\u0280",
                "e",
                "\u028e",
                "\u00f8",
                "\u0275",
                "\u028f",
                "\u025e",
                "\u0250",
                "\u0234",
                "\u0271",
                "\u0281",
                "\u0264",
                "\u028a",
                "\u0259",
                "\u0268",
                "\u027e",
                "\u027a",
                "\u0272",
                "i",
                "\u0274",
                "\u0276",
                "\u027b",
                "u",
                "\u0254",
                "\u025c",
                "l",
                "\u0279",
                "\u014b",
                "\u028c",
                "n",
                "\u026f",
                "\u0252",
                "\u025b",
                "o",
                "\u00e6",
                "\u029f",
                "m",
                "\u0273",
                "\u0153",
                "a",
                "\u0251",
                "\u0289",
                "\u026a",
                "y",
                "\u027d"
            ],
            "vocalic": [
                "\u0258",
                "e",
                "\u00f8",
                "\u0275",
                "\u028f",
                "\u0294",
                "\u025e",
                "\u0250",
                "\u0264",
                "\u028a",
                "\u0259",
                "\u0268",
                "w",
                "i",
                "\u0276",
                "j",
                "u",
                "\u0254",
                "\u0270",
                "\u025c",
                "\u028c",
                "\u026f",
                "\u0252",
                "\u025b",
                "o",
                "\u00e6",
                "\u0153",
                "a",
                "h",
                "\u0251",
                "\u0289",
                "\u0266",
                "\u026a",
                "y",
                "\u0265"
            ],
            "voiced": [
                "b",
                "d",
                "\u0256",
                "\u025f",
                "g",
                "\u0262",
                "b\u02b0",
                "d\u02b0",
                "\u0256\u02b0",
                "\u025f\u02b0",
                "g\u02b0",
                "\u0262\u02b0",
                "m",
                "\u0271",
                "n",
                "\u0273",
                "\u0272",
                "\u014b",
                "\u0274",
                "\u0299",
                "r",
                "\u0280",
                "\u2c71",
                "\u027e",
                "\u027d",
                "\u03b2",
                "v",
                "\u00f0",
                "z",
                "\u0292",
                "\u0290",
                "\u029d",
                "\u0263",
                "\u0281",
                "\u0295",
                "\u0266",
                "dz",
                "d\u0292",
                "\u026e",
                "\u028b",
                "\u0279",
                "\u027b",
                "j",
                "\u0270",
                "l",
                "\u0234",
                "\u028e",
                "\u029f",
                "w",
                "i",
                "y",
                "e",
                "\u00f8",
                "\u025b",
                "\u0153",
                "a",
                "\u0276",
                "\u0268",
                "\u0289",
                "\u0258",
                "\u0275",
                "\u0259",
                "\u0259",
                "\u025c",
                "\u025e",
                "\u026f",
                "u",
                "\u0264",
                "o",
                "\u028c",
                "\u0254",
                "\u0251",
                "\u0252",
                "\u026a",
                "\u028f",
                "\u00e6",
                "\u0250",
                "\u028a"
            ],
            "voiceless": [
                "p",
                "t",
                "\u0288",
                "c",
                "k",
                "q",
                "\u0294",
                "p\u02b0",
                "t\u02b0",
                "\u0288\u02b0",
                "c\u02b0",
                "k\u02b0",
                "q\u02b0",
                "\u0278",
                "f",
                "\u03b8",
                "s",
                "\u0283",
                "\u0282",
                "\u00e7",
                "x",
                "\u03c7",
                "\u0127",
                "h",
                "ts",
                "t\u0283",
                "\u026c"
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
            "sel"
        ],
        "select name": "Basic word order:",
        "select what": "word order"
    }
};
