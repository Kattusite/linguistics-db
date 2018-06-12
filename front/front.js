// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Initialize popovers
  reloadPopovers();
}

// On click handler for single trait button
// Hides second trait div
function handleSingleTrait() {
  console.log("single clicked");
  hideElement($("#trait-div-2")[0]);
}

// On click handler for double trait button
// Displays second trait div
function handleDoubleTrait() {
  console.log("double clicked");
  unhideElement($("#trait-div-2")[0]);
}

// On click handler for select phonemes
function handleSelectPhonemes() {
   // Possibly use the selector attribute of popovers to initialize them here
   var domStr =`

   `;

   this.setAttribute("data-content", domStr);
}

// Phoneme List functions
var PHONEME_GLYPHS = {
  "n":"n",
  "t":"t",
  "m":"m",
  "k":"k",
  "j":"j",
  "s":"s",
  "p":"p",
  "l":"l",
  "w":"w",
  "h":"h",
  "b":"b",
  "d":"d",
  "g":"g",
  "engma":"ŋ",
  "esh":"ʃ",
  "glottal stop":"ʔ",
  "voiceless postalveolar affricate":"tʃ",
  "f":"f",
  "r":"r",
  "palatal nasal":"ɲ",
  "z":"z",
  "voiceless alveolar affricate":"ts",
  "voiced postalveolar affricate":"dʒ",
  "x":"x",
  "v":"v",
}

// Given a string identifying a phoneme, get the glyph for that phoneme. 
function getGlyph(phoneme) {
  if (!phoneme in PHONEME_GLYPHS) {
    console.err("Phoneme " + phoneme + " has no associated glyph.");
  }
  return PHONEME_GLYPHS[phoneme];
}


// Add the display: none style to the given DOM element
function hideElement(element) {
  element.classList.add("hidden");
}

// Remove the display: none style to the given DOM element
function unhideElement(element) {
  element.classList.remove("hidden");
}

// Create and return a new phoneme selector DOM element as a string
function createPhonemeSelectorString() {

}

// Create a popup in which users can click the phoneme to select/unselect it
// using bootstrap!


// Write one function for each of the input types.

// ie create phonemeSelector

// ie create checkboxes for other traits???

// Reload popovers to ensure proper initialization.
function reloadPopovers() {
  // Hide and remove old popover
  //$("[data-toggle=popover]").popover("dispose");

  // Add new one
  $("[data-toggle=popover]").popover();
}
