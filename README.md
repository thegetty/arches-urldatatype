# URL Datatype for Arches.

The URL Link Datatype for Arches, organized into an Arches package for ease of addition. Once installed, it allows a user to record URL links in Arches for a given resource by adding a URL datatype to a suitable location of the Resource's model.

## Installation

Normal Arches package installation procedure applies. Run the following within the Arches python environment at the top of the Arches application root directory:

    python manage.py packages -o load_package -s https://github.com/thegetty/arches-urldatatype/archive/v1.1.zip -y 

Or download the latest release (eg https://github.com/thegetty/arches-urldatatype/archive/v1.1.zip), unpack into a directory on the Arches instance and install the package from there. This may be a more suitable solution for local deployment if it will be developed by the user:

    python manage.py packages -o load_package -s /path/to/url/package -y

Note that to update the application after making changes made to the package files can be done by reloading the package.

## Usage

This datatype and widget package is intended to add a new simple datatype that holds and validates a single hyperlink with an optional text label. This is presented in the report display as a clickable link, allowing Resources held within Arches to directly link to external pages. Any valid http/https URL will be accepted by the datatype.

## License and Copyright Information
 
© J. Paul Getty Trust.  All rights reserved.
