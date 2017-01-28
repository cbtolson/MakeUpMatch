//Constants for the SVG
var width = 500,
height = 500;

//Set up the colour scale
var color = d3.scale.category20();

//Set up the force layout
var force = d3.layout.force()
.charge(-120)
.linkDistance(80)
.size([width, height]);

//Append a SVG to the body of the html page. Assign this SVG as an object to svg
var svg = d3.select("#fullviz")
.attr("width", width)
.attr("height", height);

//Read the data from the mis element
var graph = {{ graph|tojson }};

//Creates the graph data structure out of the json data
force.nodes(graph.nodes)
.links(graph.links)
.start();

//Create all the line svgs but without locations yet
var link = svg.selectAll(".link")
.data(graph.links)
.enter().append("line")
.attr("class", "link")
.style("stroke-width", function (d) {
       return Math.sqrt(d.value);
       });

//Do the same with the circles for the nodes - no
//Changed
var node = svg.selectAll(".node")
.data(graph.nodes)
.enter().append("g")
.attr("class", "node")
.call(force.drag);

node.append("circle")
.attr("r", 8)
.style("fill", function (d) {
       return color(d.group);
       })

node.append("text")
.attr("dx", 10)
.attr("dy", ".35em")
.text(function(d) { return d.name });
//End changed


//Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
force.on("tick", function () {
         link.attr("x1", function (d) {
                   return d.source.x;
                   })
         .attr("y1", function (d) {
               return d.source.y;
               })
         .attr("x2", function (d) {
               return d.target.x;
               })
         .attr("y2", function (d) {
               return d.target.y;
               });
         
         //Changed
         
         d3.selectAll("circle").attr("cx", function (d) {
                                     return d.x;
                                     })
         .attr("cy", function (d) {
               return d.y;
               });
         
         d3.selectAll("text").attr("x", function (d) {
                                   return d.x;
                                   })
         .attr("y", function (d) {
               return d.y;
               });
         
         //End Changed
         
         });
