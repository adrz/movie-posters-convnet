myData = [];
map_id_title = {};

url_www = 'http://51.15.248.42/';


function updatePosters(event){
    var title = $('input:first').val();
    retrieve_movie(map_id_title[title]);
    event.preventDefault();
}

function updatePage() {
    $('input:first').val(myData[0].title_display);
    console.log(myData[0].url_img);
    $("#poster-img").attr("src", url_www+'data/posters/'+(myData[0].id-1) + '.jpg');
    for (var i = 1; i < 7; i++)
    {
	$("#poster-img"+i).attr("src", url_www+'data/posters/'+(myData[i].id-1)+'.jpg');
    }
}

$( "form" ).submit(function( event ) {
    updatePosters(event);
});


function click_img(num) {
    retrieve_movie(myData[num].id);
}

document.getElementById('random').onclick = function() {
    n_movies = Object.keys(map_id_title).length;
    var idx_rnd = Math.floor((Math.random() * n_movies));
    retrieve_movie(idx_rnd);
}

$body = $("body");


$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
    ajaxStop: function() { $body.removeClass("loading"); }    
});

url_api = 'http://51.15.248.42/v1/';

$(document).ready(function() {
    crossDomain: true;
    $.ajax({
        type:"get",
        url: url_api + 'idmovies',
	dataType: "json",
        success: function(data) {
            //geoData = data;
            map_id_title = data;
	},
        complete: function() {
            //setTimeout(loadData, 1000);
        }
    });

    retrieve_movie(222);
});

function retrieve_movie(id) {
    url = url_api + id.toString();
    $.ajax({
        type:"get",
        url: url,
	dataType: "json",
        success: function(data) {
            //geoData = data;
            myData = data;
        },
        complete: function() {
	    updatePage();
        }
    });
};
