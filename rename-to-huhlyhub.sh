#!/bin/bash

# HuhlyHub Rename Script
# Run this from the root of the repository on the rename branch.

set -e  # exit on any error

echo "🚀 Starting rename from HuhlyHub to HuhlyHub..."

# ------------------------------------------------------------
# 1. Replace all text variations
# ------------------------------------------------------------
echo "📝 Replacing 'huhlyhub' with 'huhlyhub'..."
find . -type f -not -path "./.git/*" -exec sed -i 's/huhlyhub/huhlyhub/g' {} +

echo "📝 Replacing 'huhlyhub' with 'huhlyhub'..."
find . -type f -not -path "./.git/*" -exec sed -i 's/huhlyhub/huhlyhub/g' {} +

echo "📝 Replacing 'HuhlyHub' with 'HuhlyHub'..."
find . -type f -not -path "./.git/*" -exec sed -i 's/HuhlyHub/HuhlyHub/g' {} +

echo "📝 Replacing 'HUHLYHUB' with 'HUHLYHUB'..."
find . -type f -not -path "./.git/*" -exec sed -i 's/HUHLYHUB/HUHLYHUB/g' {} +

echo "📝 Replacing 'huhlyhub' with 'huhlyhub' (if any)..."
find . -type f -not -path "./.git/*" -exec sed -i 's/huhlyhub/huhlyhub/g' {} +

# ------------------------------------------------------------
# 2. Rename directories containing the old names
# ------------------------------------------------------------
echo "📁 Renaming directories..."

# Find directories named *huhlyhub* and rename to huhlyhub
find . -type d -name "*huhlyhub*" -not -path "./.git/*" | while read dir; do
    newdir=$(echo "$dir" | sed 's/huhlyhub/huhlyhub/g')
    if [ "$dir" != "$newdir" ]; then
        mv "$dir" "$newdir"
        echo "   Renamed directory $dir -> $newdir"
    fi
done

# Find directories named *huhlyhub* and rename to huhlyhub
find . -type d -name "*huhlyhub*" -not -path "./.git/*" | while read dir; do
    newdir=$(echo "$dir" | sed 's/huhlyhub/huhlyhub/g')
    if [ "$dir" != "$newdir" ]; then
        mv "$dir" "$newdir"
        echo "   Renamed directory $dir -> $newdir"
    fi
done

# ------------------------------------------------------------
# 3. Special handling for Python package __init__.py (if any)
# ------------------------------------------------------------
# Some packages might have the old name in their metadata – we already replaced text.

echo "✅ Rename complete!"
echo ""
echo "🔍 Next steps:"
echo "   1. Review changes with 'git diff'"
echo "   2. Commit: git add . && git commit -m \"Rebrand: HuhlyHub → HuhlyHub\""
echo "   3. Push: git push -u origin rename-to-huhlyhub"
echo "   4. Then update your GitHub repo name and external accounts (see checklist)."
