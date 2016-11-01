Compare two build logs, and output the changes in warnings in your own format. Configurable with simple YAML files allowing you to tweak the comparison and be notified about only the things you need to be. Output the introductions, fixes and other details using your choice of templating engine, so that you can see only what you need to. Extend the detail by adding your own easy to write data collection methods.

## Dependencies
[PyYAML](http://pyyaml.org/) is required to parse any configuration files.
By default, [Templite+](http://www.joonis.de/en/code/templite) is used as the templating engine, however you can change this to whatever you like.

All dependencies can be installed using `pip`
```
$ pip install pyyaml
$ pip install templite
```

## Usage
`-b --build_log [required]`: A path to the build log to be compared. This is usually the newest of the logs.  
`-r --ref_log [optional]`: A path to the build log to be compared against. This is usually the oldest of the logs. If this is missing, an empty log will be used in its place.  
`-c --compiler [required]`: The name of a compiler. The available ones can be seen in the help text. This compiler should be the closest match to the one used to compile the logs.  
`-f --config [optional]`: Some paths to configuration files to be loaded. Multiple files should be space separated.  
`-t --template [required]`: A path to the template file to follow.  
`-o --output [optional]`: The output filename. Defaults to stdout.  

Full usage can be shown by running
```
$ python logcompare.py -h
```

## Configuration
YAML configuration files are used to help filter and modify warnings found in logs. These can help reduce false positive introductions and remove third party or incorrect warnings.  

Two filters are currently provided:  

`suppress`: Specifications under suppression will not counted towards the total number. They can accessed separately in the data collection and template stages.  
`override`: Specifications can be overridden to change the message. This can help remove uncertainty in messages such as stacksize. Overridden warnings are still counted as normal warnings, but can also be iterated independently.   Overriding requires one field `new` which will be the new message of matched warnings.  

`suppress` and `override` are top level keys. Under each should be a YAML list of warning specifications.

Warning specifications can contain any of the following fields:  
`fullpath`: The fullpath of the file containing the warning. e.g. `path/to/file.c`  
`filepath`: Just the path. e.g. `path/to/`  
`filename`: Just the filename. e.g. `file.c`  
`linenum`: The line number the warning was reported on.  
`code`: The warning code given. e.g. C1234, -Wall  
`message`: The message given with the warning.  
All fields are optional and can be either text or Python regular expressions. Regular expressions can be denoted by starting and ending the value with `/`.  

Full YAML specification can be found at [pyyaml.org](http://pyyaml.org/).

## Compilers
Some compilers have already been added by myself. New compilers can be added by you either directly in the `compiler.py` file or elsewhere in your code. Compilers must contain the two fields `name` and `warn`, containing the name of the compiler and a compiled regular expression matching warnings respectively. Compilers added by you that aren't in `compiler.py` will not be picked up by argparse, so you will not be able to use them via the command line.

## Collectors
After the parsing of logs and application of configurations, data collection is applied to the BuildLog objects. Predefined methods to collect statistics and counts are already supplied in the `collectors` directory and will be used. You can add your own data collection methods to the directory and they will be picked up and used automatically. Methods will only be picked up if they are in the `collectors` directory and start with `collect_`. Collection methods must take two BuildLog objects, the build and reference log respectively, and must return a dictionary.

## Templating
A powerful and lightweight templating engine, Templite+, is used by default. However, you can change this. The template used by the CLI is initialised in `logcompare/__init__.py`.
