var count = 0;

$(document).ready(function() {
	$("#qbtn").click(function() {
		count = count + 1;
		var groupid = "group" + count;
		var questionid = "question" + count;
		var optionid = "option" + count;
		var removeid = "option" + count;
		$("#questionid").prepend($(
	    '<div id="' + groupid + '" name="' + groupid + '"> \
		<div class="input-group" style="margin-top:2px;"> \
		<span class="input-group-addon addOnWidth1 question">Question</span> \
		<input autofocus type="text" class="form-control" id="' + questionid +'" name="' + questionid + '"> \
		<span class="input-group-addon"><button class="removeQuestion" type="button" id="' + removeid + '" name="' + removeid + '"> \
		<span style="color: #a83349" class="glyphicon glyphicon-minus" data-toggle="tooltip" title="Remove this question"></span></button></span> \
		<span class="input-group-addon"><button class="addOption" type="button" id="' + optionid + '" name="' + optionid + '"> \
		<span style="color: #2c9473" class="glyphicon glyphicon-plus" data-toggle="tooltip" title="Add Option"></span></button></span> \
		</div>'
		));
	});
	
	//since option button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".addOption", function() {
		var eventId = $(this).attr("id");
		var groupId = "#" + eventId.replace("option","group");
		$(groupId).append($(
			'<div class="input-group col-sm-6 col-md-6" style="margin-top:1px;"> \
				<span class="input-group-addon addOnWidth1 options">Option</span> \
	            <input autofocus type="text" class="form-control"> \
				<span class="input-group-addon"><button class="removeOption" type="button"> \
				<span style="color: #a83349" class="glyphicon glyphicon-minus" data-toggle="tooltip" title="Add Option"></span></button></span> \
	        </div>'
		));
	});
	
	//since removeQuestion button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".removeQuestion", function() {
		var eventId = $(this).attr("id");
		var groupId = "#" + eventId.replace("option","group");
		$(groupId).remove();
	});
	
	//since removeOption button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".removeOption", function() {
		$(this).closest("div").remove();
	});
});
