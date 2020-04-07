function validateInput() {
	var username = document.forms['formLogin']['username'].value;
	var password = document.forms['formLogin']['password'].value;
	if (username == "") {
		document.getElementById("noUsername").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noPassword").style.display = "none";
		document.getElementById("inputUsername").style.borderColor = "red";
		document.getElementById("inputPassword").style.borderColor = "transparent";
		return false;
	} else if (password == "") {
		document.getElementById("noPassword").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noUsername").style.display = "none";
		document.getElementById("inputUsername").style.borderColor = "transparent";
		document.getElementById("inputPassword").style.borderColor = "red";
		return false;
	}
}