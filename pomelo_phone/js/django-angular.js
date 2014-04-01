/*
 * AngularJS modules to be used together with
 * https://github.com/jrief/django-angular
 *
 * Copyright (c) 2014 Jacob Rief
 * Licensed under the MIT license.
 */

(function(angular, undefined) {
'use strict';

// Correct Angular's form.FormController behavior after rendering bound forms.
var djng_forms = angular.module('ng.django.forms', []);

// This directive overrides some of the internal behavior on forms if used together with AngularJS.
// If not used, the content of bound forms is not displayed, because AngularJS does not know about
// the concept of bound forms.
djng_forms.directive('form', function() {
	return {
		restrict: 'E',
		scope: 'isolate',
		priority: -1,
		link: function(scope, element, attrs) {
			var form = scope[attrs.name];
			var fields = angular.element(element).find('input');
			angular.forEach(fields, function(field) {
				if (form[field.name] !== undefined) {
					// restore the field's content from the rendered content of bound fields
					form[field.name].$setViewValue(field.defaultValue);
				}
			});
			// restore the form's pristine state
			form.$setPristine();
		}
	};
});

// This directive can be added to an input field which shall validate inserted dates, for example:
// <input ng-model="a_date" type="text" validate-date="^(\d{4})-(\d{1,2})-(\d{1,2})$" />
// Now, such an input field is only considered valid, if the date is a valid date and if it matches
// against the given regular expression.
djng_forms.directive('validateDate', function() {
	var validDatePattern = null;

	function validateDate(date) {
		var matched, dateobj;
		if (!date) // empty field are validated by the "required" validator
			return true;
		dateobj = new Date(date);
		matched = validDatePattern ? Boolean(date.match(validDatePattern)) : true;
		return matched && !isNaN(dateobj);
	}

	return {
		require: 'ngModel',
		restrict: 'A',
		link: function(scope, elem, attrs, controller) {
			if (attrs.validateDate) {
				// if a pattern is set, only valid dates with that pattern are accepted
				validDatePattern = new RegExp(attrs.validateDate, 'g');
			}

			// watch for modifications on input fields containing attribute 'validate-date="/pattern/"'
			scope.$watch(attrs.ngModel, function(date) {
				if (controller.$pristine)
					return;
				controller.$setValidity('date', validateDate(date));
			});
		}
	}
});

// If forms are validated using Ajax, the server shall return a dictionary of detected errors to the
// client code. The success-handler of this Ajax call, now can set those error messages on their
// prepared list-items. The simplest way, is to add this code snippet into the controllers function
// which is responsible for submitting form data using Ajax:
//     $http.post("/path/to/url", $scope.data).success(function(data) {
//         djangoForm.setErrors($scope.form, data.errors);
//     });
// djangoForm.setErrors returns false, if no errors have been transferred.
djng_forms.provider('djangoForm', function() {
	var NON_FIELD_ERRORS = '__all__';

	function isNotEmpty(obj) {
		for (var p in obj) { 
			if (obj.hasOwnProperty(p))
				return true;
		}
		return false;
	}

	this.$get = function() {
		return {
			// setErrors takes care of updating prepared placeholder fields for displaying form errors
			// deteced by an AJAX submission. Returns true if errors have been added to the form.
			setErrors: function(form, errors) {
				// remove errors from this form, which may have been rejected by an earlier validation
				form.$message = '';
				if (form.$error.hasOwnProperty('rejected')) {
					var old_keys = [];
					angular.forEach(form.$error.rejected, function(rejected) {
						old_keys.push(rejected.$name);
					});
					angular.forEach(old_keys, function(key) {
						form[key].$message = '';
						form[key].$setValidity('rejected', true);
					});
				}
				// add the new upstream errors
				angular.forEach(errors, function(errors, key) {
					if (errors.length > 0) {
						if (key === NON_FIELD_ERRORS) {
							form.$message = errors[0];
						} else {
							form[key].$message = errors[0];
							form[key].$setValidity('rejected', false);
						}
					}
				});
				// reset into pristine state, since the customer restarts with the form
				form.$setPristine();
				return isNotEmpty(errors);
			}
		};
	};
});


// Add three-way data-binding for AngularJS with Django using websockets.
angular.module('ng.django.websocket', []).provider('djangoWebsocket', function() {
	var _prefix;
	var _console = { log: noop, warn: noop, error: noop };
	var heartbeat_interval = 0;

	function noop() {}

	this.prefix = function(prefix) {
		_prefix = prefix;
		return this;
	};

	// Set the heartbeat interval in milliseconds, which must be bigger than 1000.
	// The default is 0, which means that no heartbeat messages are sent.
	this.setHeartbeat = function(interval) {
		heartbeat_interval = interval >= 1000 ? interval : 0;
		return this;
	};

	this.setLogLevel = function(logLevel) {
		switch (logLevel) {
		case 'debug':
			_console = console;
			break;
		case 'log':
			_console.log = console.log;
		case 'warn':
			_console.warn = console.warn;
		case 'error':
			_console.error = console.error;
		default:
			break;
		}
		return this;
	};

	this.$get = ['$window', '$q', '$timeout', '$interval', function($window, $q, $timeout, $interval) {
		var ws, deferred, timer_promise = null, wait_for = null, scope, channels, collection;
		var heartbeat_msg = '--heartbeat--', heartbeat_promise = null, missed_heartbeats = 0;

		function connect(uri) {
			try {
				_console.log("Connecting to "+uri);
				deferred = $q.defer();
				ws = new WebSocket(uri);
				ws.onopen = on_open;
				ws.onmessage = on_message;
				ws.onerror = on_error;
				ws.onclose = on_close;
				timer_promise = null;
			} catch (err) {
				deferred.reject(new Error(err));
			}
		}

		function on_open(evt) {
			_console.log('Connected');
			wait_for = 500;
			deferred.resolve();
			if (heartbeat_promise === null && heartbeat_interval > 0) {
				missed_heartbeats = 0;
				heartbeat_promise = $interval(send_heartbeat, heartbeat_interval);
			}
		}

		function on_close(evt) {
			_console.log("Connection closed");
			if (!timer_promise && wait_for) {
				timer_promise = $timeout(function() {
					connect(ws.url);
				}, wait_for);
				wait_for = Math.min(wait_for + 500, 5000);
			}
		}

		function on_error(evt) {
			_console.error("Websocket connection is broken!");
			deferred.reject(new Error(evt));
		}

		function on_message(evt) {
			if (evt.data === heartbeat_msg) {
				// reset the counter for missed heartbeats
				missed_heartbeats = 0;
				return;
			}
			try {
				var server_data = JSON.parse(evt.data);
				scope.$apply(function() {
					angular.extend(scope[collection], server_data);
				});
			} catch(e) {
				_console.warn('Data received by server is invalid JSON: ' + evt.data);
			}
		}

		function send_heartbeat() {
			try {
				missed_heartbeats++;
				if (missed_heartbeats > 3)
					throw new Error("Too many missed heartbeats.");
				ws.send(heartbeat_msg);
			} catch(e) {
				$interval.cancel(heartbeat_promise);
				heartbeat_promise = null;
				_console.warn("Closing connection. Reason: " + e.message);
				ws.close();
			}
		}

		function listener(newValue, oldValue) {
			if (newValue !== undefined) {
				ws.send(JSON.stringify(newValue));
			}
		}

		return {
			connect: function(scope_, channels_, collection_) {
				var parts = [], location = $window.location;
				scope = scope_;
				channels = channels_;
				collection = collection_;
				parts.push(location.protocol === 'https' ? 'wss:' : 'ws:');
				parts.push('//');
				parts.push(location.host);
				parts.push(_prefix);
				parts.push(location.pathname);
				parts.push('?');
				parts.push(channels.join('&'));
				connect(parts.join(''));
				scope[collection] = scope[collection] || {};
				deferred.promise.then(function() {
					scope.$watchCollection(collection, listener);
				});
				return deferred.promise;
			}
		};
	}];
});

})(window.angular);
