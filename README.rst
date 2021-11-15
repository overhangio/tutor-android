Android application plugin for `Tutor <https://docs.tutor.overhang.io>`__
=========================================================================

This is a plugin to easily build an Android mobile application for your `Open edX <https://open.edx.org>`__ instance.

Installation
------------

::

    pip install tutor-android

Usage
-----

Enable the plugin and start the platform::

    tutor plugins enable android
    tutor local quickstart


The ``.apk`` file will then be available for download at http(s)://mobile.LMS_HOST/app.apk. When running locally, this will be: http://mobile.local.overhang.io/app.apk. You can forward this address to your students for download.

Building a custom Android app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Android app is built from the `official edx-app-android repository <https://github.com/edx/edx-app-android/>`__. To change this repository or the app version, you can simply build a different docker image with::

    tutor images build \
        --build-arg ANDROID_APP_REPOSITORY=https://github.com/mycustomfork/edx-app-android \
        --build-arg ANDROID_APP_VERSION=master \
        android

Releasing an Android app
~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: this is an untested feature.

Releasing an Android app on the Play Store requires to build the app in release mode. To do so, modify the following Tutor settings::

    tutor config save \
      --set ANDROID_RELEASE_STORE_PASSWORD=yourstorepassword \
      --set ANDROID_RELEASE_KEY_PASSWORD=yourreleasekeypassword \
      --set ANDROID_RELEASE_KEY_ALIAS=yourreleasekeyalias \
      --set ANDROID_ENABLE_RELEASE_MODE=true

Then, place your keystore file in ``$(tutor config printroot)/env/plugins/android/build/app/config/app.keystore``. Finally, rebuild the image by starting the "android-app" container::

    tutor local start -d android-app

Customising the Android app
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Customising the application, such as the logo or the background image, is currently not supported. If you are interested by this feature, please tell us about it in the Tutor `discussion forums <https://discuss.overhang.io>`_.

License
-------

This software is licensed under the terms of the AGPLv3.
