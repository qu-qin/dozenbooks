"use strict";

beambook.utils.User = (function() {

	var _PERSIST_KEY = "KINDLE_USER";

	var _saveUser = function(user) {
		localStorage.setItem(_PERSIST_KEY, user);
	};

	var _getUser = function() {
		return localStorage.getItem(_PERSIST_KEY);
	};

	return {
		saveUser: _saveUser,
		getUser: _getUser
	};

})();