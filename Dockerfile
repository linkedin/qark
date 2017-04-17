FROM python:2.7
LABEL maintainer <ilya@ilyaglotov.com>

# Install JRE
RUN apt-get update && apt-get -y install openjdk-7-jre-headless \
    curl

RUN mkdir /qark
WORKDIR /qark

# Install Android SDK
ENV ANDROID_SDK_VERSION r24.3.4
ENV HOST_OS linux
ENV ANDROID_SDK_PACKAGE="android-sdk_${ANDROID_SDK_VERSION}-${HOST_OS}.tgz"
RUN curl -s https://dl.google.com/android/${ANDROID_SDK_PACKAGE} -o ${ANDROID_SDK_PACKAGE}
RUN tar xzf ${ANDROID_SDK_PACKAGE}

# Install QARK dependencies
ADD . /qark
WORKDIR /qark
RUN pip install -r requirements.txt

# Volume for an APK or application sources
RUN mkdir /apk
VOLUME /apk

# By default QARK can start to analyze apks on the mounted volume.
# Report will be on the same folder.
WORKDIR /qark/qark
# CMD python qarkMain.py --source 1 --pathtoapk /apk/*.apk --exploit 0 --basepath /qark/android-sdk-linux --reportdir /apk/
