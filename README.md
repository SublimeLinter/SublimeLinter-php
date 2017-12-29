SublimeLinter-php
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-php.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-php)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [php -l](http://www.php.net/manual/en/features.commandline.options.php). It will be used with files that have the “PHP”, “HTML”, or “HTML 5” syntax.

## Installation
SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before installing this plugin, you must ensure that `php` is installed on your system. To install `php`, download and run the appropriate installer: [Linux/OS X](http://www.php.net/downloads.php) or [Windows](http://windows.php.net/download/).

In order for `php` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

#### Specific Executable
It is possible to specify the `php` executable that should be used to lint your code, taking precedence over the executable available in your PATH.

##### Example:

```json
{
    "SublimeLinter": {
        "linters": {
            "php": {
                "cmd": "/path/to/php"
            }
        }
    }
}
```


## Settings
- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
