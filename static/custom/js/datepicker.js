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
        maxDate:moment().format("YYYY-MM-DD"),
    });
    
    $("#edate").datetimepicker(
    {
        format:"YYYY-MM-DD",
        maxDate:moment().format("YYYY-MM-DD")
    });
    
    //link start date and end date window
    $("#sdate").on("dp.change", function (e) {
        $("#edate").data("DateTimePicker").minDate(e.date);
    });
    $("#edate").on("dp.change", function (e) {
        $("#sdate").data("DateTimePicker").maxDate(e.date);
    });
    
    
    $("#dateform").submit(function(event) {
        if (formCheckDates() === true) {
            //continue
        }   else {
            console.log("invalid dates");
            event.preventDefault();
        }
    });
    
    function formCheckDates() {
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
            console.log("Error validating form : \n" + err);
            return false;
        }
        
        return allOk;
    }
});
