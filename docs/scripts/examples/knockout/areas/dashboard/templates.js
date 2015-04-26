//
//Knight generated templates file
//
"use strict";
if (!ko.templates) ko.templates = {};
(function (templates) {
	var o = {
		'dashboard-part': '<h3 data-bind="text: title"></h3> <p data-bind="text: content"></p>',
		'dashboard': '<h2>Dashboard</h2> <!-- part one --> <div data-bind="template: { name: \'dashboard-part\', data: partOne }"></div> <!-- part two --> <div data-bind="template: { name: \'dashboard-part\', data: partTwo }"></div>'
	};
	var x;
	for (x in o) {
		templates[x] = o[x];
	}
})(ko.templates);