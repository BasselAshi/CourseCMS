function validateInput() {
	var username = document.forms['formRegister']['username'].value;
	var password = document.forms['formRegister']['password'].value;
	var repassword = document.forms['formRegister']['repassword'].value;
	if (username == "") {
		document.getElementById("noUsername").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noPassword").style.display = "none";
		document.getElementById("wrongUsernamePassword").style.display = "none";
		document.getElementById("inputUsername").style.borderColor = "red";
		document.getElementById("inputPassword").style.borderColor = "transparent";
		document.getElementById("inputRePassword").style.borderColor = "transparent";
		return false;
	} else if (password == "") {
		document.getElementById("noPassword").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noUsername").style.display = "none";
		document.getElementById("wrongUsernamePassword").style.display = "none";
		document.getElementById("inputUsername").style.borderColor = "transparent";
		document.getElementById("inputPassword").style.borderColor = "red";
		document.getElementById("inputRePassword").style.borderColor = "transparent";
		return false;
	} else if (password != repassword) {
		document.getElementById("noPassword").style.display = "none";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noUsername").style.display = "none";
		document.getElementById("wrongUsernamePassword").style.display = "block";
		document.getElementById("inputUsername").style.borderColor = "transparent";
		document.getElementById("inputPassword").style.borderColor = "transparent";
		document.getElementById("inputRePassword").style.borderColor = "red";
		return false;
	}
}