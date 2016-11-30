set CC=gcc.exe
set CXX=g++.exe 
set FC=gfortran.exe

bash .\configure -noX11 gnu
make
mingw32-make
mingw32-make install
xcopy /E %PREFIX%\bin %PREFIX%\Scripts\
if errorlevel 1 exit 1
