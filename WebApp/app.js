angular.module('appApp', ['ngRoute', 'ngResource'])

    .config(function ($routeProvider) {
        "use strict";
        $routeProvider
            .when('/polizze', {
                templateUrl: 'polizze.html'
            })
            .when('/anagrafica', {
                templateUrl: 'anagrafica.html'
            })
            .when('/vistadati', {
                templateUrl: 'vistadati.html'
            })
            .otherwise({
                redirectTo: '/polizze'
            });
    })

    .controller('DropDownController', function () {
        "use strict";
        var dropdown = this;

        dropdown.configure = function () {
            alert("Configure");
        };

        dropdown.logout = function () {
            alert("Log Out");
        };
    })

    .controller('UserSearchController', function () {
        "use strict";
        var usersearch = this;

        usersearch.search = {"name": "", "gender": "", "age": "", "fiscalcode": "", "address": "", "email": "", "note": ""};

        usersearch.doSearch = function () {
            alert("Search " + JSON.stringify(usersearch.search));
        };
    })

    .controller('PolicyController', function () {
        "use strict";
        var policy = this;

        policy.search = {"note": "", "carnumber": "", "contractor": "", "number": ""};

        policy.doSearch = function () {
            alert("Search " + JSON.stringify(policy.search));
        };
    })

    .controller('RecordController', function () {
        "use strict";
        var record = this, i;

        record.data = [];

        for (i = 0; i < 100; i += 1) {
            record.data[i] = {
                name: "Mario Rossi",
                gender: "M",
                age: String(i),
                fiscalcode: 'MRORSS1234567',
                address: 'Via talleri 14',
                email: 'mario.rossi@gmail.com'
            };
        }

        $('#record-table').bootstrapTable({
            columns: [{
                field: 'name',
                title: 'Nome'
            }, {
                field: 'gender',
                title: 'Sesso'
            }, {
                field: 'age',
                title: 'Età'
            }, {
                field: 'fiscalcode',
                title: 'Codice Fiscale'
            }, {
                field: 'address',
                title: 'Indirizzo'
            }, {
                field: 'email',
                title: 'Email'
            }],
            data: record.data
        });
    })

    .controller('PolicyRecordController', function () {
        "use strict";
        var record = this, i;

        record.data = [];

        for (i = 0; i < 100; i += 1) {
            record.data[i] = {
                number: String("0000000" + i),
                contractor: "Mario Rossi",
                carnumber: "CZ898NF"
            };
        }

        $('#policyrecord-table').bootstrapTable({
            columns: [{
                field: 'number',
                title: 'Numero'
            }, {
                field: 'contractor',
                title: 'Nome'
            }, {
                field: 'carnumber',
                title: 'Targa'
            }],
            data: record.data
        });
    });
