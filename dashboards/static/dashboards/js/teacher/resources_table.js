let ResourcesChartCounter = 0;

class ResourcesChart {
  constructor(chartConfig) {
    this.create(ResourcesChart.validData(chartConfig)).draw();
  }

  static validData(chartConfig) {
    if (chartConfig.data === undefined) {
      console.error("Invalid dataset");
      throw new Exception();
    }

    if (chartConfig.name === undefined) chartConfig.name = `resourcesChart ${ResourcesChartCounter++}`;

    if (chartConfig.target === undefined) chartConfig.target = "body";

    if (chartConfig.dimensions === undefined) chartConfig.dimensions = {};
    if (chartConfig.dimensions.width === undefined) chartConfig.dimensions.width = 300;
    if (chartConfig.dimensions.height === undefined) chartConfig.dimensions.height = 300;

    if (chartConfig.layout == undefined) chartConfig.layout = {};
    if (chartConfig.layout.qtd == undefined) chartConfig.layout.qtd = 50;
    if (chartConfig.layout.absForce == undefined) chartConfig.layout.absForce = 0.5;

    chartConfig.interactions = d3.validEvents(chartConfig.interactions);

    if (chartConfig.tooltip !== undefined) {
      if (chartConfig.tooltip.text === undefined) {
        chartConfig.tooltip = undefined;
      } else {
        chartConfig.tooltip.name = `${chartConfig.name}-toolTip`;

        if (chartConfig.svg) chartConfig.tooltip.parent = chartConfig.parent;
        else chartConfig.tooltip.parent = `#${chartConfig.name}-container`;
      }
    }

    return chartConfig;
  }

  create(chartConfig) {
    const a = this;
    this.chartConfig = chartConfig;

    a.names = Array.removeRepetitions(a.chartConfig.data.map(d => d.resource_name));
    a.names = a.names.sort();

    a.data = a.names.map(d => {
      return { resource: d, value: 0 };
    });

    for (let i = 0; i < a.chartConfig.data.length; i++) {
      const index = a.names.indexOf(a.chartConfig.data[i].resource_name);

      if (a.data[index].access_url === undefined) a.data[index].access_url = a.chartConfig.data[i].access_url;
      a.data[index].value += a.chartConfig.data[i].value;
    }

    a.data = a.data.sort((d1, d2) => {
      return d1.value < d2.value ? 1 : d1.value > d2.value ? -1 : 0;
    });

    this.a1 = 0;

    this.nodes = a.data.filter((d, i) => {
      if (i < a.chartConfig.layout.qtd) {
        a.a1 += d.value;

        return true;
      }

      return false;
    });

    a.nodes = a.nodes.map((i, j) => {
      return { user: `user${j}`, name: i.name, value: i.value, image: i.image, link: i.link };
    });

    this.svg = d3
      .select(a.chartConfig.parent)
      .append("svg")
      .attr("id", `${a.chartConfig.name}-container`);

    this.g = this.svg.append("g");

    this.bubbles = this.g
      .selectAll(".user-dot")
      .data(a.nodes)
      .enter()
      .append("g")
      .attr("class", "user-dot");

    return this;
  }

  draw() {
    const a = this;

    this.prop =
      Math.sqrt(((a.chartConfig.dimensions.width - 50) * (a.chartConfig.dimensions.height - 50)) / a.a1) / 2.5;

    a.nodes = a.nodes.map(d => {
      d.r = Math.round(Math.sqrt(d.value) * a.prop);

      return d;
    });

    const forcexy = (abs, prop) => {
      return { x: Math.sqrt((abs * abs * prop) / (prop + 1)), y: Math.sqrt((abs * abs) / (prop + 1)) };
    };

    const forceprop = x => {
      return 2.287081443 * Math.exp(-0.9045466968 * x);
    };

    this.forces = forcexy(
      a.chartConfig.layout.absForce,
      forceprop(a.chartConfig.dimensions.width / a.chartConfig.dimensions.height),
    );

    function constant(_) {
      return function() {
        return _;
      };
    }

    function boundedBox() {
      let nodes, sizes, bounds;
      let size = constant([0, 0]);

      function force() {
        let node, size;
        let xi, x0, x1, yi, y1, y2;
        let i = -1;

        while (++i < nodes.length) {
          node = nodes[i];
          size = sizes[i];

          xi = node.x + node.vx;

          x0 = bounds[0][0] - xi;
          x1 = bounds[1][0] - (xi + size[0]);

          yi = node.y + node.vy;

          y0 = bounds[0][1] - yi;
          y1 = bounds[1][1] - (yi + size[1]);

          if (x0 > 0 || x1 < 0) {
            node.x += node.vx;
            node.vx = -node.vx;

            if (node.vx < x0) {
              node.x += x0 - node.vx;
            }

            if (node.vx > x1) {
              node.x += x1 - node.vx;
            }
          }

          if (y0 > 0 || y1 < 0) {
            node.x += node.vx;
            node.vx = -node.vx;

            if (node.vx < y0) {
              node.x += y0 - node.vx;
            }

            if (node.vx > y1) {
              node.x += y1 - node.vx;
            }
          }
        }
      }

      force.initialize = _ => {
        sizes = (nodes = _).map(size);
      };

      force.bounds = function(_) {
        return arguments.length ? ((bounds = _), force) : bounds;
      };

      force.size = _ => {
        return arguments.length ? ((size = typeof _ === "function" ? _ : constant(_)), force) : size;
      };

      return force;
    }

    this.boxForce = boundedBox()
      .bounds([[0, 0], [a.chartConfig.dimensions.width, a.chartConfig.dimensions.height]])
      .size(d => {
        return [d.r * 2, d.r * 2];
      });

    function ticked() {
      a.svg.selectAll(".user-dot").attr("transform", d => {
        return `translate(${d.x}, ${d.y})`;
      });
    }

    this.simulation = d3
      .forceSimulation(this.nodes)
      .velocityDecay(0.2)
      .force("x", d3.forceX().strength(this.forces.x))
      .force("y", d3.forceY().strength(this.forces.y))
      .force(
        "collide",
        d3
          .forceCollide()
          .radius(d => {
            return d.r + 0.5;
          })
          .iterations(2),
      )
      .on("tick", ticked);

    this.svg.attr("width", a.chartConfig.dimensions.width).attr("height", a.chartConfig.dimensions.height);

    this.g
      .attr("transform", `translate(${a.chartConfig.dimensions.width / 2}, ${a.chartConfig.dimensions.height / 2})`)
      .attr("id", "bubbleChart");

    this.svg
      .append("defs")
      .append("linearGradient")
      .attr("id", "svgGradient")
      .attr("x1", "0%")
      .attr("x2", "100%")
      .attr("y1", "0%")
      .attr("y2", "100%")
      .selectAll("stop")
      .data([
        { class: "start", offset: "0%", stop_color: "#007991", stop_opacity: "1" },
        { class: "end", offset: "100%", stop_color: "#78ffd6", stop_opacity: "1" },
      ])
      .enter()
      .append("stop")
      .attr("class", d => d.class)
      .attr("offset", d => d.offset)
      .attr("stop-color", d => d.stop_color)
      .attr("stop-opacity", d => d.stop_opacity);

    this.svg
      .select("defs")
      .selectAll("pattern")
      .data(a.nodes)
      .enter()
      .append("pattern")
      .attr("id", (d, i) => d.user)
      .attr("width", d => d.r)
      .attr("height", d => d.r)
      .append("image")
      .attr("xlink:href", (d, i) => d.image)
      .attr("width", d => 2 * d.r)
      .attr("height", d => 2 * d.r)
      .attr("x", 0)
      .attr("y", 0);

    this.bubbles
      .append("circle")
      .attr("class", "img")
      .attr("r", d => d.r)
      .attr("stroke", "url(#svgGradient")
      .attr("fill", "#007991")
      .attr("stroke-width", 1)
      .attr("opacity", 1);

    this.bubbles
      .select(".img")
      .transition()
      .delay((d, i) => 900 * Math.sqrt(i))
      .attr("fill", d => `url(#${d.user})`);

    this.bubbles
      .select(".temp")
      .transition()
      .delay((d, i) => 910 * Math.sqrt(i))
      .duration(500)
      .attr("opacity", 0);

    this.bubbles
      .select(".temp")
      .transition()
      .delay((d, i) => 910 * Math.sqrt(i) + 510)
      .remove();

      if (isNaN(this.prop) || !isFinite(this.prop)) {
        this.svg
          .append("rect")
          .attr("width", "100%")
          .attr("fill", "#fff");
        this.svg
          .append("text")
          .attr("x", "20%")
          .attr("y", "50%")
          .attr("dy", "0em")
          .text("Para período selecionado não houve");
        this.svg
          .append("text")
          .attr("x", "20%")
          .attr("y", "50%")
          .attr("dy", "1em")
          .text("registro de acesso dos participantes");
      }


    this.tooltipConstruct();
    this.addInteractions();

    return this;
  }

  tooltipConstruct() {
    const a = this;

    if (this.toolTip === undefined) {
      if (this.chartConfig.tooltip !== undefined) {
        this.toolTip = new ToolTip(this.chartConfig.tooltip);

        a.chartConfig.interactions.mouseover.push((element, data) => a.toolTip.show(data));
        a.chartConfig.interactions.mousemove.push((element, data) => a.toolTip.move());
        a.chartConfig.interactions.mouseout.push((element, data) => a.toolTip.hide());
      }
    }

    return this;
  }

  addInteractions() {
    const a = this;

    if (a.interactionsAdded) {
      return;
    }

    a.interactionsAdded = true;
    a.chartConfig.interactions.mouseover.push((element, data) => {
      const currentEl = d3.select(element).select("rect");

      currentEl.attr("opacity", 0.8);
    });

    a.chartConfig.interactions.mouseout.push((element, data) => {
      const currentEl = d3.select(element).select("rect");
      currentEl.attr("opacity", 1);
    });

    d3.addEvents(a.bubbles, a.chartConfig.interactions);

    return this;
  }
 }

$(function() {
  const dataRecourseUrl = $(".table_resources").data("url");
  $(".resources_access_table").show();
  loadDataResources(dataRecourseUrl, "", "");
  
});

function makeRecouresTable(data, nrows) {
  const $table = $("#resources_table");
  const $pagination = $("#resources_table_pag");

  const pages_resources_table = Math.ceil(data.length / nrows);

  const $tbody = $table.find("tbody");

  $tbody.html("");
  $pagination.html("");

  data.forEach((item, index) => {
    
    const display = index >= nrows ? 'style="display: none"' : "";

    let line = `<tr id='resources_access_${index}' class='resource_access' ${display}>`;

    line = `${line}<td>${index + 1}</td>`;
    line = `${line}<td><a href='${item.access_url}'>${item.resource_name}</a></td>`;
    line = `${line}<td>${item.qtd_access}</td>`;
    line = `${line}</tr>`;
    
    $tbody.append(line);
  });

  $pagination.append("<li class='page-item previous'>&lt;</li>");

  [...Array(pages_resources_table).keys()].forEach(i => {
    const page = `<li class='page-item page-item-number' data-page=${i + 1}>${i + 1}</li>`;
    
      $pagination.append(page);
      if(i>9)
        $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).hide();
  });

  $("#resources_table_pag .page-item-number[data-page=1]").addClass("active");

  $pagination.append("<li class='page-item next'>&gt;</li>");

  $("#resources_table_pag .page-item-number").click(e => {
    const page = $(e.target).data("page");
    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#resources_table_pag .page-item-number").removeClass("active");
    $(e.target).addClass("active");

    $("#resources_table .resource_access").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $("#resources_table_pag .previous").click(() => {
    let page = $("#resources_table_pag .page-item-number.active").data("page");
    
    page = page === 1 ? 1 : page - 1;
    if(page>10){
      
      [...Array(pages_resources_table).keys()].forEach(i => {
        
        if(i<page+5 && i> page-5)
          $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).show();
        });
    }
    else { 
      [...Array(pages_resources_table).keys()].forEach(i => {
        if(i>9)
            $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).hide();
        else
        $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).show();
      });

    }
    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#resources_table_pag .page-item-number").removeClass("active");
    $(`#resources_table_pag .page-item-number[data-page=${page}]`).addClass("active");

    $("#resources_table .resource_access").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $("#resources_table_pag .next").click(() => {
    let page = $("#resources_table_pag .page-item-number.active").data("page");
    
    page = page === pages_resources_table ? pages_resources_table : page + 1;
    if(page>10){
      
      [...Array(pages_resources_table).keys()].forEach(i => {
        
        if(i<page+5 && i> page-5)
          $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).show();
        else if(i<pages_resources_table-9)
          $(`#resources_table_pag .page-item-number[data-page=${i+1}]`).hide();
      });

    }
    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#resources_table_pag .page-item-number").removeClass("active");
    $(`#resources_table_pag .page-item-number[data-page=${page}]`).addClass("active");

    $("#resources_table .resource_access").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });
  $("#resources_table th.sort").off("click");
  $("#resources_table th.sort").on("click", el => {
    el.preventDefault();
    el.stopPropagation();

    const $el = $(el.target);
    const sort = $el.data("sort");
    const $icon = $($el.find("i"));
    const isAscending = $icon.hasClass("fa-sort-up");

    if (isAscending) {
      $("#resources_table th.sort i")
        .removeClass("fa-sort-up")
        .removeClass("fa-sort-down")
        .removeClass("fa-sort")
        .addClass("fa-sort");

      $icon.removeClass("fa-sort").addClass("fa-sort-down");

      if (sort === "resource_name") {
        data.sort((a, b) => a.resource_name.localeCompare(b.resource_name)).reverse();

        makeRecouresTable(data, 10);
      } else {
        data.sort((a, b) => (a.qtd_access > b.qtd_access ? 1 : a.qtd_access < b.qtd_access ? -1 : 0)).reverse();

        makeRecouresTable(data, 10);
      }
    } else {
      $("#students_table th.sort i")
        .removeClass("fa-sort-up")
        .removeClass("fa-sort-down")
        .removeClass("fa-sort")
        .addClass("fa-sort");

      $icon.removeClass("fa-sort").addClass("fa-sort-up");

      if (sort === "resource_name") {
        data.sort((a, b) => a.resource_name.localeCompare(b.resource_name));

        makeRecouresTable(data, 10);
      } else {
        data.sort((a, b) => (a.qtd_access > b.qtd_access ? 1 : a.qtd_access < b.qtd_access ? -1 : 0));

        makeRecouresTable(data, 10);
      }
    }
  });
}

function loadDataResources(url, dataIni, dataEnd) {
  $(".resources_access_table").show();
  $.get(url, { data_ini: dataIni, data_end: dataEnd }, dataset => {
    
    dataset = dataset.map(d => {
    d.value = d.qtd_access;
      

      return d;
    });
    

    makeRecouresTable(dataset, 10);
  });
  
}
