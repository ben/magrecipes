var ingredientnames = [];

var next_ingredient_index = 0;

var springMonths = [
  "March",
  "April",
  "May",
];
var summerMonths = [
  "June",
  "July",
  "August",
];
var autumnMonths = [
  "September",
  "October",
  "November",
];
var winterMonths = [
  "January",
  "February",
  "December",
];
var allMonths = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
function selectInSet(set, value) {
  for (i in set) viewModel[set[i]](value);
}


$(function() {
  // JQuery buttons
  $("button, input:submit").button()

  // Month dropdown selection and reset logic
  $("#monthselect").attr('selectedIndex', 0); // Reset to base state when using the back button
  $("#monthselect").change(function() {
    var idx = this.selectedIndex;
    if (idx != 0) {
      window.location = "/" + this.options[idx].text;
    }
  });

  // Delete-confirm logic
  $(".deleteinit").click(function() {
    $(".deleteconfirm").show();
    return false;
  })
  $(".deleteconfirmyes").click(function() {
    this.parentNode.submit();
    return false;
  })
});
