(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

$(document).ready(function() {
	// show buttons on tr mouseover
	$(".hover tr").live("mouseenter", function() {
	  $(this).find("td:last-child").html('<a href="javascript:void(0);" onClick="editrow(' + $(this).attr("id") + ')">Edit</a>&nbsp;&nbsp;<a href="javascript:void(0);" onClick="deleterow(' + $(this).attr("id") + ')">Delete</a>');
	}); //
  
	// remove button on tr mouseleave
	$(".hover tr").live("mouseleave", function() {
	  $(this).find("td:last-child").html("&nbsp;");
	});
  
	// TD click event
	$(".hover tr").live("click", function(event) {
	  if (event.target.nodeName == "TD") {
		alert("You can track TD click event too....Isnt it amazing !!!");
	  }
	});
  });
  editrow = function(itemId) {
	alert("You clicked 'Edit' link with row id :" + itemId);
  }
  deleterow = function(itemId) {
	alert("You clicked 'Delete' link with row id :" + itemId);
  }
