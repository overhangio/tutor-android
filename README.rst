Android application plugin for `Tutor <https://docs.tutor.edly.io>`__
=====================================================================

This is a plugin to easily build an Android mobile application for your `Open edX <https://open.edx.org>`__ instance.

Installation
------------

.. code-block:: bash

    tutor plugins install android

Usage
-----

Enable the plugin and start the platform:

.. code-block:: bash

    tutor plugins enable android
    tutor local launch

The ``.apk`` file will then be available for download at http(s)://mobile.LMS_HOST/app.apk. When running locally,
this will be: http://mobile.local.openedx.io/app.apk. You can forward this address to your students for download.

Building a custom Android app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Android app is built from the `official openedx-app-android repository <https://github.com/openedx/openedx-app-android/>`__.
To change this repository or the app version, you can simply build a different docker image with:

.. code-block:: bash

    tutor images build \
        --build-arg ANDROID_APP_REPOSITORY=https://github.com/mycustomfork/openedx-app-android \
        --build-arg ANDROID_APP_VERSION=master \
        android

Alternatively, you can build an image from a local checked-out fork of openedx-app-android:

.. code-block:: bash

    tutor mounts add /path/to/openedx-app-android
    tutor local launch

Making courses visible in app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, courses are not visible in the mobile app. To make them available, go to
Studio → YOUR COURSE → Settings → Advanced Settings and set ``Mobile Course Available`` to true.


Releasing an Android app
~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: this is an untested feature.

Releasing an Android app on the Play Store requires to build the app in release mode. To do so,
modify the following Tutor settings:

.. code-block:: bash

    tutor config save \
      --set ANDROID_RELEASE_STORE_PASSWORD=yourstorepassword \
      --set ANDROID_RELEASE_KEY_PASSWORD=yourreleasekeypassword \
      --set ANDROID_RELEASE_KEY_ALIAS=yourreleasekeyalias \
      --set ANDROID_ENABLE_RELEASE_MODE=true

Then, place your keystore file in ``$(tutor config printroot)/env/plugins/android/build/app/config/app.keystore``.
Finally, rebuild the image by starting the "android-app" container:

.. code-block:: bash

    tutor local start -d android-app

Customising the Android app
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Customising the application, such as the logo or the background image, is currently not supported.
If you are interested by this feature, please tell us about it in the Tutor `discussion forums <https://discuss.overhang.io>`_.

Customising the app configuration (``tutor.yaml``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Android app reads its configuration from a ``tutor.yaml`` file rendered at build time.
All commonly customised fields are exposed as ``ANDROID_*`` Tutor settings, so you can change
them with ``tutor config save --set <KEY>=<VALUE>``. For example, to enable Firebase:

.. code-block:: bash

    tutor config save \
      --set ANDROID_FIREBASE_ENABLED=true \
      --set ANDROID_FIREBASE_PROJECT_ID=my-project \
      --set ANDROID_FIREBASE_API_KEY=AIzaSy...

The available settings include ``ANDROID_ENVIRONMENT_DISPLAY_NAME``, ``ANDROID_URI_SCHEME``,
``ANDROID_FAQ_URL``, ``ANDROID_OAUTH_CLIENT_ID``, ``ANDROID_PLATFORM_FULL_NAME``,
``ANDROID_THEME_DIRECTORY``, ``ANDROID_TOKEN_TYPE``, the agreement URLs
(``ANDROID_PRIVACY_POLICY_URL``, ``ANDROID_COOKIE_POLICY_URL``, ``ANDROID_DATA_SELL_CONSENT_URL``,
``ANDROID_TOS_URL``, ``ANDROID_EULA_URL``), ``ANDROID_SUPPORTED_LANGUAGES``, the
``ANDROID_DISCOVERY_*`` and ``ANDROID_PROGRAM_*`` groups, ``ANDROID_FIREBASE_*``,
``ANDROID_SEGMENT_IO_*``, ``ANDROID_BRAZE_*``, ``ANDROID_GOOGLE_*``, ``ANDROID_MICROSOFT_*``,
``ANDROID_FACEBOOK_*``, ``ANDROID_BRANCH_*``, and the feature flags
``ANDROID_WHATS_NEW_ENABLED``, ``ANDROID_SOCIAL_AUTH_ENABLED``,
``ANDROID_COURSE_NESTED_LIST_ENABLED`` and ``ANDROID_COURSE_UNIT_PROGRESS_ENABLED``.

For settings that are not exposed as Tutor variables, your own Tutor plugin can append YAML
to ``tutor.yaml`` via the ``android-tutor-yaml`` patch:

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item((
        "android-tutor-yaml",
        "MY_CUSTOM_KEY: my-value\n",
    ))

The Open edX Android app uses SnakeYAML, which keeps the last value when a key is duplicated.
That means a top-level key written by the patch will **replace** the value emitted earlier in
the file, so use ``ANDROID_*`` settings for partial tweaks within a group (for example
``ANDROID_FIREBASE_ENABLED``) and reserve the patch for adding new keys or for wholesale
replacement of an entire group.

If neither approach is sufficient, you can replace the rendered ``tutor.yaml`` outright by
editing ``$(tutor config printroot)/env/plugins/android/build/config/tutor.yaml`` before
running ``tutor images build android-app``.

Troubleshooting
---------------

This Tutor plugin is maintained by Abdul-Muqadim from `Edly <https://edly.io>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-android/blob/release/LICENSE.txt>`_.
