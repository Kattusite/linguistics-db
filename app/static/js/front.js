/*****************************************************************************/
/*                               Global Variables                            */
/*****************************************************************************/

// Should we list all members of the matching language set?
// Changed by handleListToggle
var listMode = false;

// Should the expanded/collapsed state of the matching language list be
// remembered between queries?
var REMEMBER_LIST_STATE = false;

// Which dataset should we use for queries?
// var DATASET = "F17"
// var DATASET = "S19";
var DATASET = "F25";

// COLORS
var DANGER  = "alert-danger";
var INFO    = "alert-info";
var WARN    = "alert-warning";
var SUCCESS = "alert-success";

// Different types of requests to be submitted
var QUERY = "query"
var GRAPH = "graph"

/*****************************************************************************/
/*                                Initializers                               */
/*****************************************************************************/
// On load initializer function
function frontInit() {
  console.log("Loading page...");

  // Update the document with trait selectors from template
  traitSelectorInit();

  // Iterate over constants in selectors_const.js, initializing all popovers / selectors
  for (key in SELECTORS_DICT) {
    var selector = SELECTORS_DICT[key];
    var mode = selector["mode"];
    var cls = selector["popover prefix"];
    if (["boolean", "no query"].includes(mode)) continue;
    else if (mode == "pick k ipa") {
      initIPAChart(cls);
    }
    else if (["pick one", "pick class", "pick multi", "pick k"].includes(mode)){
      initPopovers(cls);
    }
    else {
      console.err("Attempted to initialize a selector with unrecognized mode");
    }
  }

  reloadPopovers();
  reloadTooltips();

  initGraphs();
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

/* Target all uninitialized popovers of class tgtClass.uninit
 * Create each of these a unique popover with content copied from a template, whose
 * html id is: `#${tgtClass}-template`
 * For instance initPopover("dummy-class") will replace all ".dummy-class.uninit"
 * with ".dummy-class.init", and update the data-content with the return value
 * of createSelectorString(templateID).
 */
function initPopovers(tgtClass) {
  var uninit = `.${tgtClass}.uninit`;
  var templateID = `#${tgtClass}-template`;
  var str = createSelectorString(templateID);
  $(uninit).attr("data-content", str);
  $(uninit).addClass("init");
  $(uninit).addClass("selector-init"); // for CSS styling
  $(uninit).removeClass("uninit");
}

/* Given the base name of a tgt class, initialize all uninitialized members of that
 * class by copying the contents of the element specified by the selector template. */
 function initIPAChart(tgtClass) {
   var uninit = `.${tgtClass}.uninit`;
   var templateID = `#${tgtClass}-template`;
   var $template = $(templateID).clone();
   $template.addClass("init");
   $template.removeClass("template");
   $template.removeAttr("id");

   var $uninit = $(uninit);
   $uninit.replaceWith($template);
 }

/*****************************************************************************/
/*                               Output Functions                            */
/*****************************************************************************/

/* Set mode (color palette) of the output alert box to be the mode specified
 * as an argument (WARN = yellow, ERROR = red, INFO = blue, SUCCESS = green) */
function setOutputMode(mode) {
  if (![DANGER, INFO, WARN, SUCCESS].includes(mode))
    console.log("Attempted to set unexpected output mode for the results alert div.");

  var $resultDiv = $("#results-div");
  $resultDiv.removeClass(`${DANGER} ${INFO} ${WARN} ${SUCCESS}`);
  $resultDiv.addClass(mode);
}

function displayError(err) {
  var $result = $("#results");
  setOutputMode(DANGER);
  $result.text(err);
}

function displayInfo(info) {
  var $result = $("#results");
  setOutputMode(INFO);
  $result.text(info);
}

/*****************************************************************************/
/*                                Event Handlers                             */
/*****************************************************************************/

// On click handler for single trait button
// Hides second trait div
function handleSingleTrait() {
  // Do nothing if 1 already visible.
  if ($("#trait-divs").children(":visible").length == 1) return;
  hideElement($("#trait-divs").children()[1]);

  // Collapse gracefully - currently buggy b/c trait-divs lack collapsible class
  // also they are expanding too far and then snapping back instantly.
  // $("trait-divs").children().eq(1).collapse("hide");

  // Clear the results to avoid confusion
  resetResults();
}

// On click handler for double trait button
// Displays second trait div
function handleDoubleTrait() {
  // Do nothing if 2 already visible.
  if ($("#trait-divs").children(":visible").length == 2) return;
  unhideElement($("#trait-divs").children()[1]);

  // Collapse gracefully - currently buggy b/c trait-divs lack collapsible class
  // also they are expanding too far and then snapping back instantly.
  // $("trait-divs").children().eq(1).collapse("show");



  // Clear the results to avoid confusion
  resetResults();
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

  // Clear the results
  resetResults();
}

// Handle changes to the mode selector.
// Disable k input if "all" selected, else enable it.
function handleModeSelect(el) {
  var $el = $(el);
  var $ksel = $el.siblings(".k-selector");

  var sel = $el.val();
  // None not currently supported, but might be in the future
  if (!["all","none"].includes(sel)) {
    $ksel.removeAttr("disabled");
  }
  else {
    $ksel.attr("disabled", "");
    // Update the value of k based on selList.length, if mode is all
    var $traitDiv = $el.closest("div");
    var selList = $traitDiv.attr("selList");

    // Get list from selList attr string, or assume 0 length if it doesnt exist
    if (selList) {
      selList = selList.split(",");
      $ksel.val(selList.length);
    }
    else {
      $ksel.val(0);
    }
  }
}

// Get the text of the calling element, and replace the word "Hide" with "Show"
// or vice versa
function toggleShowHideText(el) {
  var txt = $(el).text();
  if (txt.includes("Show")) {
    txt = txt.replace("Show", "Hide");
  }
  else if (txt.includes("Hide")) {
    txt = txt.replace("Hide", "Show");
  }
  $(el).text(txt);
}

// Returns true iff the provided jQuery wrapper has a child of class .k-selector
// that is disabled.
function isKDisabled($el) {
  return $el.find(".k-selector[disabled]").length > 0;
}

// Given a popover div (i.e. containing an lbox table), store its HTML in the
// associated popover's data attribute.
// Using the provided selList, set the trait div's selList attribute and popover
// button's text to reflect the selections, using labelFn as a function to
// generate the button text
function updatePopover(popoverDiv, selList, labelFn) {
  var $popoverDiv = $(popoverDiv);
  // NOTE [aria-describedby] fails if multiple popovers are open concurrently.
  var $popoverButton = $("[aria-describedby]");
  var $traitDiv = $popoverButton.closest("div");

  // Store the state of the popover
  var popoverContent = $popoverDiv[0].outerHTML;
  $popoverButton.attr("data-content", popoverContent);

  // Store the selList for use in queries
  $traitDiv.attr("selList", selList);

  // Update the button text
  var lbl = labelFn(selList);
  $popoverButton.text(lbl);
}

// Get the number of cols in a given table (max # of td's in a single row)
function numColsInTable(table) {
  var $rows = $(table).find("tr");
  var cols = 0;
  for (row of $rows) {
    cols = Math.max(cols, $(row).children("td").length);
  }
  return cols;
}

// Given a table, return a list (selList) of all the selected elements in that
// table, in column-major order (all selected from 1st col, then 2nd col, etc.)
function getSelectedFromTable(table) {
  var selList = []

  // NOTE: $(table).find(".selected") won't work because it gives row-major results
  var numCols = numColsInTable(table);
  for (var i = 0; i < numCols; i++) {
    var $rows = $(table).find("tr");
    for (row of $rows) {
      var $sel = $(row).children("td").eq(i).filter(".selected");
      $sel.each(function() { selList.push($(this).text()); });
    }
  }
  return selList;
}

// On click function for element representing a label in the pbox.
// Save the state of the pbox inside the data-content, reload popover
// Update link text.
function handlePboxLabel(element) {
  var $el = $(element);
  var $popoverDiv = $el.closest("table").closest("div");
  var $traitDiv = $("[aria-describedby]").closest("div");

  // (Un)select the pbox label.
  toggleClass(element, "selected");

  var selList = getSelectedFromTable($table[0]);

  // Save the state + values of the popover for next time it opens / queries
  updatePopover($popoverDiv, selList, function(selLs) {
    var lbl = "Select phonemes...";
    if (selLs.length > 0) lbl = selLs.join(", ");
    return lbl;
  });

  // Update the k-selector's value if it is disabled (i.e. mode="all")
  if (isKDisabled($traitDiv)) {
    $traitDiv.find(".k-selector").val(selList.length);
  }
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
  var $traitDiv = $("[aria-describedby]").closest("div");

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

  var selList = getSelectedFromTable($table[0]);

  // Save the state of the popover for the next time it is opened
  var ctype = $table.hasClass("ccbox-popover-table") ? "consonant" : "vowel";
  updatePopover($popoverDiv, selList, function(selLs) {
    return getStrFromClasses(selLs, ctype);
  });

  // Update the k-selector's value if it is disabled (i.e. mode="all")
  if (isKDisabled($traitDiv)) {
    $traitDiv.find(".k-selector").val(selList.length);
  }
}

// Handle clicks on an Lbox element. Select the clicked on box.
// If multiple selections are prohibited, deselect all other boxes.
// mutli = true ==> multiple selections allowed
function handleLboxLabel(element, multi) {
  // Find the containing table.
  var $el = $(element);
  var $table = $el.closest("table");
  var $popoverDiv = $el.closest("table").closest("div");
  var $traitDiv = $("[aria-describedby]").closest("div");

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

  // Collect all selected elements from the table into a list
  var selList = getSelectedFromTable($table[0]);

  // Store the popover contents for the next time it is opened
  updatePopover($popoverDiv, selList, function(selLs) {
    var lbl = "Select trait...";
    if (selList.length > 0) lbl = selList.join(", ");
    return lbl;
  });

  // Update the k-selector's value if it is disabled (i.e. mode="all")
  if (isKDisabled($traitDiv)) {
    $traitDiv.find(".k-selector").val(selList.length);
  }
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
// I think it's going to be too much of a pain
function toggleClassesOthers () {
  console.error("Not yet implemented");
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

// Click handler for ipa vowel vox labels
function handleIpavboxLabel(element) {
  handleIpacboxLabel(element);
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

    // Select / deselect entire matching row/col (e.g. all plosives, all voiceds)
    toggleClassesAll(element, matches.toArray(), "selected");
  }
  // Else, toggle just that element
  else {
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

  // Find all selected glyphs in the table.
  var selList = getSelectedFromTable($table);

  // Inform the table of its query for the server, as a list of glyphs
  $traitDiv.attr("selList", selList);

  // Update the k-selector's value if it is disabled (i.e. mode="all")
  if (isKDisabled($traitDiv)) {
    $traitDiv.find(".k-selector").val(selList.length);
  }
}

// Returns true if the given mode is valid, else return false,
// and display an error message.
function validateMode(mode) {
  // Ensure mode exists
  if (!mode) {
    displayError("Request expected equality mode but found none!");
    console.log("Request expected equality mode but found none!");
    return false;
  }

  // Ensure mode is an acceptable value
  var validModes = ["at least", "at most", "less than",
                    "more than", "exactly", "not equal to",
                    "all"];
  if (!validModes.includes(mode)) {
    displayError("Please enter a valid equality mode.");
    console.log(`Invalid mode ${mode} was provided to a request.`);
    return false;
  }

  return true;
}

// Returns true if the given k is valid, else return false,
// and display an error message.
function validateK(k) {
  // Ensure k exists
  if (!k) {
    displayError("Please enter a number");
    console.log("k value expected but not found");
    return false;
  }

  // k must be a purely numerical value.
  k = Number(k);
  if (Number.isNaN(k)) {
    displayError("Please enter a number only");
    console.log("A number was expected for k, but other text was received.");
    return false;
  }

  // k must be an integer.
  if (!Number.isInteger(k)) {
    displayError("Please enter a whole number");
    console.log("Requests require whole number values of k.")
    return false;
  }

  // k must be positive
  if (k < 0) {
    displayError("Please enter a positive number");
    console.log("Requests require non-negative values of k.");
    return false;
  }

  return true;
}

// Returns true if the given selList is valid, else return false,
// and display an error message.
function validateSelList(selList) {
  if (!selList) {
    displayError("Please select something");
    console.log("Request expected selList but found none!");
    return false;
  }

  // Ensure selList is nonempty
  if (selList.length == 0) {
    displayError("Please select something");
    console.log("Nothing was selected!");
    return false;
  }
  return true;
}

// Returns true if the given sel is valid, else return false,
// and display an error message.
// Note: sel is an array (valid if length 1)
function validateSel(sel) {
  // Ensure sel is a valid selList.
  if (!validateSelList(sel)) return false;

  // Ensure sel is of length 1 (a single selection)
  var n = sel.length;
  if (n != 1) {
    displayError("Exactly one item must be selected.");
    console.log(`Request expected sel, but found array of size ${n}!`);
    return false;
  }

  return true;
}

// Return true if the requirements list contains only recognized requirements
// Else return false and pritn an error msg.
function validateRequirements(requirements) {
  for (var r of requirements) {
    if (!["mode", "k", "selList", "sel"].includes(r)) {
      console.error(`Unexpected request requirement: ${r}. Aborting...`);
      return false;
    }
  }
  return true;
}

// Returns true if the provided request parameters are valid, and false otherwise.
// E.g. Make sure that if a request requires a selList, that list is provided and
// nonempty.
function validateRequest(request) {
  // Find out the request type, and get its archetypal definition from selectors_const.js
  var trait = request["trait"];
  var def = SELECTORS_DICT[trait];

  // Abort with an error msg if the provided trait lacks a definition in selectors_const.js
  if (!def) {
    console.log("Encountered unexpected trait during request validation - Aborting!");
    return false;
  }

  // If the request does not have any required reply variables, skip validation.
  var requirements = def["reply vars"];
  if (!requirements) {
    console.log("No query requirements found... Skipping validation.");
    return true;
  }

  // If the request has an unexpected requirement, abort with an error msg.
  if (!validateRequirements(requirements)) return false;

  // Ensure a (legal) mode is defined, if required
  if (requirements.includes("mode")) {
    var mode = request["mode"];
    if (!validateMode(mode)) return false;
  }

  // Ensure a (legal) k value is defined, if required
  if (requirements.includes("k")) {
    var k = request["k"];
    if  (!validateK(k)) return false;
  }

  // Ensure a (legal) selList value is defined, if required
  if (requirements.includes("selList")) {
    var selList = request["selList"];
    if (!validateSelList(selList)) return false;
  }
  // Ensure a (legal) sel value is defined, if required
  // (this just means selList is legal, and has length 1)
  if (requirements.includes("sel")) {
    var selList = request["selList"];
    if (!validateSel(selList)) return false;
  }

  // All checks passed, query is valid!
  return true;
}

// Submission handler to send AJAX requests to server
// TODO Document the fields of the submission

// Extract the information from each of the active trait divs, and send a POST
// containing a list of requests as the payload
// responseType specifies whether to send a query request (Expects answer as a list)
// or a graph request (Expects answer as raw data to be plotted)
function handleSubmit(responseType) {
  if (!responseType) responseType = QUERY;

  var requests = [];

  // Build a request (dict/object) for each active trait
  var $traits = getActiveTraits();
  for (var i = 0; i < $traits.length; i++) {
    var $t = $traits.eq(i);
    var requestParams = {}; // stores vars to be sent to server for query

    // Obtain the definition of this query type from selectors_const.js
    var trait = $t.attr("type");
    var def = SELECTORS_DICT[trait];

    // Abort with an error msg if the provided trait lacks a definition in selectors_const.js
    if (!def) {
      console.error("Encountered unexpected trait while building request - Aborting!");
      return false;
    }

    // Get the required variables for this query type, or [] if none are found.
    var requirements = def["reply vars"];
    if (!requirements) requirements = [];

    // If the request has unexpected requirement, skip this query; show err msg
    if (!validateRequirements(requirements)) continue;

    // TODO: Consider integrating validation directly in this step.
    // No need to validate the query as a whole if we validate all its subparts
    // directly.

    var replyParams = {}; // stores vars to be inserted into reply str.

    // Extract and process the mode info from trait div
    if (requirements.includes("mode")) {
      var mode = $t.find(".mode-selector").val();
      replyParams["mode"] = mode;
      requestParams["mode"] = mode;
    }

    // Extract and process the k info from trait div
    if (requirements.includes("k")) {
      var k = $t.find(".k-selector").val();
      replyParams["k"] = k;
      requestParams["k"] = k;
    }

    // Extract and process the selList info from trait div
    if (requirements.includes("selList")) {
      var selList = $t.attr("selList");
      var prettySelList = "prettySelList";
      if (selList) {
        selList = selList.split(",");
        prettySelList = selList.join(", ");

        // If this is a class query, prettify the string even further.
        if (def["mode"] == "pick class") {
          var type = (def["html id"] == "consonant-class-selector" ? "consonant" : "vowel");
          prettySelList = getStrFromClasses(selList, type);
        }

      }
      replyParams["selList"] = prettySelList;
      requestParams["selList"] = selList;
    }

    // Extract and process the sel info from trait div
    if (requirements.includes("sel")) {
      var selList = $t.attr("selList");
      if (selList) selList = selList.split(",");

      if (!validateSel(selList)) {
        // TODO centralize error checking in a nicer way
        console.log("Skipping an invalid request");
        continue;
      }
      /*
      if (!(selList && selList.length == 1)) {
        console.error("Malformed sel (replace this err with proper validation)");
        continue;
      }
      */
      sel = selList[0];
      replyParams["sel"] = sel;
      requestParams["selList"] = selList;
      requestParams["sel"] = sel;
    }

    // Generate the reply string.
    // TODO: no reason to keep this clientside, might as well do in py.
    var reply = def["reply"];
    if (!reply) {
      console.error(`No reply string defined for ${trait}`);
      continue;
    }

    for (var r of requirements) {
      reply = reply.replace("%s", replyParams[r]);
    }

    // Create a request and add it to the request list
    requestParams["trait"]        = trait;
    requestParams["reply"]        = reply;

    // If this request is invalid, don't consider it.
    if (!validateRequest(requestParams)) {
      console.log("Skipping an invalid request...");
      continue;
    }

    requests.push(requestParams);
  }

  // If there are no requests to send, don't send anything
  if (requests.length == 0) {
    console.log("No valid requests specified, aborting without submitting...");
    return;
  }

  var payload = "payload=" + JSON.stringify(requests);
  // Hacky: build a request string from params directly.
  payload += `&listMode=${listMode}`;
  payload += `&dataset=${DATASET}`;
  payload += `&responseType=${responseType}`;

  console.log("Sending post with payload: " + payload);
  $.post("/",
         payload,
         callback
       );
}

// Handle clicks on the collapsible list button
// Does nothing unless REMEMBER_LIST_STATE = true.
// If so, update the state of the matching language list to be either expanded/collapsed
function handleListToggle() {
  if (!REMEMBER_LIST_STATE) return;
  listMode = !listMode;
}

/*****************************************************************************/
/*                                 Resets                                    */
/*****************************************************************************/

// Reset all entered values and selections
function resetQuerySelections() {
  if (!confirm("Are you sure you wish to clear all selections?")) return;

  // Reload the entire page.
  frontInit(); // hopefully this isn't overkill
}

// Reset the output box to its default state
function resetResults() {
  displayInfo("Submit a valid query to get started.");
}

// Reset the queries and results
// This involves de-selecting any selected elements, and clearing the results
function handleReset() {
  resetQuerySelections();
  resetResults();
}

/*****************************************************************************/
/*                                Callback                                   */
/*****************************************************************************/
// Callback function for AJAX -- in development
function callback(response) {
  response = JSON.parse(response);

  // Extract the reply fields
  // TODO: Remove hardcoded strings, put them in the constants js file
  var retCode = response["code"];
  var message = response["payload"];
  var data = response["data"];

  // Make sure the results div is in the correct mode.
  var mode = `alert-${retCode}`;
  setOutputMode(mode)

  // Display the results.
  $("#results").html(message);

  reloadTooltips();

  // Experimental: Draw the graphs for which data was provided
  // if (data != "") {
  //   // TODO: Make these headers general.
  //   headers = ["phoneme", "occurrences"];
  //   options = {};
  //
  //   drawBarChart(data, headers, options)
  // }
}

/*****************************************************************************/
/*                                Creators                                   */
/*****************************************************************************/

// Create and return a new selector DOM element as a string
// Use the string jqueryStr to locate the selector template to be copied.
// BUG Currently all instances share same id
// NOTE outerHTML not compatible with older browsers!'
// TODO rename copySelectorFromTemplate
function createSelectorString(jqueryStr) {
  if (!jqueryStr) {
    console.error("Error: creating selector string without ID!");
    jqueryStr = "#cbox-template";
  }

  // Locate the template
  var template = $(jqueryStr)[0];

  // Alter template so it can be displayed (remove template markings)
  var oldID = template.id;
  $(template).removeClass("template");
  $(template).attr("id", "");

  var str = template.outerHTML;

  // Undo alterations to template so it is suitable for copying again
  template.id = oldID;
  template.classList.add("template");

  return str;
}

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

// Given an array of the natural classes desired, prettify a string that combines
// all requested classes in a human readable way.
function getStrFromClasses(arr, type) {
  if (!type || !["consonant", "vowel"].includes(type)) {
    console.error("Bad type provided to getStrFromClasses!");
    type = "consonant";
  }

  var VOICING = 0;
  var PLACE   = 1;
  var MANNER  = 2;

  var str = "";

  // Was the given trait filtered?
  var flags = [];
  for (var i = 0; i < flags.length; i++) {
    flags.push(false);
  }
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
