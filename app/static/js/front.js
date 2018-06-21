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
var CONSONANT_CLASSES  = {
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
};

/*****************************************************************************/
/*                                Initializers                               */
/*****************************************************************************/
// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Update the document with trait selectors from template
  traitSelectorInit();

  // Initialize popovers
  consonantPopoverInit();
  vowelPopoverInit();
  reloadPopovers();
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

// Initialize all uninitialized consonant selector popovers
function consonantPopoverInit() {
  // TODO the first two lines are basically useless right now as the UID is mishandled
  // Try using jQuery.each() for "more correct" iteration
  var str = createConsonantSelectorString();
  var uid = str.match(/template-[0-9a-fA-F]+/g)[0].replace(/template-/g,"");
  $(".cbox-selector-uninit").attr("data-content", createConsonantSelectorString());
  $(".cbox-selector-uninit").attr("id", "cbox-selector-" + uid);
  $(".cbox-selector-uninit").addClass("cbox-selector-init");
  $(".cbox-selector-uninit").removeClass("cbox-selector-uninit");
}

// Initialize all uninitialized vowel selector popovers
function vowelPopoverInit() {
  // TODO the first two lines are basically useless right now as the UID is mishandled
  var str = createVowelSelectorString();
  var uid = str.match(/template-[0-9a-fA-F]+/g)[0].replace(/template-/g,"");
  $(".vbox-selector-uninit").attr("data-content", createVowelSelectorString());
  $(".vbox-selector-uninit").attr("id", "vbox-selector-" + uid);
  $(".vbox-selector-uninit").addClass("vbox-selector-init");
  $(".vbox-selector-uninit").removeClass("vbox-selector-uninit");
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

    // Generate the correct reply string based on the trait type
    var reply;
    switch (id) {
      case CONSONANT_ID:
        reply = "contain " + modeStr + " " + k + " of " + consStr;
        break;
      case CONSONANT_CLASS_ID:
      // TODO
        reply = "contain " + modeStr + " " + k + " of " + consStr;
        break;
      case VOWEL_ID:
      // TODO
        reply = "contain " + modeStr + " " + k + " of " + vowelStr;
        break;
      case VOWEL_CLASS_ID:
        reply = "contain " + modeStr + " " + k + " of " + vowelStr;
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

// Create and return a new phoneme selector DOM element as a string
// Use the string type to choose between consonant ("c") or vowel ("v")
// BUG Currently all instances share same id
// NOTE outerHTML not compatible with older browsers!
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
