# pytest-codecarbon

Pytest plugin for measuring carbon emissions.

# Installation

This plugin is installed via pip using:
```
pip3 install pytest-codecarbon
```

# Usage

To use, simply run pytest with the `--carbon` option. When the tests have run, you will find an `emissions.csv` file containing each test, and the cumulative carbon/time usage after each test. You can also use `--carbon-dir` to specify a different directory for the `emissions.csv` file.


