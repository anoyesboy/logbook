function get_airplane(e) {
  var target = e.target;
  var targetParent = target.parentNode;

  if (targetParent.hasAttribute('href')) {
    var targetURL = targetParent.getAttribute("href");
    
    var allRows = document.querySelectorAll('#airplanes tr');
    if (allRows.length > 0) {
      for (var i = 0; i < allRows.length; i++) {
        allRows[i].setAttribute('class','');
      }
    }
    targetParent.setAttribute('class', 'on');

    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      if (xhr.status === 200) {
        var responseObj = JSON.parse(xhr.responseText);
        var makeModelContent = "<h3>Make and Model</h3>";
        makeModelContent += "<div><dl><dt>Tail Number</dt><dd>" + responseObj.tail_number + "</dd>";
        makeModelContent += "<dt>Make and Model</dt><dd>";
        var nickName;
        if (responseObj.nickname) {
          nickName = responseObj.nickname;
        } else {
          nickName = "";
        }
        makeModelContent += responseObj.make + " " + responseObj.model + " " + nickName + "</dd>";
        makeModelContent += "<dt>Engine Type</dt><dd>" + responseObj.engine_type + "</dd>";
        makeModelContent += "<dt>Complex</dt><dd>" + responseObj.is_complex + "</dd></dl>";
        makeModelContent += "<dl><dt>Category and Class</dt><dd>" + responseObj.cat_class + "</dd>";
        if (responseObj.type_rating) {
          makeModelContent += "<dt>Type Rating</dt><dd>" + responseObj.type_rating + "</dd>";
        }
        makeModelContent += "<dt>Gear Design</dt><dd>" + responseObj.gear_design + "</dd>";
        makeModelContent += "<dt>Gear System</dt><dd>" + responseObj.gear_system + "</dd></dl></div>";

        var flightContent = "<h3>Flights</h3>";
        flightContent += "<table><tr><th>Date</th><th>Route</th><th>Time</th></tr>";
        var route = "";
        for (var i = 0; i < responseObj.flights.length; i++) {
          flightContent += "<tr><td>" + responseObj.flights[i].date + "</td>";
          route = responseObj.flights[i].route;
          if (route.length > 36) {
            route = route.substring(0, 36) + " ...";
            flightContent += "<td title=\"" + responseObj.flights[i].route + "\">" + route + "</td>";
          } else {
            flightContent += "<td>" + route + "</td>";
          }
          flightContent += "<td>" + responseObj.flights[i].flight_time + " hr</td></tr>";
        }
        flightContent += "</table>";
      }
      document.getElementById("make-model").innerHTML = makeModelContent;
      document.getElementById("airplane-flights").innerHTML = flightContent;
    }
    xhr.open("GET", targetURL, true);
    xhr.send(null);
    e.preventDefault();
  }
}
var flights = document.getElementById("airplane-table");
flights.addEventListener("click", function(e) {
  get_airplane(e);
}, false);

