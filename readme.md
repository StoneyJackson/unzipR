# unzipR

A libarary for recursively extracting files.

## License

GPLv3

## Features

* Supports multiple compression formats:
    * bzip2
    * zip
    * tar
    * gzip
    * rar (see _Optional_ below)
    * 7z (see _Optional_ below)
* Provides recursive deletion of zip files.

## Requires

* Python 3

## Optional

* For rar support, install `unrar` and `rarfile.py`. For example, on OSX:

        brew install unrar
        pip3 install rarfile

* For 7zip support, install `7z`. For example, on OSX:

        brew install p7zip

## Use

See unzipr.py.
