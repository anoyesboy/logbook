var tailSelect = document.getElementById("tail_id");
tailSelect.addEventListener('change', (e) => {
  var newTail = document.getElementById("new_tail_number");
  if (e.target.value == 0) {
    newTail.setAttribute('class', '');
  } else {
    newTail.setAttribute('class', 'hide');
  }
}, false);

var instructorSelect = document.getElementById("instructor_id");
var newInstructor = document.getElementById("instructor");
instructorSelect.addEventListener('change', (event) => {
  if (event.target.value == 0) {
    newInstructor.setAttribute('class', '');
  } else {
    newInstructor.setAttribute('class', 'hide');
  }
}, false);

var studentSelect = document.getElementById("student_id");
var newStudent = document.getElementById("student");
studentSelect.addEventListener('change', (event) => {
  if (event.target.value == 0) {
    newStudent.setAttribute('class', '');
  } else {
    newStudent.setAttribute('class', 'hide');
  }
}, false);
