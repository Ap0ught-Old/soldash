function initialise() {
	compareSlaveVersionsWithMaster();
}

function command_click(command, host, element_id) {
	/**
	 * command: solr command to be executed
	 * host: of the form 
	 *   {hostname: 'localhost', port: 8888, auth: {username: 'abc', password: 'def'}}
	 * element_id: id of the element that was clicked to trigger this function
	 */
	changeIcon(element_id, 'working');
	var auth = '';
	if(! $.isEmptyObject(host['auth'])) {
		auth = '&username=' + host['auth']['username'] + '&password=' + host['auth']['password'];
	}
	$.ajax({
	  url: '/execute/' + command,
	  type: 'POST',
	  data: 'host=' + host['hostname'] + '&port=' + host['port'] + auth,
	  success: function(data, status, jqXHR){
		handleResponse(command, data, status, host, element_id);
		}
	});
}

function handleResponse(command, data, status, host, element_id) {
	/**
	 * command: same as in command_click()
	 * data: jsonified response from server
	 * status: whether the call itself could be made to the solr server
	 *   (status being 'ok' doesn't preclude data['status'] from being 'ERROR')
	 * host: same as in command_click()
	 * element_id: same as in command_click() 
	 */
	if(data['data']['status'] == 'ERROR') {
		changeIcon(element_id, 'error');
		setStatusBar(data['data']['message'], 'error', 5);
	} else if(data['data']['status'] == 'OK') {
		changeIcon(element_id, 'success');
		setStatusBar('Success!', 'success', 2);
	}
}

function setStatusBar(text, css, hide_seconds) {
	/**
	 * text: the status bar's html content
	 * css: a css class to add
	 * hide_seconds: hide the statusbar after n seconds
	 * 
	 */
	var bar = $('#statusbar');
	bar.removeAttr('style');
	bar.removeClass('hidden success error');
	bar.addClass(css);
	bar.html(text);
	setTimeout(function() {
	    bar.fadeOut('slow');
	}, hide_seconds * 1000);
}

function changeIcon(element_id, new_icon) {
	/**
	 * element_id: id of the element that was clicked to trigger this function 
	 * new_icon: a css class to be added to change the icon
	 */
	$('#' + element_id).removeClass('ready success error working');
	$('#' + element_id).addClass(new_icon);
}

/**
 * Functions for IndexVersion checking and comparisons. 
 * 
 */
function compareSlaveVersionsWithMaster() {
	var master = getMasterVersion();
	if(!master) {
		return false;
	}
	var slaves = $('.slave');
	for(var i=0; i<slaves.length; i++) {
		var row_id = getRowID(slaves[i]);
		if(getIndexVersion(row_id) !== master) {
			$('#' + row_id).children('.version').addClass('out_of_sync');
		}
	}
}

function getMasterVersion() {
	var masters = $('.master');
	var retval = areAllVersionsEqual(masters);
	if(!retval) {
		alert('Master instances have differing IndexVersions.');
	}
	return retval
}

function areAllVersionsEqual(cells) {
	var master_indexes = [];
	for(var i=0; i<cells.length; i++) {
		var row_id = getRowID(cells[i]);
		master_indexes.push(getIndexVersion(row_id));
	}
	var last_entry; 
	for(var i=0; i<master_indexes.length; i++) {
		if (i==0) {
			last_entry = master_indexes[i];
		} else {
			if(master_indexes[i] !== last_entry) {
				return false;
			}
		}
	}
	return last_entry;
}

function getRowID(element) {
	var cell = $(element);
	return cell.closest('tr')[0].id;
}

function getIndexVersion(row_id) {
	return $('#' + row_id).children('.version').text();
}
function getIndexVersionFromElementID(element_id) {
	return getIndexVersion(getRowID($(element_id)))
}

/**
 * End
 *
 */
