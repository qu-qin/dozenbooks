"use strict";

beambook.utils.Sender = (function() {

	var _url = "/api/send";

	var _send = function(email, fileName, links) {

		var options = {
			type: "PUT",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify({
				email: email,
				file: fileName,
				links: JSON.parse(links)
			})
		};

		return $.ajax(_url, options);

	};

	return {
		send: _send
	};

})();