$(function() {
	var DEFAULT_FIELDS = ['name', 'ingredients', 'procedure'];

	var $inputs = $('#recipe-edit *:input, #recipe-edit select'),
	    $menu = $('<ul>').appendTo('#recipe-fields-menu');

	$inputs.each(function() {
		var $input = $(this),
		    type = $input.attr('type');

		if (type == 'hidden' || type == 'submit') return;

		var visible = initField($input),
		    $menuItem = addToMenu($input, visible);

		if (_.indexOf(DEFAULT_FIELDS, $input.attr('name')) == -1) {
			addFieldToggle($input, $menuItem);
		}
	});

	$('<li>', {
		'class': 'expand-all',
		html: $('<a>', {
			href: '#',
			html: 'Rozbalit vše',
			click: function() {
				$inputs.closest('tr').fadeIn();
				$(this).closest('ul').find('li').hide();
				return false;
			}
		})
	}).appendTo($menu);

	function initField($input) {
		var name = $input.attr('name'),
		    $row = $input.closest('tr'),
		    $errorList = $row.find('ul.errorlist'),
		    hasValue = $input.val() && !$input.is('select');

		if (_.indexOf(DEFAULT_FIELDS, name) != -1 || hasValue || $errorList.length) {
			$row.show();
			return true;
		} else {
			$row.hide();
			return false;
		}
	}

	function addToMenu($input, visible) {
		var name = $input.closest('tr').find('th').text();
		name = name.substr(0, name.length - 1); // remove colon

		var $item = $('<li>', {
			html: $('<a>', {
				href: '#',
				html: name,
				data: { $input: $input }
			})
		});
		visible ? $item.hide() : $item.show();
		$item.appendTo($menu);

		return $item;
	}

	function addFieldToggle($input, $menuItem) {
		var $toggle = $('<a>', {
			href: '#',
			html: 'Schovat',
			data: { $menuItem: $menuItem },
			'class': 'hide'
		});
		$input.closest('td').append($toggle);
	}

	// hide field
	$('#recipe-edit td a').click(function() {
		$(this).data('$menuItem').fadeIn();
		$menu.find('.expand-all').fadeIn();
		$(this).closest('tr').hide();
		return false;
	});

	// show field
	$menu.find('a').click(function() {
		$(this).data('$input').closest('tr').fadeIn();
		$(this).closest('li').hide();
		return false;
	});

	$('.gallery a').fancybox();
});
