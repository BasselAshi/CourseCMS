function validateInput() {
	var username = document.forms['formLogin']['username'].value;
	var password = document.forms['formLogin']['password'].value;
	// console.log(password);
	if (username == "") {
		document.getElementById("noUsername").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noPassword").style.display = "none";
		return false;
	} else if (password == "") {
		document.getElementById("noPassword").style.display = "block";
		document.getElementById("loginMsg").style.display = "none";
		document.getElementById("noUsername").style.display = "none";
		return false;
	}
}