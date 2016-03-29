$(document).ready(function() {
	//remove tooltip
	$("#sdate").focusin(function(){
		$(this).tooltip("hide");
	});
	
	$("#edate").focusin(function(){
		$(this).tooltip("hide");
	});
	
	$("#butts").focusin(function(){
		$("#multiselect").tooltip("hide");
	});
	
	
	$("#sdate").focusout(function(){
		$("#id_end_date").val($("#id_start_date").val());
	});
	

	
	$("#sdate").datetimepicker(
	{
		format:"YYYY-MM-DD",
		minDate:new Date()
	});
	
	$("#edate").datetimepicker(
	{
		format:"YYYY-MM-DD",
		minDate:new Date()
	});
	
	$('#multiselect').multiselect();
	
	$("#openpoll").submit(function(event) {
		if (formCheck() === true) {
			console.log("allok");
		}	else {
			event.preventDefault();
		}
	});
	
	function formCheck() {
		allOk = true;
		var sds = $("#id_start_date").val();
		var eds = $("#id_end_date").val();
		var gns = $("#multiselect_to").val();
		
		//check if group is selected
		if (gns === null) {
			$("#multiselect").tooltip({trigger:"manual", title:"Select at least one group",placement:"top"});
			$("#multiselect").tooltip("show");
			allOk = false;
		}
		//check if start date string is empty
		if(sds.trim()){
			
		} else {
			$("#sdate").tooltip({trigger:"manual", title:"Date can't be empty",placement:"top"});
			$("#sdate").tooltip("show");
			allOk = false;
		}
		//check if end date is empty
		if(eds.trim()){
			
		} else {
			$("#edate").tooltip({trigger:"manual", title:"Date can't be empty",placement:"top"});
			$("#edate").tooltip("show");
			allOk = false;
		}
	
		try {
			var sd = new Date(sds);
			var ed = new Date(eds);
			if (sd > ed) {
				allOk = false;
				$("#edate").tooltip({trigger:"manual", title:"Expiry date can't be less than open date.",placement:"top"});
				$("#edate").tooltip("show");
			}
		} catch(err) {
			allOk = false;
			$("#sdate").tooltip({trigger:"manual", title:"Invalid date format.",placement:"top"});
			$("#sdate").tooltip("show");
			$("#edate").tooltip({trigger:"manual", title:"Invalid date format.",placement:"top"});
			$("#edate").tooltip("show");
		}
		
		return allOk;
	}
});
