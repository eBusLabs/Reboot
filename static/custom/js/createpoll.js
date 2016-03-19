var questionCount = 0;
var optionCount = 0;

$(document).ready(function() {
	//hide tooltip if user is correcting error
	$(".panel-body").on("focus", ".form-control", function() {
		var id = "#" + $(this).attr("id");
		$(id).tooltip("hide");
	});
	
	$("#qbtn").click(function() {
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
		$("#errormsg").attr("style", "display:none;")
		event.preventDefault();
		var postJson = '{';
		var allOk = true;
		
		//check poll name is not empty
		var pollName = $("#pollName").val();
		if (pollName.trim()) {
			postJson = postJson + '"pollname":"' + pollName + '","questions":[';
		}	else {
			$("#pollName").tooltip({trigger:"manual", title:"Poll name can't be empty",placement:"top"});
			$("#pollName").tooltip("show");
			return;
		}
		
		$($(".gqa").get().reverse()).each(function() {
			var questionId = "#" + $(this).attr("id").replace("group","question");
			var optionClasss = "." + $(this).attr("id").replace("group","question");
			//check if question box is empty
			if($(questionId).val().trim()) {
				var val = $(questionId).val();
				postJson = postJson + '{"question":"' +  val + '","options":[{'
				$(optionClasss).each(function(){
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
				postJson = postJson.substr(0,(postJson.length - 1));
				postJson = postJson + '}]},';
			} else {
				$(questionId).tooltip({trigger:"manual", title:"Question can't be empty",placement:"top"});
				$(questionId).tooltip("show");
				allOk = false;
			}
		});
		
		function csrfSafeMethod(method) {
		    // these HTTP methods do not require CSRF protection
		    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		
		//if all is ok, parse json and send to server
		if (allOk) {
			postJson = postJson.substr(0,(postJson.length - 1));
			postJson = postJson + ']}';
			var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
			try {
				console.log("Json : " + postJson);
				jQuery.parseJSON(postJson)
				$.ajaxSetup({
				    beforeSend: function(xhr, settings) {
				        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				            xhr.setRequestHeader("X-CSRFToken", csrftoken);
				        }
				    }
				});
				//$.post("/addpoll/", postJson);
				$.post("/addpoll/",postJson, function(data, textStatus, req) {
					if (textStatus === "success") {
						console.log("Data : " + data);
						console.log("textStatus : " + textStatus );
						console.log("request : " + req);
						$("html").replaceWith($(data));
						
					} else {
						console.log("xhr failure");
					}
				});
			} catch (err){
				console.log("Erros parsing Json : " + err);
			}
		} else {
			$("#errormsg").attr("style", "display:default;")
		}
	});
});
