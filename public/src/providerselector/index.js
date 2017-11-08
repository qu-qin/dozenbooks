"use strict";

beambook.views.ProviderSelectorView = beambook.views.BaseView.extend({

	el: "#providerSelector",

	events: {
		"click .provider": "_activateProvider"
	},

	_$providerList: null,

	_providerUrlTemplate: null,
	_providerSelectorTemplate: null,

	initialize: function() {
		console.log("init provider selector view");
		this._cacheElements();
		this._cacheTemplates();
	},

	render: function() {
		var providerList = this._providerSelectorTemplate({
			providers: beambook.utils.OAuthProviders.PROVIDERS
		});
		this._$providerList.append(providerList);
		this.$el.addClass("active");
	},

	_cacheElements: function() {
		this._$providerList = this.$el.find(".providers");
	},

	_cacheTemplates: function() {
		this._providerUrlTemplate = _.template("/providers/<%- provider %>");
		this._providerSelectorTemplate = _.template(
			this.$el.find("#providerSelectorTemplate").html()
		);
	},

	_activateProvider: function(e) {
		var providerName = $(e.currentTarget).data("name");
		window.location.href = this._providerUrlTemplate({provider: providerName.toLowerCase()});
	}

});