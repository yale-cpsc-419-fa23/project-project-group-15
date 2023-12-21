// insert navbar into webpage using jquery

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
