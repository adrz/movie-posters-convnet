myData = [];
map_id_title = {};

function updatePosters(event){
    var title = $('input:first').val();
    retrieve_movie(map_id_title[title]);
    updatePage();
    event.preventDefault();
}

mytt = '';
function updatePage() {
    $('input:first').val(myData[0].title_display);
    console.log(myData[0].url_img);
    mytt = myData[0].url_img;
    $("#poster-img").attr("src", myData[0].url_img);
    for (var i = 1; i < 7; i++)
    {
	$("#poster-img"+i).attr("src", myData[i].url_img);
    }
}

$( "form" ).submit(function( event ) {
    updatePosters(event);
});


function click_img(num) {
    retrieve_movie(myData[num].id);
    updatePage();
}

document.getElementById('random').onclick = function() {
    var idx_rnd = Math.floor((Math.random() * n_movies));
    updatePage(mockData[idx_rnd]);
}



// var ajax = new XMLHttpRequest();
// ajax.open("GET", "datasets/data_autocomplete_all.json", true);
// ajax.onload = function(mockData) {
//     mockData = JSON.parse(ajax.responseText);
// 	var list = JSON.parse(ajax.responseText).map(function(i) { return i.title; });
// 	new Awesomplete(document.querySelector("input"),{ list: list });
// };
// ajax.send();

// var mockData = [];
// var n_movies = 0;
// $.getJSON("datasets/data_autocomplete_all.json", function(json){
//     mockData = json;
//     n_movies = mockData.length;
//     var first_row = getDatabyKey('title', 'We Are Marshall , 2006 , ver 1')[0];
//     updatePage(first_row);
    
// });

url_api = 'http://home.iwoaf.com:5000/v1/';

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
            //setTimeout(loadData, 1000);
        }
    });
}
