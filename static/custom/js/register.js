//include generic js
$(document).ready(function() {
	//Handle form submission
	$("#regform").submit(function(event) {
		var uidOk = checkUserId();
		var pwdOk = checkPassword();
		if (uidOk && pwdOk) {
			return;
		} else {
			event.preventDefault();
		}
	});
	$("#id_user_name").focus(function() {
		$("#id_user_name").tooltip("hide");
	});
	$("#id_passworda").focus(function() {
		$("#id_passworda").tooltip("hide");
	});
	$("#id_passwordb").focus(function() {
		$("#id_passwordb").tooltip("hide");
	});
});

function checkUserId() {
	var userId = $("#id_user_name").val();
	if (userId.length < 4 || userId.length > 30) {
		$("#id_user_name").tooltip({trigger:"manual", title:"UserId must be between 4 and 30 character",placement:"top"});
		$("#id_user_name").tooltip("show");
		return false;
	} else {
		$("#id_user_name").tooltip("hide");
		return true;
	}
}

function checkPassword() {
	var pwdA = $("#id_passworda").val();
	var pwdB = $("#id_passwordb").val();
	if (pwdA === pwdB) {
		//check length
		$("#id_passwordb").tooltip("hide");
		if (pwdA.length > 3) {
			$("#id_passworda").tooltip("hide");
			return true;
		} else {
			$("#id_passworda").tooltip({trigger:"manual", title:"Password must be greater than 3 character",placement:"top"});
			$("#id_passworda").tooltip("show");
			return false;
		}
	} else {
		$("#id_passwordb").tooltip({trigger:"manual", title:"Password don't match.",placement:"top"});
		$("#id_passwordb").tooltip("show");
		return false;
	}
}


