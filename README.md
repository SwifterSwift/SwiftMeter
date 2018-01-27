# SwiftMeter

[WIP] Script to create statistical reports about Swift codebases

### Installation

- This script is written in Python 3. If you don't have Python installed, navigate to Python's [website](https://www.python.org/) to download and install the software.
- Clone the repository or download the [*meter.py*](https://github.com/SwifterSwift/SwiftMeter/blob/master/meter.py) file.
- Open a new terminal tab/window and move to the directory where meter.py was downloaded.
- follow the instructions below to analyze your swift code base.

### Usage

#### Analytics for a single swift file

```bash
python meter.py -f path_to_swift_file
```

#### Get analytics for all swift files in a directory

```bash
python meter.py -d path_to_sources_directory
```

This will iterate over all swift files in the given directory and its subdirectories recursively

#### Create [shields.io](https://shields.io/) badges for the README

Add the `-b` flag to the end to create [shields.io](https://shields.io/) badges.

```bash
python meter.py -d path_to_sources_directory -b
```

#### Verbose logging

Add the `-v` flag to the end to create log verbose messages while processing swift files.

```bash
python meter.py -d path_to_sources_directory -v
```

#### Help

To learn more about usage use the `-h` flag

```bash
python meter.py -h
```

### Example output

```bash
Swift codebase statistics:
{
    "swift_files": 56,
    "total_lines": 8941,
    "code_lines": 4207,
    "enums": 6,
    "classes": 0,
    "structs": 5,
    "extensions": 101,
    "functions": 229,
    "static_functions": 40,
    "variables": 220,
    "static_variables": 502,
    "ib_inspectables": 28,
    "initializers": 10,
    "failable_initializers": 9,
    "operators": 11,
    "total_non_static_units": 468,
    "total_static_units": 542,
    "total_units": 1010
}
```

### Found an Issue?

If you find a bug or a mistake in the source code, you can help us by submitting an [issue](https://github.com/SwifterSwift/SwiftMeter/issues/new). Even better you can submit a Pull Request with a fix!

### License

SwiftMeter is released under the [MIT License](https://github.com/SwifterSwift/SwiftMeter/blob/master/LICENSE).
