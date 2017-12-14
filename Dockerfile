FROM python:2.7
LABEL url "https://www.github.com/linkedin/qark"

# Install JRE
RUN apt-get update && \
    apt-get -y install openjdk-7-jre-headless \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /qark
WORKDIR /qark

# Install Android SDK
ENV ANDROID_SDK_VERSION r24.3.4
ENV HOST_OS linux
ENV ANDROID_SDK_PACKAGE="android-sdk_${ANDROID_SDK_VERSION}-${HOST_OS}.tgz"

RUN curl -s https://dl.google.com/android/${ANDROID_SDK_PACKAGE} \
    -o ${ANDROID_SDK_PACKAGE} \
  && apt-get purge -y curl \
  && tar xzf ${ANDROID_SDK_PACKAGE} \
  && rm -f ${ANDROID_SDK_PACKAGE}

# Install QARK dependencies
ADD qark requirements.txt /qark/
RUN pip install -r requirements.txt \
  && rm -rf /root/.cache

# Volume for an APK or application sources
RUN mkdir /apk
VOLUME /apk

# By default QARK can start to analyze apks on the mounted volume.
# Report will be on the same folder.
# CMD python qarkMain.py --source 1 --pathtoapk /apk/*.apk --exploit 0 --basepath /qark/android-sdk-linux --reportdir /apk/

ENTRYPOINT ["python", "qarkMain.py"]
