$(document).ready(function() {
	
	//action on click of open button
	$( "#polllist" ).on( "click",".openButton", function() {
		//get poll id
		var id = $(this).attr("id").replace("take","");
		// set form value
		$("#pollid").val(id);
		var poll_name_id = "#pn" + id;
		var poll_name = $(poll_name_id).text();
		$("#poll_name").val(poll_name);
	});
	
	$("#draftform").submit(function(event) {
		if (formCheck() === true) {
			//submit the form
		}	else {
			event.preventDefault();
		}
	});
	
	function formCheck() {
		var id = $("#pollid").val();
		var pname = $("#poll_name").val();
		//check id
		if(id.trim()){
			//continue
		} else {
			return false;
		}
		if(pname.trim()){
			//continue
		} else {
			return false;
		}

			
	}
});
