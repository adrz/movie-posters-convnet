

//
function updatePosters(event){
    var title = $('input:first').val();
    var row = getDatabyKey('title', title)[0];
    updatePage(row);
    event.preventDefault();
}

function updatePage(row) {
    $('input:first').val(row['title'])
    d3.select("#poster-img").attr("src", row['url_imgs']);
    for (var i = 1; i < 7; i++)
    {
	d3.select("#poster-img"+i).attr("src", row['closest_'+i]);
//	d3.select('#score'+i).html('Score ' +i+': ' + row['score_'+i]);
    }
}

$( "form" ).submit(function( event ) {
    updatePosters(event);
});

function getDatabyKey(key, value) {
    return mockData.filter(
	function(mockData) {
	    return mockData[key] == value
	}
    );
}

function click_img(num) {
    url = d3.select('#poster-img'+num).attr('src');
    row = getDatabyKey('url_imgs', url)[0];
    updatePage(row);
}

document.getElementById('random').onclick = function() {
    var idx_rnd = Math.floor((Math.random() * n_movies));
    updatePage(mockData[idx_rnd]);
}



var ajax = new XMLHttpRequest();
ajax.open("GET", "datasets/data_autocomplete_all.json", true);
ajax.onload = function(mockData) {
    mockData = JSON.parse(ajax.responseText);
	var list = JSON.parse(ajax.responseText).map(function(i) { return i.title; });
	new Awesomplete(document.querySelector("input"),{ list: list });
};
ajax.send();

var mockData = [];
var n_movies = 0;
$.getJSON("datasets/data_autocomplete_all.json", function(json){
    mockData = json;
    n_movies = mockData.length;
    var first_row = getDatabyKey('title', 'We Are Marshall , 2006 , ver 1')[0];
    updatePage(first_row);
    
});
