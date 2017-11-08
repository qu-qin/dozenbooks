"use strict";

beambook.Router = Backbone.Router.extend({

	routes: {
		"search/:query": "_search",
		"providerselector": "_providerselector",
		"*other": "_home"
	},

	before: function(route) {

		if (route === "providerselector") {
			return true;
		}

		console.log("[Router] check provider...");

		var enabledProviders = beambook.utils.OAuthProviders.getEnabledProviders();

		if (_.isEmpty(enabledProviders)) {
			console.log("[Router] no provider enabled");
			this.navigate("/providerselector", {trigger: true});
			return false;
		}

	},

	_home: function() {
		beambook.utils.ViewManager.homeView();
	},

	_search: function(query) {
		var searchView = beambook.utils.ViewManager.searchView();
		searchView.search(query);
	},

	_providerselector: function() {
		beambook.utils.ViewManager.providerSelectorView();
	}

});