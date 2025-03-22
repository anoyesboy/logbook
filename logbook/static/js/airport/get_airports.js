function get_airports(e) {
  var target = e.target;
  var targetParent = target.parentNode;

  if (targetParent.hasAttribute("href")) {
    var targetURL = targetParent.getAttribute("href");
    
    var allCountries = document.querySelectorAll('#countries tr');
    if (allCountries.length > 0) {
      for (var i = 0; i < allCountries.length; i++) {
        allCountries[i].setAttribute('class','');
      }
    }
    targetParent.setAttribute('class','on');

    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
      if (xhr.status === 200) {
        var responseObj = JSON.parse(xhr.responseText);
        var newContent = "";
        if (responseObj.has_states) {
          for (var i = 0; i < responseObj.states.length; i++) {
            newContent += "<h3>" + responseObj.states[i].descr + "</h3>";
            newContent += "<table><tr><th class=\"airport-ident\">Airport</th><th>City</th></tr>";
            for (var j = 0; j < responseObj.states[i].airports.length; j++) {
              newContent += "<tr href=\"/airport/" + responseObj.states[i].airports[j].id + "/get_flights\"><td>";
              newContent += responseObj.states[i].airports[j].identifier + "</td>";
              newContent += "<td>" + responseObj.states[i].airports[j].city + "</td></tr>";
            }
            newContent += "</table>";
          }
        } else {
          newContent += "<h3>Airports</h3><table><tr><th class=\"airport-ident\">Airport</th><th>City</th></tr>";
          for (var i = 0; i < responseObj.airports.length; i++) {
            newContent += "<tr href=\"/airport/" + responseObj.airports[i].id + "/get_flights\"><td>";
            newContent += responseObj.airports[i].identifier + "</td>";
            newContent += "<td>" + responseObj.airports[i].city + "</td></tr>";
          }
        }
        newContent += "</table>";
      }
      document.getElementById("flights").innerHTML = "";
      document.getElementById("airports").innerHTML = newContent;
    }
    xhr.open("GET", targetURL, true);
    xhr.send(null);
    e.preventDefault();
  }
}
var countries = document.getElementById("countries");
countries.addEventListener("click", function(e) {
  get_airports(e);
}, false);

