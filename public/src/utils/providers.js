"use strict";

beambook.utils.OAuthProviders = (function() {

	var _PERSIST_KEY = "OAUTH_PROVIDERS";

	var _PROVIDERS = [
		{
			name: "VDisk",
			icon: "icon-weibo"
		}
	];

	var _saveOAuthToken = function(provider, authToken, expiry, refreshToken) {

		var savedProviders = _getEnabledProviders(),
			tokenDetails = {
				authToken: authToken,
				expiry: expiry
			};

		if (!_.isEmpty(refreshToken)) {
			tokenDetails.refreshToken = refreshToken;
		}

		savedProviders[provider.name] = tokenDetails;
		_save(savedProviders);
	};

	var _getEnabledProviders = function() {

		var savedProviders = _getSavedProviders(),
			now = Date.now();

		var enabledProviders = {};

		_PROVIDERS.forEach(function(provider) {
			var savedProvider = savedProviders[provider.name];
			if (savedProvider && (savedProvider.expiry > now || savedProvider.refreshToken)) {
				enabledProviders[provider.name] = savedProvider;
			}
		});

		_save(enabledProviders);
		return enabledProviders;

	};

	var _getSavedProviders = function() {
		var savedProviders = localStorage.getItem(_PERSIST_KEY);
		if (!savedProviders) {
			return {};
		}
		return JSON.parse(savedProviders);
	};

	var _save = function(providers) {
		localStorage.setItem(_PERSIST_KEY, JSON.stringify(providers));
	};

	var _clear = function() {
		localStorage.removeItem(_PERSIST_KEY);
	};

	return {
		PROVIDERS: _PROVIDERS,
		getEnabledProviders: _getEnabledProviders,
		saveOAuthToken: _saveOAuthToken,
		clear: _clear
	};

})();