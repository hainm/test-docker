set CC=gcc.exe
set CXX=g++.exe 
set FC=gfortran.exe

.\configure -noX11 gnu
mingw32-make
mingw32-make install
xcopy /E %PREFIX%\bin %PREFIX%\Scripts\
if errorlevel 1 exit 1
