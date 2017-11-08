"use strict";

beambook.views.BaseView = Backbone.View.extend({

	show : function () {

		if (this.render) {
			this.render();
		}

		this.$el.addClass("active");

	},

	hide : function () {
		this.$el.removeClass("active");
	}

});