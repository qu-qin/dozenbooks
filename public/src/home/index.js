"use strict";

beambook.views.HomeView = beambook.views.BaseView.extend({

	el: "#home",

	events: {
		"click .icon-search.fab": "_processSearchKeyword",
		"keyup #searchField": "_searchFieldKeyup",
		"click #resetAuth": "_resetAuth",
		"click #nextPage": "_nextPage",
		"click .action": "_send"
	},

	_$spinner: null,
	_$searchContainer: null,
	_$searchField: null,
	_$searchResults: null,
	_$searchResultsPaging: null,
	_$searchError: null,

	_searchResultsTemplate: null,
	_sendingSpinnerTemplate: null,

	_paging: {
		page: 1,
		pageSize: 30
	},

	_userPopupView: null,

	initialize: function() {

		console.log("init home view");

		_.bindAll(this, "_renderResults", "_handleSearchError");

		this._cacheElements();
		this._cacheTemplates();

		_.delay(function() {
			$("#searchField").focus();
		}, 300);

	},

	_cacheElements: function() {
		this._$spinner = this.$el.find("#searchSpinner");
		this._$searchField = this.$el.find("#searchField");
		this._$searchContainer = this.$el.find(".search-container");
		this._$searchResults = this.$el.find("#searchResults");
		this._$searchResultsPaging = this.$el.find("#paging");
		this._$searchError = this.$el.find("#searchError");
	},

	_cacheTemplates: function() {
		this._searchResultsTemplate = _.template(
			this.$el.find("#searchResultsTemplate").html()
		);
		this._sendingSpinnerTemplate = _.template(
			this.$el.find("#sendingSpinner").html()
		);
	},

	_searchFieldKeyup: function(e) {

		if (e.keyCode !== 13) {
			return;
		}

		this._processSearchKeyword();

	},

	_processSearchKeyword: function() {

		if (_.isEmpty(this._$searchField.val().trim())) {
			return;
		}

		this._$searchField.blur();
		this._$searchContainer.addClass("searching");
		this._$searchResults.empty().hide();
		this._$searchError.hide();
		this._$searchResultsPaging.hide();

		this._paging.page = 1;

		this._search();
	},

	_resetAuth: function() {
		console.log("reset auth");
		beambook.utils.OAuthProviders.clear();
		document.location.reload(false);
	},

	_nextPage: function() {
		this._$searchResultsPaging.hide();
		this._paging.page++;
		this._search();
	},

	_search: function() {

		var keyword = this._$searchField.val();

		this._showSpinner();

		setTimeout($.proxy(function() {
			beambook.utils.Searcher.search(keyword, this._paging.page, this._paging.pageSize)
				.done(this._renderResults)
				.fail(this._handleSearchError);
		}, this), 300);

	},

	_renderResults: function(results) {

		this._hideSpinner();

		/*jshint camelcase: false */
		var searchResults = this._parseSearchResults(results.results),
			renewedToken = results.renew_token;

		if (renewedToken) {
			this._renewAuthToken(renewedToken);
		}

		var html = this._searchResultsTemplate({results: searchResults});
		this._$searchResults.append(html).show();

		if (searchResults.length === this._paging.pageSize) {
			this._$searchResultsPaging.show();
		}
		else {
			this._$searchResultsPaging.hide();
		}

		if (!searchResults.length && !this._$searchResults.find(".result").length) {
			this._$searchResults.append("<div class=\"no-results\">No results found.</div>");
		}

	},

	_renewAuthToken: function(renewedToken) {
		var provider = _.find(beambook.utils.OAuthProviders.PROVIDERS, function(authProvider) {
			return renewedToken.provider.toLowerCase() === authProvider.name.toLowerCase();
		});

		/*jshint camelcase: false */
		beambook.utils.OAuthProviders.saveOAuthToken(provider,
			renewedToken.token, renewedToken.expiry, renewedToken.refresh_token);
	},

	_parseSearchResults: function(searchResults) {

		if (!searchResults) {
			return [];
		}

		var results = [],
			self = this;

		searchResults.forEach(function(searchResult) {
			results.push({
				name: searchResult.name,
				size: searchResult.size,
				type: self._getFileExtension(searchResult.name),
				links: JSON.stringify(searchResult.links)
			});
		});

		return results;
	},

	_getFileExtension: function(fileName) {
		return fileName.split(".").pop();
	},

	_handleSearchError: function(error) {

		console.log(error);

		this._hideSpinner();

		// unauthorized, clear the localstorage and reload page
		if (error.status === 401) {
			this._resetAuth();
			return;
		}

		this._$searchError.show();

	},

	_send: function(e) {

		var user = beambook.utils.User.getUser();

		if (!user) {

			this._initUserPopupView();

			var self = this;
			this._userPopupView.open(function() {
				self._send(e);
			});

			return;

		}

		var $action = $(e.currentTarget);

		if ($action.hasClass("sending") || $action.hasClass("sent")) {
			return;
		}

		var fileName = $action.siblings(".name").text(),
			links = $action.siblings(".links").val();

		$action.addClass("sending");
		$action.find(".icon-send").hide();
		$action.append(this._sendingSpinnerTemplate());

		beambook.utils.Sender.send(user, fileName, links)
			.done(function() {
				$action.find(".spinner").remove();
				$action.removeClass("sending").addClass("sent");
			})
			.fail(function() {
				$action.find(".spinner").remove();
				$action.removeClass("sending");
				$action.find(".icon-send").show();
				window.alert("Fail to send file.");
			});

	},

	_initUserPopupView: function() {

		if (!this._userPopupView) {
			this._userPopupView = new beambook.views.UserPopup();
		}

	},

	_showSpinner: function() {
		this._$spinner.find(".sk-spinner").addClass("sk-spinner-wave");
		this._$spinner.addClass("show");
	},

	_hideSpinner: function() {
		this._$spinner.removeClass("show");
		this._$spinner.find(".sk-spinner").removeClass("sk-spinner-wave");
	}

});