Android application plugin for `Tutor <https://docs.tutor.overhang.io>`__
=========================================================================

This is a plugin to easily build an Android mobile application for your `Open edX <https://open.edx.org>`__ instance.

Installation
------------

::

    pip install tutor-android

Usage
-----

Enable the plugin::

    tutor plugins enable android

To build the application in debug mode, run::

    tutor android build debug

The ``.apk`` file will then be available in ``$(tutor config printroot)/data/android``. Transfer it to an Android phone to install the application. You should be able to sign in and view available courses.

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

Releasing an Android app on the Play Store requires to build the app in release mode. To do so, edit the ``$TUTOR_ROOT/config.yml`` configuration file and define the following variables::

    ANDROID_RELEASE_STORE_PASSWORD
    ANDROID_RELEASE_KEY_PASSWORD
    ANDROID_RELEASE_KEY_ALIAS

Then, place your keystore file in ``$(tutor config printroot)/env/plugins/android/apps/app.keystore``. Finally, build the application with::

    tutor android build release

Customising the Android app
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Customising the application, such as the logo or the background image, is currently not supported. If you are interested by this feature, please tell us about it in the Tutor `discussion forums <https://discuss.overhang.io>`_.


License
-------

This software is licensed under the terms of the AGPLv3.
