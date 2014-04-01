var pomeloApp = angular.module('pomelo-phone', []);

var pomeloApp = angular.module('pomelo-phone').config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

pomeloApp.controller('AppController', function ($scope, $http) {
    $http.get('http://localhost:8000/users/').success(function(data) {
        $scope.users = data;
    });
});

