"use strict";

beambook.views.UserPopup = beambook.views.BaseView.extend({

	el: "#userPopup",

	events: {
		"click #confirmUserEmail": "_saveUser"
	},

	_callback: null,

	open: function(callback) {

		this._callback = callback;

		$.magnificPopup.open({
			mainClass: "mfp-move-from-top",
			removalDelay: 500,
			items: {
				src: "#userPopup",
				type: "inline"
			}
		});

	},

	_saveUser: function() {

		var userEmail = this.$el.find(".user-email").val();

		if (_.isEmpty(userEmail)) {
			return;
		}

		beambook.utils.User.saveUser(userEmail);
		$.magnificPopup.close();

		if (this._callback) {
			this._callback();
		}

	}

});