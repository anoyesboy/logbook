function get_flight_detail(e) {
  var target = e.target;
  var targetParent = target.parentNode;

  if (targetParent.hasAttribute('href')) {
    var targetURL = targetParent.getAttribute("href");
    
    var allRows = document.querySelectorAll('#flights tr');
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
        var newContent = "<h3>Flight Details</h3>";
        newContent += "<div><dl><dt>Date</dt><dd>" + responseObj.date + "</dd>";
        newContent += "<dt>Tail Number</dt><dd>" + responseObj.tail + "</dd></dl>";
        newContent += "<dl><dt>Regulation</dt><dd>Part " + responseObj.reg + "</dd>";
        newContent += "<dt>Make and Model</dt><dd>" + responseObj.make + " " + responseObj.model + "</dd></dl></div>";
        var route = "", tip, city, state, country;
        for (var i = 0; i < responseObj.airports.length; i++) {
          city = responseObj.airports[i].city;
          state = responseObj.airports[i].state;
          country = responseObj.airports[i].country;
          tip  = city + ", " + state + ", " + country;
          route += "<span title=\"" + tip + "\">" + responseObj.airports[i].identifier + "</span>";
          if (i < responseObj.airports.length - 1) {
            route += " - ";
          }
        }
        newContent += "<h3>Route</h3><p>" + route + "</p>";
        newContent += "<h3>Flight Times</h3>";
        newContent += "<div><dl><dt>Flight Time</dt><dd>" + responseObj.flight_time + " hr</dd>";
        newContent += "<dt>Night</dt><dd>" + responseObj.night + " hr</dd>";
        newContent += "<dt>Actual Instrument</dt><dd>" + responseObj.actual + " hr</dd>";
        newContent += "<dt>Simulated Instrument</dt><dd>" + responseObj.simulated + " hr</dd>";
        if (responseObj.x_c) {
          newContent += "<dt>Cross Country Time</dt><dd>" + responseObj.flight_time + " hr</dd></dl>";
        } else {
          newContent += "</dl>";
        }
        newContent += "<dl><dt>Crew Position</dt><dd>" + responseObj.crew_position + "</dd>";
        newContent += "<dt>Simulator Time</dt><dd>" + responseObj.simulator + " hr</dd>";
        if (responseObj.solo) {
          newContent += "<dt>Solo Time</dt><dd>" + responseObj.flight_time + " hr</dd></dl></div>";
        } else {
          newContent += "</dl></div>";
        }
        newContent += "<h3>Flight Instruction</h3>";
        newContent += "<div><dl><dt>Flight Instructor</dt><dd>" + responseObj.instructor + "</dd></dl>";
        newContent += "<dl><dt>Student</dt><dd>" + responseObj.student + "</dd></dl></div>";
        newContent += "<h3>Takeoffs and Landings</h3>";
        newContent += "<div><dl><dt>Day Takeoffs</dt><dd>" + responseObj.takeoff_day + "</dd>";
        newContent += "<dt>Night Takeoffs</dt><dd>" + responseObj.takeoff_night + "</dd></dl>";
        newContent += "<dl><dt>Day Landings</dt><dd>" + responseObj.landing_day + "</dd>";
        newContent += "<dt>Night Landings</dt><dd>" + responseObj.landing_night + "</dd></dl></div>";
        newContent += "<h3>Instrument Procedures</h3>";
        var approaches = "None";
        var numApps = responseObj.approach.length;
        if (numApps > 0) {
          approaches = "";
          for (var i = 0; i < numApps; i++) {
            approaches += responseObj.approach[i];
            if (i < numApps - 1) {
              approaches += ", ";
            }
          }
        }
        var holding = "No";
        if (responseObj.hold) {
          holding = "Yes";
        }
        newContent += "<div><dl><dt>Approaches</dt><dd>" + approaches + "</dd></dl>";
        newContent += "<dl><dt>Holding</dt><dd>" + holding + "</dd></dl></div>";
        newContent += "<h3>Remarks</h3><p>" + responseObj.remarks + "</p>";
      }
      document.getElementById("flight-detail").innerHTML = newContent;
    }
    xhr.open("GET", targetURL, true);
    xhr.send(null);
    e.preventDefault();
  }
}
var flights = document.getElementById("flights");
flights.addEventListener("click", function(e) {
  get_flight_detail(e);
}, false);

