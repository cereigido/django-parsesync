# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [1.1.1] - 2015-08-03

### Fixed
- Management commands were not being included.

## [1.1.0] - 2015-08-03

### Added
- Support for saving and retrieving files from Parse.
- Backwards compatibility for parsetodjango command arguments that used to work only in Django 1.8+.

### Fixed
- Parsing of DateField in some cases was generating invalid iso format to be posted to Parse.

## [1.0.0] - 2015-07-30
- Initial Version
