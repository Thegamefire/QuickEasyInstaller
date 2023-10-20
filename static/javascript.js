
document.getElementById('clear').addEventListener("click", clearAll)
document.getElementById('select-all').addEventListener("click", selectAll)
document.getElementById('choco-install-btn').addEventListener("click", installChoco)
document.getElementById('choco-no-btn').addEventListener("click", killApp)
document.getElementById('close-app-btn').addEventListener("click", killApp)
document.getElementById('minimize-app-btn').addEventListener("click", minimizeApp)
document.getElementById('close-credits-btn').addEventListener("click", closeCredits)
document.getElementById('info-link').addEventListener("click", openCredits)
document.getElementById('close-done-alert-btn').addEventListener("click", closeOperationCompleted)
document.getElementById('done-test').addEventListener("click", showOperationCompleted)
document.getElementById('clipboard-btn').addEventListener("click", copySeed)
document.getElementById('seed-btn').addEventListener('click', selectPackage)




var loggedInfo = ['<p class="normal-log">Test normal log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log what a great test this is lorem ipsum nog wat shit ben ik al ver genoeg, ik heb geen idee wij gaan verder wiiiiiiiiiiii</p>', '<p class="normal-log">Test normal displaylog</p>', '<p class="warning-log">This is a warning log</p>', '<p class="error-log">This is an error log</p>']


// SSE Listener //
const eventSource = new EventSource('/sse');
let lastSSEMessage = null
let collected_err = {}

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
			} else {
				if (data == "Completed Operation") {
					showOperationCompleted()
				}
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

function openCredits(event) {
    document.getElementById("credits-alert-container").style.display = "block"
	setTimeout(function(){
    document.getElementById("credits-alert-container").style.opacity = "1"
	}, 250);
}
function closeCredits(event) {
	document.getElementById("credits-alert-container").style.opacity = "0"
	setTimeout(function(){
    document.getElementById("credits-alert-container").style.display = "none"
	}, 250);
}

function showOperationCompleted(event) {
	let operationResult = ""
	for (const warningMessage of loggedInfo) {
		if (!(warningMessage.substring(10, 20) == "normal-log")) {
			operationResult = operationResult + warningMessage.replace('warning-log', 'warning-result').replace('error-log', 'error-result')
		}
	}
	console.log(operationResult)
	document.getElementById('install-result-container').innerHTML = operationResult


    document.getElementById("done-alert-container").style.display = "block"
	setTimeout(function(){
    document.getElementById("done-alert-container").style.opacity = "1"
	}, 250);
}
function closeOperationCompleted(event) {
	document.getElementById("done-alert-container").style.opacity = "0"
	setTimeout(function(){
    document.getElementById("done-alert-container").style.display = "none"
	}, 250);
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
		collected_err.Append(type + " " + message)
	}
	displayLogString = ""
	for (const logMessage of loggedInfo) {
		displayLogString = displayLogString+logMessage
	}
	displayLog.innerHTML=displayLogString
    displayLog.scrollTop = displayLog.scrollHeight + 10;
}

function copySeed() {
	checkboxes = document.getElementsByClassName("selection-checkbox")
	checked_applications = []
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == true) {
			checked_applications.push(checkboxes[i].value)
		}
    }
	console.log(`Checked applications = ${checked_applications}`);

	console.log(JSON.stringify({app_list: checked_applications}))
	$.ajax({
		type : "POST",
		url : '/copy-seed',
		dataType: "json",
		data: JSON.stringify({app_list: checked_applications}),
		contentType: 'application/json;charset=UTF-8',
		success: function (data) {
			console.log(data);
			}
	});
}

function selectPackage() {
	let package_seed = document.getElementById('package-seed-input').value
	let checkboxes = document.getElementsByClassName("selection-checkbox")
	let apps_from_seed = []

	$.ajax({
		type : "post",
		url : '/select-package',
		dataType: "json",
		data: JSON.stringify({seed: package_seed}),
		async: false,
		timeout: 10000,
		contentType: 'application/json;charset=UTF-8',
		success: function (data) {
			console.log(data);
			apps_from_seed = data['app_list']
			}
		});
	console.log(apps_from_seed)

	for (var i = 0; i < checkboxes.length; i++) {
		checkboxes[i].checked = false;
	}
	for (var i = 0; i < apps_from_seed.length; i++) {
		console.log(apps_from_seed[i])
		console.log(i)

        for (var j = 0; j < checkboxes.length; j++) {
			if (checkboxes[j].value == apps_from_seed[i]) {
				checkboxes[j].checked = true;
			}
		}
	}
}

addToDisplayLog("This is a normal log")
