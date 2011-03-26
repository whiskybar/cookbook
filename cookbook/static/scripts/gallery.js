$(function() {
	// do feature detection
	var multipleUpload = !!$('<input type="file" multiple>').get(0).files;
	if (!FileReader || (!Modernizr.draganddrop && !multipleUpload)) {
		showUnsupportedError();
		return;
	}

	var ALLOWED_TYPES = ['image/png', 'image/jpg'],
	    queue = loadFromStorage();

	function showUnsupportedError() {
		$('<div>', {
			id: 'gallery-upload-unsupported',
			html: 'Pro nahrání obrázků použijte prosím moderní moderní prohlížeč.'

		}).appendTo('#recipe-edit');
	}

	if (!$('#recipe-edit')) {
		return;
	}

	function buildMultipartString(files) {
		var boundary = '------multipartformboundary' + (new Date).getTime(),
		    dashdash = '--',
		    crlf = '\r\n';

		var builder = '';

		builder += dashdash;
		builder += boundary;
		builder += crlf;

		_.each(files, function(file) {
			builder += 'Content-Disposition: form-data; name="images"';
			if (file.fileName) {
				builder += '; filename="' + file.fileName + '"';
			}
			builder += crlf;

			builder += 'Content-Type: application/octet-stream';
			builder += crlf + crlf;

			builder += file.getAsBinary();
			builder += crlf;

			builder += dashdash;
			builder += boundary;
			builder += crlf;
		});

		builder += dashdash;
		builder += boundary;
		builder += dashdash;
		builder += crlf;

		return [boundary, builder];
	}

	function uploadQueue() {
		var message = buildMultipartString(queue),
		    xhr = new XMLHttpRequest();

		var uri = window.location.pathname;
		uri = uri.substr(0, uri.length - 1).split('/');
		uri.pop();
		uri.push('upload', '');
		uri = uri.join('/');

		xhr.open('POST', uri, true);
		xhr.setRequestHeader('content-type', 'multipart/form-data; boundary=' + message[0]);
		xhr.sendAsBinary(message[1]);
		return false;
	}

	function loadFromStorage() {
		var len = parseInt(localStorage.getItem('queueLength')),
		    queue = [];
		for (var i = 0; i < len; i++) {
			queue.push(localStorage.getItem('queueItem-' + (i+1)));
		}
		return queue;
	}

	function saveToStorage() {
		localStorage.setItem('queueLength', queue.length);
		_.each(queue, function(f, i) {
			localStorage.setItem('queueItem-' + i, f);
		});
	}

	function renderQueue() {
		$list = $('<ul>');
		_.each(queue, function(f) {
			$('<li>', {
				html: $('<img>', {
					src: f
				}),
				click: function() {
					removeFromQueue(f);
				}
			}).appendTo($list);
		});
		$dropzone.find('.status').html($list);
		saveToStorage();
	}

	function removeFromQueue(f) {
		queue = _.filter(queue, function(tested) {
			return tested != f;
		});
		renderQueue();
	}

	function addToQueue(files) {
		_.each(files, function(f) {
		//_.each(e.dataTransfer.files, function(f) {
			/*if (_.indexOf(ALLOWED_TYPES, f.type) === -1) {
				console.error('Sorry, file type not allowed.');
				return;
			}*/

			var fr = new FileReader;
			fr.onloadend = function() {
				//f.dataURL = fr.result;
				queue.push(fr.result);
				renderQueue();
			}
			fr.readAsDataURL(f);
		});

	}

	function hintDropzone(e) {
		var $hint = $dropzone.find('p');
		$dropzone.data('origHint', $hint.html());
		$hint.html('Obrázky prosím upustit zde.');
	}

	function unhintDropzone() {
		$dropzone.find('p').html($dropzone.data('origHint'));
	}

	var $dropzone = $('<div>', { id: 'gallery-upload' });
	//$('<p>', { html: 'Přetáhni to sem nebo tě přetáhnu.' }).appendTo($dropzone);
	$('<input type="file" multiple>').appendTo($dropzone);
	$('<div>', { 'class': 'status' }).appendTo($dropzone);
	$('<a>', {
		href: '#',
		text: 'upload',
		click: uploadQueue
	}).appendTo($dropzone);
	$dropzone.appendTo('#recipe-edit');

	/*$dropzone.bind('dragover', function() { return false; });
	$dropzone.bind('dragenter', hintDropzone);
	$dropzone.bind('dragleave', unhintDropzone);
	$dropzone.bind('dragend', unhintDropzone);

	$dropzone.get(0).addEventListener('drop', addToQueue, false);
	*/

	$('input:file').get(0).addEventListener('change', function(e) {
		addToQueue(e.target.files)
	}, false);

	renderQueue(); //todo: remove;
});
