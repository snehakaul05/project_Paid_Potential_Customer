


// Select the upvote and downvote buttons
var predict_btn = d3.select(".predict");

console.log("2btn is clicked2")

// Use D3 `.on` to attach a click handler for the upvote
predict_btn.on("click", function() {
    console.log("2btn is clicked2")
    var age = d3.select("#age").property("value");
    var timeSpent  = d3.select("#timeSpent").property("value");
    var vmCount = d3.select("#vmCount").property("value");
    var urlCount = d3.select("#urlCount").property("value");
    console.log(age)
    console.log(timeSpent)
    let url = `/predict/${timeSpent}/${age}/${vmCount}/${urlCount}`;
    d3.json(url).then(function(response) {
      console.log(response);
      predict_msg = response[0];
      console.log("2nd response ")
      console.log(response);
      let panel = d3.select("#predict-metadata");
      panel.html("");
      let div = panel.append("div");
      Object.entries(response).forEach(function([key, value]) {
        if (!value) {
          div.append("p").text(`${key}: N/A`);
        } else {
          div.append("span").attr("class", "predict-info").text(`${value}`);
          div.append("br")
          //div.append("span").text(`${value}`);
        }     
      });
    });
});



