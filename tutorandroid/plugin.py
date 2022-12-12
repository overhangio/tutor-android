from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__

config = {
    "unique": {"OAUTH2_SECRET": "{{ 24|random_string }}"},
    "defaults": {
        "VERSION": __version__,
        "APP_HOST": "mobile.{{ LMS_HOST }}",
        # Unfortunately 3.2.2 is not functional: https://github.com/openedx/build-test-release-wg/issues/211#issuecomment-1344311500
        # "APP_VERSION": "3.2.2",  # https://github.com/openedx/edx-app-android/releases
        "APP_VERSION": "3.0.2",
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-android:{{ ANDROID_VERSION }}",
        "APP_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-android-app:{{ ANDROID_VERSION }}",
        "ENABLE_RELEASE_MODE": False,
        "RELEASE_STORE_PASSWORD": "android store password",
        "RELEASE_KEY_PASSWORD": "android release key password",
        "RELEASE_KEY_ALIAS": "android release key alias",
    },
}

with open(
    os.path.join(
        pkg_resources.resource_filename("tutorandroid", "templates"),
        "android",
        "tasks",
        "lms",
        "init",
    ),
    encoding="utf8",
) as fi:
    tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
        (
            "lms",
            fi.read(),
        )
    )
tutor_hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "android",
            ("plugins", "android", "build", "android"),
            "{{ ANDROID_DOCKER_IMAGE }}",
            (),
        ),
        (
            "android-app",
            ("plugins", "android", "build", "app"),
            "{{ ANDROID_APP_DOCKER_IMAGE }}",
            (),
        ),
    ]
)


@tutor_hooks.Filters.IMAGES_PULL.add()
@tutor_hooks.Filters.IMAGES_PUSH.add()
def _add_remote_android_app_image_iff_customized(images, user_config):
    """
    Register ANDROID-APP image for pushing & pulling if and only if it has
    been set to something other than the default.

    This is work-around to an upstream issue with ANDROID-APP config. Briefly:
    User config is baked into ANDROID-APP builds, so Tutor cannot host a generic
    pre-built ANDROID-APP image. However, individual Tutor users may want/need to
    build and host their own ANDROID-APP image. So, as a compromise, we tell Tutor
    to push/pull the ANDROID-APP image if the user has customized it to anything
    other than the default image URL.
    """
    image_tag = user_config["ANDROID_APP_DOCKER_IMAGE"]
    if not image_tag.startswith("docker.io/overhangio/openedx-android-app:"):
        # Image has been customized. Add to list for pulling/pushing.
        images.append(("android-app", image_tag))
    return images


tutor_hooks.Filters.IMAGES_PULL.add_item(
    (
        "android",
        "{{ ANDROID_DOCKER_IMAGE }}",
    )
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "android",
        "{{ ANDROID_DOCKER_IMAGE }}",
    )
)

####### Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorandroid", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("android/build", "plugins"),
        ("android/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorandroid", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"ANDROID_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"ANDROID_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)
