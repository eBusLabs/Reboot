function lengthCheck(string, minimumLength, maximumLength) {
	if (string.length < minimumLength && string.length > maximumLength) {
		return false;
	} else {
		return true;
	}
}

function passwordMatch(passwordA, passwordB) {
	if (passwordA === passwordB) {
		return true;
	} else {
		return false;
	}
}
