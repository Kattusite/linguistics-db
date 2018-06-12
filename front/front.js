// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Initialize popovers
  phonemePopoverInit();
  reloadPopovers();
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
// NOTE Setting "checked" is not IE friendly
// NOTE This is a potentially slow function (string concat + iterating over all boxes)
function handlePboxLabel(event, element) {
  var glyph = element.innerText;
  console.log("Button " + glyph + " clicked.");

  // Find the checkbox and table
  var tgt = "#" + element.getAttribute("for");
  var checkbox = $(tgt)[0];

  //         label  -->    td     -->     tr    --> tablebody --> table
  var table = element.parentElement.parentElement.parentElement.parentElement
  var div = table.parentElement;
  var str = div.outerHTML;
  console.log(table);

  // Iterate over all labels in this table
  // If checkbox is checked, replace its text with "checked" and add its glyph
  // to the glyph list.
  // Special Case: If checkbox is the one that was clicked, it maybe hasn't updated yet.
  // BUG this happens before the box gets checked.

  // TODO Change the whole checkbox thing to be divs with a special class added/removed.
  // this is gonna be painful otherwise. 
  var glyphList = [];
  var rows = table.children[0].children; // table -> tbody -> array of TRs
  for (var i = 0; i < rows.length; i++) {
    var entries = rows[i].children;
    for (var j = 0; j < entries.length; j++) {
      var td = entries[j];
      var box = td.children[0];
      console.log(box);
      if (box.checked) {
        // Does nothing! yay
        str = str.replace(new RegExp("(" + box.id + ")", "g"), "$1 checked");
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



  // Save the content changes in the popover attribute.
  link.attr("data-content", str);



  //reloadPopovers();
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
  // NOTE outerHTML not compatible with older browsers!
  var template = $("#pbox-template")[0];
  var uid = UID();
  template.id += "-" + uid;
  var str = template.outerHTML;

  // Add a UID to each id= and for= attribute\
  str = str.replace(/(pbox-template-[^\"0-9][^\"0-9]?)/g, "$1-" + uid);

  // Change the template id back to original
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
var UID_COUNT = 0;
function UID() {
  var uid = numToUID(UID_COUNT);
  UID_COUNT++;
  return uid;
}
