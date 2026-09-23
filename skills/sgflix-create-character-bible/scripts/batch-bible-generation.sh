#!/bin/bash
# Batch Bible Generation Script
# Generates all 8 pages of a character bible using Codex with reference image
# Usage: ./batch-bible-generation.sh <character_name> <reference_image> <output_dir>

set -e

CHARACTER_NAME="$1"
REF_IMAGE="$2"
OUTPUT_DIR="$3"
TMP_DIR="/tmp"

if [ -z "$CHARACTER_NAME" ] || [ -z "$REF_IMAGE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <character_name> <reference_image> <output_dir>"
    echo "Example: $0 mario /path/to/ref.png /Users/speed/bibles/mario_vs_sweettooth/mario/images"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Page names
PAGES=(
    "page_01_primary_hero_reference"
    "page_02_orthographic_turnaround"
    "page_03_morphology_proportions_silhouette"
    "page_04_expression_emotion_sheet"
    "page_05_cranial_appendage_details"
    "page_06_surface_treatment_construction"
    "page_07_extremities_props_accessories"
    "page_08_materials_color_rigging_motion"
)

echo "=== Generating $CHARACTER_NAME Character Bible ==="
echo "Reference Image: $REF_IMAGE"
echo "Output Directory: $OUTPUT_DIR"
echo ""

# Generate page 1 without reference
echo "$(date '+%H:%M:%S') - Generating Page 01: Primary Hero Reference..."
before_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)

PROMPT=$(cat "$TMP_DIR/${CHARACTER_NAME}_page1.txt")
codex exec --skip-git-repo-check -m gpt-image-2 -- "$PROMPT"

sleep 2
after_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)

if [ "$after_count" -gt "$before_count" ]; then
    latest=$(find ~/.codex/generated_images -name "*.png" -print0 | xargs -0 ls -t | head -1)
    cp "$latest" "$OUTPUT_DIR/${PAGES[0]}.png"
    echo "$(date '+%H:%M:%S') - ✓ Saved Page 01 ($(ls -lh "$OUTPUT_DIR/${PAGES[0]}.png" | awk '{print $5}'))"
else
    echo "$(date '+%H:%M:%S') - ✗ Failed to generate Page 01"
fi
echo ""

# Generate pages 2-8 with page 1 as reference
for i in {1..7}; do
    page_num=$(printf "%02d" $((i + 1)))
    page_name="${PAGES[$i]}"
    
    echo "$(date '+%H:%M:%S') - Generating Page $page_num: ${page_name#page_${page_num}_}..."
    before_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
    
    PROMPT=$(cat "$TMP_DIR/${CHARACTER_NAME}_page${page_num}.txt")
    codex exec --skip-git-repo-check -m gpt-image-2 -i "$OUTPUT_DIR/${PAGES[0]}.png" -- "$PROMPT"
    
    sleep 2
    after_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l)
    
    if [ "$after_count" -gt "$before_count" ]; then
        latest=$(find ~/.codex/generated_images -name "*.png" -print0 | xargs -0 ls -t | head -1)
        cp "$latest" "$OUTPUT_DIR/${page_name}.png"
        echo "$(date '+%H:%M:%S') - ✓ Saved Page $page_num ($(ls -lh "$OUTPUT_DIR/${page_name}.png" | awk '{print $5}'))"
    else
        echo "$(date '+%H:%M:%S') - ✗ Failed to generate Page $page_num"
    fi
    echo ""
done

echo "=== Generation Complete ==="
echo ""
echo "Generated files:"
ls -lh "$OUTPUT_DIR"/