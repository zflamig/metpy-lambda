FROM lambci/lambda:build-python3.7

# Install dependencies

RUN curl -L http://download.osgeo.org/proj/proj-4.9.3.tar.gz | tar zxf - -C /tmp \
    && cd /tmp/proj-4.9.3 \
    && ./configure --prefix=/var/task \
    && make -j $(nproc) \
    && make install \
    && cd /tmp \
    && rm -rf proj*

RUN curl -L http://download.osgeo.org/geos/geos-3.7.1.tar.bz2 | tar jxf - -C /tmp \
    && cd /tmp/geos-3.7.1 \
    && ./configure --prefix=/var/task \
    && make -j $(nproc) \
    && make install \
    && cd /tmp \
    && rm -rf geos*

# Install python packages we want

RUN pip install --upgrade metpy pytest pandas pint pooch traitlets scipy netCDF4 matplotlib python-dateutil==2.8.0 -t python/
RUN export PYTHONPATH=/var/task/python:$PYTHONPATH; LD_LIBRARY_PATH=/var/task/lib:$LD_LIBRARY_PATH; export PATH=/var/task/bin:$PATH; pip install --global-option=build_ext --global-option="-I/var/task/include" --global-option="-L/var/task/lib" --upgrade cartopy==0.18.0b1 -t python/


# Shrink layer size by stripping libraries and removing unnecessary files

RUN find python/numpy -name "*.so" | xargs strip
RUN find python/pandas -name "*.so" | xargs strip
RUN find lib -name "*.so" | xargs strip
RUN rm -rf lib/*.a python/setuptools/*.exe python/pandas/tests python/scipy/stats/tests python/matplotlib/tests python/pyarrow/tests python/mpl_toolkits/tests python/scipy/linalg/tests python/numpy/tests

# Package the layer up into a zip file we can extract

RUN zip -r9 "metpy_layer.zip" ./python ./lib

