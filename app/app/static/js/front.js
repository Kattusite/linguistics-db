/*****************************************************************************/
/*                               Global Variables                            */
/*****************************************************************************/

var NUM_TRAITS = 1; // The number of traits currently being queried

/*****************************************************************************/
/*                                Initializers                               */
/*****************************************************************************/

// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Update the document with trait selectors from template
  traitSelectorInit();

  // Initialize popovers
  phonemePopoverInit();
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

// Initialize all uninitialized phoneme selector popovers
function phonemePopoverInit() {
  var str = createPhonemeSelectorString();
  var uid = str.match(/template-[0-9a-fA-F]+/g)[0].replace(/template-/g,"");
  $(".pbox-selector-uninit").attr("data-content", createPhonemeSelectorString());
  $(".pbox-selector-uninit").attr("id", "pbox-selector-" + uid);
  $(".pbox-selector-uninit").addClass("pbox-selector-init");
  $(".pbox-selector-uninit").removeClass("pbox-selector-uninit");
}

/*****************************************************************************/
/*                                Event Handlers                             */
/*****************************************************************************/

// On click handler for single trait button
// Hides second trait div
function handleSingleTrait() {
  console.log("single clicked");
  hideElement($("#trait-divs").children()[1]);
  NUM_TRAITS = 1;
}

// On click handler for double trait button
// Displays second trait div
function handleDoubleTrait() {
  console.log("double clicked");
  unhideElement($("#trait-divs").children()[1]);
  NUM_TRAITS = 2;
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
// NOTE Setting "checked" is not IE friendly
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
  console.log("Button " + glyph + " clicked.");

  // Find the checkbox and table
  var tgt = "#" + element.getAttribute("for");
  var checkbox = $(tgt)[0];

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

  //reloadPopovers();
}

// Submission handler to send AJAX requests to server
function handleSubmit() {
  // var cons = $(".pbox-selector-init").attr("queryStr")
  // var consStr = $(".pbox-selector-init")[0].innerText;
  // var k    = $(".active-trait").children("input").val()
  // var modeStr = $(".active-trait").children(".mode-selector").val()
  // var mode = getModeFromStr(modeStr);
  // var reply = "languages contain " + modeStr + " " + k + " of " + consStr

  var payload =
    "testAttr=testValue" +
    "&consonants=" + cons +
    "&k=" + k +
    "&mode=" + mode +
    "&reply=" + reply;

  var reqArr = [];

  var traits = getActiveTraits();
  for (var i = 0; i < traits.length; i++) {
    var t = $(traits[i]);
    var reqObj = {};
    var id = traits[i].id.replace(/-\d+/g, "");

    var cons = t.children(".pbox-selector-init:visible").attr("queryStr");
    var consStr = t.children(".pbox-selector-init:visible").text();
    var k = t.children(".k-input").val()
    var modeStr = t.children(".mode-selector").val();
    var mode = getModeFromStr(modeStr);

    // TODO generalize this
    var reply = "contain " + modeStr + " " + k + " of " + consStr;

    reqObj["trait"] = id;
    reqObj["consonants"] = cons;
    reqObj["k"] = k;
    reqObj["mode"] = mode;
    reqObj["reply"] = reply;

    reqArr.push(reqObj);
  }

  payload = "payload=" + JSON.stringify(reqArr);


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
  // alert(reply);
  $("#results").text(reply)
}

/*****************************************************************************/
/*                                Creators                                   */
/*****************************************************************************/
// Create and return a new phoneme selector DOM element as a string
// BUG Currently all instances share same id
function createPhonemeSelectorString(uid) {
  // NOTE outerHTML not compatible with older browsers!
  var template = $("#pbox-template")[0];
  if (!uid) {
    uid = UID();
  }
  template.id += "-" + uid;
  var str = template.outerHTML;

  // Add a UID to each id= and for= attribute\
  str = str.replace(/(pbox-[^\"0-9][^\"0-9]?-)template/g, "$1" + uid);

  // Change the template id back to original
  template.id = "pbox-template";
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

// Given a dictionary, return it as a serialized string suitable for AJAX requests
// Incredibly hacky, but robust enough
function serialize(dict) {
  var keys = Object.keys(dict);
  var form = document.createElement("form");
  for (var i = 0; i < keys.length; i++) {
    var input = document.createElement("input");
    input.name = keys[i];
    input.value = dict[keys[i]];
    form.appendChild(input);
  }
  return $(form).serialize();
}


// Returns the shorthand mode string from the long readable form
// TODO make this into a dict for easier modification
// TODO move this to python -- not really needed on frontend
function getModeFromStr(str) {
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
