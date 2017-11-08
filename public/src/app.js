"use strict";

window.beambook = (function() {

	return {

		views: {},
		utils: {},
		route: null,

		initialize: function() {
			this.route = new beambook.Router();
			Backbone.history.start();
		}
	};

})();