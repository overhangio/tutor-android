# syntax=docker/dockerfile:1
FROM docker.io/ubuntu:23.10 AS base
LABEL maintainer="Overhang.IO <contact@overhang.io>"

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked apt update && \
    apt upgrade -y && \
    apt install -y wget unzip git openjdk-17-jre openjdk-17-jdk

RUN mkdir /app

###### Install Android SDK
FROM base AS sdk

# Install Android SDK
# Inspired from https://github.com/LiveXP/docker-android-sdk/blob/master/Dockerfile
# Get sdk version from here: https://developer.android.com/studio#command-tools
ENV ANDROID_SDK_VERSION 10406996
ENV ANDROID_SDK_PATH /app/android-sdk
ENV ANDROID_HOME /app/android-sdk
RUN mkdir ${ANDROID_HOME}
WORKDIR /app/android-sdk
RUN wget --quiet https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    unzip commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip && \
    rm commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip

# Accept licenses
# https://developer.android.com/studio/command-line/sdkmanager
# Check target version: https://github.com/edx/edx-app-android/blob/master/constants.gradle
ARG ANDROID_API_LEVEL=33
RUN yes | /app/android-sdk/cmdline-tools/bin/sdkmanager --sdk_root=${ANDROID_HOME} --install "platforms;android-$ANDROID_API_LEVEL" 1> /dev/null

###### Checkout code
FROM base AS code
# Install android app repo
ARG ANDROID_APP_REPOSITORY=https://github.com/openedx/edx-app-android.git

# Please add ANDROID_APP_VERSION value in tutor config from release version https://github.com/openedx/edx-app-android/tags
ARG ANDROID_APP_VERSION={% if OPENEDX_COMMON_VERSION == "master" %}master{% else %}release/{{ ANDROID_APP_VERSION }}{% endif %}
ADD --keep-git-dir $ANDROID_APP_REPOSITORY#$ANDROID_APP_VERSION /app/edx-app-android

###### Empty layer to mount custom repo at build time
FROM scratch AS edx-app-android
COPY --from=code /app/edx-app-android /

###### Common layer, which will be used to build the user-specific image later
FROM sdk AS common

COPY --from=edx-app-android / /app/edx-app-android
WORKDIR /app/edx-app-android

# Install gradle and all dependencies
RUN ./gradlew -v
RUN ./gradlew tasks

###### Build image with app-specific settings
FROM common as build

# User-customized config
COPY ./config/edx.properties ./OpenEdXMobile/default_config/edx.properties
COPY ./config/tutor.yaml ./OpenEdXMobile/default_config/tutor.yaml
{% if ANDROID_ENABLE_RELEASE_MODE %}
# Add release settings
COPY ./config/gradle.properties ./gradle.properties.tutor
RUN cat ./gradle.properties.tutor >> ./gradle.properties
{% endif %}

# uncomment this line for for release APK. 
# RUN sed -i "s/APPLICATION_ID = .*/APPLICATION_ID = \"{{ LMS_HOST|reverse_host|replace("-", "_") }}\"/g" constants.gradle
RUN ./gradlew assembleProd{{ "Release" if ANDROID_ENABLE_RELEASE_MODE else "Debuggable" }}

#### File server to serve apk file
# https://hub.docker.com/_/caddy?tab=tags
FROM docker.io/caddy:2.6.4-alpine as production
COPY --from=build /app/edx-app-android/OpenEdXMobile/build/outputs/apk/prod/{{ "release" if ANDROID_ENABLE_RELEASE_MODE else "debuggable" }}/edx-{{ "release" if ANDROID_ENABLE_RELEASE_MODE else "debuggable" }}-{{ ANDROID_APP_VERSION }}.apk /srv/app.apk
CMD caddy file-server --listen=:8000 --root=/srv
