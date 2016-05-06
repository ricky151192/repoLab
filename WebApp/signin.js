angular.module('signinApp', [])
    .controller('signinController', ['$http', function ($http) {
        "use strict";
        var signin = this;

        signin.signin = function () {
            // chiamata lato server
            $http.get("oca-api/authentication/", {params: {"username": signin.username, "password": signin.password}})
                .then(function (response) {
                    if (response.data.accessGranted === true) {
                        // OK
                        signin.error = "";
                        signin.haserrorclass = "";
                    } else {
                        // segnala l'errore
                        signin.error = response.data.error;
                        signin.haserrorclass = "has-error";
                    }
                });
        };
    }]);


