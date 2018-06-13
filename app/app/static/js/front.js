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
  $.post("/",
         "testAttr=testValue&consonants=" + $(".pbox-selector-init").attr("queryStr"),
         callback
       );
}


/*****************************************************************************/
/*                                Callback                                   */
/*****************************************************************************/
// Callback function for AJAX -- in development
function callback(reply) {
  console.log(reply);
  // alert(reply);
  $("#results").text(reply)
}

/*****************************************************************************/
/*                                Creators                                   */
/*****************************************************************************/
// Create and return a new phoneme selector DOM element as a string
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
  var uid = UID();

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
