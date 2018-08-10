# Notes for the json format:

* Should remove the syllable fields and replace with:

~~~~
"syllable": {
    "codas": [1, 2, 3, 4],
    "onsets": [1, 2]
}
OR
"syllables": ["VC", "VCC", "CCV"]
~~~~

* Need to add all of the typology fields:

~~~~
{
  "morphological type": [
    "isolating",
    "analytic",
    "fusional",
    "agglutinating",
    "polysynthetic"
  ],
  "word formation": [
    "affixation",
    "suffixation",
    "prefixation",
    "infixation",
    "compounding",
    "root-and-pattern",
    "internal change",
    "suppleton",
    "stress or tone shift",
    "reduplication",
    "conversion",
    "purely isolating" # (None)
  ],
  "word formation frequency": "exclusively suffixing",
  "word order": "SVO" # (or "multiple" or "none")
  "headedness": "consistently head-initial"
  "agreement": "none" # or "ergative/absolutive" or "nominative/accusative" or "other"
  "case": "none" # or "ergative/absolutive" or "nominative/accusative" or "other"


~~~~

* Legal word formation frequencies are:
    [exclusively/mostly] [suffixing/prefixing/non-affixal/isolating]
    equal prefixing and suffixing
    equal affixation and other
