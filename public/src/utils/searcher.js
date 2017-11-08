"use strict";

beambook.utils.Searcher = (function() {

	var _urlTemplate = _.template("/api/search?query=<%= query %>&page=<%= page %>&page_size=<%= pageSize %>");

	var _search = function(keyword, page, pageSize) {

		console.log("search for..." + keyword + " page: " + page + " page size: " + pageSize);

		var url = _urlTemplate({query: keyword, page: page, pageSize: pageSize}),
			options = _buildSearchOptions();

		return $.ajax(url, options);

	};

	var _buildSearchOptions = function() {

		var options = {},
			now = Date.now(),
			enabledProviders = beambook.utils.OAuthProviders.getEnabledProviders();

		options.type = "GET";
		options.headers = {};

		for (var providerName in enabledProviders) {

			if (!enabledProviders.hasOwnProperty(providerName)) {
				continue;
			}

			var provider = enabledProviders[providerName];

			options.headers["x-auth-provider"] = providerName;

			if (provider.authToken && provider.expiry > now) {
				options.headers["x-auth-token"] = provider.authToken;
			}

			if (provider.refreshToken) {
				options.headers["x-auth-refresh-token"] = provider.refreshToken;
			}

		}

		return options;
	};

	return {
		search: _search
	};

})();