$(document).ready(function() {
	//Handle form submission
	$("#resetform").submit(function(event) {
		var pwdOk = checkPassword();
		if (pwdOk) {
			return;
		} else {
			event.preventDefault();
		}
	});
	$("#id_oldpwd").focus(function() {
		$("#id_oldpwd").tooltip("hide");
	});
	$("#id_newpwd").focus(function() {
		$("#id_newpwd").tooltip("hide");
	});
	$("#id_cnfpwd").focus(function() {
		$("#id_cnfpwd").tooltip("hide");
	});
});

function checkPassword() {
	var pwdA = $("#id_oldpwd").val();
	var pwdB = $("#id_newpwd").val();
	var pwdC = $("#id_cnfpwd").val();
	if (pwdA.length < 4) {
		$("#id_oldpwd").tooltip({trigger:"manual", title:"Password must be greater than 3 character",placement:"top"});
		$("#id_oldpwd").tooltip("show");
		return false;
	} else {
		$("#id_oldpwd").tooltip("hide");
	}
	if (pwdB === pwdC) {
		//check length
		$("#id_newpwd").tooltip("hide");
		if (pwdB.length > 3) {
			$("#id_newpwd").tooltip("hide");
			return true;
		} else {
			$("#id_newpwd").tooltip({trigger:"manual", title:"Password must be greater than 3 character",placement:"top"});
			$("#id_newpwd").tooltip("show");
			return false;
		}
	} else {
		$("#id_cnfpwd").tooltip({trigger:"manual", title:"Password don't match.",placement:"top"});
		$("#id_cnfpwd").tooltip("show");
		return false;
	}
}


