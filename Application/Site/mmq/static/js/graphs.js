//q
//	.defer(d3.json, "/data/nfl/?down=1&quarter=4&PlayType=kneel")
//	.await(makeGraphs);

function makeGraphs(error, guessesJSON, nflJSON) {
	if (error) throw error;
	//Store the returned NFL JSON data
	alert(typeof guessesJSON)
	var guessesResults = guessesJSON;
	
	//Alert the user to the number of returned results
	if (guessesResults.length == 0){
		alert(guessesResults.length + ' results returned!')
	} else {
		alert(guessesResults.length + ' results returned!')
	}
	
	//Crossfilter
	var ndx = crossfilter(guessesResults);
	
	console.log(ndx.size())
	
	var all = ndx.groupAll();
	
}