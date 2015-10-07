import os
import re
from os import listdir
from os.path import join, isdir
from core.folders import traversers as Traversers
from core.literature.scribe import Scribe
from core.literature.text import Text

def get_areas_names(path):
    areas = [f for f in listdir(path) if isdir(join(path,f))]
    return areas

def generate_templates_files(path, mode, appname = "app", underscore_js_compile = None, templates_variable = None, comment = None):
    """
        Creates templates.js files for areas found under the given path
    """
    if mode is None:
        mode = "no"
    modeval = re.compile("^ko$|^ng$|^no$", re.I)
    if modeval.search(mode) is None:
        raise Exception("invalid 'templateMode' configuration: it must be KO | NG | NO - case insensitive")
    
    mode = mode.upper()
    
    if mode == "NO" and templates_variable is None:
        templates_variable = "templates"
    
    # declare html traverser
    t = Traversers.HtmlTraverser()
    # find all areas names
    areas = get_areas_names(path)

    for a in areas:
        area_path = os.path.join(path, r"{}".format(a))

        # get all html files under this areaPath
        htmls = t.get_files(area_path)
        if len(htmls) == 0:
            continue

        print("...processing \"{}\" in {}".format(a, area_path))

        if mode == "KO":
            get_templates(area_path, htmls, underscore_js_compile, "ko.templates", comment)
        elif mode == "NO":
            get_templates(area_path, htmls, underscore_js_compile, templates_variable, comment)
        elif mode == "NG":
            get_templates_for_angular(area_path, htmls, appname, underscore_js_compile, comment)
        else:
            print("ERROR: mode not set")

def get_templates_for_angular(path, all_html_files, appname, underscore_js_compile, comment):
    """
        Creates templates.js files for AngularJs
    """
    f = []
    pat = r"<!--template=\"([a-zA-Z0-9\\-]+)\"-->"
    f.append("//")
    f.append("//Knight generated templates file.")
    if comment is not None:
        f.append("// * ")
        f.append("// * " + comment)
        f.append("// * ")
    f.append("//")
    f.append("(function () {")

    f.append("  var o = {")
    k = len(all_html_files)
    i = 0
    for h in all_html_files:
        i += 1
        # get file content
        txt = Scribe.read(h)

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

        f.append("    \'{0}\': \'{1}\'{2}".format(name, txt, "," if i < k else ""))
        
    f.append("  };")

    f.append("  var f = function(a) {")
    if underscore_js_compile is None or underscore_js_compile == "":
        #plain templates
        f.append("    var x;")
        f.append("    for (x in o) {")
        f.append("      a.put(x, o[x]);")
        f.append("    }")
    else:
        #templates run into UnderscoreJs template function
        f.append("    var ctx = {};".format(underscore_js_compile))
        f.append("    _.each(o, function (v, k) {")
        f.append("      a.put(k, _.template(v, ctx));")
        f.append("    });")

    f.append("  };")
    f.append("  f.$inject = ['$templateCache'];")
    f.append("  {0}.run(f);".format(appname))
    f.append("})();")

    code = "\n".join(f)
    # save templates.js
    outputPath = os.path.join(path, "templates.js")
    print("...saving file {}".format(outputPath))
    Scribe.write(code, outputPath)

def get_templates(path, all_html_files, underscore_js_compile, templates_variable, comment):
    """
        Creates templates.js files for KnockOut
    """
    f = []
    pat = r"<!--template=\"([a-zA-Z0-9\\-]+)\"-->"
    f.append("//")
    f.append("//Knight generated templates file.")
    if comment is not None:
        f.append("// * ")
        f.append("// * " + comment)
        f.append("// * ")
    f.append("//")
    f.append("if (!" + templates_variable + ") " + templates_variable + " = {};")
    f.append("(function (templates) {")

    f.append("  var o = {")

    k = len(all_html_files)
    i = 0
    for h in all_html_files:
        i += 1
        # get file content
        txt = Scribe.read(h)

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

        f.append("    '{}\': \'{}\'{}".format(name, txt, "," if i < k else ""))

    f.append("  };")

    if underscore_js_compile is None or underscore_js_compile == "":
        #plain templates
        f.append("  var x;")
        f.append("  for (x in o) {")
        f.append("    templates[x] = o[x];")
        f.append("  }")
    else:
        #templates run into UnderscoreJs template function
        f.append("  var ctx = {};".format(underscore_js_compile))
        f.append("  _.each(o, function (v, k) {")
        f.append("    x[k] = _.template(v, ctx);")
        f.append("  });")

    f.append("})(" + templates_variable + ");")

    code = "\n".join(f)

    # save templates.js
    outputPath = os.path.join(path, "templates.js")
    print("...saving file {}".format(outputPath))
    Scribe.write(code, outputPath)
