
//Result Colors
var colors = {'pass':'#4daf4a','run':'#377eb8','punt':'#e41a1c','fg':'#ff7f00','kneel':'#984ea3'};
console.log(colors);
console.log(colors['pass']);

function makeTable(error, guessData){
    columns = [{
        field: 'PlayType',
        title: 'Play Type'
    }, {
        field: 'down',
        title: 'Down'
    }, {
        field: 'quarter',
        title: 'Quarter'
    }, {
        field: 'clock',
        title: 'Time Under'
    }, {
        field: 'yards',
        title: 'Yards to go'
    }, {
        field: 'field',
        title: 'Field Position'
    }, {
        field: 'score',
        title: 'Score Difference'
    }];
    $.extend($.fn.bootstrapTable.columnDefaults, {
  	   sortable: true
    });

    $('#table').bootstrapTable({
      columns: columns,
      data: guessData
    });
  };

function createModelChart(prediction){
  console.log('Creating Model Chart', prediction);
  Highcharts.chart('prediction-chart', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false,
        spacingTop: 0,
        spacingBottom: 0,
        spacingLeft: 0,
        spacingRight: 0,
        height:300,
    },
    title: {
        text: '',
        align: 'center',
        //verticalAlign: 'top',
        //y: 40,
    },
    subtitle: {
        text: 'Classification probabilities for each decision.',
        y: 30,
        style: {
          fontSize: '13px',
          fontFamily: '"Roboto","Helvetica Neue",Helvetica,Arial,sans-serif'
        }
    },
    tooltip: {
        pointFormat: '{point.percentage:.1f}%'
    },
    plotOptions: {
        pie: {
            stickyTracking: true,
            dataLabels: {
                enabled: true,
                distance: 25,
                style: {
                    fontWeight: 'bold',
                    color: 'black'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '85%']
        }
    },

    legend: {
      enabled: true
    },

    credits: false,

    series: [{
        type: 'pie',
        name: 'Browser share',
        innerSize: '50%',
        showInLegend: true,
        data: [
            { name: 'Pass' ,
              y: parseFloat(prediction.Pass),
              color: colors.pass,
              dataLabels: {enabled: parseFloat(prediction.Pass) > 10}
            },
            { name: 'Run',
              y: parseFloat(prediction.Run),
              color: colors.run,
              dataLabels: {enabled: parseFloat(prediction.Run) > 10}
            },
            { name: 'Punt',
              y: parseFloat(prediction.Punt),
              color: colors.punt,
              dataLabels: {enabled:parseFloat(prediction.Punt) > 10}
            },
            { name: 'FG',
              y: parseFloat(prediction['Field Goal']),
              color: colors.fg,
              dataLabels: {enabled:parseFloat(prediction['Field Goal']) > 10}
            },
            { name: 'Kneel',
              y: parseFloat(prediction['QB Kneel']),
              color: colors.kneel,
              dataLabels: {enabled:parseFloat(prediction['QB Kneel']) > 10}
            }
        ]
    }]
  });
};

function createNFLChart(data){
  console.log('Creating NFL Chart', data);
  $('#nfl-table').bootstrapTable({
        data: [
          {
            'playtype':'Pass',
            'count':parseFloat(data.pass)
          },
          {
            'playtype':'Run',
            'count':parseFloat(data.run)
          },
          {
            'playtype':'Punt',
            'count':parseFloat(data.punt)
          },
          {
            'playtype':'Field Goal',
            'count':parseFloat(data.fg)
          },
          {
            'playtype':'QB Kneel',
            'count':parseFloat(data.kneel)
          },
        ]
    });
};

function createGuessChart(data){
  console.log('Creating Guess Chart', data);
  $('#guess-table').bootstrapTable({
        data: [
          {
            'playtype':'Pass',
            'count':parseFloat(data.pass)
          },
          {
            'playtype':'Run',
            'count':parseFloat(data.run)
          },
          {
            'playtype':'Punt',
            'count':parseFloat(data.punt)
          },
          {
            'playtype':'Field Goal',
            'count':parseFloat(data.fg)
          },
          {
            'playtype':'QB Kneel',
            'count':parseFloat(data.kneel)
          },
        ]
    });
};

function makeData(data){
  var filters = ['Pass','Run','Punt','Field Goal','QB Kneel'];
  var newData = {};
  for (f in filters){
    newData[filters[f]]=[];
  };
  for(item in data){
    for(f in filters){
      newData[filters[f]].push([item,parseFloat(data[item][filters[f]])]);
    };
  };
  return newData;
};

function makeDetailChart(div, title, xAxisTitle, myData, myCategories){
  Highcharts.chart(div + '-detail-chart', {
		title:{
    		text:'Prediction Details - ' + title
    },
    xAxis: {
        //minPadding: 0.05,
        //maxPadding: 0.05,
        allowDecimals: false,
        labels: {
                formatter: function() {
                    return myCategories[this.value];
                }
        },
        title: {
          text: xAxisTitle
        },
        plotLines: [{
          color: '#000000', // Red
          width: 2,
          value: parseInt($('.sel-' + div).text()), // Position, you'll have to translate this to the values on your x axis
          zIndex:5
          /*label: {
                useHTML: true,
                text: ' Selected Value ',
                verticalAlign: 'bottom',
                textAlign: 'right',
                y:-15,
                x: -12,
                style: {
                  fontWeight: 'bold',
                  fontSize: '15px',
                  color: 'black'
                }
            }*/
        }]
    },
    tooltip: {
      pointFormat: '<span>{series.name}</span>: <b>{point.percentage:.2f}%</b>',
      split: true
    },
    plotOptions: {
        area: {
            stacking: 'percent',
            lineColor: '#ffffff',
            lineWidth: 1,
            marker: {
                lineWidth: 1,
                lineColor: '#ffffff'
            }
        }
    },
    credits:false,
    series: [{
        marker: {enabled: false},
    		name:'Pass',
    		type:'area',
        data: myData.Pass,
        color:colors.pass
    },{
        marker: {enabled: false},
        name:'Run',
    		type:'area',
        data: myData.Run,
        color:colors.run
    },{
        marker: {enabled: false},
    		name:'Punt',
    		type:'area',
        data: myData.Punt,
        color:colors.punt
    },{
        marker: {enabled: false},
    		name:'FG',
    		type:'area',
        data: myData['Field Goal'],
        color:colors.fg
    },{
        marker: {enabled: false},
    		name:'Kneel',
    		type:'area',
        data: myData['QB Kneel'],
        color:colors.kneel
    }]
  });
}

function createDetailCharts(data){
  console.log('Creating Detail Chart', data);

  //Chart Series Setup
  var qtrData = makeData(data[0]['quarter']);
  var downData = makeData(data[1]['down']);
  var yardsData = makeData(data[2]['yards']);
  var clockData = makeData(data[3]['timeunder']);
  var fieldData = makeData(data[4]['yrdline100']);
  var scoreData = makeData(data[5]['scorediff']);

  scoreData.Pass.sort(function(a,b){return parseInt(a[0])-parseInt(b[0]);})
  scoreData.Run.sort(function(a,b){return parseInt(a[0])-parseInt(b[0]);})
  scoreData.Punt.sort(function(a,b){return parseInt(a[0])-parseInt(b[0]);})
  scoreData['Field Goal'].sort(function(a,b){return parseInt(a[0])-parseInt(b[0]);})
  scoreData['QB Kneel'].sort(function(a,b){return parseInt(a[0])-parseInt(b[0]);})

  var qtrCategories = [1,2,3,4];
  var downCategories = [1,2,3,4];
  var yardsCategories = [];
  for (i=25;i>-1;i--){yardsCategories.push(i);};
  var clockCategories = [];
  for (i=15;i>0;i--){clockCategories.push(i);};
  var fieldCategories = [];
  for (i=100;i>-1;i--){fieldCategories.push(i);};
  var scoreCategories = [];
  for (i=-60;i<61;i++){scoreCategories.push(i);};

  for (item in yardsData){yardsData[item] = yardsData[item].reverse();};
  for (item in clockData){clockData[item] = clockData[item].reverse();};
  for (item in fieldData){fieldData[item] = fieldData[item].reverse();};

  //Quarter Chart
  makeDetailChart('quarter', 'Quarter', 'Quarter', qtrData, qtrCategories);
  makeDetailChart('down', 'Down', 'Down', downData, downCategories);
  makeDetailChart('yards', 'Yards to Go', 'Yards', yardsData, yardsCategories);
  makeDetailChart('clock', 'Time Left', 'Minutes', clockData, clockCategories);
  makeDetailChart('field', 'Yard Line', 'Yard Line', fieldData, fieldCategories);
  makeDetailChart('score', 'Score Delta', 'Point Difference', scoreData, scoreCategories);
};


function makeCharts(error, modelJSON, guessJSON, nflJSON) {
	if (error) throw error;
	//Store the returned NFL JSON data
	//Alert the user to the number of returned results
	if (guessJSON.length == 0){
		console.log('guessJSON: ' + guessJSON.length + ' results returned!')
	} else if(nflJSON.length == 0) {
		console.log('nflJSON: ' + nflJSON.length + ' results returned!')
	} else if(modelJSON.length == 0){
		console.log('modelJSON: ' + modelJSON.length + ' results returned!')
	}

	// Create Charts
  createModelChart(modelJSON[6].request);
  createNFLChart(nflJSON);
  createGuessChart(guessJSON);
  createDetailCharts(modelJSON);
  $('.chart-stage').slideDown(1000);
};
