// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var yAxis = d3.axisLeft(y).tickFormat(d3.format("1", 1e1));

var svg = d3.select("#us_cat_svg");
var margin = { top: 20, right: 20, bottom: 40, left: 40 };
var width = svg.attr("width") - margin.left - margin.right;
var height = svg.attr("height") - margin.top - margin.bottom;
var xlabel = "Video Category";
var ylabel = "Number of Videos";

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

plotCatData("./data/yt_us_popcategories.csv", g, height, width);

// text label for the x axis
svg.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + 55) + ")")
    .style("text-anchor", "middle")
    .style("font", "18px sans-serif")
    .style("padding-top", "-25px")
    .html(xlabel);

// text label for the y axis
svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font", "18px sans-serif")
    .text(ylabel);

// annotation. text + line
svg.append("text")
    .attr("transform", "translate(" + 800 + " ," + 300 + ")")
    // .attr("transform", "translate(" + (width / 2) + " ," + (height + 55) + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .text("Gaming is not dominant category.");
svg.append("line").attr("x1", 800).attr("x2", 890).attr("y1", 300).attr("y2", 550).attr("stroke", "red");

// annotation : text + line
svg.append("text")
    .attr("transform", "translate(" + 280 + " ," + 100 + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .html("As expected, more videos under entertainment than others.");
svg.append("line").attr("x1", 270).attr("x2", 120).attr("y1", 100).attr("y2", 170).attr("stroke", "red");

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var svg_uk = d3.select("#uk_cat_svg");
var g_uk = svg_uk.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

plotCatData("./data/yt_gb_popcategories.csv", g_uk, height, width);

// text label for the x axis
svg_uk.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + 55) + ")")
    .style("text-anchor", "middle")
    .style("font", "18px sans-serif")
    .style("padding-top", "10px")
    .html(xlabel);
// text label for the y axis
svg_uk.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("font", "18px sans-serif")
    .style("text-anchor", "middle")
    .text(ylabel);

// annotation. text + line
svg_uk.append("text")
    .attr("transform", "translate(" + 500 + " ," + 300 + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .html("Gaming is dominant compared to US.");
svg_uk.append("line").attr("x1", 501).attr("x2", 501).attr("y1", 300).attr("y2", 510).attr("stroke", "red");


// annotation. text + 2 lines
svg_uk.append("text")
    .attr("transform", "translate(" + 280 + " ," + 100 + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .html("Compared to US, Music is more prominant than Entertainment.");
svg_uk.append("line").attr("x1", 270).attr("x2", 120).attr("y1", 100).attr("y2", 190).attr("stroke", "red");
svg_uk.append("line").attr("x1", 270).attr("x2", 185).attr("y1", 100).attr("y2", 235).attr("stroke", "blue");

svg_uk.append("text")
    .attr("transform", "translate(" + 700 + " ," + 250 + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .html("Pet's & animals is unique, this one not as famous in USA/CA.");
svg_uk.append("line").attr("x1", 701).attr("x2", 820).attr("y1", 250).attr("y2", 545).attr("stroke", "red");


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Canada plots.
var svg_ca = d3.select("#ca_cat_svg");
var g_ca = svg_ca.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
let width_ca = svg.attr("width") - margin.left - margin.right;
let height_ca = svg.attr("height") - margin.top - margin.bottom;

plotCatData("./data/yt_ca_popcategories.csv", svg_ca, height_ca, width_ca);

// text label for the x axis
svg_ca.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + 55) + ")")
    .style("text-anchor", "middle")
    .style("font", "18px sans-serif")
    .style("padding-top", "-10px")
    .html(xlabel);

// text label for the y axis
svg_ca.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left - 30)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font", "18px sans-serif")
    .text(ylabel);


// annotation. text + line
// svg_ca.append("text")
//     .attr("transform", "translate(" + 500 + " ," + 300 + ")")
//     .style("text-anchor", "middle")
//     .style("font", "11px sans-serif")
//     .style("padding-top", "12px")
//     .html("Gaming is dominant comparatively.");
// svg_ca.append("line").attr("x1", 501).attr("x2", 501).attr("y1", 300).attr("y2", 510).attr("stroke", "red");

// annotation. text + line
svg_ca.append("text")
    .attr("transform", "translate(" + 300 + " ," + 100 + ")")
    .style("text-anchor", "middle")
    .style("font", "11px sans-serif")
    .style("padding-top", "12px")
    .html("Like US, entertainment dominates,but CA stands out with News & Politics at 2nd position.");
svg_ca.append("line").attr("x1", 270).attr("x2", 80).attr("y1", 100).attr("y2", 190).attr("stroke", "red");
svg_ca.append("line").attr("x1", 270).attr("x2", 135).attr("y1", 100).attr("y2", 240).attr("stroke", "blue");
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function plotCatData(file, g, height, width) {
    d3.csv(file, function (error, data) {
        if (error) throw error;

        var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
            y = d3.scaleLinear().rangeRound([height, 0]),
            colorScale = d3.scaleOrdinal(d3.schemeCategory20);  // set the colour scale

        // sort the data based on years of experience.
        //data.sort(function(a,b ) {return d3.descending(a.Metric)});

        x.domain(data.map(function (d) { return d.category_title; }));
        y.domain([d3.min(data, function (d) { return parseInt(d.Metric); }) - 100, d3.max(data, function (d) { return parseInt(d.Metric); })]);
        // colorScale.domain(data.map(function (d){ console.log("category =>" , d.category_title, " Rank => ", d.rank); return d.rank; }));
        colorScale.domain(data.map(function (d) { return d.rank; }));

        // add bars.
        g.selectAll(".xbar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) { return x(d.category_title); })
            .attr("y", function (d) { return y(parseInt(d.Metric)); })
            .attr("width", x.bandwidth())
            .attr("height", function (d) { return height - y(parseInt(d.Metric)); })
            .style("fill", function (d) { return colorScale(d.rank); });

        // add x-axis
        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // add y-axis
        g.append("g")
            .attr("class", "axis axis--y")
            // .call(d3.axisLeft(y).ticks(10, "%"))
            .call(d3.axisLeft(y))
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end");
        // .text("Frequency");
    })
};


function openCountry(evt, countryName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(countryName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Get the element with id="btn_us" and click on it
document.getElementById("btn_us").click();