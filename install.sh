#!/bin/bash
set -e

ADDIN_NAME="CliffDrop"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$SCRIPT_DIR/$ADDIN_NAME"

# --- Locate Fusion AddIns directory ---
DEST=""
if [ -d "$HOME/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns" ]; then
    DEST="$HOME/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/$ADDIN_NAME"
elif [ -d "$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns" ]; then
    DEST="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/$ADDIN_NAME"
fi

if [ -z "$DEST" ]; then
    echo ""
    echo "  ERROR: Could not find the Fusion AddIns directory."
    echo "  Looked in:"
    echo "    ~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns"
    echo "    ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"
    echo ""
    echo "  Make sure Autodesk Fusion is installed before running this script."
    exit 1
fi

echo ""
echo "  CliffDrop Installer"
echo "  ===================="
echo "  Source : $SRC"
echo "  Target : $DEST"
echo ""

# --- Remove previous install ---
if [ -d "$DEST" ]; then
    echo "  Removing previous installation..."
    rm -rf "$DEST"
fi

# --- Copy add-in files ---
echo "  Copying files..."
cp -R "$SRC" "$DEST"

echo ""
echo "  Installation complete!"
echo ""
echo "  Next steps:"
echo "    1. Open (or restart) Autodesk Fusion"
echo "    2. Go to UTILITIES tab > ADD-INS"
echo "    3. Find \"CliffDrop\" in the Add-Ins list and click Run"
echo "    4. The \"Cycloidal Curve\" command appears in SOLID > CREATE"
echo ""
