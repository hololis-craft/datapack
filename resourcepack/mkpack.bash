#!/bin/bash

# Directory structure:
# - mkpack.bash : Creates the resource pack zip files for both Java and Bedrock editions
# - je/ : Root directory for Java Edition resource pack
#   - pack.mcmeta : Metadata file for the resource pack
#   - assets/ : Directory containing all asset files (textures, sounds, etc.)

pushd je
zip -r ../hololis_craft_je.zip .
popd
# java -jar ../PackConverter/bootstrap/build/libs/Thunder.jar nogui --input hololis_craft_je.zip --output hololis_craft_be.mcpack
