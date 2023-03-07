/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $(".datepicker").datepicker({
      format: "dd mmmm, yyyy",
      yearRange: 100,
      showClearBtn: true,
      i18n: {
          done: "Select"
      }
  });
});

/* Adds materialize expandable accordian */

var elem = document.querySelector('.collapsible.expandable');
var instance = M.Collapsible.init(elem, {
  accordion: false
});