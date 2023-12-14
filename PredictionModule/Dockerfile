FROM arm32v7/python:3.7-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1

ARG ARCH=arm32v7

RUN apt-get update --no-install-recommends
RUN apt-get --yes install --no-install-recommends libatlas-base-dev
RUN apt-get clean

RUN pip3 install numpy --index-url=https://www.piwheels.org/simple --no-cache-dir
RUN pip3 install scipy --index-url=https://www.piwheels.org/simple --no-cache-dir
RUN pip3 install statsmodels --index-url=https://www.piwheels.org/simple --no-cache-dir
# RUN pip3 install matplotlib --index-url=https://www.piwheels.org/simple --no-cache-dir
# RUN pip3 install sklearn --index-url=https://www.piwheels.org/simple --no-cache-dir
# RUN pip3 install arch --index-url=https://www.piwheels.org/simple --no-cache-dir

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN apt-get --yes install --no-install-recommends apt-utils
RUN apt-get --yes install --no-install-recommends libjpeg-dev
RUN apt-get --yes install --no-install-recommends libwebp-dev
RUN apt-get --yes install --no-install-recommends libopenjp2-7
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
RUN apt-get clean

EXPOSE 1094
#COPY dataset.csv /.
COPY . /.
CMD ["python","-u","app.py"]
