jQuery(document).ready(function($) {
});

function bind_key_and_click_handler() {
    $('#id_text').on("keypress",function(event){
          $('.has-error').hide(); 
    });
    
    $('#id_text').click(function(event){
          $('.has-error').hide(); 
       });
}; 
