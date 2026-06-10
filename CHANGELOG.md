# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.6.0] - 2026-06-10

The main goal of the `v0.6.x` lineup will be improving the accuracy of the tracking pipeline.

### Changed

- *(BREAKING)* Massively speed up hash checking, but invalidates all previous hashes
- Raised the minimum treshold for identifying stickers

### Fixed

- Bug where a single sticker would sometimes fail to be detected
- Color extraction accuracy improvements
- Icon fix for Windows

## [v0.5.1] - 2026-06-03

### Changed

- The default folder was changed to the user's Documents folder

### Fixed

- Bug where the default theme upon installing is `Breeze Dark`, but in the menu `Native` is selected
- Installer on MacOS
- Application name on MacOS
- External link in the GazePlotter section not clickable on MacOS 

## [v0.5.0] - 2026-06-02

With `v0.5.x` we're working on MacOS support.

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

With `v0.4.x` we're starting to add support for Areas of Interest. For now only rectangles are supported, but most of the code for polygon support is already implemented, I just need to implement the interatctive selector.

### Added

- Rectangular Areas of Interest
- GazePlotter exporter

### Changed

- Time value in exports changed from frame to milisecond

## [v0.3.0] - 2026-05-06

This is the first public release of Tacty.
