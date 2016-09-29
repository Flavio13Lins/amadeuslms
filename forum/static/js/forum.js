/*
*
* Function to load forum to modal
*
*/
function showForum(url, forum_id) {
    $.ajax({
        url: url, 
        data: {'forum_id': forum_id},
        success: function(data) {
            $(".forum_topics").html(data);

            var frm = $('#form_post');
            frm.submit(function () {
                $.ajax({
                    type: frm.attr('method'),
                    url: frm.attr('action'),
                    data: frm.serialize(),
                    success: function (data) {
                        $("#posts_list").append(data);
                        frm[0].reset();
                    },
                    error: function(data) {
                        console.log(frm.serialize());
                        console.log('Error');
                    }
                });
                return false;
            });
        }
    });

    $('#forumModal').modal();
}

function answer(id, url) {
    $.ajax({
        url: url, 
        success: function(data) {
            $("#post_"+id).find(".answer_post").html(data);
        }
    });

    $("#post_"+id).find(".answer_post").show();
}

function showPosts(url, forum) {
    if ($("#collapse" + forum).hasClass('in')) {
        $("#collapse" + forum).collapse('hide');
    } else {
        $.ajax({
            url: url, 
            data: {'forum': forum},
            success: function(data) {
                $("#collapse" + forum).find(".well").html(data);
            }
        });

        $("#collapse" + forum).collapse('show');
    }
}

function showPostsAnswers(url, post) {
    if ($("#collapse" + post).hasClass('in')) {
        $("#collapse" + post).collapse('hide');
    } else {
        $.ajax({
            url: url, 
            data: {'post': post},
            success: function(data) {
                $("#collapse" + post).find(".well").html(data);
            }
        });

        $("#collapse" + post).collapse('show');
    }
}