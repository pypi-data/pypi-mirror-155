# malwaretl_stoq_transformer
Transform step in malwarETL pipeline for captured files

This includes a few clustom stoQ plugins:
 1. A custom EMBER-format Lief because I want to make sure the data collected here matches the 
EMBER dataset format. The `to_json` LIEF method does not include some values if they're False, empty lists, etc in 
the final json, and that is a problem for training since those are values that I want to be able to learn on. Also,
some of the values were strangely different (`len(lief_obj.imported_functions) != len(lief_json["imports}]`) so I could
not be convinced that the json dump was clearly comparable to the EMBER dataset data.
 2. A custom version of the regular Lief plugin, because the lief library is looking for input as a list, rather than as a
straight bytestring, so the default Lief plugin didn't work.
 3. A custom dispatcher that looks at the mimetype of a file, and selectively dispatches files to workers depending on the mimetype.


This project is designed to be used in two ways (at the same time):
    1. Collector or Transformer projects import the library, get a stoq instance for their collector, and progressively hand
        files to that instance for scanning as they download them.
    2. Collector or Transformer projects use the Docker image generated here as the base image for their images, so that
        the stoq requirements are pre-installed in their starting image.


The original Stoq plugins that I modified were licensed under the Apache License, and are copyrighted by the 
PUNCH Cyber Analytics Group.