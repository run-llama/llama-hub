#!/bin/bash

# rename this to whatever you want
CLI_NAME="lcli_local"

# Define the path for the new command script
# RENAME lcli
COMMAND_SCRIPT="/usr/local/bin/$CLI_NAME"

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Get the full path to base.py dynamically
SCRIPT_DIR=$(pwd)
FULL_PATH_TO_BASE_PY="$SCRIPT_DIR/base.py"

# Create the wrapper script
echo '#!/bin/bash' > "$COMMAND_SCRIPT"
echo "python $FULL_PATH_TO_BASE_PY \"\$@\"" >> "$COMMAND_SCRIPT"

# Make the wrapper script executable
chmod +x "$COMMAND_SCRIPT"

echo "$CLI_NAME command is now available."