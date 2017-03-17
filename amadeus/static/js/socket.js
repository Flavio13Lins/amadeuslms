if (("Notification" in window)) {
	if (Notification.permission !== 'denied') {
		Notification.requestPermission();
	}
}

socket = new WebSocket("ws://" + window.location.host + "/");

socket.onmessage = function(e) {
	content = JSON.parse(e.data);

	if (content.type == "mural") {
		if (content.subtype == "post") {
			muralNotificationPost(content);
		} else if (content.subtype == "mural_update") {
			muralNotificationMuralUpdate(content);
		} else if (content.subtype == "mural_delete") {
			muralNotificationMuralDelete(content);
		} else if (content.subtype == "comment") {
			muralNotificationComment(content);
		}
	} else if (content.type == "chat") {
		messageReceived(content);
	}
}
// Call onopen directly if socket is already open
if (socket.readyState == WebSocket.OPEN) socket.onopen();

function muralNotificationPost(content) {
	var page = window.location.pathname,
		render = (content.paths.indexOf(page) != -1),
		is_resource = (page.indexOf("resource") != -1);

	if ((render && page.indexOf(content.post_type) != -1) || (render && content.post_type == "general") || (render && is_resource)) {
		if (content.accordion) {
			var section = $(content.container);

			if (section.is(':visible')) {
				section.find('.posts').prepend(content.complete);

		        section.find('.no-subjects').hide();
		    }
		} else {
			$(content.container).prepend(content.complete);

	        $('.no-subjects').attr('style', 'display:none');
		}	
	} else {
		$('.mural_badge').each(function () {
			var actual = $(this).text();

			if (actual != "+99") {
				actual = parseInt(actual, 10) + 1;

				if (actual > 99) {
					actual = "+99";
				}

				$(this).text(actual);
			}

			$(this).show();
		});

		$('.mural-tabs').find('li').each(function () {
			var identity = $(this).data('mural');

			if (identity == content.post_type) {
				var span = $(this).find('span'),
					actual = span.text();

				actual = parseInt(actual, 10) + 1;

				span.text(actual);
			}
		});

		if (content.post_type == "subjects") {
			var slug = content.container.substring(1, content.container.length),
				subject_mbadge = $("#subject_" + slug).find('.mural_notify'),
				actual = subject_mbadge.text();

			if (actual != "+99") {
				actual = parseInt(actual, 10) + 1;

				if (actual > 99) {
					actual = "+99";
				}

				subject_mbadge.text(actual);
			}

			subject_mbadge.show();
		}
	}

	if (("Notification" in window)) {
		var options = {
			icon: content.user_icon,
			body: content.simple_notify
		}

	    if (Notification.permission === "granted") {
	    	var notification = new Notification("", options);

	    	setTimeout(notification.close.bind(notification), 3000);
	    }
  	}
}

function muralNotificationMuralUpdate(content) {
	var page = window.location.pathname,
		render = (content.paths.indexOf(page) != -1);

	if (render) {
		var mural_item = $(content.container);

		if (mural_item.is(":visible") || mural_item.is(":hidden")) {
			mural_item.before(content.complete);

			mural_item.remove();
		}
	}
}

function muralNotificationMuralDelete(content) {
	var page = window.location.pathname,
		render = (content.paths.indexOf(page) != -1);

	if (render) {
		var mural_item = $(content.container);

		if (mural_item.is(":visible") || mural_item.is(":hidden")) {
			mural_item.remove();
		}
	}
}

function muralNotificationComment(content) {
	var page = window.location.pathname,
		render = (content.paths.indexOf(page) != -1),
		is_resource = (page.indexOf("resource") != -1),
		checker = "general";

	switch (content.post_type) {
		case "categorypost":
			checker = "categories";
			break;
		case "subjectpost":
			checker = "subjects";
			break;
	}

	if ((render && page.indexOf(checker) != -1) || (render && content.post_type == "generalpost" && page.indexOf("categories") == -1 && page.indexOf("subjects") == -1) || (render && is_resource)) {
		var section = $(content.container);

		if (section.is(":visible") || section.is(":hidden")) {
			var comments = section.find('.comment-section');

			comments.append(content.complete);
		}
	} else {
		$('.mural_badge').each(function () {
			var actual = $(this).text();

			if (actual != "+99") {
				actual = parseInt(actual, 10) + 1;

				if (actual > 99) {
					actual = "+99";
				}

				$(this).text(actual);
			}

			$(this).show();
		});

		$('.mural-tabs').find('li').each(function () {
			var identity = $(this).data('mural');

			if ((identity == checker) || (identity == "general" && content.post_type == "generalpost")) {
				var span = $(this).find('span'),
					actual = span.text();

				actual = parseInt(actual, 10) + 1;

				span.text(actual);
			}
		});

		if (content.post_type == "subjectpost") {
			var subject_mbadge = $("#subject_" + content.type_slug).find('.mural_notify'),
				actual = subject_mbadge.text();

			if (actual != "+99") {
				actual = parseInt(actual, 10) + 1;

				if (actual > 99) {
					actual = "+99";
				}

				subject_mbadge.text(actual);
			}

			subject_mbadge.show();
		}
	}

	if (("Notification" in window)) {
		var options = {
			icon: content.user_icon,
			body: content.simple_notify
		}

	    if (Notification.permission === "granted") {
	    	var notification = new Notification("", options);

	    	setTimeout(notification.close.bind(notification), 3000);
	    }
  	}
}

function messageReceived(content) {
	var talk_modal = $("#" + content.container);

	if (talk_modal.is(':visible')) {
		var new_msg_btn = talk_modal.find('.messages_new'),
			msg_container = talk_modal.find('.messages-container');

		talk_modal.find('.messages-list').append(content.complete);

		new_msg_btn.show();

		new_msg_btn.click(function () {
			var height = msg_container[0].scrollHeight;

            msg_container.animate({scrollTop: height}, 0);

            $(this).hide();
		});
	}

	if (("Notification" in window)) {
		var options = {
			icon: content.user_icon,
			body: content.simple_notify
		}

	    if (Notification.permission === "granted") {
	    	var notification = new Notification(content.notify_title, options);

	    	setTimeout(notification.close.bind(notification), 3000);
	    }
  	}	
}