/*
 * Scripts for the survey filling portion of the site.
 * First thought is to do it manually by tacking links together, but this
 * is definitely a hack.
 *
 * More correct way would be using Apps Script API:
 https://developers.google.com/apps-script/reference/forms/form-response#withItemResponse(ItemResponse)
 https://developers.google.com/apps-script/api/how-tos/enable#using_the_apps_script_api_in_your_app
 https://developers.google.com/apps-script/guides/services/authorization
 *
 * It would be lovely to get this working but might be a better idea
 * to prioritize graphs & visualizations - google forms works OK for now
 */

surveyPrefix = "https://docs.google.com/forms/d/e/";
surveySuffix = "/viewform?";
surveySample = "entry.940131576=43&entry.512319289=33";


// Pre-filled Forms URLs
surveys = {
  F17: [

  ],
  S19: [
    "1FAIpQLSfmWpC_QZFkEo6xIE41TdykNADlnpDJyAG0_alO3z54ee9Ytw",
    "1FAIpQLSeR9sSG9Ca6duTNtMLhlrOWeuj9uMtnN8MYqBRlV4gTIHPf9A"
  ],
};

// This function is intended to be run on the google sheets site, not this site.
// It rips the entry IDs for the survey.
function ripIDs() {
  ids = {}

  inputs = $("div input[name]");
  for (let p of inputs) {
    name = $(p).attr("name");
    text = $(p).attr("aria-label");
    text = $(p).parent().text();
    ids[name] = text;
  }

  console.log(ids);
}


// Initialize everything needed for the survey autofiller
function surveyInit() {
  frontInit();


}

// Generate the link for the
function handleSurveySubmit() {
  let url = "http://www.google.com";


  window.location.href = url;
}
