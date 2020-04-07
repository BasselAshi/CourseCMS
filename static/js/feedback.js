function validateInput() {
	var q1 = document.forms['formFeedback']['q1'].value;
	var q2 = document.forms['formFeedback']['q2'].value;
	var q3 = document.forms['formFeedback']['q3'].value;
	var q4 = document.forms['formFeedback']['q4'].value;
	if (q1 == "" || q2 == "" || q3 == "" || q4 == "") {
		alert("Please answer all questions!");
		return false;
	}
}