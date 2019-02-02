// Function to initilize the page
function init() {

  var selector1 = d3.select("#selCustomer");
  
  d3.json("/allCustomers").then((data) => {

    data.customers.forEach((customer) => {
      selector1
        .append("option")
        .text(customer)
        .property("value", customer);
  
    });



    // Use the first country from the list to build the initial plots
    const customer = data.customers[0];
    topURLPlot();
    //mapPlot(1950);
    
  });
  


}


// Function to build new charts when select a country
function optionChangedCustomer(newCustomer) {

  customerInfo(newCustomer);
}


// Function to build new charts when select a country
function optionChangedCustomer(newCustomer) {

  customerInfo(newCustomer);
}

function customerInfo(customer) {
    console.log("Comonay have been selecetd " + customer);
    let url = `/customer_info/${customer}`; 
  
    d3.json(url).then(function(data) {
  
      // Select the panel with id of `#country-metadata`
      let panel = d3.select("#customer-metadata");
  
      // Clear any existing metadata
      panel.html("");
  
      let div = panel.append("div");
      Object.entries(data).forEach(function([key, value]) {
        if (!value) {
          div.append("p").text(`${key}: N/A`);
        } else {
          div.append("span").attr("class", "customer-info").text(`${key}: ${value}`);
          div.append("br")
          //div.append("span").text(`${value}`);
        }     
      });
    });
  }
  


init();
