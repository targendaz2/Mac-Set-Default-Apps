# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
* Created module to mock the macOS file system for local tests

### Changed
* CI tests are run against an actual macOS file system

## [1.3.0] - 2019-12-02
### Changed
* A restart is no longer needed to apply changes
* Updated README to remove instructions to restart after using `set` command

## [1.2.0] - 2019-11-28
### Added
* Ability to set default apps by file extension via the `-e` switch
* Ability to read already set default apps via file extension

### Changed
* Documented `-e` switch in README

## [1.1.3] - 2019-11-26
### Fixed
* The wrong directory was targeted instead of the current user's home

## [1.1.2] - 2019-11-26
### Fixed
* Using the `-feu` switch would ignore valid user homes

## [1.1.1] - 2019-11-26
### Fixed
* Using the `-feu` switch would attempt to fill invalid user homes

## [1.1.0] - 2019-11-26
### Added
* Added a change log
* Ability to modify the default apps of all existing users via the `-feu` switch

### Changed
* Documented `-feu` switch in README
* Improved clarity of README

## [1.0.0] - 2019-11-09
### Added
* Initial release
