// insert jquery into webpage -- not working currently
// let script=document.createElement('script');
// script.src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js";
// document.getElementsByTagName('head')[0].appendChild(script);



function getNavbar(){
    let url='/navbar'
    let request = $.ajax({
        type: 'GET',
        url: url,
        success: setNavbar
    });
}

function setNavbar(response){
    $('#navbar').html(response)
}

function setup(){
    //insert navbar div

    // let navbar_div=$('<div id="navbar"> </div>');
    $('body').prepend('<div id="navbar"> </div>');
    getNavbar();
}


$('document').ready(setup);
