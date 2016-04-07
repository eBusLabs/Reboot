$(document).ready(function() {
	//stop auto slide
	$(".carousel").carousel({
	    interval: false
	}); 
	
	$("#btnPollTake").focusout(function(){
		$("#btnPollTake").tooltip("hide");
	});

	$("#pollTaken").submit(function(event) {
		if (formCheck() === true) {
			//submit the form
		}	else {
			event.preventDefault();
		}
	});
	

	function formCheck() {
	var rc = true;
	var previousName = "";
	var currentName = "";
	$(".list-group-item input").each(
			function(index) {
				currentName = $(this).attr("name");
				var indiId = "#indi_" + currentName.replace("question_", "");
				if (currentName === previousName) {
					//continue
				} else {
					if (!$("input[name=" + currentName + "]:checked").val()) {
						$(indiId).attr("style","background-color:red;")
						rc = false;
					} else {
						$(indiId).attr("style","background-color:green;")
					}
					previousName = currentName;
				}
			});

	if (rc === false) {
		$("#btnPollTake").tooltip({
			trigger : "manual",
			title : "Answer red bubbles.",
			placement : "top"
		});
		$("#btnPollTake").tooltip("show");
	}
	return rc;
}//formCheck()
});
