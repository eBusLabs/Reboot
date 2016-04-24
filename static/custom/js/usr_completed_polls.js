$(document).ready(function() {
    //action on click list
    $( ".list-group-item" ).on( "click", function() {
        var id = $(this).attr("id").replace("pn","");
        $("#pollid").val(id);
        console.log($("#pollid").val());
    }); 
    
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
