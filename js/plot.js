// https://github.com/douglasbagnall/image-tsne

function plot(json, size){

    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);

    var svg = d3.select("body").append("svg")
        .attr("width", w/2-10)
        .attr("height", (w/2-10)*2/3);
    var img = d3.select('body')
        .append("img")
        .attr('id', 'current_img')
        .attr('width', w/3-10);


    svg.append('g').selectAll('.myPoint')
        .data(json)
        .enter()
        .append('image')
        .attr("xlink:href", function(d){ return d[2] })
        .attr("x", function(d){ return d[0]})
        .attr("y", function(d){ return d[1]})
        .attr("width", size[0])
        .attr("height", size[1])
        .on("click", function(d, i){
            img.attr('src', d[3]);
        });

    var zoom = d3.behavior.zoom().scaleExtent([0.5, 100]);
    svg.call(zoom);
    zoom.on("zoom", function(){
        var e = d3.event;
        var w = size[0] / e.scale;
        var h = size[1] / e.scale;
        var transform = 'translate(' + e.translate + ')' +' scale(' + e.scale + ')';
        svg.selectAll('image')
            .attr('transform', transform)
            .attr('width', w)
            .attr('height', h);
    });
}

function updateWindow(){
   var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
   d3.select("svg")
        .attr("width", w/2-10)
        .attr("height", (w/2-10)*2/3);
   d3.select('img')
        .attr('id', 'current_img')
        .attr('width', w/3-10);
}
window.onresize = updateWindow;

function get_dataset(){
    var dataset = window.location.search.substr(1);
    return "datasets/" + dataset + ".json";
}

function get_size(){
    var dataset = window.location.search.substr(1);
    return lut[dataset];
}

d3.json(get_dataset(), function(error, json) {
    if (error) return console.warn(error);
    plot(json, get_size());
});
