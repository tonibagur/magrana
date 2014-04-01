var pomeloApp = angular.module('pomelo-phone', ['ng.django.forms','ng.django.websocket']);

var pomeloApp = angular.module('pomelo-phone').config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.headers.common['X-CSRFToken'] = '{% csrf_value %}';
});

pomeloApp.constant('urls', {
    fetch_youtube: "http://localhost:8000/fetch-youtube-data.json",
    //fetch_youtube: "http://localhost:8000/get_youtube",
});

pomeloApp.controller('MyFormCtrl', function($scope, $http, $window, djangoForm) {
    console.debug('entro myformctrl');
	$scope.submit = function() {
		if ($scope.gift_data) {
            console.debug('entro gift_data');
			$http.post("http://localhost:8000/gift_form/", $scope.gift_data).success(function(out_data) {
				if (!djangoForm.setErrors($scope.valid_form, out_data.errors)) {
					// on successful postin, redirect onto thank you page
					$window.location.href = "/";
				}
			}).error(function() {
				console.error('An error occured during submission');
			});
		}
		return false;
	};
});


/*pomeloApp.controller('MainCtrl', function($scope,$http,urls) {
    console.debug('before get');
    // merge $scope.my_prefix into object containing the action keyword
    var in_data = {action: 'get_youtube'};
    angular.copy($scope.my_prefix, in_data);
    $http.post(urls.fetch_youtube).success(function(data) {
        console.debug('in get');
        if (data.success) {
            console.debug('data.success');
            $scope.youtubeData = data;
        } else {
            console.debug('data.failure');
        }
    }).error(function(data){console.debug('error ocurred')});
});*/

pomeloApp.controller('MainCtrl', function($scope, $http) {
  // Hidden our previous section's content
  // construct our http request
  $http({
    method: 'GET',
    url: "http://localhost:8000/fetch-youtube-data.json"
  }).success(function(data, status) {
    // Now we have a list of the stories (data.list.story)
    // in the data object that the NPR API 
    // returns in JSON that looks like:
    // data: { "list": {
    //   "title": ...
    //   "story": [
    //     { "id": ...
    //       "title": ...
    $scope.youtubeData = data;
  }).error(function(data, status) {
    console.debug('data.failure');
  });
});


/*<script>				
					//var csrftoken = $.cookie('csrftoken');
					document.getElementById("id_file").onchange = function() {
						$.ajax({
							type: 'POST',
							url: '/save_draft/',
							data: {
								'receiver': $("#receiver").val(),
								'email' : $("#email").val(),
								'price' : $("#price").val(),
								'message' : $("#message").val(),
								'product' : $("#product").val(),
							},
							success: function(data) {
								document.getElementById('loading_image').style.display = 'block';
								document.getElementById("id_youtube_form").submit();
							}
						});
					};
				</script>*/
