export CC=gcc.exe
export CXX=g++.exe 
export FC=gfortran.exe

yes | ./configure -noX11 --with-python `which python` gnu
mingw32-make
mingw32-make install
xcopy /E %PREFIX%\bin %PREFIX%\Scripts\
if errorlevel 1 exit 1
