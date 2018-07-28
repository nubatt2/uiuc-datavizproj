function addCategoryDropdown(categoryFile, channelsFile) {
    d3.tsv(categoryFile, function (data) {
        // use data here
        //.filter(function(d) { return d.close < 400 })
        var select = d3.select('#category_index');

        // remove everything that already exists.
        d3.select("#category_index").selectAll("*").remove();

        // add new stuff.
        select.selectAll('option')
            .data(data).enter()
            .append('option')
            .text(function (d) { return d.category_title; });

        let selectedText;
        let detailsList = document.getElementById("category_index");
        if(detailsList) {
            detailsList.selectedIndex = 0;
            selectedText = detailsList.options[detailsList.selectedIndex].text;
        }

        addbarChart(channelsFile, selectedText);
    });
}

// this is the function which adds bar chart and related fields.
function addbarChart(file, selectedCategory) {

    // clean anything existing
    d3.selectAll("#detailSvg > *").remove();

    // details chart!
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    var yAxis = d3.axisLeft(y).tickFormat(d3.format("1", 1e1));
    var tooltip = d3.select("body").append("div").attr("class", "toolTip");

    var detailsChart = d3.select("#detailSvg");
    var margin = { top: 20, right: 20, bottom: 40, left: 40 };
    var width = detailsChart.attr("width") - margin.left - margin.right;
    var height = detailsChart.attr("height") - margin.top - margin.bottom;

    var g =
        detailsChart.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    let detailsList = document.getElementById("category_index");
    let selectedText = detailsList.options[detailsList.selectedIndex].text;

    d3.csv(file, function (data) {
        console.log(data)
        let filteredData = data.filter(function (d) { return d.category_title == selectedText });

        let x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
            y = d3.scaleLinear().rangeRound([height, 0]),
            colorScale = d3.scaleOrdinal(d3.schemeCategory10);  // set the colour scale

        // sort the data based on years of experience.
        //data.sort(function(a,b ) {return d3.descending(a.Metric)});

        x.domain(filteredData.map(function (d) { return d.channel_title; }));
        y.domain([0, d3.max(filteredData, function (d) { return parseInt(d.Metric); })]);
        colorScale.domain(filteredData.map(function (d) { return parseInt(d.rank); }));

        // add bars.
        g.selectAll(".xbar")
            .data(filteredData)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (d) { return x(d.channel_title); })
            .attr("y", function (d) { return y(parseInt(d.Metric)); })
            .attr("width", x.bandwidth())
            .attr("height", function (d) { return height - y(parseInt(d.Metric)); })
            .style("fill", function (d) { return colorScale(d.rank); })
            .on("mouseover", function (d) {
                tooltip
                    .style("left", d3.event.pageX - 50 + "px")
                    .style("top", d3.event.pageY - 70 + "px")
                    .style("display", "inline-block")
                    // .html((d.channel_title) + "<br>" + "Videos#" + (d.Metric)+ "<br>" + "Views#" + (d.ViewsCount) + "<br>" + "Likes#" + (d.LikesCount)+ "<br>" + "Comments#" + (d.CommentsCount));
                    // .html((d.channel_title) + "<br>" + "Videos#" + (d.Metric) + "<br>" + "Views#" + (d.ViewsCount) + "<br>" + "Comments#" + (d.CommentsCount));
                    .html("Comments#" + (d.CommentsCount) + "<br>" + "Views#" + (d.ViewsCount));
            })
            .on("mouseout", function (d) { tooltip.style("display", "none"); });
        // g.select(".overlay").on("mousemove", mousemove);

        // add x-axis
        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));

        // Add the X Axis rotated
        // Add the X Axis

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


    });

    // text label for the x axis
    detailsChart.append("text")
        .attr("transform", "translate(" + (width / 2) + " ," + (height + 60) + ")")
        .style("text-anchor", "middle")
        .style("font", "18px sans-serif")
        .style("padding-top", "-15px")
        .html("Channel Name");

    // text label for the y axis
    detailsChart.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left + 50)
        .attr("x", 0 - (height / 2) - 50)
        .attr("dx", "1em")
        // .attr("dy", "1em")
        .style("text-anchor", "middle")
        .style("font", "18px sans-serif")
        .text("Number of Videos");

    // All chart Title
    detailsChart.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Value vs Date Graph");
};

function addDetailedGraph() {
    var detailsList = document.getElementById("category_index");
    var selectedText = detailsList.options[detailsList.selectedIndex].text;
    console.log(selectedText);

    // remove previous chart.
    d3.selectAll("#detailSvg > *").remove();
    addbarChart(currentDetailsFileName, selectedText);
}

function addDetailsGraphC() {
    var detailsList = document.getElementById("country_index");
    var selectedValue = detailsList.options[detailsList.selectedIndex].value;
    currentDetailsFileName = country_channelmap.get(selectedValue)
    currentSummaryFileName = country_catmap.get(selectedValue);

    // this function adds dropdown and populated default bar.
    addCategoryDropdown(currentSummaryFileName, currentDetailsFileName);

    //console.log("Selected value = ", selectedValue, "Selected cat file = ", currentSummaryFileName, "Selected channels file", currentDetailsFileName);
}

function drawDrilldown(country){
    document.getElementById("country_index").options.namedItem(country).selected=true;

    // now that index is set. let it flow through regular.
    addDetailsGraphC();
}

let country_catmap = new Map();
// setting the values
country_catmap.set("US", "./data/yt_us_popcategories.csv");
country_catmap.set("UK", './data/yt_gb_popcategories.csv');
country_catmap.set("CA", './data/yt_ca_popcategories.csv');

let country_channelmap = new Map();
// setting the values
country_channelmap.set("US", "./data/yt_us_popchannels.csv");
country_channelmap.set("UK", './data/yt_gb_popchannels.csv');
country_channelmap.set("CA", './data/yt_ca_popchannels.csv');

var defaultSummaryFileName = "./data/yt_us_popcategories.csv";
var defaultDetailsFileName = "./data/yt_us_popchannels.csv";
var defaultCategory = "Entertainment";

let currentSummaryFileName = defaultSummaryFileName;
let currentDetailsFileName = defaultDetailsFileName;

addCategoryDropdown(defaultSummaryFileName, currentDetailsFileName);