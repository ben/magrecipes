var ingredientnames = [];

var next_ingredient_index = 0;

function add_new_ingredient_row()
{
  // Add the row
  $('#ingredienttable > tbody:last').append(
    '<tr class="ingrediententry"> \
<td><input class="ingredientnamefield" name="ingredient' + next_ingredient_index + '" /></td> \
<td><input name="amount' + next_ingredient_index + '" /></td> \
<td><input name="note' + next_ingredient_index + '" /></td>'
  );
  // Enable autocomplete
  $( ".ingredientnamefield" ).autocomplete({
	 source: ingredientnames,
    delay: 0,
  });
  // Increment identifiers
  next_ingredient_index++;      
}

$(function() {
  $("button, input:submit").button()

  add_new_ingredient_row();

  $("#morerows").click(function() {
    add_new_ingredient_row();
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
