$(document).ready(function() {
    
    //remove tooltip
    $("#sdate").focusin(function(){
        $(this).tooltip("hide");
    });
    
    $("#edate").focusin(function(){
        $(this).tooltip("hide");
    });
    
    
    $("#sdate").datetimepicker(
    {
        format:"YYYY-MM-DD",
        maxDate: new Date()
    });
    
    $("#edate").datetimepicker(
    {
        format:"YYYY-MM-DD",
        maxDate: new Date()
    });
    
    
    //action on click list
    $( ".list-group-item" ).on( "click", function() {
        var id = $(this).attr("id").replace("pn","");
        $("#pollid").val(id);
        console.log($("#pollid").val());
    }); 
    
    $("#listpoll").submit(function(event) {
        if (formCheckListPoll() === true) {
            //continue
        }   else {
            console.log("allnotok");
            event.preventDefault();
        }
    });
    
    function formCheckListPoll() {
        allOk = true;
        try {
            //check if start date is valid date
            var sdate = $("#id_sdate").val();
            var edate = $("#id_edate").val();
            
            if (sdate.trim()) {
                //check if date is valid
            } else {
                $("#sdate").tooltip({trigger:"manual", title:"Date can't be empty",placement:"top"});
                $("#sdate").tooltip("show");
                allOk = false;
            }
            
            if (edate.trim()) {
                //check if date is valid
            } else {
                $("#edate").tooltip({trigger:"manual", title:"Date can't be empty",placement:"top"});
                $("#edate").tooltip("show");
                allOk = false;
            }
            
            if (sdate > edate) {
                $("#sdate").tooltip({trigger:"manual", title:"Start date must be less than end date",placement:"top"});
                $("#sdate").tooltip("show");
                allOk = false;
            }
        } catch(err) {
            console.log("Error validating form showpoll : \n" + err);
            return false;
        }
        
        return allOk;
    }
    
    $("#showpoll").submit(function(event) {
        if (formCheckShowPoll() === true) {
            console.log("allok");
        }   else {
            console.log("allnotok");
            event.preventDefault();
        }
    });
    
    function formCheckShowPoll() {
        try {
            return true;
        } catch(err) {
            console.log("Error validating form showpoll : \n" + err);
            return false;
        }
    }
    
});
