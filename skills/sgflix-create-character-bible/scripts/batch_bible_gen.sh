#!/bin/bash
# SGFLIX Character Bible Batch Generator
# Usage: ./batch_bible_gen.sh <bible_dir> <ref_image>
#
# Generates pages 2-8 using page 01 as reference for identity consistency.
# Page 01 must already exist at <bible_dir>/images/page_01_primary_hero_reference.png
#
# Prompts must be pre-written to /tmp/page{2-8}.txt (one per file, no shell escaping)
#
# Prevents duplicate cascade by tracking before/after image count.

set -euo pipefail

BIBLE_DIR="${1:?Usage: $0 <bible_dir> <ref_image>}"
REF_IMAGE="${2:?Usage: $0 <bible_dir> <ref_image>}"
MODEL="gpt-image-2"

# Verify page 01 exists
if [ ! -f "$BIBLE_DIR/images/page_01_primary_hero_reference.png" ]; then
    echo "ERROR: Page 01 not found at $BIBLE_DIR/images/page_01_primary_hero_reference.png"
    echo "Generate page 01 first, then run this script for pages 2-8."
    exit 1
fi

# Verify reference image exists
if [ ! -f "$REF_IMAGE" ]; then
    echo "ERROR: Reference image not found at $REF_IMAGE"
    exit 1
fi

PAGES=(
    "page_02_orthographic_turnaround"
    "page_03_morphology_proportions_silhouette"
    "page_04_expression_emotion_sheet"
    "page_05_cranial_appendage_details"
    "page_06_surface_treatment_construction"
    "page_07_extremities_props_accessories"
    "page_08_materials_color_rigging_motion"
)

generate_page() {
    local page_name="$1"
    local prompt_num="$2"
    local prompt_file="/tmp/page${prompt_num}.txt"
    local output_path="$BIBLE_DIR/images/${page_name}.png"

    if [ ! -f "$prompt_file" ]; then
        echo "SKIP: $prompt_file not found"
        return 1
    fi

    echo "$(date '+%H:%M:%S') - Generating ${page_name}..."

    # Snapshot existing images BEFORE generation
    before_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l | tr -d ' ')

    PROMPT=$(cat "$prompt_file")
    codex exec --skip-git-repo-check -m "$MODEL" -i "$REF_IMAGE" -- "$PROMPT" 2>&1 | tail -5

    # Check for usage limit
    # (the output above may contain the error — also check the next find)
    sleep 3

    after_count=$(find ~/.codex/generated_images -name "*.png" 2>/dev/null | wc -l | tr -d ' ')

    if [ "$after_count" -gt "$before_count" ]; then
        latest=$(find ~/.codex/generated_images -name "*.png" -print0 2>/dev/null | xargs -0 ls -t 2>/dev/null | head -1)
        cp "$latest" "$output_path"
        echo "$(date '+%H:%M:%S') - Saved: $output_path ($(ls -lh "$output_path" | awk '{print $5}'))"
    else
        echo "$(date '+%H:%M:%S') - FAILED: No new image generated for ${page_name}"
        echo "         Possible causes: usage limit, timeout, safety filter"
        # Do NOT copy old image — prevents duplicate cascade
        return 1
    fi
    echo ""
}

echo "=== SGFLIX Character Bible Batch Generator ==="
echo "Bible dir: $BIBLE_DIR"
echo "Reference: $REF_IMAGE"
echo "Model: $MODEL"
echo ""

i=2
for page in "${PAGES[@]}"; do
    generate_page "$page" "$i"
    ((i++))
done

echo ""
echo "=== BATCH COMPLETE ==="
echo ""

# Verify uniqueness with MD5
echo "MD5 verification:"
all_unique=true
declare -A seen_hashes
for f in "$BIBLE_DIR"/images/page_*.png; do
    hash=$(md5 -q "$f" 2>/dev/null)
    name=$(basename "$f")
    if [ -n "${seen_hashes[$hash]:-}" ]; then
        echo "  DUPLICATE: $name matches ${seen_hashes[$hash]}"
        all_unique=false
    else
        seen_hashes[$hash]="$name"
        echo "  OK: $name ($hash)"
    fi
done

echo ""
if $all_unique; then
    echo "All pages are unique. Bible is complete."
else
    echo "WARNING: Duplicate pages detected. Re-run failed pages individually."
fi

echo ""
ls -lh "$BIBLE_DIR/images/"
