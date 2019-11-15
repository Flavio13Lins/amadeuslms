let cloudWord = undefined;

function makeTable(data, tableId, paginationId, nrows) {
  const $table = $(tableId);
  const $pagination = $(paginationId);
  const pages = Math.ceil(data.length / nrows);

  const $tbody = $table.find("tbody");

  $tbody.html("");
  $pagination.html("");

  data.forEach((item, index) => {
    const display = index >= nrows ? 'style="display: none"' : "";

    let line = `<tr id='resource_${index}' class='tag_resource' ${display}>`;

    line = `${line}<td style="white-space: inherit"><a href='${item.access_url}'>${item.resource_name}</a></td>`;
    line = `${line}<td>${item.qtd_my_access}</td>`;
    line = `${line}<td>${item.qtd_access}</td>`;

    line = `${line}</tr>`;

    $tbody.append(line);
  });

  $pagination.append("<li class='page-item previous'>&lt;</li>");

  [...Array(pages).keys()].forEach(i => {
    const page = `<li class='page-item page-item-number' data-page=${i + 1}>${i + 1}</li>`;

    $pagination.append(page);
  });

  $(".page-item-number[data-page=1]").addClass("active");

  $pagination.append("<li class='page-item next'>&gt;</li>");

  $(".page-item-number").click(e => {
    const page = $(e.target).data("page");
    const init = page * nrows - nrows;
    const end = page * nrows;

    $(".page-item-number").removeClass("active");
    $(e.target).addClass("active");

    $(".tag_resource").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $(".previous").click(() => {
    let page = $(".page-item-number.active").data("page");

    page = page === 1 ? 1 : page - 1;

    const init = page * nrows - nrows;
    const end = page * nrows;

    $(".page-item-number").removeClass("active");
    $(`.page-item-number[data-page=${page}]`).addClass("active");

    $(".tag_resource").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $(".next").click(() => {
    let page = $(".page-item-number.active").data("page");

    page = page === pages ? pages : page + 1;

    const init = page * nrows - nrows;
    const end = page * nrows;

    $(".page-item-number").removeClass("active");
    $(`.page-item-number[data-page=${page}]`).addClass("active");

    $(".tag_resource").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });
}

function makeTagTable(data, nrows) {
  const $table = $("#tag-access");
  const $pagination = $("#tag-pagination");

  const pages = Math.ceil(data.length / nrows);

  const $tbody = $table.find("tbody");

  $tbody.html("");
  $pagination.html("");

  data.forEach((item, index) => {
    const display = index >= nrows ? 'style="display: none"' : "";

    let line = `<tr id='tag_${index}' class='tag_cloud' ${display}>`;

    line = `${line}<td>${index + 1}</td>`;
    line = `${line}<td><a class='tag_table_resources' data-link='${item.link}'>${item.key}</a></td>`;
    line = `${line}<td>${item.value}</td>`;
    line = `${line}</tr>`;

    $tbody.append(line);
  });

  $pagination.append("<li class='page-item previous'>&lt;</li>");

  [...Array(pages).keys()].forEach(i => {
    const page = `<li class='page-item page-item-number' data-page=${i + 1}>${i + 1}</li>`;

    $pagination.append(page);
  });

  $("#tag-pagination .page-item-number[data-page=1]").addClass("active");

  $pagination.append("<li class='page-item next'>&gt;</li>");

  $("#tag-pagination .page-item-number").click(e => {
    const page = $(e.target).data("page");
    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#tag-pagination .page-item-number").removeClass("active");
    $(e.target).addClass("active");

    $("#tag-access .tag_cloud").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $("#tag-pagination .previous").click(() => {
    let page = $("#tag-pagination .page-item-number.active").data("page");

    page = page === 1 ? 1 : page - 1;

    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#tag-pagination .page-item-number").removeClass("active");
    $(`#tag-pagination .page-item-number[data-page=${page}]`).addClass("active");

    $("#tag-access .tag_cloud").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $("#tag-pagination .next").click(() => {
    let page = $("#tag-pagination .page-item-number.active").data("page");

    page = page === pages ? pages : page + 1;

    const init = page * nrows - nrows;
    const end = page * nrows;

    $("#tag-pagination .page-item-number").removeClass("active");
    $(`#tag-pagination .page-item-number[data-page=${page}]`).addClass("active");

    $("#tag-access .tag_cloud").each((i, el) => {
      if (i >= init && i < end) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  });

  $("#tag-access .tag_table_resources").on("click", e => {
    const $el = $(e.target);
    const link = $el.data("link");
    const tag = $el.text();

    $("#modal_cloudy_loading_ball").css("display", "inherit");
    $("#modal-table").css("display", "none");

    const modal = $("#tagModal");
    const container = $("#resources-list");

    modal.find("#modalTittle").text(`Tag: ${tag.toUpperCase()}`);

    container.html("");

    $.get(link, dataset => {
      dataset = dataset.sort((d1, d2) => {
        if (isNaN(d1.qtd_access) || +d1.qtd_access == 0) {
          d1.qtd_access = 0;
        }

        if (isNaN(d2.qtd_access) || +d2.qtd_access == 0) {
          d2.qtd_access = 0;
        }

        if (isNaN(d1.qtd_my_access) || +d1.qtd_my_access == 0) {
          d1.qtd_my_access = 0;
        }

        if (isNaN(d2.qtd_my_access) || +d2.qtd_my_access == 0) {
          d2.qtd_my_access = 0;
        }

        const p1 = d1.qtd_my_access / d1.qtd_access,
          p2 = d2.qtd_my_access / d2.qtd_access;

        return p1 > p2 ? 1 : p1 < p2 ? -1 : d1.qtd_access < d2.qtd_access ? 1 : d1.qtd_access > d2.qtd_access ? -1 : 0;
      });

      makeTable(dataset, "#table-container", "#resources_pag", 10);

      $("#modal_cloudy_loading_ball").css("display", "none");
      $("#modal-table").css("display", "inherit");
    });

    $("#tagModal").modal("show");
  });
}

function cloud() {
  const dimensions = document.getDimensions("#cloudy");
  let width =
    dimensions.w -
    $("#cloudy")
      .css("padding-left")
      .match(/[0-9]+/)[0] -
    $("#cloudy")
      .css("padding-right")
      .match(/[0-9]+/)[0];

  width = width === 0 ? 775 : width;

  const height = (width * 1) / 2 > 360 ? 360 : width / 2 < 50 ? 50 : width / 2;

  $.get($("#cloudy").data("url"), data => {
    d3.select("#cloudy_loading_ball").style("display", "none");

    data = data.map(item => ({
      key: item.tag_name,
      value: item.qtd_access,
      myvalue: item.qtd_my_access,
      link: item.details_url,
      text: item.tag_name,
    }));

    data.sort((d1, d2) => (d1.value > d2.value ? -1 : d1.value < d2.value ? 1 : 0));

    makeTagTable(data, 10);

    const tags = data.slice(0, Math.floor((30 / 1000) * width));

    const dataconfig = {
      parent: "#cloudy",
      data: tags,
      tableData: data,
      max: 50,
      font: "Roboto,Helvetica,Arial,sans-serif",
      spiral: "rectangular",
      scale: "linear",
      angles: {
        from: 0,
        to: 0,
        n: 1,
      },
      dimensions: {
        w: width,
        h: height,
      },
      interactions: {
        click: (element, data) => {
          d3.select("#modal_cloudy_loading_ball").style("display", "inherit");
          d3.select("#modal-table").style("display", "none");

          const modal = document.querySelector("#tagModal");
          const container = d3.select("#resources-list");

          modal.querySelector("#modalTittle").innerText = `Tag: ${data.text.toUpperCase()}`;

          container.selectAll(".resource").remove();

          $.get(data.link, dataset => {
            dataset = dataset.sort((d1, d2) => {
              
              if (isNaN(d1.qtd_access) || +d1.qtd_access == 0) {
                d1.qtd_access = 0;
              }

              if (isNaN(d2.qtd_access) || +d2.qtd_access == 0) {
                d2.qtd_access = 0;
              }

              if (isNaN(d1.qtd_my_access) || +d1.qtd_my_access == 0) {
                d1.qtd_my_access = 0;
              }

              if (isNaN(d2.qtd_my_access) || +d2.qtd_my_access == 0) {
                d2.qtd_my_access = 0;
              }

              const p1 = d1.qtd_my_access / d1.qtd_access,
                p2 = d2.qtd_my_access / d2.qtd_access;

              return p1 > p2
                ? 1
                : p1 < p2
                ? -1
                : d1.qtd_access < d2.qtd_access
                ? 1
                : d1.qtd_access > d2.qtd_access
                ? -1
                : 0;
            });

            makeTable(dataset, "#table-container", "#resources_pag", 10);

            d3.select("#modal_cloudy_loading_ball").style("display", "none");
            d3.select("#modal-table").style("display", "inherit");
          });

          $("#tagModal").modal("show");
        },
      },
      tooltip: {
        text: "Tag: <key>\nTotal de acessos: <value> \nMeus acessos: <myvalue>",
      },
      filltext: (a, transition) => {
        transition = transition || 0;

        a.fillpattern = d3
          .scaleLinear()
          .domain([0, 1])
          .interpolate(d3.interpolateHcl)
          .range([d3.rgb("#8EC99A"), d3.rgb("#162318")]);

        const prop = a.chartConfig.mymax / a.chartConfig.max;

        a.scalePercent = (x, y) => {
          if (x > y) {
            return (y * 0.1 * prop) / x + 0.2;
          }

          return 1 - (x * 0.7) / (y * prop);
        };

        a.wordsv5
          .transition()
          .duration(transition)
          .attr("fill", (d, i) => a.fillpattern(a.scalePercent(d.myvalue, d.value)));
      },
    };

    cloudWord = new CloudWord(dataconfig);
  });
}

function view_toogle() {
  if (cloudWord) cloudWord.view_toogle();
}

$(function() {
  cloud();
});
