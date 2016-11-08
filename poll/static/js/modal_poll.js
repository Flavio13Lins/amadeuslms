// 
// //controles do modal
// $(window).ready(function() { // utilizado para abrir o modal quando tiver tido algum erro no preenchimento do formulario
//   if($('.not_submited').length){
//       $('#poll').modal('show');
//   }
// });

var Answer = {
    init: function(url) { // utilizado para adicionar um novo campo de resposta
      $.get(url, function(data){
        $("#form").append(data);
        var cont = 1;
        $("#form div div div input").each(function(){
                $(this).attr('name',cont++);
        });
      });
    }
};

var Submite = {
  create: function(url,dados, slug){
    $('#poll').modal('hide');
    var poll = null;
      $.post(url,dados, function(data){
        $.ajax({
          method: "get",
          url: data["view"],
          success: function(view){
            $('#list-topic-'+ slug +'-poll').append(view);
          }
        });
        $.ajax({
          method: "get",
          url: data["edit"],
          success: function(edit){
            $('#list-topic-'+ slug +'-poll-edit').append(edit);
          }
        });
        $("#requisicoes_ajax").empty();
        alertify.alert('Link successfully created!');
      }).fail(function(data){
        $("div.modal-backdrop.fade.in").remove();
        $("#requisicoes_ajax").empty();
        $("#requisicoes_ajax").append(data.responseText);
        $('#poll').modal('show');
      });
  },
  update: function(url,dados, slug_poll, slug_topic){
    $('#poll').modal('hide');
      $.post(url,dados, function(data){
        $('#list-topic-'+ slug_topic +'-poll #'+slug_poll).remove();
        $('#list-topic-'+ slug_topic +'-poll #'+slug_poll).remove();
        $('#list-topic-'+ slug_topic +'-poll').append(data);
        $('#list-topic-'+ slug_topic +'-poll-edit').append(data);
        $("#requisicoes_ajax").empty();
        alertify.alert('Link successfully updated!')
      }).fail(function(data){
        $("div.modal-backdrop.fade.in").remove();
        $("#requisicoes_ajax").empty();
        $("#requisicoes_ajax").append(data.responseText);
        $('#poll').modal('show');
      });
  },
  remove: function(url,dados, id_li_link){
    $('#poll').modal('hide');
      $.post(url,dados, function(data){
        $(id_li_link).remove();
        $(id_li_link+"_div").remove();
        $("#requisicoes_ajax").empty();
        $("div.modal-backdrop.fade.in").remove();
      }).fail(function(){
        $("#requisicoes_ajax").empty();
        $("#requisicoes_ajax").append(data);
        $('#poll').modal('show');
      });
  }
}
