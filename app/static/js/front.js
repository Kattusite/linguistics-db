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

// Canonical lists of vowel + consonant classes
// Consonants:   n,t,m,k,j,s,p,l,w,h,b,d,g,ŋ,ʃ,ʔ,tʃ,f,r,ɲ,z,ts,dʒ,x,v
// NOTE To save future headache, please delegate this to a python script that
// compares a list of phonemes to the canonical list and generates the bitstrings accordingly.
// Much easier to work with lists of phonemes than bitstrings, as they are less change-sensitive

var VOICING = 0;
var PLACE   = 1;
var MANNER  = 2;

/*var CONSONANT_CLASSES  = {
  "consonant": "",
  "consonantal": "",
  "sonorant": "",
  "fricative": "",
  "labial":"",
  "plosives": "000000000...1111111"
};
// Vowels:  a,e,o,i,u,ə,ɨ,ɯ,y,ʌ,ø,ɵ,ʉ
var VOWEL_CLASSES = {
  "high": "000...111",
  "mid": "",
  "low": "",
  "front": "",
  "back": "",
  "open": ""
}; */

/*****************************************************************************/
/*                                Initializers                               */
/*****************************************************************************/
// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Update the document with trait selectors from template
  traitSelectorInit();

  // Initialize popovers (consonant, vowel, consonant classes, vowel classes)
  initPopovers("cbox-selector",  createConsonantSelectorString);
  initPopovers("vbox-selector",  createVowelSelectorString);
  initPopovers("ccbox-selector", createConsonantClassSelectorString);
  initPopovers("vcbox-selector", createVowelClassSelectorString);

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
 * Create each of these a unique popover with content determined by contentFn
 * For instance initPopover("dummy-class") will replace all ".dummy-class-uninit"
 * with ".dummy-class-init", and update the data-content with the return value
 * of contentFn.
 */
 // TODO the first two UID lines are basically useless right now as the UID is mishandled
 // Try using jQuery.each() for "more correct" iteration
 // The current way leads to a minor BUG in which popover UIDs mismatch enclosing div UIDs
function initPopovers(tgtClass, contentFn) {
  var uninit = tgtClass + "-uninit";  // e.g. ".cbox-selector-uninit"
  var init   = tgtClass + "-init";    // e.g. ".cbox-selector-init"

  var str = contentFn();
  var uid = str.match(/template-[0-9a-fA-F]+/g)[0].replace(/template-/g,"");
  $("." + uninit).attr("data-content", contentFn());
  $("." + uninit).attr("id", tgtClass + "-" + uid);
  $("." + uninit).addClass(init);
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
  var queryStr  = ""; // To be sent in server request (string of 1s and 0s)
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
        queryStr = queryStr + "1";
      }
      else {
        queryStr = queryStr + "0";
      }
    }
  }

  // Update the link text to be the glyph list, or placeholder if empty.
  // NOTE [aria-describedby] might misbehave for multiple phoneme selectors present on the document at once
  // it works by finding the popovers that are *currently* visibly popped open, so there *should* be only one
  var link = $("[aria-describedby]");
  if (glyphList.length == 0) {
    link.text("Select phonemes...");
  }
  else {
    var lbl = "";
    for (var i = 0; i < glyphList.length; i++) {
      lbl += glyphList[i];
      if (i != glyphList.length - 1) {
        lbl += ", ";
      }
    }
    link.text(lbl);
  }

  // Inform the link text DOM object of its query string.
  link.attr("queryStr", queryStr);

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

// Submission handler to send AJAX requests to server
// TODO Document the fields of the submission
// TODO Make sure the query is valid (i.e. at least 1 phoneme selected, a syllable was entered)
function handleSubmit() {
  var reqArr = [];

  var traits = getActiveTraits();
  for (var i = 0; i < traits.length; i++) {
    var t = $(traits[i]);
    var reqObj = {};
    var id = traits[i].id.replace(/-\d+/g, "");

    var cons      = t.children(".cbox-selector-init:visible").attr("queryStr");
    var vowel     = t.children(".vbox-selector-init:visible").attr("queryStr");
    var consStr   = t.children(".cbox-selector-init:visible").text();
    var vowelStr  = t.children(".vbox-selector-init:visible").text();
    var k         = t.children(".k-input").val()
    var modeStr   = t.children(".mode-selector").val();
    var mode      = getModeFromStr(modeStr);


    // Obtain the three natural classes selected
    // TODO make this less hacky and more stable
    var classArr =  []
    var classStr = "";

    // Generate the correct reply string based on the trait type
    // Some cases have special other info that must be calculated (ie for natural class arrays)
    var reply;
    switch (id) {
      case CONSONANT_ID:
        reply = "contain " + modeStr + " " + k + " of " + consStr;
        break;
      case CONSONANT_CLASS_ID:
        classArr = t.children(".ccbox-selector-init:visible").attr("queryArr").split(",");
        classStr = getStrFromClasses(classArr, "consonant");
        reply = "contain " + modeStr + " " + k + " of " + classStr;
        break;
      case VOWEL_ID:
        reply = "contain " + modeStr + " " + k + " of " + vowelStr;
        break;
      case VOWEL_CLASS_ID:
        classArr = t.children(".ccbox-selector-init:visible").attr("queryArr").split(",");
        classStr = getStrFromClasses(classArr, "vowel");
        reply = "contain " + modeStr + " " + k + " of " + classStr;
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
    }

    reqObj["trait"]       = id;
    reqObj["consonants"]  = cons;
    reqObj["vowels"]      = vowel;
    reqObj["k"]           = k;
    reqObj["mode"]        = mode;
    reqObj["reply"]       = reply;
    reqObj["classes"]     = classArr;

    reqArr.push(reqObj);
  }

  var payload = "payload=" + JSON.stringify(reqArr);

  console.log("Sending post with payload: " + payload);
  $.post("/",
         payload,
         callback
       );
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
// Create and return a new consonant selector DOM element as a string
function createConsonantSelectorString(uid) {
  return createPhonemeSelectorString("c", uid);
}

// Create and return a new vowel selector DOM element as a string
function createVowelSelectorString(uid) {
  return createPhonemeSelectorString("v", uid);
}

function createConsonantClassSelectorString(uid) {
  return createPhonemeSelectorString("cc", uid);
}

function createVowelClassSelectorString(uid) {
  return createPhonemeSelectorString("vc", uid);
}

// Create and return a new phoneme selector DOM element as a string
// Use the string type to choose between consonant ("c") or vowel ("v")
// BUG Currently all instances share same id
// NOTE outerHTML not compatible with older browsers!'
// TODO rename copySelectorFromTemplate
function createPhonemeSelectorString(type, uid) {
  if (!type) {
    console.err("Error: creating a typeless phoneme selector")
    type = "c";
  }
  if (!uid) {
    uid = UID();
  }
  var template = $("#" + type + "box-template")[0];
  template.id += "-" + uid;
  var str = template.outerHTML;

  // Add a UID to each id= and for= attribute\
  str = str.replace(/(box-[^\"0-9][^\"0-9]?-)template/g, "$1" + uid);

  // Change the template id back to original
  template.id = type + "box-template";
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
