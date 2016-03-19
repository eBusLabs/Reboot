var questionCount = 0;
var optionCount = 0;

$(document).ready(function() {
	//hide tooltip if user is correcting error
	$(".panel-body").on("focus", ".form-control", function() {
		var id = "#" + $(this).attr("id");
		$(id).tooltip("hide");
	});
	
	$(".panel-body").on("focus", ".addOption", function() {
		var qid = $(this).closest(".gqa").attr("id");
		var id = "#" + qid.replace("group","question");
		$(id).tooltip("hide");
	});
	
	$("#qbtn").click(function() {
		//hide tooltip if it is there
		$("#qbtn").tooltip("hide");
		questionCount = questionCount + 1;
		var groupId = "group" + questionCount;       	              //group contain question and options
		var questionId = "question" + questionCount;                  //question id
		var addOptionId = "addOption" + questionCount;		 	      //add option button id
		var removeQuestionId = "removeQuestion" + questionCount;      //remove question button id
		$("#questionId").prepend($(
	    '<div id="' + groupId + '" name="' + groupId + '" class="gqa"> \
		<div class="input-group" style="margin-top:2px;"> \
		<span class="input-group-addon addOnWidth1 question">Question</span> \
		<input type="text" class="form-control" id="' + questionId + '"> \
		<span class="input-group-addon"><button class="removeQuestion" type="button" id="' + removeQuestionId + '"> \
		<span style="color: #a83349" class="glyphicon glyphicon-minus" data-toggle="tooltip" title="Remove this question"></span></button></span> \
		<span class="input-group-addon"><button class="addOption" type="button" id="' + addOptionId + '"> \
		<span style="color: #2c9473" class="glyphicon glyphicon-plus" data-toggle="tooltip" title="Add Option"></span></button></span> \
		</div>'
		));
		var qId = "#" + questionId;
		$(qId).focus();
	});
	
	//since option button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".addOption", function() {
		optionCount = optionCount + 1;
		var eventId = $(this).attr("id");
		var groupId = "#" + eventId.replace("addOption","group");
		var questionId = eventId.replace("addOption","question");
		var optionId = "option" + optionCount;
		$(groupId).append($(
			'<div class="input-group col-sm-6 col-md-6" style="margin-top:1px;"> \
				<span class="input-group-addon addOnWidth1 options">Option</span> \
	            <input type="text" class="form-control ' + questionId + '" id="' + optionId + '"> \
				<span class="input-group-addon"><button class="removeOption" type="button"> \
				<span style="color: #a83349" class="glyphicon glyphicon-minus" data-toggle="tooltip" title="Add Option"></span></button></span> \
	        </div>'
		));
		var oId = "#" + optionId;
		$(oId).focus();
	});
	
	//since removeQuestion button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".removeQuestion", function() {
		//remove question and option group
		var grp = "#" + $(this).attr("id").replace("removeQuestion", "group");
		$(grp).remove();
	});
	
	//since removeOption button is added dynamically we need on function
	$( ".panel-body" ).on( "click",".removeOption", function() {
		$(this).closest("div").remove();
	});
	
	$("#createpoll").submit(function(event) {
		if (formCheck() === true) {
			console.log("cooooool");	
		}	else {
			event.preventDefault();
		}
	});
	
	function formCheck() {
		$("#errormsg").attr("style", "display:none;")
		var allOk = true;
		var postJson = '{';
		
		//check poll name is not empty
		var pollName = $("#pollName").val();
		if (pollName.trim()) {
			postJson = postJson + '"pollname":"' + pollName + '","questions":[';
		}	else {
			$("#pollName").tooltip({trigger:"manual", title:"Poll name can't be empty",placement:"top"});
			$("#pollName").tooltip("show");
			return;
		}
		//loop through questions
		var qCount = 0;
		$($(".gqa").get().reverse()).each(function() {
			qCount = qCount + 1;
			var questionId = "#" + $(this).attr("id").replace("group","question");
			var optionClasss = "." + $(this).attr("id").replace("group","question");
			//check if question box is empty
			if($(questionId).val().trim()) {
				var val = $(questionId).val();
				postJson = postJson + '{"question":"' +  val + '","options":[{'
				//loop through options of a question
				var oCount = 0;
				$(optionClasss).each(function(){
					oCount = oCount + 1;
					var optionId = "#" + $(this).attr("id");
					//check if option box is empty
					if($(optionId).val().trim()) {
						postJson = postJson + '"option":"' + $(optionId).val() + '",';
					} else {
						$(optionId).tooltip({trigger:"manual", title:"Option can't be empty",placement:"top"});
						$(optionId).tooltip("show");
						allOk = false;
					}
				});
				if (oCount < 2) {
					$(questionId).tooltip({trigger:"manual", title:"Question must have two options",placement:"top"});
					$(questionId).tooltip("show");
					allOk = false;
				}
				postJson = postJson.substr(0,(postJson.length - 1));
				postJson = postJson + '}]},';
			} else {
				$(questionId).tooltip({trigger:"manual", title:"Question can't be empty",placement:"top"});
				$(questionId).tooltip("show");
				allOk = false;
			}
		});
		
		console.log("QCount : " + qCount);
		if(qCount === 0) {
			$("#qbtn").tooltip({trigger:"manual", title:"No Question in polls",placement:"top"});
			$("#qbtn").tooltip("show");
			allOk = false;
		}
		//if all is ok, parse json and send to server
		if (allOk) {
			postJson = postJson.substr(0,(postJson.length - 1));
			postJson = postJson + ']}';
			try {
				jQuery.parseJSON(postJson);
				$("#jsonData").attr("value",postJson);
			} catch(err) {
				allOk = false;
				console.log(postJson);
				console.log(err);
			}
		} else {
			allOk = false;
			$("#errormsg").attr("style", "display:default;");
		}
		
		return allOk;
	}
});
