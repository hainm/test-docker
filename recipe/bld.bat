set CC=gcc.exe
set CXX=g++.exe 
set FC=gfortran.exe

set AMBERHOME=%cd%
python update_amber --show-applied-patches
python update_amber --update
python update_amber --show-applied-patches
bash .\configure -noX11 gnu
make
mingw32-make
mingw32-make install
xcopy /E %PREFIX%\bin %PREFIX%\Scripts\
if errorlevel 1 exit 1
