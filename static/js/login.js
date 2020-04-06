function validateInput() {
	let username = document.forms['formLogin']['username'].value;
	if (username == "") {
		document.forms["formLogin"]["loginMsg"].value = "hi";
		return false;
	}
}