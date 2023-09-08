$(document).ready(function() { 
    let buttons = $(".link");

    console.log(buttons.length);

    buttons.each(function(i, btn) {
        $(btn).click(function() {
            console.log("click");
            // $(".link").removeClass("active");
            $(this).addClass("active");
        });
    });
});