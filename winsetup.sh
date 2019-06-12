#!/bin/bash
cd dist/4dchess
cd vpython/vpython_libraries
for file in *.html
do
  mv "$file" "${file%.html}.htmlc"
done
cd ..
mkdir vpython_librariesc vpython_datac
xcopy vpython_libraries vpython_librariesc /E /H /K
xcopy vpython_data vpython_datac /E /H /K