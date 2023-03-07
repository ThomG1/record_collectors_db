/*
    jQuery for MaterializeCSS initialization
*/

let selects = document.querySelectorAll("select");
M.FormSelect.init(selects);

$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $("select").formSelect();
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