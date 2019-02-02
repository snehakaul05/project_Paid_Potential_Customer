// Anjali's plotting functions
//function for populations";
// console.log("Lets Start plot population");


function countFrequency(arr) {
  result = { };
  for(var i = 0; i < arr.length; ++i) {
      if(!result[arr[i]])
          result[arr[i]] = 0;
      ++result[arr[i]];
  }
  return result;
}
function topURLPlot() {

  let url_all = `allCustomerData`; 
 
  d3.json(url_all).then(function(response) {
    // console.log(response);
    urls = response.map(customerData => customerData.most_hit_topic);
    //console.log(urls);
    var results;
    results = countFrequency(urls);
    var trace= {
      type: "bar",
      name: "Top URL Count",
      orientation:'v',
      marker: {
        color: ('coral'),
        opacity: 0.8,
        line: {
          color: 'rgb(8,48,107)',
          width: 1.5
         }
        },
      x:Object.keys(results) ,
      y:Object.values(results)
      
    };


    var layout = {
      title: "Top URL Hits Across Categories",
      xaxis: {
				tickangle : -30,
				title: "URL Categories"
      },
      yaxis: {
        autorange: true,
			
				title: "Number Of URL Hits"
      }
    };
		

    var data = [trace];
 
    
    
    Plotly.newPlot("url-plot", data,layout);

});
}




function displayPredict(){
  var age = d3.select("#age");
  var timeSpent  = d3.select("#timeSpent");
  var vmCount = d3.select("#vmCount");
  var urlCount = d3.select("#urlCount");
  let url = `/predict/${timeSpent}/${age}/${vmCount}/${urlCount}`; 

  d3.json(url_all).then(function(response) {
    console.log(response);



  });

}


		
  
	
topURLPlot();