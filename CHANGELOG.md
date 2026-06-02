# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.5.0] - 2026-06-02

### Added

- MacOS support (targeting Apple Silicon)

### Fixed

- Bugs/inefficiencies in the release pipeline

## [v0.4.2] - 2026-05-30

### Added

- Changelog window
- Automatic changelog parsing in the deployment Github Action
- Open source credits in the About window

## [v0.4.1] - 2026-05-29

### Fixed

- `Stimulus` field in GazePlotter export set to video file name

## [v0.4.0] - 2026-05-29

With v0.4 we're starting to add support for Areas of Interest. For now only rectangles are supported, but most of the code for polygon support is already implemented, I just need to implement the interatctive selector.

### Added

- Rectangular Areas of Interest
- GazePlotter exporter

### Changed

- Time value in exports changed from frame to milisecond

## [v0.3.0] - 2026-05-06

This is the first public release of Tacty.
