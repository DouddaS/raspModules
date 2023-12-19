# Author: Henda Sfx

#!/bin/bash
FROM arm32v7/python:3.7-slim-buster
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ARG ARCH=arm32v7

# Turns off buffering for easier container logging
#ENV PYTHONUNBUFFERED=1

RUN apt-get update --no-install-recommends
RUN apt-get --yes install --no-install-recommends apt-utils
RUN apt-get --yes install --no-install-recommends libjpeg-dev
RUN apt-get --yes install --no-install-recommends libwebp-dev
RUN apt-get --yes install --no-install-recommends libatlas-base-dev
RUN apt-get --yes install --no-install-recommends gfortran
RUN apt-get --yes install --no-install-recommends libpng-dev
RUN apt-get --yes install --no-install-recommends libtiff5-dev
RUN apt-get --yes install --no-install-recommends libopenjp2-7
RUN apt-get --yes install --no-install-recommends libopenexr-dev
RUN apt-get --yes install --no-install-recommends libavcodec-dev
RUN apt-get --yes install --no-install-recommends libavformat-dev
RUN apt-get --yes install --no-install-recommends libswscale-dev
RUN apt-get --yes install --no-install-recommends libgtk-3-dev
#RUN apt-get --yes install --no-install-recommends g++
RUN apt-get --yes install --no-install-recommends cmake>=3.12
#RUN apt-get --yes install --no-install-recommends make
RUN apt-get --yes install --no-install-recommends wget unzip
RUN apt-get --yes install --no-install-recommends libxvidcore-dev
RUN apt-get --yes install --no-install-recommends libx264-dev
RUN apt-get --yes install --no-install-recommends libv4l-dev
RUN apt-get --yes install --no-install-recommends pkg-config
RUN apt-get --yes install --no-install-recommends build-essential
#RUN apt-get --yes install --no-install-recommends python-dev
#RUN apt-get --yes install --no-install-recommends python3-dev


#10-08-2022
RUN apt-get --yes install --no-install-recommends python3 
RUN apt-get --yes install --no-install-recommends python3-pip 
RUN apt-get --yes install --no-install-recommends python3-dev 
RUN apt-get --yes install --no-install-recommends python3-pyqt5
RUN pip3 install numpy --index-url=https://www.piwheels.org/simple --no-cache-dir


RUN apt-get clean

#RUN pip install numpy --index-url=https://www.piwheels.org/simple --no-cache-dir
RUN pip3 install "picamera[array]" --no-cache-dir

#11-08-2022
#RUN apt-get --yes install python3-opencv
#RUN apt-get clean
#doesnt work
RUN pip3 install opencv-python --index-url=https://www.piwheels.org/simple --no-cache-dir

#RUN mkdir -p ~/opencv cd ~/opencv && \
#    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.1.zip && \
#    unzip opencv.zip && \
#    mv opencv-4.1.1 opencv && \
#    rm opencv.zip && \
#    mkdir -p build && \ 
#    cd build && \
#    cmake ../opencv \
#    -DWITH_OPENGL=ON \
#    -DENABLE_NEON=ON \
#    -DENABLE_VFPV3=ON \  
#    -DFORCE_VTK=ON \
#    -DWITH_TBB=ON \
#    -DWITH_GDAL=ON \
#    -DWITH_XINE=ON \
#    -DBUILD_EXAMPLES=OFF .. && \
#    make -j4 && \
#    make install && \ 
#    ldconfig

COPY requirements.txt /requirements.txt
RUN pip install --index-url=https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

EXPOSE 1090
COPY . /.
CMD ["python","app.py"]
