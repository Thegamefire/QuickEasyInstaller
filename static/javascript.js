
document.getElementById('clear').addEventListener("click", clearAll)
document.getElementById('select-all').addEventListener("click", selectAll)
document.getElementById('choco-install-btn').addEventListener("click", installChoco)
document.getElementById('choco-no-btn').addEventListener("click", killApp)
document.getElementById('close-app-btn').addEventListener("click", killApp)
document.getElementById('minimize-app-btn').addEventListener("click", minimizeApp)

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
		} // If adding when adding new message has delay between receiving messages split on &&&&
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



