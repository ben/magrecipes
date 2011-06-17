var ingredientnames = [];

var next_ingredient_index = 0;

function add_new_ingredient_row()
{
  // Add the row
  $('#ingredienttable > tbody:last').append(
    '<tr class="ingrediententry"> \
<td><input class="ingredientautocomplete" name="ingredient' + next_ingredient_index + '" /></td> \
<td><input name="amount' + next_ingredient_index + '" /></td> \
<td><input name="note' + next_ingredient_index + '" /></td>'
  );
  // Enable autocomplete
  refreshIngredientAutocomplete();
  // Increment identifiers
  next_ingredient_index++;      
}

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
  return false;
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

  // New-recipe form logic
  add_new_ingredient_row();

  $("#morerows").click(function() {
    add_new_ingredient_row();
    return false;
  });

  // Months subset selection
  $('#spring').click (function() {
    return selectInSet(springMonths, true);
  });
  $('#summer').click (function() {
    return selectInSet(summerMonths, true);
  });
  $('#autumn').click (function() {
    return selectInSet(autumnMonths, true);
  });
  $('#winter').click (function() {
    return selectInSet(winterMonths, true);
  });
  $('#none').click (function() {
    return selectInSet(allMonths, false);
  });
  $('#all').click(function() {
    return selectInSet(allMonths, true);
  })
});
