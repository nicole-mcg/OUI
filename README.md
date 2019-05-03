###### Note: This repository contains scripts to download, install and build OUI. If you're here to check out the code online go here: [Engine](https://github.com/nik-m2/OUI-engine) or [Runtime](https://github.com/nik-m2/OUI-runtime)

# OUI

<p align="center">
    OUI is a cross-platform UI engine written from the ground up in C++. It allows you to easily build programs with rich UIs that can be built for <a href="#supported-platforms">many operating systems</a>. The functionality for your program can be written in C++ or JavaScript (coming soon).
    <br><br>
    Simple Demo App
    <br>
    <img src="https://user-images.githubusercontent.com/20328954/55766682-bb1c1800-5a43-11e9-9a90-2d085f60d916.gif"/>
<p align="center">
    
## Features

### Current

- Written from the ground up in C++, the only dependency is SDL2
- Has custom parsers for languages based on XML & CSS
- Supports style sheets, style inheritence and state-based styles (e.g `.classname:hover { ... } `)
- Prewritten optimized components (buttons, text fields, menus, scroll panels)
- Event system for components
- Has been built and run on Windows, Mac, and Linux so far (with few modifications needed for full functionality)
- C++ interface

### Planned

- Implementation of flexbox spec https://www.w3.org/TR/css-flexbox-1/
- JavaScript interface
- Mobile support

## Supported Platforms

- [x] Windows
- [ ] MacOS/OSX (Supported, but no build scripts provided in this repo)
- [ ] Linux (In development)
- [ ] Android (Coming soon)
- [ ] iOS (Coming soon)
- [ ] Web Browsers

## Contributing

### Building

`python scripts/win_setup.py` to download dependencies (SDL2, GTest, OUI-engine, OUI-runtime)

`python scripts/win_build.py` to build to `./bin` folder (This will run setup if it has not been done)

### Running tests

`python scripts/win_test.py [project|test_suite] [test_suite]` To run tests

This will run `win_build.py` and `win_setup` (if needed)

 - `project`: can be either `engine` or `runtime` (optional)

 - `test_suite`: is a case sensitive test suite (optional)

Examples:

`python scripts/win_test.py engine ParserState`

`python scripts/win_test.py ParserState`
