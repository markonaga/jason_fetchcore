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
	// Use host ip to generate authentication URL
	url = credentials.hip + "/api/v1/auth/login/";
	
	// Create JSON object from login credentials.
	data = JSON.stringify(credentials);
    
	console.log("Sending POST request");

	$.post(url, data, function () {
		alert("Data: " + data + "\nStatus: " + status);
	});
}




    // on cancel dont do anything


    // on login is clicked, run the connect.js with fields info


    // if checkbox is checked save the fields for next time
