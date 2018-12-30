/*****************************************************************************/
/*                               Global Variables                            */
/*****************************************************************************/

var CONSONANT_ID            = "consonant-selector";
var CONSONANT_CLASS_ID      = "consonant-class-selector";
var VOWEL_ID                = "vowel-selector";
var VOWEL_CLASS_ID          = "vowel-class-selector";
var CONSONANT_PLACES_ID     = "consonant-places";
var CONSONANT_MANNERS_ID    = "consonant-manners";
var COMPLEX_CONSONANT_ID    = "complex-consonants";
var TONE_ID                 = "tone-selector";
var STRESS_ID               = "stress-selector";
var SYLLABLE_ID             = "syllable-selector";
var MORPHOLOGY_ID           = "morphological-selector";
var WORD_FORMATION_ID       = "word-formation-selector";
var FORMATION_FREQ_ID       = "formation-freq-selector";
var WORD_ORDER_ID           = "word-order-selector";
var HEADEDNESS_ID           = "headedness-selector";
var AGREEMENT_ID            = "agreement-selector";
var CASE_ID                 = "case-selector";
var IPA_CONSONANT_ID        = "ipa-consonant-selector";
var IPA_VOWEL_ID            = "ipa-vowel-selector";

// Should we list all members of the matching language set?
// Changed by handleListToggle
var listMode = false;

// TODO Declare constants for class names here (e.g. .vbox-template)

// TODO make these local to the one function that uses them to keep namespace
// relatively clean.
var VOICING = 0;
var PLACE   = 1;
var MANNER  = 2;

/*****************************************************************************/
/*                                Initializers                               */
/*****************************************************************************/
// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Update the document with trait selectors from template
  traitSelectorInit();

  // Initialize popovers (consonant, vowel, consonant classes, vowel classes)
  // Plus all of the list-based popovers
  initPopovers("cbox-selector",     "#cbox-template");
  initPopovers("vbox-selector",     "#vbox-template");
  initPopovers("ccbox-selector",    "#ccbox-template");
  initPopovers("vcbox-selector",    "#vcbox-template");
  initPopovers("m-lbox-selector",   "#morphology-template");
  initPopovers("wf-lbox-selector",  "#word-formation-template");
  initPopovers("ff-lbox-selector",  "#formation-freq-template");
  initPopovers("wo-lbox-selector",  "#word-order-template");
  initPopovers("h-lbox-selector",   "#headedness-template");
  initPopovers("a-lbox-selector",   "#agreement-template");
  initPopovers("c-lbox-selector",   "#case-template");
  initPopovers("s-lbox-selector",   "#syllable-template")
  // initPopovers("ipacbox-selector",  "#ipacbox-template");

  // Replace IPA chart placeholders with actual copies of the IPA chart.
  initIPAChart("ipac-selector", "#ipacbox-template");

  reloadPopovers();
  reloadTooltips();
}

// Initialize trait selector divs by replacing the placeholder trait selectors
// with a clone of the template. Hide all but the first of these traitSelectors.
function traitSelectorInit() {
  // Clone the template and remove its ID to ensure no duplicates
  var $template = $("#trait-div-template").clone();
  $template.removeAttr("id");

  // Strip template class from the cloned template & its children
  $template.removeClass("template");
  $template.children().removeClass("template");

  // Replace all placeholders with templates, hiding all but the first.
  $template.addClass("hidden");
  $("#trait-divs").children().replaceWith($template);
  $("#trait-divs").children().eq(0).removeClass("hidden");
}

/* Target all uninitialized popovers of class tgtClass.
 * Create each of these a unique popover with content determined copied from the
 * template located by the jquery string template
 * For instance initPopover("dummy-class") will replace all ".dummy-class-uninit"
 * with ".dummy-class-init", and update the data-content with the return value
 * of createSelectorString(templateID).
 */
 // TODO the first two UID lines are basically useless right now as the UID is mishandled
 // Try using jQuery.each() for "more correct" iteration
 // The current way leads to a minor BUG in which popover UIDs mismatch enclosing div UIDs
function initPopovers(tgtClass, templateID) {
  var uninit = tgtClass + "-uninit";  // e.g. ".cbox-selector-uninit"
  var init   = tgtClass + "-init";    // e.g. ".cbox-selector-init"

  var str = createSelectorString(templateID);
  var uid = str.match(/template-[0-9a-fA-F]+/g)[0].replace(/template-/g,"");
  $("." + uninit).attr("data-content", createSelectorString(templateID));
  $("." + uninit).attr("id", tgtClass + "-" + uid);
  $("." + uninit).addClass(init);
  $("." + uninit).addClass("selector-init");
  $("." + uninit).removeClass(uninit);
}

/* Given the base name of a tgt class, initialize all uninitialized members of that
 * class by copying the contents of the element specified by the selector template. */
 function initIPAChart(tgtClass, template) {
   var uninit = tgtClass + "-uninit";
   var init   = tgtClass + "-init";

   var $template = $(template).clone();
   $template.addClass(init);
   $template.removeClass("template");
   $template.removeAttr("id");

   var $uninit = $(`.${uninit}`);
   $uninit.replaceWith($template);
 }


/*****************************************************************************/
/*                                Event Handlers                             */
/*****************************************************************************/

// On click handler for single trait button
// Hides second trait div
function handleSingleTrait() {
  console.log("single clicked");
  hideElement($("#trait-divs").children()[1]);
}

// On click handler for double trait button
// Displays second trait div
function handleDoubleTrait() {
  console.log("double clicked");
  unhideElement($("#trait-divs").children()[1]);
}

// On change handler for selecting a trait from dropdown.
// Element represents the <select> element that was changed
function handleTraitSelect(element) {
  // Get the index of the trait div to be displayed (+1 to skip <select> itself)
  var index = element.selectedIndex + 1;
  var $selElement = $(element).parent().children().eq(index);

  // Activate selected element and deactivate others.
  $(element).siblings("div").addClass("inactive");
  $(element).siblings("div").removeClass("active");
  $selElement.removeClass("inactive");
  $selElement.addClass("active");
}

// On click function for element representing a label in the pbox.
// Save the state of the pbox inside the data-content, reload popover
// Update link text.
function handlePboxLabel(element) {
  var $el = $(element);
  var $table = $el.closest("table");
  var $popoverDiv = $table.parent();

  // (Un)select the pbox label.
  toggleClass(element, "selected");

  // Save the state of the popover for the next time it is opened.
  var popoverContent = $popoverDiv[0].outerHTML;
  var $popoverButton = $("[aria-describedby]");
  var $traitDiv = $popoverButton.closest("div");
  $popoverButton.attr("data-content", popoverContent);

  // Find all selected pbox labels and create a list of their glyphs
  var selList = [];
  var $sel = $table.find(".pbox-label.selected");
  $sel.each(function() { selList.push($(this).text()); });

  // Store the query info to be sent to the server
  $traitDiv.attr("selList", selList);

  // Update the popoverButton text to be glyph list, or placeholder if empty.
  // NOTE [aria-describedby] fails if multiple popovers are open concurrently.
  var isValid = selList.length > 0;
  var lbl = "Select phonemes...";
  if (isValid) {
    lbl = selList.join(", ");
  }
  $popoverButton.text(lbl);
}

/* On click handler for the natural class selector. On a click, deselect the
 * currently selected element of this type, and select this one instead.
 * Update the associated link text for the popover. */
 /* This function assumes that at no point will more or less than one natural
  * class of each type be selected. */
function handleClboxLabel(element) {
  var $el = $(element);
  var $table = $el.closest("table");
  var $popoverDiv = $table.parent();

  // Figure the type (column) of element clicked (e.g. voicing, place, manner)
  var type = $el.attr("type");

  // If element was already selected, deselect it; select "Any..." instead
  // Note: assumes "Any..." is the first entry in table with the same type
  var isSel = $(element).hasClass("selected");
  if (isSel) {
    $el.removeClass("selected");
    $table.find(`[type=${type}]`).eq(0).addClass("selected");
  }
  // If element was not selected, deselect all others of its type & select this instead
  else {
    $table.find(`[type=${type}]`).removeClass("selected");
    $el.addClass("selected");
  }

  // Save the state of the popover for the next time it is opened
  var $popoverButton = $("[aria-describedby]");
  var $traitDiv = $popoverButton.closest("div");
  var popoverContent = $popoverDiv[0].outerHTML;
  $popoverButton.attr("data-content", popoverContent);

  // Get the fields needed for server queries, and store the query info for later
  var selList = [];
  var $sel = $table.find(".selected");
  $sel.each(function() { selList.push($(this).text()); });
  $traitDiv.attr("selList", selList);

  // After initial click any query is valid
  // link.attr("isValid", true);

  // Figure out if we want consonants or vowels
  var ctype = $table.hasClass("consonant-class-selector") ? "consonant" : "vowel";

  // Update the popoverButton text to reflect new selections
  $popoverButton.text(getStrFromClasses(selList, ctype));
}

// Handle clicks on an Lbox element. Select the clicked on box.
// If multiple selections are prohibited, deselect all other boxes.
// mutli = true ==> multiple selections allowed
function handleLboxLabel(element, multi) {
  // Find the containing table.
  var $el = $(element);
  var $table = $el.closest("table");
  var $popoverDiv = $table.closest("div");

  // (Un)select the lbox label that was clicked.
  if ($el.hasClass("selected")) {
    $el.removeClass("selected");
  }
  else {
    // If multiple selections disallowed, deselect all other labels in table
    if (!multi) {
      $table.find(".lbox-label").removeClass("selected");
    }
    $el.addClass("selected");
  }

  // Store the popover contents for the next time it is opened
  var $popoverButton = $("[aria-describedby]");
  var $traitDiv = $popoverButton.closest("div");
  var popoverContent = $popoverDiv[0].outerHTML;
  $popoverButton.attr("data-content", popoverContent);

  // Collect all selected elements from the table into a list
  var selList = [];
  var $sel = $table.find(".selected");
  $sel.each(function() { selList.push($(this).text()); });

  // Store the info needed to make a query to the server.
  $traitDiv.attr("selList", selList);

  // Update the link text to be the sel list, or placeholder if empty.
  var lbl = "Select trait...";
  var isValid = selList.length > 0;
  if (isValid) lbl = selList.join(", ");
  $popoverButton.text(lbl);
}

// Toggle a single element's class -- i.e. if element already has class, remove
// it, and if element lacks class, add it
function toggleClass(el, cls) {
  if ($(el).hasClass(cls)) {
    $(el).removeClass(cls);
  } else {
    $(el).addClass(cls);
  }
}

// Toggle all classes together
// If el already has class cls, remove cls from el and all elements in els
// Else, add cls to el and all elements in els
function toggleClassesAll(el, els, cls) {
  if ($(el).hasClass(cls)) {
    $(el).removeClass(cls);
    for (var i = 0; i < els.length; i++) {
      $(els[i]).removeClass(cls);
    }
  } else {
    $(el).addClass(cls);
    for (var i = 0; i < els.length; i++) {
      $(els[i]).addClass(cls);
    }
  }
}

// Toggle each class individually
// If el already has class cls, remove cls from el. Else, add cls to el.
// Do this same procedure separately for each element in els
function toggleClassesEach(el, els, cls) {
  toggleClass(el, cls);
  for (var i = 0; i < els.length; i++) {
    toggleClass(els[0], cls);
  }
}

// Unset all unselected classes
// This one is supposed to model intersectivity.
// I think it's going to be too much of a PITA
function toggleClassesOthers () {
}

// Given an IPA Header el, return an array of all the
// elements falling under that header in that table.
function getElementsOfHeader(el) {
  var $el = $(el);
  var $table = $el.closest("table");
  var category = $el.attr("category");
  var trait    = $el.attr("trait");

  var matches = $table.find(`[${category}='${trait}']`);

  // If in "other" row, search for special class instead of an attr
  if (trait == "other") {
    matches = $table.find(".ipa-box.other");
  }

  return matches;
}



// Click handler for ipa consonant box labels
function handleIpacboxLabel(element) {
  // Get the enclosing table.
  var $el = $(element);
  var $table = $el.closest("table");
  var $traitDiv = $table.parent().parent();

  // Toggle the clicked element.
  // If clicked element was a header, toggle all matching elements.
  if ($el.hasClass("ipa-header")) {

    // Get a list of the phonemes matching this header
    var matches = getElementsOfHeader(element);

    // Select or unselect ALL the elements in the list as a group.
    // Afterwards, either ALL matching phonemes are selected, or ALL are not.
    toggleClassesAll(element, matches.toArray(), "selected");

  }
  // Else, toggle just that element
  // Decide selecting this element causes a header category to be (un)selected
  else {
    // Carry out the toggle.
    toggleClass(element, "selected");

  }

  // Check if the toggle caused any headers to (no longer) be selected
  var headers = $table.find(".ipa-header").toArray();
  for (var i = 0; i < headers.length; i++) {
    var matches = getElementsOfHeader(headers[i]);

    // Find out how many matches are not selected.
    var nonselected = $(matches).not(".selected").length;

    // If all elements are selected, highlight the header.
    if (nonselected == 0) {
      $(headers[i]).addClass("selected");
    }
    // If some elements are unselected, de-highlight the header.
    else {
      $(headers[i]).removeClass("selected");
    }
  }

  // Save the contents of the table in a string so the popover will be updated
  /*
  var div = table.parentElement;
  var outerHTML = div.outerHTML;

  var link = $("[aria-describedby]");
  */

  // Find all selected glyphs in the table.
  var selList = [];
  $table.find(".ipa-box.selected").each(function() {
      selList.push($(this).text());
    }
  )
  var isValid = selList.length > 0;

  // Update the link text to be the sel list, or placeholder if empty
  /*
  var lbl = "";
  if (selList.length == 0) {
    lbl = "Select trait..."
  }
  else {
    lbl = selList.join(", ");
  }
  link.text(lbl);
  */

  // Inform the table of its query for the server, as a list of glyphs
  $traitDiv.attr("selList", selList);
  $traitDiv.attr("isValid", isValid);

  // Save the content changes in the popover attribute.
  // link.attr("data-content", outerHTML);

}

// Submission handler to send AJAX requests to server
// TODO Document the fields of the submission
// TODO Make sure the query is valid (i.e. at least 1 phoneme selected, a syllable was entered)

// Extract the information from each of the active trait divs, and send a POST
// containing a list of requests as the payload
function handleSubmit() {
  var requests = [];
  var $traits = getActiveTraits();
  for (var i = 0; i < $traits.length; i++) {
    var $t = $traits.eq(i);
    var requestParams = {};

    // Get the list of selected elements from the "selList" attr string
    var selList = $t.attr("selList");
    var prettySelList = "prettySelList";
    if (selList) {
      selList = selList.split(",");
      prettySelList = selList.join(", ");
    }

    // If selList has size 1, additionally set sel to selList[0]
    var sel = "sel";
    if (selList && selList.length == 1)
      sel = selList[0];

    // Get the values of k & mode
    var k       = $t.find(".k-selector").val();
    var modeStr = $t.find(".mode-selector").val();
    var mode    = getModeFromStr(modeStr);

    var trait = $t.attr("type");

    // Pick most commonly used values as defaults
    var reply = `contain ${modeStr} ${k} of ${prettySelList}`;

    // Generate the correct reply string based on the trait type
    // Some cases have special other info that must be calculated (ie for natural class arrays)
    switch (trait) {
      case CONSONANT_ID:
      case VOWEL_ID:
      case IPA_CONSONANT_ID:
      case IPA_VOWEL_ID:
        reply = `contain ${modeStr} ${k} of ${prettySelList}`;
        break;
      case CONSONANT_CLASS_ID:
        prettySelList  = getStrFromClasses(selList, "consonant");
        reply = `contain ${modeStr} ${k} of ${prettySelList}`;
        break;
      case VOWEL_CLASS_ID:
        prettySelList  = getStrFromClasses(selList, "vowel");
        reply = `contain ${modeStr} ${k} of ${prettySelList}`;
        break;
      case CONSONANT_PLACES_ID:
        reply = "contain 3+ places of articulation for consonants";
        break;
      case CONSONANT_MANNERS_ID:
        reply = "contain 2+ manners of articulation for consonants";
        break;
      case COMPLEX_CONSONANT_ID:
        reply = "contain complex consonants";
        break;
      case TONE_ID:
        reply = "have tone";
        break;
      case STRESS_ID:
        reply = "have predictable stress";
        break;
      case SYLLABLE_ID:
        reply = `use ${modeStr} ${k} of the syllable structures ${selList}`;
        break;
      case MORPHOLOGY_ID:
        reply = `use ${modeStr} ${k} of the morphological types ${prettySelList}`;
        break;
      case WORD_FORMATION_ID:
        reply = `use ${modeStr} ${k} of ${prettySelList} to form words`;
        break;
      case FORMATION_FREQ_ID:
        reply = `use ${prettySelList} strategies to form words`;
        break;
      case WORD_ORDER_ID:
        reply = `have ${prettySelList} word order`;
        break;
      case HEADEDNESS_ID:
        reply = `are ${prettySelList}`;
        break;
      case AGREEMENT_ID:
        reply = `have ${prettySelList} agreement`;
        break;
      case CASE_ID:
        reply = `have ${prettySelList} case`;
        break;
      default:
        console.error("Error! Tried to submit a query of unknown trait:" + trait);
        break;
    }

    // Create a request and add it to the request list
    requestParams["trait"]        = trait;
    requestParams["selList"]      = selList;
    requestParams["sel"]          = sel;
    requestParams["k"]            = k;
    requestParams["mode"]         = mode;
    requestParams["reply"]        = reply;

    requests.push(requestParams);
  }

  var payload = "payload=" + JSON.stringify(requests);
  payload += `&listMode=${listMode}`; // Hacky

  console.log("Sending post with payload: " + payload);
  $.post("/",
         payload,
         callback
       );
}

// Toggles the setting of listMode -- are lists shown/hidden by default?
function handleListToggle() {
  listMode = !listMode;
}

/*****************************************************************************/
/*                                Callback                                   */
/*****************************************************************************/
// Callback function for AJAX -- in development
function callback(reply) {
  $("#results").html(reply)
  reloadTooltips();
}

/*****************************************************************************/
/*                                Creators                                   */
/*****************************************************************************/

// Create and return a new selector DOM element as a string
// Use the string jqueryStr to locate the selector template to be copied.
// BUG Currently all instances share same id
// NOTE outerHTML not compatible with older browsers!'
// TODO rename copySelectorFromTemplate
function createSelectorString(jqueryStr, uid) {
  if (!jqueryStr) {
    console.error("Error: creating selector string without ID!");
    jqueryStr = "#cbox-template";
  }
  if (!uid) {
    uid = UID();
  }
  // Locate the template
  var template = $(jqueryStr)[0];

  // Alter template so it can be displayed (remove template markings)
  var oldID = template.id;
  template.id += "-" + uid;
  template.classList.remove("template");
  var str = template.outerHTML;

  // Add a UID to each id= and for= attribute\
  str = str.replace(/(box-[^\"0-9][^\"0-9]?-)template/g, "$1" + uid);

  // Undo alterations to template so it is suitable for copying again
  template.id = oldID;
  template.classList.add("template");

  return str;
}

// Create + return a clone of the trait templates
function cloneTraitTemplate() {
  var template = $("#trait-div-template").clone()[0];
  var uid = "-" + UID();

  template.id = template.id.replace(/-template/g, uid);
  var children = template.children;
  for (var i = 0; i < children.length; i++) {
    children[i].id = children[i].id.replace(/-template/g, uid);
  }

  return template;
}

// Write one function for each of the input types.
// ie create phonemeSelector
// ie create checkboxes for other traits???

/*****************************************************************************/
/*                                Getters                                    */
/*****************************************************************************/

// Get a list of active trait div query elements (those traits that would be submitted)
function getActiveTraits() {
  var activeDivList = $(".trait-div:visible");
  var activeTraitList = activeDivList.children(".active");
  return activeTraitList;
}

/*****************************************************************************/
/*                                Helpers                                    */
/*****************************************************************************/
// Add the display: none style to the given DOM element
function hideElement(element) {
  element.classList.add("hidden");
}

// Remove the display: none style to the given DOM element
function unhideElement(element) {
  element.classList.remove("hidden");
}

// Reload popovers to ensure proper initialization.
function reloadPopovers() {
  // BUG? Need to hide and remove old popover
  //$("[data-toggle=popover]").popover("dispose");
  $("[data-toggle=popover]").popover();
}

function reloadTooltips() {
  $("[data-toggle=tooltip]").tooltip();
}

// Returns the shorthand mode string from the long readable form
// TODO make this into a dict for easier modification
// TODO move this to python -- not really needed on frontend
function getModeFromStr(str) {
  if (!str) return null;
  if (str.includes("exactly"))            return "EQ";
  else if (str.includes("at least"))      return "GEQ";
  else if (str.includes("at most"))       return "LEQ";
  else if (str.includes("not equal to"))  return "NEQ";
  else if (str.includes("less than"))     return "LT";
  else if (str.includes("more than"))     return "GT";
  else {
    console.log("Error! An illegal string was passed to getModeFromStr");
    return "EQ";
  }
}

// Returns the shorthand mode string from the long readable form
// TODO make this into a dict for easier modification
// TODO actually just scrap it and make strings exactly equal
function getStrFromMode(mode) {
  if      (mode == "EQ")  return "exactly";
  else if (mode == "NEQ") return "not equal to";
  else if (mode == "LEQ") return "at most";
  else if (mode == "GEQ") return "at least";
  else if (mode == "LT")  return "less than";
  else if (mode == "GT")  return "more than";
  else {
    console.log("Error! An illegal string was passed to getStrFromMode");
    return "exactly";
  }
}

// Given an array of the natural classes desired, prettify a string that combines
// all requested classes in a human readable way.
function getStrFromClasses(arr, type) {
  var str = "";

  // Was the given trait filtered?
  var flags = [];
  for (var i = 0; i < flags.length; i++) {
    flags.push(false);
  }
  type = (type == "consonant") ? "consonant" : "vowel";
  for (var i = 0; i < arr.length; i++) {
    if (typeof arr[i] != typeof "") {
      console.error("Improper array element passed to natural class parser!");
      return "error";
    }
    // If the selected class isn't a placeholder ("Any ...")
    // Then append a lowercase version of the corresponding class
    if (!arr[i].toLowerCase().includes("Any ".toLowerCase())) {
      str += " " + arr[i].toLowerCase();
      flags[i] = true;
    }
  }

  // Done appending the pieces. Now we clean up the string to make it sound natural.

  // If we are dealing with a vowel, just append " vowels" to the end and return.
  if (type == "vowel") {
    str += " vowels";
    return str;
  }

  // If there is no place or manner, just add the broadest possible phoneme class (consonant/vowel)
  if (!flags[PLACE] && !flags[MANNER]) {
    str += " " + type;
  }

  // If no filtering was done, just return "consonants" or "vowels" as appropriate
  if (str.length == 0) {
    str = type;
  }

  // Trim whitespace and return (with an "s" appended to the end to make plural)
  return str.trim() + "s";
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
var UID_COUNT = 0;
function UID() {
  var uid = numToUID(UID_COUNT);
  UID_COUNT++;
  return uid;
}
