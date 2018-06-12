// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Initialize popovers
  phonemePopoverInit();
  reloadPopovers();
}

// Initialize all uninitialized phoneme selector popovers
function phonemePopoverInit() {
  $(".pbox-selector-uninit").attr("data-content", createPhonemeSelectorString());
  $(".pbox-selector-uninit").addClass("pbox-selector-init");
  $(".pbox-selector-uninit").removeClass("pbox-selector-uninit");
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

// On click function for element representing a label in the pbox.
// Save the state of the pbox inside the data-content, reload popover
// Update link text.
function handlePboxLabel(element) {
  var glyph = element.innerText;
  console.log("Button " + glyph + " clicked.");

  // Add the checked attribute to the box.
  $(element.for).attr("checked", "");

  // Update the link text to be a list of glyphs

  //         label  -->    td     -->     tr    --> tablebody --> table
  var table = element.parentElement.parentElement.parentElement.parentElement
  var div = table.parentElement;

  // Save the content changes in the popover attribute.
  var linkID = $("[aria-describedby]");
  linkID.attr("data-content", div.outerHTML);
  reloadPopovers();
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
// TODO use incrementing UIDs.
function createPhonemeSelectorString() {
  // NOTE Not compatible with older browsers!
  // BUG each label's IDs are not unique!!!
  var template = $("#pbox-template")[0];
  var uid = UID();
  template.id += "-" + uid;
  var str = template.outerHTML;

  // Add a UID to each id= and for= attribute
  // replace("pbox-template-X(X)", "pbox-template-X(X)-uid"

  template.id = "pbox-template";
  return str;
}

// Attach phoneme selector popovers to

// Write one function for each of the input types.
// ie create phonemeSelector
// ie create checkboxes for other traits???

// Reload popovers to ensure proper initialization.
function reloadPopovers() {
  // BUG? Need to hide and remove old popover
  //$("[data-toggle=popover]").popover("dispose");
  $("[data-toggle=popover]").popover();
}

// Convert num to base 36 (used for unique ID generation)
// Not strictly necessary but it makes everything look cooler.
function numToUID(num) {
  var b36str = num.toString(36);
  // Pad with 0 on left until 6 chars long.
  while (b36str.length < 6) {
    b36str = "0" + b36str;
  }
  return b36str;
}

// Generate and return a new UID guaranteed to be distinct from all
// previously generated UIDs created in this session.
function UID() {
  var uid = numToUID(UID_count);
  UID_count++;
  return uid;
}
