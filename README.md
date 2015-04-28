# Knight
**Angular** and **Knockout** templates packer. Tool to pack .html files into .js for **Angular** or **Knockout**.

**Features**:
- Console application with documented interface (includes *--help*)
- Cross platform: being in Python, it can run on Linux, Windows and Mac
- Executables ready to use, provided for Windows users who don't want to or cannot install Python
- Allows to run UnderscoreJs *template* compilation over templates (useful, for example, to implement localization)
- Examples in both Angular and Knockout, of view composition with cached templates
- Provides a way to manage in-memory templates in Knockout **(instead of using script tags with type="text/html")**

**Repository structure**:
- The **source** folder contains the Python source code.
- This code can be executed by both Python 2.x and Python 3.x.
- The **source** folder also contains a setup.py file used with <a href="http://cx-freeze.readthedocs.org/">cx_Freeze</a> to generate the executables.
- The **built** folder contains executables versions of the application: Windows users who don't want to (or cannot) install Python, can use the .exe file provided there.
- The **docs** folder contains information used for this documentation, and files for examples in Angular and Knockout.

**Examples**:
- Simply download the code and open the index.html in a browser (examples don't require a local web server)
- Some of the external libraries are loaded using CDN

Commands
--------------
- -h --help displays the help for the console application
![Help](https://github.com/RobertoPrevato/Knight/blob/master/docs/images/console-app-help.png)
- -p / --path *path* -m / --mode *mode {ko,ng}* starting from the given folder path, looks recursively inside each direct child folder for .html files, and generates for each directory a **templates.js** file containing the packed HTML files.
![Templates Generation](https://github.com/RobertoPrevato/Knight/blob/master/docs/images/console-app-templates.png)

Optional parameters
--------------
- -a --appname *application name* when generating templates.js files for Angular, the name of a global variable referencing the application object (default == "app").
- -u --underscoreJsCompile *js global variable name* allows to run UnderscoreJs compilation on templates, using the given global variable/function. The parameter determines the context passed as argument for **_.template** function (default == null).