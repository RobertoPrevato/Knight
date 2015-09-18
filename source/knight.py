"""
 * Knight 1.0.0
 * https://github.com/RobertoPrevato/Knight
 *
 * Copyright 2015, Roberto Prevato
 * http://ugrose.com
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
"""
import argparse

separator = "******************************************************\n"

parser = argparse.ArgumentParser(description= 'Packs .html templates into .js files, for Angular or Knockout.',
                                 epilog = "{}\n{}".format("author: Roberto Prevato roberto.prevato@gmail.com", separator))

parser.add_argument('-p', '--path', dest= 'path',
                    required=True, help='path to root folder from where to start the research of .html files')

parser.add_argument('-m', '--mode', dest='mode',
                    required=True, choices=['ko', 'ng'], help='ng to generate Angular templates; ko to generate Knockout templates')

parser.add_argument('-a', '--appname', dest='appname',
                    default="app", help='when generating templates for Angular, the name of the application')

parser.add_argument('-u', '--underscoreJsCompile',
                    dest='underscore_js_compile', default="", help='allows to run UnderscoreJs compilation on templates using the given global variable/function')

args = parser.parse_args()

from lib import ScriptsHelper

def main(options):
    ScriptsHelper.generate_templates_files(options.path, options.mode, options.appname, options.underscore_js_compile)

main(args)
