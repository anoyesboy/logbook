function get_flights(e) {
  var target = e.target;
  var targetParent = target.parentNode;

  if (targetParent.hasAttribute('href')) {
    var targetURL = targetParent.getAttribute("href");
    var allAirports = document.querySelectorAll('#airports tr');
    if (allAirports.length > 0) {
      for (var i = 0; i < allAirports.length; i++) {
        allAirports[i].setAttribute('class','');
      }
    }
    targetParent.setAttribute('class','on');

    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      if (xhr.status === 200) {
        var responseObj = JSON.parse(xhr.responseText);
        var route = "";
        var newContent = "<h3>Flights</h3><table><tr><th>Date</th><th>Tail</th><th>Route</th></tr>";
        for (var i = 0; i < responseObj.flights.length; i++) {
          newContent += "<tr><td>" + responseObj.flights[i].date + "</td><td>" + responseObj.flights[i].tail_number + "</td>";
          route = responseObj.flights[i].route;
          if (route.length > 20) {
            route = route.substring(0, 22) + " ...";
          }
          newContent += "<td>" + route + "</td></tr>";
        }
        newContent += "</table>";
      }
      document.getElementById("flights").innerHTML = newContent;
    }
    xhr.open("GET", targetURL, true);
    xhr.send(null);
    e.preventDefault();
  }
}
var airports = document.getElementById("airports");
airports.addEventListener("click", function(e) {
  get_flights(e);
}, false);

