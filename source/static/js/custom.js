(function($) {
    "use strict"; // Start of use strict
    
    function block_ui(){
        
        $.blockUI({ css: { 
            border: 'none', 
            padding: '15px', 
            backgroundColor: '#000', 
            '-webkit-border-radius': '10px', 
            '-moz-border-radius': '10px', 
            opacity: .5, 
            color: '#fff'
        } }); 
        
    }

    function unblock_ui(){
        $.unblockUI();
    }

    function post_chart_image(callback){
        var _url = "/backend/get_images_chart";
        var settings = {
            "url": _url,
            "method": "POST",
            "timeout": 0            
        };

        $.ajax(settings).done(function (response) {            
            callback(response);
        }).fail(function(response){
            callback("error");            
        });
    }

    var current_page = window.location.pathname;
    if(current_page === "/wallet_status/maintable"){
        
    }
    else if(current_page==="/backend/get_images_chart"){
        block_ui();

        post_chart_image(function(res){
            alert(res);
            $("#status_div").html("<h3>All chart image are saved !!!</h3>");
            unblock_ui();
        });
    }
    

})(jQuery); // End of use strict