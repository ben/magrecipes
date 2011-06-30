var converter = new Attacklab.showdown.converter();

function stickyViewModel(obj) {
  this.text = obj.text;
  this.html = converter.makeHtml(obj.text);
  this.key = obj.key;
}

viewModel = {{ json|safe }};

viewModel.instructions_html = converter.makeHtml(viewModel.instructions)
viewModel.source_html = converter.makeHtml("Source: " + viewModel.source)

var stickies = viewModel.stickies;
viewModel.stickies = ko.observableArray();
for (var i=0; i<stickies.length; i++) {
  viewModel.stickies.push(new stickyViewModel(stickies[i]));
}

viewModel.enabledMonths = []
if (viewModel.january) { viewModel.enabledMonths.push("January"); }
if (viewModel.february) { viewModel.enabledMonths.push("February"); }
if (viewModel.march) { viewModel.enabledMonths.push("March"); }
if (viewModel.april) { viewModel.enabledMonths.push("April"); }
if (viewModel.may) { viewModel.enabledMonths.push("May"); }
if (viewModel.june) { viewModel.enabledMonths.push("June"); }
if (viewModel.july) { viewModel.enabledMonths.push("July"); }
if (viewModel.august) { viewModel.enabledMonths.push("August"); }
if (viewModel.september) { viewModel.enabledMonths.push("September"); }
if (viewModel.october) { viewModel.enabledMonths.push("October"); }
if (viewModel.november) { viewModel.enabledMonths.push("November"); }
if (viewModel.december) { viewModel.enabledMonths.push("December"); }

if (viewModel.enabledMonths.length == 12) viewModel.joinedMonths = "Year-round";
else if (viewModel.enabledMonths.length == 0) viewModel.joinedMonths = "No season";
else viewModel.joinedMonths = viewModel.enabledMonths.join(', ');

function bindStickyDeletes()
{
  $('.sticky .deleteconfirmyes').unbind('click').click(function() {
    var theKey = $(this).siblings('input').attr('value');
    $.post('/deletesticky',
           {key: theKey,},
           function(data) {
             for (var i in viewModel.stickies()) {
               if (viewModel.stickies()[i].key == theKey) {
                 viewModel.stickies.splice(i, 1);
                 return;
               }
             }
           });
    return false;
  })
}

$(function() {
  $('#stickyform').ajaxForm({
    dataType: 'text/javascript',
    success: function(data) {
      viewModel.stickies.push(new stickyViewModel(JSON.parse(data)));
      $('#stickyform textarea').attr('value', '');
      bindDeleteConfirmations();
      bindStickyDeletes();
    },
  });

  bindStickyDeletes(); 

});
