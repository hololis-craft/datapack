#!/bin/bash

# Directory structure:
# - mkpack.bash : Creates the resource pack zip files for both Java and Bedrock editions
# - je/ : Root directory for Java Edition resource pack
#   - pack.mcmeta : Metadata file for the resource pack
#   - assets/ : Directory containing all asset files (textures, sounds, etc.)
# - be/ : Root directory for Bedrock Edition resource pack
#   - manifest.json : Metadata file for the resource pack

pushd je
zip -r ../hololis_craft_je.zip .
popd
pushd be
zip -r ../hololis_craft_be.mcpack .
popd
