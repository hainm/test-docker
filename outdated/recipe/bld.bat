set CC=gcc.exe
set CXX=g++.exe 
set FC=gfortran.exe

set AMBERHOME=%cd%
python update_amber --show-applied-patches
python update_amber --update
python update_amber --show-applied-patches
echo n | bash .\configure -noX11 --with-python C:\Miniconda3\envs\py27\python.exe gnu
make
make install
xcopy /E %PREFIX%\bin %PREFIX%\Scripts\
if errorlevel 1 exit 1
