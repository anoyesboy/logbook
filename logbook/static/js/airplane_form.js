var modelSelect = document.getElementById("model_id");
var makeModelColumn = document.getElementById("make-model-column");
var modelDetailsColumn = document.getElementById("model-details-column");
modelSelect.addEventListener('change', (event) => {
  if (event.target.value == 0) {
    makeModelColumn.setAttribute('class', 'column');
    modelDetailsColumn.setAttribute('class', 'column');
  } else {
    makeModelColumn.setAttribute('class', 'column hide');
    modelDetailsColumn.setAttribute('class', 'column hide');
  }
}, false);

var makeSelect = document.getElementById("make_id");
var newMakeLabel = document.getElementById("new-make-label");
var newMakeField = document.getElementById("new-make-field");
makeSelect.addEventListener('change', (event) => {
  if (event.target.value == 0) {
    newMakeLabel.setAttribute('class', '');
    newMakeField.setAttribute('class', '');
  } else {
    newMakeLabel.setAttribute('class', 'hide');
    newMakeField.setAttribute('class', 'hide');
  }
}, false);

var typeRatingSelect = document.getElementById("type_rating_id");
var newTypeRatingLabel = document.getElementById("new-type-rating-label");
var newTypeRatingField = document.getElementById("new-type-rating-field");
typeRatingSelect.addEventListener('change', (event) => {
  if (event.target.value == 0) {
    newTypeRatingLabel.setAttribute('class', '');
    newTypeRatingField.setAttribute('class', '');
  } else {
    newTypeRatingLabel.setAttribute('class', 'hide');
    newTypeRatingField.setAttribute('class', 'hide');
  }
}, false);
