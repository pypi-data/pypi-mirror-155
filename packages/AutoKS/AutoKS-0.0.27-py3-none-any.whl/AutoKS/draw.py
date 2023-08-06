# !/usr/bin/env python
# -*- coding: utf-8 -*-

from webview import create_window, start


def draw(
        graph,
        show=True,
        save=False,
        filename='filename',
        encoding='utf-8',
        canvas_size=(500, 500),
        node_font='sans-serif',
        node_fontsize=12,
        node_fontcolor='crimson',
        node_fillcolor='#ffebcd',
        node_size=12,
        edge_color='#7ab8cc',
        edge_size=2,
        edge_distance=100,
        charge=-300,
        detailed=False
):
    """
    show and/or save a graph.

    using d3.js and pywebview.
    see https://d3js.org/ & https://github.com/r0x0r/pywebview

    :param graph: a NetworkX graph.
    :param show: show graph immediately if show=True, or do not show until a
    draw_html(...show=True) is running. The graph is drawing using d3.js
    (version 3, i.e., d3v3) and is interactive. You can also modify the style of
    graph by adding other parameters.
    :param save: save output as a html file. The graph being saved is a svg
    object in the html file. Scalable vector graphic (svg) is a type of image
    format and can be open by browser software such as Chrome, Edge and Firefox,
    and can be edited by using Adobe Illustrator). Currently AutoKS can not save
    a graph as the svg file directly, but you can extract it from the html file.
    :param filename: filename of output html file. Default is "filename".
    :param encoding: encoding of output html file. Default is "utf-8".
    :param canvas_size: a list or tuple specifying the size of canvas. Default
    is (500, 500), which means 500*500 pixels.
    :param node_font: a string specifying the font of nodes in the graph.
    Default is "sans-serif".
    :param node_fontsize: a number specifying the size of labels in nodes.
    Default is 12.
    :param node_fontcolor: a string specifying the color of labels in nodes, can
    be written in HEX format or just a color name (as long as d3.js know it).
    Default is "crimson".
    :param node_fillcolor: a string specifying the color of nodes. Default is
    "#ffebcd".
    :param node_size: a number specifying the size of nodes in the graph.
    Default is 12.
    :param edge_color: a string specifying the color of edges. Default is
    "#7ab8cc".
    :param edge_size: a number specifying the width of edges in the graph.
    Default is 2.
    :param edge_distance: a number specifying the distance among nodes. Default
    is 100.
    :param charge: a number specifying the charge in the graph. Default is -300.
    :param detailed: show html contents or not. Default is False.
    :return: a list of edges.
    """

    # edges information
    edges = []
    for (u, v, wt) in graph.edges.data():
        # u and v are each node in a proposition
        edges.append({'source': f"{u}", 'target': f"{v}"})
    edges = f"{edges}"
    for i in ["source",
              "target"]:  # replace "'source'"/"'target'" to "source"/"target"
        edges = edges.replace(f"'{i}'", i)

    html = f"""
<!DOCTYPE html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<style>

.link {{
    fill: {edge_color};
    stroke: {edge_color};
    stroke-width: {edge_size}px;
}}

.node circle {{
    fill: {node_fillcolor};
    stroke: {node_fillcolor};
    stroke-width: {node_size}px;
}}

text {{
    fill: {node_fontcolor};
    font: {node_fontsize}px {node_font};
    font-weight: bold;
    pointer-events: none;
}}

</style>
<body>
<script src="https://d3js.org/d3.v3.min.js"></script>
<script>
// this script derive from http://bl.ocks.org/mbostock/2706022

// http://blog.thomsonreuters.com/index.php/mobile-patent-suits-graphic-of-the-day/
const links = {edges};
const nodes = {{}};

// Compute the distinct nodes from the links.
links.forEach(function(link) {{
  link.source = nodes[link.source] || (nodes[link.source] = {{name: link.source}});
  link.target = nodes[link.target] || (nodes[link.target] = {{name: link.target}});
}});

const width = {canvas_size[0]},
        height = {canvas_size[1]};

const force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance({edge_distance})
        .charge({charge})
        .on("tick", tick)
        .start();

const svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

const link = svg.selectAll(".link")
        .data(force.links())
        .enter().append("line")
        .attr("class", "link");

const node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .call(force.drag);

node.append("circle")
    .attr("r", 10);

node.append("text")
    .attr("dy", ".2em")
    .style("text-anchor", "middle")
    .text(function(d) {{ return d.name; }});

function tick() {{
  link
      .attr("x1", function(d) {{ return d.source.x; }})
      .attr("y1", function(d) {{ return d.source.y; }})
      .attr("x2", function(d) {{ return d.target.x; }})
      .attr("y2", function(d) {{ return d.target.y; }});

  node
      .attr("transform", function(d) {{ return "translate(" + d.x + "," + d.y + ")"; }});
}}

function mouseover() {{
  d3.select(this).select("circle").transition()
      .duration(750)
      .attr("r", 16);
}}

function mouseout() {{
  d3.select(this).select("circle").transition()
      .duration(750)
      .attr("r", 8);
}}

// d3.select("body").append("button")
//         .attr("type","button")
//         .attr("class", "downloadButton")
//         .text("Download SVG")
//         .on("click", function() {{
//             // download the svg
//             downloadSVG();
//         }});

</script>

    """

    if detailed is True:
        print(html)

    if save:
        f = open(f'{filename}.html', 'a', encoding=encoding)
        f.write(html)
        f.close()
        print(f'Save graph to "{filename}.html" successfully.')

    if graph.name:
        title = graph.name
    else:
        title = 'test'

    create_window(title=title,
                  html=html,
                  width=600,
                  height=600,
                  on_top=True)
    if show:
        start()

    return edges
