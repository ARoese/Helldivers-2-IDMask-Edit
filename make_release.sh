#!/bin/bash
VERSION=$(python info.py)
echo Making release for v$VERSION

rm -r release
mkdir -p release

git archive HEAD -o "release/id_mask_release.zip"
cd release

mkdir "IDMask-Edit"

unzip id_mask_release.zip -d "IDMask-Edit"
zip "IDMask-Edit-v$VERSION.zip" -r "IDMask-Edit"
rm -r "IDMask-Edit" id_mask_release.zip

cd -

echo
echo Release created at \'"release/IDMask-Edit-v$VERSION.zip"\'