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

function selectInSet(set) {
  for (i in set) {
    $("#" + set[i]).attr('checked', true);
  }
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
    selectInSet(springMonths);
    return false;
  });
  $('#summer').click (function() {
    selectInSet(summerMonths);
    return false;
  });
  $('#autumn').click (function() {
    selectInSet(autumnMonths);
    return false;
  });
  $('#winter').click (function() {
    selectInSet(winterMonths);
    return false;
  });
  $('#none').click (function() {
    $('div.months input').attr('checked', false)
    return false;
  });
  $('#all').click(function() {
    $('div.months input').attr('checked', true)
    return false;
  })
});
