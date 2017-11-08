"use strict";

beambook.utils.Spinner = (function() {

	var _$spinner = $("#spinner"),
		_$animation = _$spinner.find(".sk-spinner"),

		_ACTIVATE_CLASS = "active",
		_ANIMATION_CLASS = "sk-spinner-wave active";

	return {

		show: function() {
			_$spinner.addClass(_ACTIVATE_CLASS);
			_$animation.addClass(_ANIMATION_CLASS);
		},

		hide: function() {
			_$spinner.removeClass(_ACTIVATE_CLASS);
			_$animation.removeClass(_ANIMATION_CLASS);
		}

	};

})();