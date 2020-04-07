function keyValidation(event) {
	if (!(event.keyCode >= 48 && event.keyCode <= 57) || (event.keyCode >= 96 && event.keyCode <= 105) || event.keyCode == 190 || event.keyCode == 110 || event.keyCode == 46) {
		event.returnValue = false;
	}
}