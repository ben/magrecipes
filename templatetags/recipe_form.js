function ingredientViewModel(name, qty, note) {
  this.name = ko.observable(name);
  this.quantity = qty;
  this.note = note;
  this.flatten = function() {
    return {
      'name' : this.name(),
      'quantity' : this.quantity,
      'note' : this.note,
    }
  }
}

model = {{json|safe}};
model.ingredientArray = function() {
  var retval = [];
  for (var i=0; i<model.ingredients.length; i++)
  {
    ing = model.ingredients[i];
    retval.push(new ingredientViewModel(ing.ingredient.name, ing.quantity, ing.note));
  }
  return retval;
}

var converter = new Attacklab.showdown.converter();

// Define viewmodel
viewModel = {
  title: ko.observable(""),
  ingredients: ko.observableArray([]),
  instructions: ko.observable(""),
  yeeld: ko.observable(""),

  January: ko.observable(false),
  February: ko.observable(false),
  March: ko.observable(false),
  April: ko.observable(false),
  May: ko.observable(false),
  June: ko.observable(false),
  July: ko.observable(false),
  August: ko.observable(false),
  September: ko.observable(false),
  October: ko.observable(false),
  November: ko.observable(false),
  December: ko.observable(false),

  doSubmit: function() {
    model.title = viewModel.title();
    model.ingredients = []
    for (i in viewModel.ingredients()) {
      d = viewModel.ingredients()[i].flatten()
      if (d['name'] != '')
        model.ingredients.push(d)
    }
    model.instructions = viewModel.instructions();
    model.yeeld = viewModel.yeeld();

    model.january = viewModel.January();
    model.february = viewModel.February();
    model.march = viewModel.March();
    model.april = viewModel.April();
    model.may = viewModel.May();
    model.june = viewModel.June();
    model.july = viewModel.July();
    model.august = viewModel.August();
    model.september = viewModel.September();
    model.october = viewModel.October();
    model.november = viewModel.November();
    model.december = viewModel.December();

    // Submit the form with proper data
    $('#json').attr('value', JSON.stringify(model))
    return true;
  }
};
viewModel.instructions_html = ko.dependentObservable(function() {
  return converter.makeHtml(this.instructions());
}, viewModel);

// Fill in viewmodel with model data
viewModel.title(model.title);
viewModel.ingredients(model.ingredientArray());
viewModel.instructions(model.instructions);
viewModel.yeeld(model.yeeld);
viewModel.January(model.january);
viewModel.February(model.february);
viewModel.March(model.march);
viewModel.April(model.april);
viewModel.May(model.may);
viewModel.June(model.june);
viewModel.July(model.july);
viewModel.August(model.august);
viewModel.September(model.september);
viewModel.October(model.october);
viewModel.November(model.november);
viewModel.December(model.december);


// When last ingredient's name changes,
//   Add a new row to the list
//   Update the global subscription to point to the new item
function lastIngredientNameChanged(newValue) {
  var currentfocus = document.activeElement;
  if (newValue != '') {
    lastIngredientSubscription.dispose();
    viewModel.ingredients.push(new ingredientViewModel('','',''));
    lastIngredientSubscription = viewModel.ingredients()[viewModel.ingredients().length-1]
      .name.subscribe(lastIngredientNameChanged);
  }
  currentfocus.focus();
}
viewModel.ingredients.push(new ingredientViewModel('','',''));
var lastIngredientSubscription = viewModel.ingredients()[viewModel.ingredients().length-1].name.subscribe(lastIngredientNameChanged);


$(function() {
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
})
