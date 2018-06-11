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

// Add the display: none style to the given DOM element
function hideElement(element) {
  element.classList.add("hidden");
}

// Remove the display: none style to the given DOM element
function unhideElement(element) {
  element.classList.remove("hidden");
}

// Create and return a new phoneme list DOM element
function createPhonemeList() {
  // Create a phoneme input box (an input element)

  // Create a + button to add another phoneme box
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
