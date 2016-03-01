/*function checkUserName(element) {
	var a = element.value
	var id = "#".concat(element.id);
	if (a.length < 4 || a.length > 30) {
		//disable other input
		$("input").prop("disabled",true);
		//Enable current input
		//$(id).get(0).setCustomValidity('Passwords must match');
		$(id).prop("disabled", false);
		$(element).attr("style","background-color: #9F6000;");
		$(element).attr("data-toggle","tooltip");
		$(element).attr("title","User ID must be between 4 and 30 characters");
	} else {
		$("input").prop("disabled",false);
		$(element).removeAttr("style");
		$(element).removeAttr("data-toggle");
		$(element).removeAttr("title");
	}
}

$(document).ready(function() {
	
	//Fucntion handling individual text box
	$("input").focusout(function() {
		var id = $(this).attr("id");

		switch (id) {
		case "id_user_name":
			checkUserName(this);
			break;
		case "id_first_name":
			break;
		case "id_last_name":
			break;
		case "id_email":
			break;
		case "id_passworda":
			break;
		case "id_passwordb":
			break;
		default:
			//
		}
	});
	
	//fucntion handling click of button
	$("#formButton").click(function(e) { // using click function
		// on contact form submit button
		e.preventDefault(); // stop form from submitting right away
		var error = false;
		if (!error) { // if not any errors
			$("#formButton").submit(); // you submit form
		}
	});
	
	
});*/