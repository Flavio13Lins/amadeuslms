function setAudios(files) {
  let totalTime = 0;

  files.forEach(file => {
    let audio = new Audio(file.file);

    if (file.resource_link !== null && file.resource_link !== undefined) {
      showResourcesTable(file.resource_link, file.tagName);
    }

    setTimeout(function() {
      let $ballon = $('.ballon').find('p');

      $($ballon).html(file.text);

      $('.ballon').show();

      audio.play();
    }, totalTime);

    totalTime += (file.duration * 1000);
  });

  setTimeout(function() {
    $('.ballon').hide();
  }, totalTime);

  return totalTime;
}

function playAvatarCloud(files) {
  $('#tagCloudy').css('box-shadow', '0 0 0 999px rgba(0, 0, 0, 0.5)');
  $('.avatarBox').css('z-index', '9');
  $('#otherIndicators svg').css('filter', 'brightness(0.5)');
  $('.graph-container svg').css('filter', 'brightness(0.5)');

  let totalTime = setAudios(files);

  setTimeout(function() {
    $('#tagCloudy').css('box-shadow', 'none');
    $('#otherIndicators svg').css('filter', 'brightness(1)');
    $('.graph-container svg').css('filter', 'brightness(1)');
  }, totalTime);
}

function showResourcesTable(link, tagName) {
  d3.select('#modal_cloudy_loading_ball').style('display', 'inherit');
  d3.select('#modal-table').style('display', 'none');

  const modal = document.querySelector('#tagModal');
  const container = d3.select('#resources-list');

  modal.querySelector('#modalTittle').innerText =
      `Tag: ${tagName.toUpperCase()}`;

  container.selectAll('.resource').remove();

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

      return p1 > p2 ? 1 :
                       p1 < p2 ? -1 :
                                 d1.qtd_access < d2.qtd_access ?
                                 1 :
                                 d1.qtd_access > d2.qtd_access ? -1 : 0;
    });

    makeTable(dataset, '#table-container', '#resources_pag', 10);

    d3.select('#modal_cloudy_loading_ball').style('display', 'none');
    d3.select('#modal-table').style('display', 'inherit');
  });

  $('#tagModal').modal('show');
}