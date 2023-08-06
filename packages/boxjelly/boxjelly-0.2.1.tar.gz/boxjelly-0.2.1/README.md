![BoxJelly logo](boxjelly/assets/images/boxjelly_logo_128.png)

# BoxJelly

**BoxJelly** is a tool for viewing and editing object tracks in video.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/downloads/)

Author: Kevin Barnard, [kbarnard@mbari.org](mailto:kbarnard@mbari.org)

---

## Cthulhu configuration **(required)**

Recently, BoxJelly ditched its internal video player in favor of [Cthulhu](https://github.com/mbari-media-management/cthulhu). This integration is still in development and has some limitations.

As a result, you must configure Cthulhu and BoxJelly before they can be used together. The following configuration is required:

1. **Set the BoxJelly framerate**. Cthulhu does not report video framerate, so a default of 29.97 is assumed. This is configurable in the BoxJelly settings (Ctrl+,).
2. **Set the Cthulhu global duration**. Set the appropriate duration for localizations in the Cthulhu "Annotations" settings. Normally, this is `1000/fps`. If you notice flickering, you may need to increase this value. If you notice overlapping boxes within the same track, you may need to decrease this value.

## Install

### From PyPI

BoxJelly is available on PyPI as `boxjelly`. To install, run:

```bash
pip install boxjelly
```

### From source

This project is build with Poetry. To install from source, run (in the project root):

```bash
poetry install
```

## Run

Once BoxJelly is installed, you can run it from the command line:

```bash
boxjelly
```

**You must have Cthulhu installed and running before you can use BoxJelly.**

Detailed usage is documented in [USAGE](docs/USAGE.md).

---

Copyright &copy; 2021&ndash;2022 [Monterey Bay Aquarium Research Institute](https://www.mbari.org)
