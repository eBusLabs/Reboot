$(document).ready(function() {
	
	//action on click of open button
	$( "#polllist" ).on( "click",".openButton", function() {
		//get poll id
		var id = $(this).attr("id").replace("open","");
		// set form value
		$("#draftaction").val("O");
		$("#pollid").val(id);
		var poll_name_id = "#pn" + id;
		var poll_name = $(poll_name_id).text();
		$("#poll_name").val(poll_name);
	});
	
	//action on click of delete button
	$( "#polllist" ).on( "click",".removeButton", function() {
		var id = $(this).attr("id").replace("del","");
		// set from value
		$("#draftaction").val("D");
		$("#pollid").val(id);
		console.log($("#sdate").val());
		console.log($("#edate").val());
	});
	
	$("#draftform").submit(function(event) {
		if (formCheck() === true) {
			//submit the form
		}	else {
			event.preventDefault();
		}
	});
	
	function formCheck() {
		//check if action is O or D
		var id = $("#pollid").val();
		var action = $("#draftaction").val();
		//check id
		if(id.trim()){
			//continue
		} else {
			return false;
		}
		if (action === "O" || action === "D") {
			return true;
		}	else {
			return false;
		}
			
	}
});
