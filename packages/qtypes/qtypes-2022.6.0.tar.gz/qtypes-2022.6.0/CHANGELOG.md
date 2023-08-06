# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2022.6.0]

### Changed
- major refactor with several syntax changes
- better performance for TreeWidget
- more dynamic support

## [2022.4.0]

### Added
- new method "clear" to TreeWidget, TreeItems

## [2022.3.1]

### Added
- insert method to TreeWidget and Base to insert at positions other than the end

### Fixed
- Use posix style path in qss when dynamically replaced with the relative path

## [2022.3.0]

### Changed
- one of each example has a bool added to togle a timer to update the values periodically

### Fixed
- floats no longer try to set the decimals while editing

## [2022.2.0]

### Fixed
- ints and strings avoid updating value when set while user has focus
- floats adjusted to update limits and tooltip even when focused

## [2022.1.1]

### Changed
- Reset default allowed values for enum if allowed values list is empty

## [2022.1.0]

### Changed
- switched to calver

## [0.3.2]

### Changed
- quieter warnings

### Fixed
- enum type now defaults to first allowed if current value not in new allowed list
- float widget avoids updating when set while user has focus
- fixed problem with column width by using integer division

## [0.3.1]

### Changed
- removed suprious dependency toml
- removed suprious dependency yaq_traits

## [0.3.0]

### Changed
- complete overhaul based on tree

### Added
- edited signal

### Fixed
- strings disabled properly at startup

## [0.2.0]

### Added
- filepath support

### Changed
- moved to get/set instead of read/write
- migrate to flit

### Fixed
- spacing issues with scroll area

## [0.1.0]

### Added
- initial release

[Unreleased]: https://github.com/yaq-project/qtypes/compare/v2022.6.0...main
[2022.6.0]: https://github.com/yaq-project/qtypes/compare/v2022.4.0...v2022.6.0
[2022.4.0]: https://github.com/yaq-project/qtypes/compare/v2022.3.1...v2022.4.0
[2022.3.1]: https://gitlab.com/yaq-project/qtypes/compare/v2022.3.0...v2022.3.1
[2022.3.0]: https://github.com/yaq-project/qtypes/compare/v2022.2.0...v2022.3.0
[2022.2.0]: https://github.com/yaq-project/qtypes/compare/v2022.1.1...v2022.2.0
[2022.1.1]: https://github.com/yaq-project/qtypes/compare/v2022.1.0...v2022.1.1
[2022.1.0]: https://github.com/yaq-project/qtypes/compare/v0.3.2...v2022.1.0
[0.3.2]: https://github.com/yaq-project/qtypes/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/yaq-project/qtypes/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/yaq-project/qtypes/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yaq-project/qtypes/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yaq-project/qtypes/tags/v0.1.0
