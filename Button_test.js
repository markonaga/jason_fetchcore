var id = document.getElementById("test");



function spawnButton() {
	var button = document.createElement("button");
	console.log("poop");
	// button.innterHTML = "Do Something"; 
	button.style.marginTop = "50px";
	button.style.marginRight = "50px";
	button.style.width = "500px";
	document.body.appendChild(button);

}