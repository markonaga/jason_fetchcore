// Get the modal
var modal = document.getElementById('login_modal');
var submit_btn = document.getElementById("submit_btn");
var user_obj = {};
var credentials;

// Open the login form
function openModal() {
	modal.style.display = 'block';
	console.log("opening login modal");
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}
// Close the login form
function closeModal() {
	modal.style.display = "none";
}

// Respond to button click
submit_btn.onclick = function() {
	var user = document.getElementById("username").value;
	var pass = document.getElementById("password").value;
	var hid = document.getElementById("HIP").value;
	savelogin(hid,user,pass);
	closeModal();
}

// Save login information for future use
function savelogin(hip, user, pass) {
	user_obj.hip = hip;
	user_obj.username = user;
	user_obj.password = pass;
	localStorage.setItem('user_obj', JSON.stringify(user_obj));

	// Update credentials variable
	retrievelogin();
}

// Retrieve saved login information
function retrievelogin() {
	console.log("Retrieving login information");
	credentials = JSON.parse(localStorage.getItem('user_obj'));
	console.log(credentials);
}

// Retrieve user info when page loads
window.onload = function(event) {
	retrievelogin();
	connect();
}

function connect() {
	// Use host ip to generate authentication URL (prepend with http so not relative URI)
	url = "http://" + credentials.hip + "/api/v1/auth/login/";
	
	// Create JSON object from login credentials.
	data = JSON.stringify(credentials);
    
	console.log("Sending POST request");

	makeCorsRequest('GET', url);
	
}

	
	// Create the XHR object.
function createCORSRequest(method, url) {
	var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
    	// XHR for Chrome/Firefox/Opera/Safari.
    	xhr.open(method, url, true);
  	} else if (typeof XDomainRequest != "undefined") {
    	// XDomainRequest for IE.
    	xhr = new XDomainRequest();
    	xhr.open(method, url);
  	} else {
    	// CORS not supported.
    	xhr = null;
  	}
  	return xhr;
}

// Helper method to parse the title tag from the response.
function getTitle(text) {
	return text.match('<title>(.*)?</title>')[1];
}

// Make the actual CORS request.
function makeCorsRequest(method, url) {
	// This is a sample server that supports CORS.
	// var url = 'http://html5rocks-cors.s3-website-us-east-1.amazonaws.com/index.html';

	var xhr = createCORSRequest(method, url);
	if (!xhr) {
		alert('CORS not supported');
		return;
	}

	// Response handlers.
	xhr.onload = function() {
		var text = xhr.responseText;
		var title = getTitle(text);
		alert('Response from CORS request to ' + url + ': ' + title);
	};

	xhr.onerror = function(error) {
		alert('Woops, there was an error making the request.');
		console.log(error);
	};

	// Add fields to the request
	xhr.setRequestHeader('username', credentials.username);
	xhr.setRequestHeader('password', credentials.password);
	// xhr.setRequestHeader('withCredentials', false);
	// xhr.setRequestHeader("contentType", "application/x-www-form-urlencoded");
	console.log(xhr);
	xhr.send();
}
