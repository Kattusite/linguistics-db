/*
 * JavaScript to handle graphs and visualizations through the google charts API
 *
 */

var googleChartsLoaded = false;

function initGraphs() {
  google.charts.load('current', {'packages':['corechart', 'bar']});
  google.charts.setOnLoadCallback(readyToDraw);
}


function readyToDraw() {
  googleChartsLoaded = true;
}

DEFAULT_CHART_OPTIONS = {
  'title': 'Language Data',
  'width': 400,
  'height': 300,
}

// Given a dictionary of options, return a dictionary with default values
// filled in for missing option entries.
// This modifies the original options.
function setDefaultOptions(options) {
  for (let key in DEFAULT_CHART_OPTIONS) {
    if (! key in options) {
      options[key] = DEFAULT_CHART_OPTIONS[key];
    }
  }
}

function drawBarChart(rawData, dataHeaders, options) {

  if (dataHeaders.length != rawData[0].length) {
    console.error("Length mismatch in chart data headers!");
    return;
  }

  // Create the data table.
  var data = new google.visualization.DataTable();

  // TODO: generalize to any # of columns
  data.addColumn('string', dataHeaders[0]);
  data.addColumn('number', dataHeaders[1]);
  data.addRows(rawData);

  // Set chart options
  // var options = {'title':chartTitle,
  //             'width':400,
  //             'height':300};

  setDefaultOptions(options);

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.charts.Bar(document.getElementById('chart_div'));
  chart.draw(data, options);
}
