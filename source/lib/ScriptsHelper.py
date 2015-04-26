import os
import re
from os import listdir
from os.path import join, isdir
from core.folders import traversers as Traversers
from core.literature.scribe import Scribe
from core.literature.text import Text

def getAreasNames(path):
	areas = [ f for f in listdir(path) if isdir(join(path,f)) ]
	return areas

def generateTemplatesFiles(path, mode, appname = "app", underscoreJsCompile = None, log = True):
	"""
		Creates templates.js files for areas found under the given path
	"""
	modeval = re.compile("^ko$|^ng$", re.I)
	if modeval.search(mode) is None:
		raise Exception("invalid 'templateMode' configuration: it must be KO | NG - case insensitive")

	# declare html traverser
	t = Traversers.HtmlTraverser()
	# find all areas names
	areas = getAreasNames(path)

	for a in areas:
		areaPath = os.path.join(path, r"{}".format(a))

		# get all html files under this areaPath
		allHtml = t.getFiles(areaPath)
		if len(allHtml) == 0:
			continue

		if log:
			print("...processing \"{}\" in {}".format(a, areaPath))

		if mode.upper() == "KO":
			getTemplatesForKnockOut(areaPath, allHtml, underscoreJsCompile)
		elif mode.upper() == "NG":
			getTemplatesForAngular(areaPath, allHtml, appname, underscoreJsCompile)
		else:
			print("ERROR: mode not set")

def getTemplatesForAngular(path, allHtmlFiles, appname, underscoreJsCompile):
	"""
		Creates templates.js files for AngularJs
	"""
	f = []
	pat = r"<!--template=\"([a-zA-Z0-9\\-]+)\"-->"
	f.append("//")
	f.append("//Knight generated templates file")
	f.append("//")
	f.append("\"use strict\";")
	f.append("(function () {")

	f.append("\tvar o = {")
	k = len(allHtmlFiles)
	i = 0
	for h in allHtmlFiles:
		i += 1
		# get file content
		txt = Scribe.readTextFile(h)

		# check if the rx matches the contents
		m = re.search(pat, txt)
		if m:
			# get the template name from the group
			name = m.group(1)
			# remove the template name comment
			txt = re.sub(pat, "", txt)
		else:
			# get the filename with extension
			name = os.path.basename(h)
			# remove extension
			name = os.path.splitext(name)[0]

		# escape single quotes
		txt = re.sub("'", "\\'", txt)
		# condensate
		txt = Text.condensate(txt)

		f.append("\t\t\'{0}\': \'{1}\'{2}".format(name, txt, "," if i < k else ""))
		
	f.append("\t};")

	f.append("\tvar f = function(a) {")
	if underscoreJsCompile is None or underscoreJsCompile == "":
		#plain templates
		f.append("\t\tvar x;")
		f.append("\t\tfor (x in o) {")
		f.append("\t\t\ta.put(x, o[x]);")
		f.append("\t\t}")
	else:
		#templates run into UnderscoreJs template function
		f.append("\t\tvar ctx = {};".format(underscoreJsCompile))
		f.append("\t\t_.each(o, function (v, k) {")
		f.append("\t\t\ta.put(k, _.template(v, ctx));")
		f.append("\t\t});")

	f.append("\t};")
	f.append("\tf.$inject = ['$templateCache'];")
	f.append("\t{0}.run(f);".format(appname))
	f.append("})();")

	code = "\n".join(f)
	# save templates.js
	outputPath = os.path.join(path, "templates.js")
	print("...saving file {}".format(outputPath))
	Scribe.saveTextFile(code, outputPath)

def getTemplatesForKnockOut(path, allHtmlFiles, underscoreJsCompile):
	"""
		Creates templates.js files for KnockOut
	"""
	f = []
	pat = r"<!--template=\"([a-zA-Z0-9\\-]+)\"-->"
	f.append("//")
	f.append("//Knight generated templates file")
	f.append("//")
	f.append("\"use strict\";")
	f.append("if (!ko.templates) ko.templates = {};")
	f.append("(function (templates) {")

	f.append("\tvar o = {")

	k = len(allHtmlFiles)
	i = 0
	for h in allHtmlFiles:
		i += 1
		# get file content
		txt = Scribe.readTextFile(h)

		# check if the rx matches the contents
		m = re.search(pat, txt)
		if m:
			# get the template name from the group
			name = m.group(1)
			# remove the template name comment
			txt = re.sub(pat, "", txt)
		else:
			# get the filename with extension
			name = os.path.basename(h)
			# remove extension
			name = os.path.splitext(name)[0]

		# escape single quotes
		txt = re.sub("'", "\\'", txt)

		# condensate
		txt = Text.condensate(txt)

		#f.append("\tx[\'{}\'] = \'{}\';".format(name, txt))
		f.append("\t\t'{}\': \'{}\'{}".format(name, txt, "," if i < k else ""))

	f.append("\t};")

	if underscoreJsCompile is None or underscoreJsCompile == "":
		#plain templates
		f.append("\tvar x;")
		f.append("\tfor (x in o) {")
		f.append("\t\ttemplates[x] = o[x];")
		f.append("\t}")
	else:
		#templates run into UnderscoreJs template function
		f.append("\tvar ctx = {};".format(underscoreJsCompile))
		f.append("\t_.each(o, function (v, k) {")
		f.append("\t\tx[k] = _.template(v, ctx);")
		f.append("\t});")

	f.append("})(ko.templates);")

	code = "\n".join(f)

	# save templates.js
	outputPath = os.path.join(path, "templates.js")
	print("...saving file {}".format(outputPath))
	Scribe.saveTextFile(code, outputPath)
