document.addEventListener("DOMContentLoaded", function () {
    const width = 800, height = 600;

    const svg = d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        ;

    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "transparent")
        .on("click", function () {
            resetHighlight();
            d3.select("#tooltip").style("opacity", 0).style("display", "none");
        });


    const g = svg.append("g");

    const jsonData = {
        "nodes": [
            { "id": "1", "x": 100, "y": 200, "data": "Hola em dic alexandre 1", "radi": "" },
            { "id": "2", "x": 300, "y": 100, "data": "Hi everyone" },
            { "id": "3", "x": 500, "y": 300, "data": "Info 3" },
            { "id": "4", "x": 200, "y": 400, "data": "Info 4" },
            { "id": "5", "x": 400, "y": 250, "data": "Info 5" },
            { "id": "6", "x": 600, "y": 150, "data": "Info 6" },
            { "id": "7", "x": 700, "y": 350, "data": "Info 7" },
            { "id": "8", "x": 450, "y": 450, "data": "Info 8" }
        ],
        "links": [
            { "source": "1", "target": "2" },
            { "source": "2", "target": "3" },
            { "source": "3", "target": "1" },
            { "source": "4", "target": "5" },
            { "source": "5", "target": "6" },
            { "source": "6", "target": "7" },
            { "source": "7", "target": "8" },
            { "source": "8", "target": "4" }
        ]
    };

    const xScale = d3.scaleLinear().domain([0, 800]).range([50, 750]);
    const yScale = d3.scaleLinear().domain([0, 600]).range([50, 550]);

    const links = g.selectAll("line")
        .data(jsonData.links)
        .enter()
        .append("line")
        .attr("x1", d => xScale(jsonData.nodes.find(n => n.id === d.source).x))
        .attr("y1", d => yScale(jsonData.nodes.find(n => n.id === d.source).y))
        .attr("x2", d => xScale(jsonData.nodes.find(n => n.id === d.target).x))
        .attr("y2", d => yScale(jsonData.nodes.find(n => n.id === d.target).y))
        .attr("stroke", "black")
        .attr("stroke-width", 2);

    const nodes = g.selectAll("g.node")
        .data(jsonData.nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${xScale(d.x)},${yScale(d.y)})`)
        .on("click", function (event, d) {
            event.stopPropagation();
            selectNode(d);
        });

    nodes.append("circle")
        .attr("r", 10)
        .attr("fill", "steelblue");

    nodes.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")
        .attr("fill", "white")
        .text(d => d.id);

    const tooltip = d3.select("body")
        .append("div")
        .attr("id", "tooltip")
        .style("position", "absolute")
        .style("background", "lightgrey")
        .style("padding", "10px")
        .style("border-radius", "5px")
        .style("opacity", 0)
        .style("display", "none");

    function selectNode(node) {
        resetHighlight();
        highlightNode(node);
        showTooltip(node);
    }

    function highlightNode(node) {
        g.selectAll(".influence, .highlight").remove();

        g.append("circle")
            .attr("class", "influence")
            .attr("cx", xScale(node.x))
            .attr("cy", yScale(node.y))
            .attr("r", 50)
            .attr("fill", "rgba(70, 130, 180, 0.3)");

        const connectedNodes = jsonData.links
            .filter(link => link.source === node.id || link.target === node.id)
            .map(link => jsonData.nodes.find(n => n.id === (link.source === node.id ? link.target : link.source)));

        g.selectAll("circle")
            .filter(d => connectedNodes.includes(d))
            .attr("fill", "orange");
    }

    function resetHighlight() {
        g.selectAll(".influence, .highlight").remove();
        g.selectAll("circle").attr("fill", "steelblue");
    }

    function showTooltip(node) {
        const data = d3.range(20).map((d, i) => ({ x: i, y: Math.sin(i / 2) * 10 + 20 }));

        tooltip.style("left", (xScale(node.x) + 60) + "px")
            .style("top", (yScale(node.y) - 20) + "px")
            .style("opacity", 1)
            .style("display", "block")
            .html(`<strong>Node ID:</strong> ${node.id}<br><strong>Data:</strong> ${node.data}`);

        const chartWidth = 200, chartHeight = 100;
        tooltip.selectAll("svg").remove();

        const chart = tooltip.append("svg")
            .attr("width", chartWidth)
            .attr("height", chartHeight);

        const x = d3.scaleLinear().domain([0, 20]).range([0, chartWidth]);
        const y = d3.scaleLinear().domain([0, 40]).range([chartHeight, 0]);

        const line = d3.line()
            .x(d => x(d.x))
            .y(d => y(d.y));

        chart.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("d", line);
    }
});
