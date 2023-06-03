#!/usr/bin/env bash

set -e

BUILD_NAME="weewx-mqtt"

BUILD_FILES=(
    "LICENSE"
    "install.py"
    "bin"
)

SRC_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

BUILD_TAG="$1"
if [[ -z "$BUILD_TAG" ]]; then
    echo "Error: Build tag not specified"
    exit 1
fi

BUILD_SUFFIX="$2"

TMP_BASE_DIR="$(mktemp -d)"
TMP_SRC_DIR="${TMP_BASE_DIR}/src"

OUTPUT_DIR="$SRC_DIR/.."

#################################################

cleanup() {
    popd

    echo "Removing temporary dir: $TMP_BASE_DIR"
    [[ -e "$TMP_BASE_DIR" ]] && rm -Rf "$TMP_BASE_DIR"
    exit
}

#################################################

trap cleanup INT TERM

echo "Using source dir: $SRC_DIR"
echo "Using temporary dir: $TMP_BASE_DIR"

echo "Copying source to $TMP_SRC_DIR"
[[ -d "$TMP_SRC_DIR" ]] || mkdir -p "$TMP_SRC_DIR"
cp -Ra "$SRC_DIR"/. "$TMP_SRC_DIR"
pushd "$TMP_SRC_DIR"
git checkout "tags/$BUILD_TAG"

BUILD_VERSION="$(git describe)"

popd

BUILD_DIR_NAME="${BUILD_NAME}-${BUILD_VERSION}"
if [[ -n "$BUILD_SUFFIX" ]]; then
    BUILD_DIR_NAME="${BUILD_DIR_NAME}-${BUILD_SUFFIX}"
fi

BUILD_DIR="${TMP_BASE_DIR}/${BUILD_DIR_NAME}"
mkdir -p "$BUILD_DIR"

for src_file in "${BUILD_FILES[@]}"; do
    src_path="$TMP_SRC_DIR/$src_file"
    cp -R "$src_path" "$BUILD_DIR"
done

pushd "$TMP_BASE_DIR"

OUTPUT_FILE_NAME="$BUILD_DIR_NAME.tar.xz"
OUTPUT_PATH="${OUTPUT_DIR}/${OUTPUT_FILE_NAME}"

tar -cvf "$OUTPUT_PATH" "$BUILD_DIR_NAME"

echo "Saved output to $OUTPUT_PATH"

cleanup
