# Knight
Angular and Knockout templates packer. Packs .html files into .js for **Angular** or **Knockout**.

**Features**:
- Provides a way to pack .html templates into .js files
- Cross platform: being in Python, it can run on Linux, Windows and Mac
- Executables ready to use, provided for those users who don't want to or cannot install Python
- Allows to run UnderscoreJs *template* compilation over templates (useful for example to implement localization)
- Examples in both Angular and Knockout, of view composition with cached templates
- Provides a way to manage in-memory templates in Knockout **(instead of using script tags with type="text/html")**

**Repository structure**:
- The **source** folder contains the tool source code, which is in Python.
- This code can be executed by both Python 2.x and Python 3.x.
- The **source** folder also contains a setup.py file used with <a href="http://cx-freeze.readthedocs.org/">cx_Freeze</a> to generate the executables.
- The **built** folder contains executables versions of the application: Windows users who don't want to (or cannot) install Python, can use the .exe file provided there.
- The **docs** folder contains information used for this documentation, and files for examples in Angular and Knockout.

**Examples**:
- Simply download the code and open the index.html in a browser (examples don't require a local web server)
- Some of the external libraries are loaded using CDN