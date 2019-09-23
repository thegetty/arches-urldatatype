# arches-urldatatype

The URL Link Datatype for Arches, organized into an Arches package for ease of addition.

## Usage

This datatype and widget package is intended to add a new simple datatype that holds and validates a single hyperlink with an optional text label. This is presented in the report display as a clickable link, allowing Resources held within Arches to directly link to external pages.

## Installation

Normal package installation procedure applies, run the following via the commandline:

    python manage.py packages -o load_package -s https://github.com/thegetty/arches-urldatatype/archive/v1.1.zip -y 

Or download the latest release (eg https://github.com/thegetty/arches-urldatatype/archive/v1.1.zip), unpack into a directory on the Arches instance and install the package from there:

    python manage.py packages -o load_package -s /path/to/url/package -y
