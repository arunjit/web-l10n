angular.module('main').
controller('UserCtrl', function($scope) {
  $scope.user = {name: 'admin', password: 'some long password'};
});
