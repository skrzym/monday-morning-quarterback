//q
//	.defer(d3.json, "/data/nfl/?down=1&quarter=4&PlayType=kneel")
//	.await(makeGraphs);
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

function makeGraphs(error, guessJSON, nflJSON, modelJSON) {
	if (error) throw error;
	//Store the returned NFL JSON data
	var guessResults = guessJSON;
	var nflResults = nflJSON;
	var modelResults = [modelJSON];
	
	console.log('guessJSON', guessResults);
	console.log('nflJSON', nflResults);
	console.log('modelJSON', modelResults);
	
	//Alert the user to the number of returned results
	if (guessResults.length == 0){
		alert('guessJSON: ' + guessResults.length + ' results returned!')
	} else if(nflResults.length == 0) {
		alert('nflJSON: ' + nflResults.length + ' results returned!')
	} else if(modelResults.length == 0){
		alert('modelJSON: ' + modelResults.length + ' results returned!')
	}
	
	// Create Charts
	var guessTable = dc.dataTable('#dc-guess-table');
	
	//Crossfilter
	var guessDX = crossfilter(guessResults);
	var guessDimension = guessDX.dimension(function(d){
		return d;
	});
	
	var guessAll = guessDX.groupAll();

	// Guess DataTable Details
	guessTable
	.width(960)
	.height(800)
    .dimension(guessDimension)
    .group(function(d) { return d.guess; })
	//.showGroups(true)
    .size(100)
    .columns([
	  'guess',
      'down',
      'quarter',
      'clock',
      'yards',
      'field',
	  'score'
    ])
    .sortBy(function(d){ return d.guess; })
    .order(d3.ascending);
	
	dc.renderAll();
};


//window.location.reload(true)
function makeGauges(error, modelResult){
		console.log(modelResult)
		
		var titleStyle={
			"font-weight": "bold",
			"font-size": "large",
			"color": "black"
		};
		
		var gaugeOptions = {

		chart: {
			type: 'solidgauge'
		},

		title: null,

		pane: {
			center: ['50%', '85%'],
			size: '100%',
			startAngle: -90,
			endAngle: 90,
			background: {
				backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
				innerRadius: '60%',
				outerRadius: '100%',
				shape: 'arc'
			}
		},

		tooltip: {
			enabled: false
		},

		// the value axis
		yAxis: {
			stops: [
				[0.25, '#DF5353'], // red
				[0.50, '#DDDF0D'], // yellow
				[0.90, '#55BF3B'] // green
			],
			lineWidth: 0,
			minorTickInterval: null,
			tickAmount: 1,
			title: {
				y: -50,
				style: {
					"font-weight": "bold",
					"font-size": "large",
					"color": "black"
				}
			},
			labels: {
				y: 16
			}
		},

		plotOptions: {
			solidgauge: {
				dataLabels: {
					y: 5,
					borderWidth: 0,
					useHTML: true
				}
			}
		}
	};

	// The Pass gauge
	var chartPass = Highcharts.chart('gauge-pass', Highcharts.merge(gaugeOptions, {
		yAxis: {
			min: 0,
			max: 100,
			title: {
				text: 'Pass - ' + modelResult.Pass + '%'
			}
		},

		credits: {
			enabled: false
		},

		series: [{
			name: 'Pass',
			data: [parseFloat(modelResult.Pass)],
			dataLabels: {
				format: '<div style="text-align:center"><span style="font-size:15px;color:' +
					((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
					   '<span style="font-size:12px;color:silver">%</span></div>'
			},
			tooltip: {
				valueSuffix: ' %'
			}
		}]

	}));
	
	// The Run gauge
	var chartRun = Highcharts.chart('gauge-run', Highcharts.merge(gaugeOptions, {
		yAxis: {
			min: 0,
			max: 100,
			title: {
				text: 'Run'
			}
		},

		credits: {
			enabled: false
		},

		series: [{
			name: 'Run',
			data: [parseFloat(modelResult.Run)],
			dataLabels: {
				format: '<div style="text-align:center"><span style="font-size:15px;color:' +
					((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
					   '<span style="font-size:12px;color:silver">%</span></div>'
			},
			tooltip: {
				valueSuffix: ' %'
			}
		}]

	}));
	
	// The Punt gauge
	var chartPunt = Highcharts.chart('gauge-punt', Highcharts.merge(gaugeOptions, {
		yAxis: {
			min: 0,
			max: 100,
			title: {
				text: 'Punt'
			}
		},

		credits: {
			enabled: false
		},

		series: [{
			name: 'Punt',
			data: [parseFloat(modelResult.Punt)],
			dataLabels: {
				format: '<div style="text-align:center"><span style="font-size:15px;color:' +
					((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
					   '<span style="font-size:12px;color:silver">%</span></div>'
			},
			tooltip: {
				valueSuffix: ' %'
			}
		}]

	}));
	
	// The Field Goal gauge
	var chartFg = Highcharts.chart('gauge-fg', Highcharts.merge(gaugeOptions, {
		yAxis: {
			min: 0,
			max: 100,
			title: {
				text: 'Field Goal'
			}
		},

		credits: {
			enabled: false
		},

		series: [{
			name: 'Field Goal',
			data: [parseFloat(modelResult['Field Goal'])],
			dataLabels: {
				format: '<div style="text-align:center"><span style="font-size:15px;color:' +
					((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
					   '<span style="font-size:12px;color:silver">%</span></div>'
			},
			tooltip: {
				valueSuffix: ' %'
			}
		}]

	}));
	
	// The QB Kneel gauge
	var chartKneel = Highcharts.chart('gauge-kneel', Highcharts.merge(gaugeOptions, {
		yAxis: {
			min: 0,
			max: 100,
			title: {
				text: 'QB Kneel'
			}
		},

		credits: {
			enabled: false
		},

		series: [{
			name: 'QB Kneel',
			data: [parseFloat(modelResult['QB Kneel'])],
			dataLabels: {
				format: '<div style="text-align:center"><span style="font-size:15px;color:' +
					((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
					   '<span style="font-size:12px;color:silver">%</span></div>'
			},
			tooltip: {
				valueSuffix: ' %'
			}
		}]

	}));
};