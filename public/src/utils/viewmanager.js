"use strict";

beambook.utils.ViewManager = (function() {

	var _homeView = null,
		_providerSelectorView = null;

	var _currentView = null;

	var _showView = function(View, viewCache) {

		if (_currentView && _currentView === viewCache) {
			return _currentView;
		}

		if (_currentView) {
			_currentView.hide();
		}

		_currentView = viewCache || new View();
		_currentView.show();

		return _currentView;

	};

	return {

		homeView: function() {
			_homeView = _showView(beambook.views.HomeView, _homeView);
			return _homeView;
		},

		providerSelectorView: function() {
			_providerSelectorView = _showView(beambook.views.ProviderSelectorView, _providerSelectorView);
			return _providerSelectorView;
		}

	};

})();