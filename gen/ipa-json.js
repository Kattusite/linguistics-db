var places = [];
var manners = [];
var voicings = ["voiceless", "voiced"];


// Populate the place + manner arrays
function init() {
  var tbody = $("tbody")[0];
  var rows = tbody.children;

  for (var i = 0; i < rows.length; i++) {
    var cols = rows[i].children;

    for (var j = 0; j < cols.length; j++) {
      // First row contains headers.
      if (i == 0) {
        // Skip placeholder
        if (j == 0) continue;
        places.push(cols[j].innerText.trim().toLowerCase());
      }

      // Later rows contain just a first element as label
      else {
        // Only care about first entry (header)
        if (j != 0) continue;
        manners.push(cols[j].innerText.trim().toLowerCase());
      }
    }
  }
}

// Go thru table extracting place/manner/voicing from position
function scrape() {
  console.log("Scraping headers...");
  init();
  console.log("places: " + places);
  console.log("manners: " + manners);
  console.log("voicings: " + voicings);

  var tbody = $("tbody")[0];

  var ipa_arr = [];

  var rows = tbody.children;
  for (var i = 0; i < rows.length; i++) {
    row = rows[i];
    tds = $(row).children("td").toArray();
    for (var j = 0; j < tds.length; j++) {
      var ipa_obj = {};
      var td = tds[j];
      var glyph = tds[j].innerText.trim();

      var place = places[Math.floor(j / 2)];
      var manner = manners[i-1];
      var voicing = voicings[j % 2];

      console.log("places: j=" + j + "  j/2=" + j/2);

      ipa_obj["glyph"] = glyph;
      ipa_obj["manner"] = manner;
      ipa_obj["place"] = place;
      ipa_obj["voicing"] = voicing;
      ipa_obj["producible"] = true;

      // If impossible: Store that it is impossible in the array
      if ($(td).hasClass("ipa-cell-impossible")) {
        ipa_obj["glyph"] = "impossible";
        ipa_obj["producible"] = false;

        ipa_arr.push(ipa_obj);
      }

      // If glyph exists: store an ipa obj in the array
      else if ($(td).hasClass("ipa-cell")) {
        ipa_arr.push(ipa_obj);
      }

      // If empty, do not add to arr (do nothing)
    }
  }

  console.log("\n\n\n\n==========================\n\n");
  console.log(JSON.stringify(ipa_arr, null, 4));
}
