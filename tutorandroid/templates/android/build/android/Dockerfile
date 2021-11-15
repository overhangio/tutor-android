FROM docker.io/ubuntu:20.04
MAINTAINER Overhang.io <contact@overhang.io>

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt upgrade -y && \
  apt install -y wget unzip git openjdk-8-jre openjdk-8-jdk

RUN mkdir /app

# Install Android SDK
# Inspired from https://github.com/LiveXP/docker-android-sdk/blob/master/Dockerfile
# Get sdk version from here: https://developer.android.com/studio#command-tools
ENV ANDROID_SDK_VERSION 7583922
ENV ANDROID_SDK_PATH /app/android-sdk
ENV ANDROID_HOME /app/android-sdk
RUN mkdir ${ANDROID_HOME}
WORKDIR /app/android-sdk
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    unzip commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    rm commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip

# Accept licenses
# https://developer.android.com/studio/command-line/sdkmanager
# Check target version: https://github.com/edx/edx-app-android/blob/master/constants.gradle
ARG ANDROID_API_LEVEL=29
RUN yes | /app/android-sdk/cmdline-tools/bin/sdkmanager --sdk_root=${ANDROID_HOME} --install "platforms;android-$ANDROID_API_LEVEL" 1> /dev/null

# Install android app repo
ARG ANDROID_APP_REPOSITORY=https://github.com/edx/edx-app-android
ARG ANDROID_APP_VERSION=release/{{ ANDROID_APP_VERSION }}
RUN git clone $ANDROID_APP_REPOSITORY --branch $ANDROID_APP_VERSION /app/edx-app-android
WORKDIR /app/edx-app-android

# Install gradle and all dependencies
RUN ./gradlew -v
RUN ./gradlew tasks
