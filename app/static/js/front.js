/*****************************************************************************/
/*                               Global Variables                            */
/*****************************************************************************/

var CONSONANT_ID            = "consonant-selector";
var CONSONANT_CLASS_ID      = "consonant-class-selector";
var VOWEL_ID                = "vowel-selector";
var VOWEL_CLASS_ID          = "vowel-class-selector";
var CONSONANT_PLACES_ID     = "consonant-places";
var CONSONANT_MANNERS_ID    = "consonant-manners";
var COMPLEX_CONSONANT_ID    = "complex-consonant";
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

  reloadPopovers();
  reloadTooltips();
}

// Initialize trait selector divs
function traitSelectorInit() {
  var tgt = $("#trait-divs")[0];
  for (var i = 0; i < tgt.children.length; i++) {
    tgt.replaceChild(cloneTraitTemplate(), tgt.children[i]);
    // Hide children after the first one.
    if (i > 0) {
      hideElement(tgt.children[i]);
    }
  }
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
function handleTraitSelect(element) {
  var sel = $(element).val();
  var index = element.selectedIndex;
  var selElement = element.parentElement.children[index+1];

  // Activate selected element and deactivate others.
  $(element).parent().children("div").addClass("inactive-trait");
  $(element).parent().children("div").removeClass("active-trait");
  $(selElement).removeClass("inactive-trait");
  $(selElement).addClass("active-trait");
}

// On click function for element representing a label in the pbox.
// Save the state of the pbox inside the data-content, reload popover
// Update link text.
// NOTE This is a potentially slow function (string concat + iterating over all boxes)
// (But in practice all numbers are small constants)
function handlePboxLabel(element) {
  // (Un)select the pbox label.
  if ($(element).hasClass("pbox-label-selected")) {
    $(element).removeClass("pbox-label-selected");
  }
  else {
    $(element).addClass("pbox-label-selected");
  }

  // Log the click.
  var glyph = element.innerText;
  // console.log("Button " + glyph + " clicked.");

  //         label  -->    td     -->     tr    --> tablebody --> table
  var table = element.parentElement.parentElement.parentElement.parentElement
  var div = table.parentElement;
  var str = div.outerHTML;

  // Iterate over all labels in this table
  // If checkbox is checked,  add its glyph to the glyph list.
  var glyphList = [];
  var rows = table.children[0].children; // table -> tbody -> array of TRs
  for (var i = 0; i < rows.length; i++) {
    var entries = rows[i].children;
    for (var j = 0; j < entries.length; j++) {
      var td = entries[j];
      var box = td.children[0];
      if ($(box).hasClass("pbox-label-empty")) {
        continue;
      }
      if ($(box).hasClass("pbox-label-selected")) {
        glyphList.push($(box).text());
      }
    }
  }

  // Update the link text to be the glyph list, or placeholder if empty.
  // NOTE [aria-describedby] might misbehave for multiple phoneme selectors present on the document at once
  // it works by finding the popovers that are *currently* visibly popped open, so there *should* be only one
  var link = $("[aria-describedby]");
  var lbl = "";
  if (glyphList.length == 0) {
    lbl = "Select phonemes...";
  }
  else {
    lbl = glyphList.join(", ");
  }
  link.text(lbl);

  // Inform the link-text DOM object of its query for the server.
  link.attr("glyphList", glyphList);

  // Save the content changes in the popover attribute.
  link.attr("data-content", str);
}

/* On click handler for the natural class selector. On a click, deselect the
 * currently selected element of this type, and select this one instead.
 * Update the associated link text for the popover. */
 /* This function assumes that at no point will more or less than one natural
  * class of each type be selected. */
function handleClboxLabel(element) {
  // Figure out if element is voicing/place/manner
  var type = "";
  for (var i = 0; i < element.classList.length; i++) {
    if (element.classList[i] == "clbox-label")          continue;
    if (element.classList[i] == "clbox-label-selected") continue;
    type = element.classList[i];
    break;
  }

  var tablebody = element.parentElement.parentElement; // td --> tr --> tablebody
  var rows = tablebody.children;

  // Find number of rows and columns
  var numRows = rows.length;
  var numCols = rows[0].children.length;

  // If the clicked element was already selected, deselect it and select "Any ..." instead
  // If the clicked element was not selected, deselect all others and select this instead.
  var isSel = $(element).hasClass("clbox-label-selected");

  // iterate through all elements of this type of natural class, and deselect them
  for (var i = 0; i < numRows; i++) {
    // (the following two steps could be combined into a single jquery expression)
    // Find the correct type of element on this row.
    var el = $(rows[i]).children("."+type);
    // If it is selected, unselect it
    if (el.hasClass("clbox-label-selected")) {
      el.removeClass("clbox-label-selected");
    }
  }

  // Select the clicked element, or default (select first row) if it was already selected.
  if (isSel) {
    $(tablebody.children[0]).find("."+type).addClass("clbox-label-selected");
  }
  else {
    $(element).addClass("clbox-label-selected");
  }


  // Now that all changes are made, changes can be saved to data-content
  var link = $("[aria-describedby]");
  var table = tablebody.parentElement;
  var div = table.parentElement;
  var str = div.outerHTML;

  // Save the content changes in the popover attribute.
  link.attr("data-content", str);

  // Update the label text and store the queryArr
  var queryArr = [];
  for (var i = 0; i < numCols; i++) {
    var sel = $(tablebody).find("td.clbox-label-selected.clbox-label-"+i).text();
    queryArr.push(sel);
  }

  // Figure out if we want consonants or vowels
  var ctype = tablebody.classList.contains("consonant-class-selector") ? "consonant" : "vowel";

  // Inform the link text DOM object of its query string.
  link.attr("queryArr", queryArr);

  // update the link text to reflect new changes
  link.text(getStrFromClasses(queryArr, ctype));

  // console.log(v, p, m);
}

// Handle clicks on an Lbox element. Select the clicked on box.
// If multiple selections are prohibited, deselect all other boxes.
// mutli = true ==> multiple selections allowed
function handleLboxLabel(element, multi) {
  // Find the containing table.
  //         label  -->     tr    --> tablebody --> table
  var table = element.parentElement.parentElement.parentElement;

  // (Un)select the lbox label that was clicked.
  if ($(element).hasClass("lbox-label-selected")) {
    $(element).removeClass("lbox-label-selected");
  }
  else {
    // If multiple selections disallowed, deselect all other labels in table
    if (!multi) {
      $(table).children().children().children(".lbox-label").removeClass("lbox-label-selected");
    }
    $(element).addClass("lbox-label-selected");
  }

  // Save the contents of the table in a string so the popover will be updated
  var div = table.parentElement;
  var outerHTML = div.outerHTML;

  // Iterate over all labels in this table
  // If selected, add its text to the displayed link.
  var selList = [];
  var rows = table.children[0].children; // table -> tbody -> array of TRs
  for (var i = 0; i < rows.length; i++) {
    var cols = rows[i].children;
    for (var j = 0; j < cols.length; j++) {
      var td = cols[j];
      if ($(td).hasClass("lbox-label-empty")) {
        continue;
      }
      if ($(td).hasClass("lbox-label-selected")) {
        selList.push($(td).text());
      }
    }
  }

  // Update the link text to be the sel list, or placeholder if empty.
  // NOTE [aria-describedby] might misbehave for multiple phoneme selectors present on the document at once
  // it works by finding the popovers that are *currently* visibly popped open, so there *should* be only one
  var link = $("[aria-describedby]");
  var lbl = "";
  if (selList.length == 0) {
    lbl = "Select trait..."
  }
  else {
    lbl = selList.join(", ");
  }
  link.text(lbl);

  // Inform the link-text DOM object of its query for the server.
  // If multiple selections allowed, this is a list, else a single element (str)
  if (multi) {
    link.attr("selList", selList);
  } else {
    link.attr("sel", selList[0]);
  }

  // Save the content changes in the popover attribute.
  link.attr("data-content", outerHTML);
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

// If el already has class cls, remove cls from el and all elements in els
// Else, add cls to el and all elements in els
function toggleClasses(el, els, cls) {
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

//

// Click handler for ipa consonant box labels
function handleIpacboxLabel(element) {
  // Get the enclosing table.
  var table = element.parentElement.parentElement.parentElement;

  // Toggle the clicked element.
  // If clicked element was a header, toggle all matching elements.
  var $el = $(element);
  if ($el.hasClass("ipa-header")) {

    // Figure out which trait this header represents
    var category = $el.attr("category");
    var trait = $el.attr("trait");

    // Get a list of the matching phonemes
    // i.e. by getting all phonemes that have an attr matching the trait string
    var matches = $(table).children().children().children(`[${category}='${trait}']`);

    // Select or unselect ALL the elements in the list as a group.
    // Afterwards, either ALL matching phonemes are selected, or ALL are not.
    toggleClasses(element, matches.toArray(), "ipa-box-selected");

  }
  // Else, toggle just that element
  // Decide selecting this element causes a header category to be (un)selected
  else {
    // Get the traits associated with this glyphs
    var place = $el.attr("place");
    var manner = $el.attr("manner");

    // For each trait, check if all are selected before the toggle
    // This means we need to deselect the category header.

    // Carry out the toggle.
    toggleClass(element, "ipa-box-selected");

    // For each trait, check if all are selected after the toggle.
    // This means we need to select the category header.


  }

  // Save the contents of the table in a string so the popover will be updated
  var div = table.parentElement;
  var outerHTML = div.outerHTML;

  // Find all selected glyphs in the table.
  var selList = $(table).children(".ipa-box-selected").arr();

  // Update the link text to be the sel list, or placeholder if empty

  // Inform the button of its query for the server, as a list of glyphs

  // Save the content changes in the popover attribute.
  link.attr("data-content", outerHTML);

}

// Submission handler to send AJAX requests to server
// TODO Document the fields of the submission
// TODO Make sure the query is valid (i.e. at least 1 phoneme selected, a syllable was entered)
// TODO selList and classList/queryArr seem to be suspiciously similar...
// TODO consStr, vowelStr, classStr, all also seem suspiciously similar
// Try to revise to use just one of these.
function handleSubmit() {
  var reqArr = [];

  var traits = getActiveTraits();
  for (var i = 0; i < traits.length; i++) {
    var t = $(traits[i]);
    var reqObj = {};
    var trait = traits[i].id.replace(/-\d+/g, "");

    // Move most of this into the switch statement
    var cons      = t.children(".cbox-selector-init:visible").attr("glyphList");
    if (cons) cons = cons.split(",");

    var consStr   = t.children(".cbox-selector-init:visible").text();
    var vowelStr  = t.children(".vbox-selector-init:visible").text();
    var k         = t.children(".k-input").val()
    var modeStr   = t.children(".mode-selector").val();
    var mode      = getModeFromStr(modeStr);

    // If the selection list attr exists visibly, grab its info and split str->arr
    var selList = t.children("a[selList]:visible").attr("selList");
    if (selList) selList = selList.split(",");

    var sel       = t.children("a[sel]:visible").attr("sel");


    // Obtain the three natural classes selected
    // TODO make this less hacky and more stable
    var glyphList;
    var classList =  [];
    var classStr = "";
    var prettifiedStr = ""; // A string representing the pretty-printed matchList

    // Generate the correct reply string based on the trait type
    // Some cases have special other info that must be calculated (ie for natural class arrays)
    var reply;
    switch (trait) {
      case CONSONANT_ID:
        prettifiedStr = t.children(".cbox-selector-init:visible").text();
        glyphList = t.children(".cbox-selector-init:visible").attr("glyphList").split(",");
        reply = "contain " + modeStr + " " + k + " of " + prettifiedStr;
        break;
      case CONSONANT_CLASS_ID:
        classList = t.children(".ccbox-selector-init:visible").attr("queryArr").split(",");
        prettifiedStr  = getStrFromClasses(classList, "consonant");
        reply = "contain " + modeStr + " " + k + " of " + prettifiedStr;
        break;
      case VOWEL_ID:
        prettifiedStr = t.children(".vbox-selector-init:visible").text();
        glyphList = t.children(".vbox-selector-init:visible").attr("glyphList").split(",");
        reply = "contain " + modeStr + " " + k + " of " + prettifiedStr;
        break;
      case VOWEL_CLASS_ID:
        classList = t.children(".vcbox-selector-init:visible").attr("queryArr").split(",");
        prettifiedStr  = getStrFromClasses(classList, "vowel");
        reply = "contain " + modeStr + " " + k + " of " + prettifiedStr;
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
        reply = "allow the syllable structure" + syllable;
        break;
      case MORPHOLOGY_ID:
        prettifiedStr = t.children(".m-lbox-selector-init:visible").text();
        reply = "use " + modeStr + " " + k +
                " of the morphological types " + prettifiedStr;
        break;
      case WORD_FORMATION_ID:
        prettifiedStr = t.children(".wf-lbox-selector-init:visible").text();
        reply = "use " + modeStr + " " + k + " of " +
                prettifiedStr + " to form words";
        break;
      case FORMATION_FREQ_ID:
        reply = "use " + sel + " strategies to form words";
        break;
      case WORD_ORDER_ID:
        reply = "have " + sel + " word order";
        break;
      case HEADEDNESS_ID:
        reply = "are " + sel;
        break;
      case AGREEMENT_ID:
        reply = "have " + sel + " agreement";
        break;
      case CASE_ID:
        reply = "have " + sel + " case";
        break;
      default:
        console.err("Error! Tried to submit a query of unknown trait:" + trait);
        break;
    }

    // Insert query data into the query list
    // TODO glyphList, classList, selList will never all be used at once...
    // so just simplify the three down into a single "list" type.
    // TODO Call it matchList for lists and matchItem for single item.  (!)
    reqObj["trait"]       = trait;
    reqObj["glyphList"]   = glyphList;
    reqObj["k"]           = k;
    reqObj["mode"]        = mode;
    reqObj["reply"]       = reply;
    reqObj["classList"]   = classList;
    reqObj["selList"]     = selList;
    reqObj["sel"]         = sel;

    reqArr.push(reqObj);
  }

  var payload = "payload=" + JSON.stringify(reqArr);
  payload += "&listMode=" + listMode; // Hacky

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
  // $("#results").text(reply)
  $("#results").html(reply)
  reloadTooltips();
}

/*****************************************************************************/
/*                                Creators                                   */
/*****************************************************************************/
// // Create and return a new consonant selector DOM element as a string
// function createConsonantSelectorString(uid) {
//   return createPhonemeSelectorString("c", uid);
// }
//
// // Create and return a new vowel selector DOM element as a string
// function createVowelSelectorString(uid) {
//   return createPhonemeSelectorString("v", uid);
// }
//
// function createConsonantClassSelectorString(uid) {
//   return createPhonemeSelectorString("cc", uid);
// }
//
// function createVowelClassSelectorString(uid) {
//   return createPhonemeSelectorString("vc", uid);
// }

// Create and return a new selector DOM element as a string
// Use the string jqueryStr to locate the selector template to be copied.
// BUG Currently all instances share same id
// NOTE outerHTML not compatible with older browsers!'
// TODO rename copySelectorFromTemplate
function createSelectorString(jqueryStr, uid) {
  if (!jqueryStr) {
    console.err("Error: creating selector string without ID!");
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
  var activeTraitList = activeDivList.children(".active-trait");
  console.log(activeTraitList);
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
      console.err("Improper array element passed to natural class parser!");
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
