// Analytics
//var _gaq = _gaq || [];
//_gaq.push(['_setAccount', 'UA-696376-6']);
//_gaq.push(['_trackPageview']);
//
//(function() {
//  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
//  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
//  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
//})();

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

function bindDeleteConfirmations() {
  $(".deleteinit").unbind('click').click(function() {
    $(this).siblings(".deleteconfirm").toggle();
    return false;
  });
  $(".deleteconfirmyes").unbind('click').click(function() {
    this.parentNode.submit();
    return false;
  });
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

  bindDeleteConfirmations();

  $('#lucky a').hover(
    function(e) {$(e.target).addClass('hovering');},
    function(e) {$(e.target).removeClass('hovering');});
});

// Shamelessly stolen from http://skfox.com/jqExamples/insertAtCaret.html
$.fn.insertAtCaret = function (myValue) {
	return this.each(function(){
			//IE support
			if (document.selection) {
					this.focus();
					sel = document.selection.createRange();
					sel.text = myValue;
					this.focus();
			}
			//MOZILLA / NETSCAPE support
			else if (this.selectionStart || this.selectionStart == '0') {
					var startPos = this.selectionStart;
					var endPos = this.selectionEnd;
					var scrollTop = this.scrollTop;
					this.value = this.value.substring(0, startPos)+ myValue+ this.value.substring(endPos,this.value.length);
					this.focus();
					this.selectionStart = startPos + myValue.length;
					this.selectionEnd = startPos + myValue.length;
					this.scrollTop = scrollTop;
			} else {
					this.value += myValue;
					this.focus();
			}
	});
};
