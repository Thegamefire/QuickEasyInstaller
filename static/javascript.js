
document.getElementById('clear').addEventListener("click", clearAll)
document.getElementById('select-all').addEventListener("click", selectAll)
document.getElementById('choco-install-btn').addEventListener("click", installChoco)
document.getElementById('choco-no-btn').addEventListener("click", killApp)
document.getElementById('close-app-btn').addEventListener("click", killApp)
document.getElementById('minimize-app-btn').addEventListener("click", minimizeApp)

var loggedInfo = ['<p class="normal-log">Test normal log</p><p class="warning-log">This is a warning log</p><p class="error-log">This is a warning log</p><p class="normal-log">Test normal displaylog</p><p class="warning-log">This is a warning log</p><p class="error-log">This is a warning log</p>']

// SSE Listener //
const eventSource = new EventSource('/sse');
let lastSSEMessage = null

eventSource.onmessage = function(event) {
    const data = event.data;
	if (data!=lastSSEMessage) {
		lastSSEMessage = data
		// Handle the incoming data as needed
		console.log(data);
		if (data.startsWith('Progressbar:')) {
			document.getElementById('progress-bar').value = data.substring(13, data.length - 1)
		} else {// If adding when adding new message has delay between receiving messages split on &&&
			if (data.startsWith("DisplayLog Append: ")) {
				args = data.split(' ')
				addToDisplayLog(args[2], args[3])
			}
		}
	}
};

eventSource.onerror = function(event) {
    console.error('Error occurred:', event);
};


function clearAll(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    checkboxes = document.getElementsByClassName("selection-checkbox")
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
    }
    $.ajax({
	type : "POST",
	url : '/',
	dataType: "json",
	data: JSON.stringify(""),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}
function selectAll(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    checkboxes = document.getElementsByClassName("selection-checkbox")
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = true;
    }
}

function installChoco(event) {
	console.log("Installing Chocolatey...")
    document.getElementById("choco-alert-container").style.opacity = "0"
	setTimeout(function(){
    document.getElementById("choco-alert-container").style.display = "none"
	}, 250);

    $.ajax({
	type : "get",
	url : '/chocoinstall',
	dataType: "json",
	data: JSON.stringify(""),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}

function killApp(event) {
    $.ajax({
	type : "get",
	url : '/shutdown',
	dataType: "json",
	data: JSON.stringify(""),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}

function minimizeApp(event) {
    $.ajax({
	type : "get",
	url : '/minimize',
	dataType: "json",
	data: JSON.stringify(""),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}

function addToDisplayLog(message, type='normal') {
	displayLog = document.getElementById("log-display");
	if (type =='normal') {
		loggedInfo.push('<p class="normal-log">'+message+'</p>')
	} else {
		if (type=='Error') {
			loggedInfo.push('<p class="error-log">'+message+'</p>')
		} else {
			if (type=='Warning') {
				loggedInfo.push('<p class="warning-log">'+message+'</p>')
			}
		}
	}
	displayLogString = ""
	for (const logMessage of loggedInfo) {
		displayLogString = displayLogString+logMessage
	}
	displayLog.innerHTML=displayLogString
    displayLog.scrollTop = displayLog.scrollHeight + 10;
}

addToDisplayLog("This is a normal log")
