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

  $('#spring').click (function() {
    var selector = 'input[name=March], input[name=April], input[name=May]'
    $(selector).attr('checked', true)
    return false;
  });
  $('#summer').click (function() {
    var selector = 'input[name=June], input[name=July], input[name=August]'
    $(selector).attr('checked', true)
    return false;
  });
  $('#autumn').click (function() {
    var selector = 'input[name=September], input[name=October], input[name=November]'
    $(selector).attr('checked', true)
    return false;
  });
  $('#winter').click (function() {
    var selector = 'input[name=December], input[name=January], input[name=February]'
    $(selector).attr('checked', true)
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
