var ingredientnames = [
  {% for i in ingredients %}
  "{{i.name}}", 
  {% endfor %}
];

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

  

});
