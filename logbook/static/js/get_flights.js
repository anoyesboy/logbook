function get_flights(e) {
  var target = e.target;

  if (target.hasAttribute('href')) {
    var targetURL = target.getAttribute("href");
    var allMonths = document.querySelectorAll('#months a');
    if (allMonths.length > 0) {
      for (var i = 0; i < allMonths.length; i++) {
        allMonths[i].setAttribute('class','');
      }
    }
    target.setAttribute('class','on');

    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      if (xhr.status === 200) {
        var responseObj = JSON.parse(xhr.responseText);
        var route = "";
        var newContent = "<h3>Flights</h3><table id=\"flights-table\"><tr><th>Date</th><th>Tail</th><th>Route</th></tr>";
        for (var i = 0; i < responseObj.flights.length; i++) {
          newContent += "<tr href=\"/get_flight_detail/" + responseObj.flights[i].id + "\"><td>";
          newContent += responseObj.flights[i].date + "</td><td>" + responseObj.flights[i].tail + "</td>";
          route = responseObj.flights[i].route;
          if (route.length > 24) {
            route = route.substring(0, 22) + " ..."
          }
          newContent += "<td>" + route + "</td></tr>";
        }
        newContent += "</table>";
      }
      document.getElementById("flight-detail").innerHTML = "";
      document.getElementById("flights").innerHTML = newContent;
    }
    xhr.open("GET", targetURL, true);
    xhr.send(null);
    e.preventDefault();
  }
}
var months = document.getElementById("months");
months.addEventListener("click", function(e) {
  get_flights(e);
}, false);

