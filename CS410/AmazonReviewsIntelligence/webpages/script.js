var product_sentiments_aggregated_overall, product_sentiments_aggregated_dates;
var last_product_title;

function loadProductsAndSentimentsFull() {
    loadJSON(function (response) {
        // Parsing JSON string into object
        product_sentiments_aggregated_overall = JSON.parse(response);
        var products = [];
        for (var i = 0; i < product_sentiments_aggregated_overall.length; i++) {
            products.push(encodeURI(product_sentiments_aggregated_overall[i].product_title));
        }
        autocomplete(document.getElementById("product_name"), products);
    }, '../data/product_sentiments_aggregated_overall.json');

    loadJSON(function (response) {
        // Parsing JSON string into object
        product_sentiments_aggregated_dates = JSON.parse(response);
    }, '../data/product_sentiments_aggregated_dates.json');
}

function loadProductsAndOverallSentiments() {
    loadJSON(function (response) {
        // Parsing JSON string into object
        product_sentiments_aggregated_overall = JSON.parse(response);
    }, '../data/product_sentiments_aggregated_overall.json');
}

function loadJSON(callback, filePath) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', filePath, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}

function showAnalytics(product_title) {
    if (product_title && last_product_title != product_title) {
        var product_id;
        var product_overall_details = getProductOverallSentimentDetails(decodeURI(product_title));
        if (product_overall_details && product_overall_details.length >= 1) {
            product_id = product_overall_details[0]["product_id"];
            document.getElementById('current_product').innerHTML = encodeURI(product_overall_details[0]["product_title"]);
            var sentiment_score = convertToFixedDecimalPlaces(product_overall_details[0]["overall_weighted_sentiment_score"]);
            document.getElementById('overall_sentiment_score').innerHTML = sentiment_score + " (" + getSentimentCategory(sentiment_score) + ")";
        
            var product_dates_details = getProductSentimentDetailsByDate(product_id); 
            plotBarChart(product_dates_details);

            last_product_title = product_title;
        }
    }
}

function getProductOverallSentimentDetails(product_title) {
    if(product_title) {
    return product_sentiments_aggregated_overall.filter(
        function (data) { return data.product_title == product_title }
    );
    }
}

function getProductSentimentDetailsByDate(product_id) {
    if(product_id) {
    return product_sentiments_aggregated_dates.filter(
        function (data) { return data.product_id == product_id }
    );
    }
}

function getSentimentCategory(sentiment_score) {
    if (sentiment_score >= -3 && sentiment_score < -2) {
        return "<span style='color:#cc0000'>Very Negative</span>";
    }
    else if (sentiment_score >= -2 && sentiment_score < -1) {
        return "<span style='color:#ff6666'>Negative</span>";
    }
    else if (sentiment_score >= -1 && sentiment_score <= 1) {
        return "<span>Neutral</span>";
    }
    else if (sentiment_score > 1 && sentiment_score <= 2) {
        return "<span style='color:#00e600'>Positive</span>";
    }
    else if (sentiment_score > 2 && sentiment_score <= 3) {
        return "<span style='color:#006600'>Very Positive</span>";
    }
}

function convertToFixedDecimalPlaces(num) {
    return num.toFixed(2);
}

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });
    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function plotBarChart(product_data) {
    const svg = d3.select('svg');
    svg.selectAll("*").remove();
    const svgContainer = d3.select('#container');

    const margin = 100;
    const width = 900 - 2 * margin;
    const height = 400 - 2 * margin;

    const chart = svg.append('g')
        .attr('transform', `translate(${margin}, ${margin})`);

    const xScale = d3.scaleBand()
        .range([0, width])
        .domain(product_data.map((s) => s.review_date))
        .padding(0.4)

    const yScale = d3.scaleLinear()
        .range([height, 0])
        .domain([-3, 3]);

    // vertical grid lines
    // const makeXLines = () => d3.axisBottom()
    //   .scale(xScale)

    const makeYLines = () => d3.axisLeft()
        .scale(yScale)

    chart.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(xScale))
        .selectAll("text")	
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", function(d) {
                return "rotate(-90)" 
                });


    chart.append('g')
        .call(d3.axisLeft(yScale));

    // vertical grid lines
    // chart.append('g')
    //   .attr('class', 'grid')
    //   .attr('transform', `translate(0, ${height})`)
    //   .call(makeXLines()
    //     .tickSize(-height, 0, 0)
    //     .tickFormat('')
    //   )

    chart.append('g')
        .attr('class', 'grid')
        .call(makeYLines()
            .tickSize(-width, 0, 0)
            .tickFormat('')
        )

    const barGroups = chart.selectAll()
        .data(product_data)
        .enter()
        .append('g')

    barGroups
        .append('rect')
        .attr('class', 'bar')
        .attr('x', (g) => xScale(g.review_date))
        .attr('y', (g) => yScale(g.aggr_weighted_sentiment_score))
        .attr('height', (g) => height - yScale(g.aggr_weighted_sentiment_score))
        .attr('width', xScale.bandwidth())
        .on('mouseenter', function (actual, i) {
            d3.selectAll('.value')
                .attr('opacity', 0)

            d3.select(this)
                .transition()
                .duration(300)
                .attr('opacity', 0.6)
                .attr('x', (a) => xScale(a.review_date) - 5)
                .attr('width', xScale.bandwidth() + 10)

            const y = yScale(actual.aggr_weighted_sentiment_score)

            line = chart.append('line')
                .attr('id', 'limit')
                .attr('x1', 0)
                .attr('y1', y)
                .attr('x2', width)
                .attr('y2', y)

            barGroups.append('text')
                .attr('class', 'divergence')
                .attr('x', (a) => xScale(a.review_date) + xScale.bandwidth() / 2)
                .attr('y', (a) => yScale(a.aggr_weighted_sentiment_score) + 30)
                .attr('fill', 'white')
                .attr('text-anchor', 'middle')
                .text((a, idx) => {
                    const divergence = (a.aggr_weighted_sentiment_score - actual.aggr_weighted_sentiment_score).toFixed(2)

                    let text = ''
                    if (divergence > 0) text += '+'
                    text += `${divergence}`

                    return idx !== i ? text : '';
                })

        })
        .on('mouseleave', function () {
            d3.selectAll('.value')
                .attr('opacity', 1)

            d3.select(this)
                .transition()
                .duration(300)
                .attr('opacity', 1)
                .attr('x', (a) => xScale(a.review_date))
                .attr('width', xScale.bandwidth())

            chart.selectAll('#limit').remove()
            chart.selectAll('.divergence').remove()
        })

    barGroups
        .append('text')
        .attr('class', 'value')
        .attr('x', (a) => xScale(a.review_date) + xScale.bandwidth() / 2)
        .attr('y', (a) => yScale(a.aggr_weighted_sentiment_score) + 30)
        .attr('text-anchor', 'middle')
        .text((a) => `${a.aggr_weighted_sentiment_score}`)

    svg
        .append('text')
        .attr('class', 'label')
        .attr('x', -(height / 2) - margin)
        .attr('y', margin / 2.4)
        .attr('transform', 'rotate(-90)')
        .attr('text-anchor', 'middle')
        .text('Weighted Sentiment Score')

    svg.append('text')
        .attr('class', 'label')
        .attr('x', width / 2 + margin)
        .attr('y', height + margin * 1.7 + 20)
        .attr('text-anchor', 'middle')
        .text('Review Date')

    svg.append('text')
        .attr('class', 'title')
        .attr('x', width / 2 + margin)
        .attr('y', 40)
        .attr('text-anchor', 'middle')
        .text('Sentiment Trends')

    svg.append('text')
        .attr('class', 'source')
        .attr('x', width - margin / 2)
        .attr('y', height + margin * 1.7)
        .attr('text-anchor', 'start')
        //.text('Source: Amazon Reviews')

}

function showProducts() {

}