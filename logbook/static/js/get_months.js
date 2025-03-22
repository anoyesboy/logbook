function get_months(e) {
  var target = e.target;
  var targetURL = target.getAttribute("href");
  
  var allYears = document.querySelectorAll('#years a');
  if (allYears.length > 0) {
    for (var i = 0; i < allYears.length; i++) {
      allYears[i].setAttribute('class','');
    }
  }
  target.setAttribute('class','on');

  var xhr = new XMLHttpRequest();
  xhr.onload = function() {
    if (xhr.status === 200) {
      var responseObj = JSON.parse(xhr.responseText);
      var newContent = "";
      for (var i = 0; i < responseObj.months.length; i++) {
        if (responseObj.months[i].in_year) {
          newContent += "<a href=\"/get_flights/" + responseObj.cur_year + "/" + responseObj.months[i].id + "\">";
          newContent += responseObj.months[i].name + "</a>";
        } else {
          newContent += "<span class=\"no-flights\">" + responseObj.months[i].name + "</span>";
        }
      }
    }
    document.getElementById("flights").innerHTML = "";
    document.getElementById("flight-detail").innerHTML = "";
    document.getElementById("months").innerHTML = newContent;
  }
  xhr.open("GET", targetURL, true);
  xhr.send(null);
  e.preventDefault();
}
var years = document.getElementById("years");
years.addEventListener("click", function(e) {
  get_months(e);
}, false);

