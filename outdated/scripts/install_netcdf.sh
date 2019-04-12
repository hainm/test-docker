curl -fsS -o netcdf-4.3.3.zip ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.zip
unzip netcdf-4.3.3.zip
cd netcdf-4.3.3
./configure --enable-static --disable-netcdf-4 --prefix=/usr/local/ --disable-dap
make -r install;
