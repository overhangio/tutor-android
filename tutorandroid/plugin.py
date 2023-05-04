from __future__ import annotations

from glob import glob
import os
import typing as t

import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__

config = {
    "unique": {"OAUTH2_SECRET": "{{ 24|random_string }}"},
    "defaults": {
        "VERSION": __version__,
        "APP_HOST": "mobile.{{ LMS_HOST }}",
        # Version 4.0.0 is not working:
        # https://github.com/overhangio/tutor-android/pull/6#issuecomment-1541510489
        "APP_VERSION": "3.1.4",
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
            os.path.join("plugins", "android", "build"),
            "{{ ANDROID_DOCKER_IMAGE }}",
            ("--target=common",),
        ),
        (
            "android-app",
            os.path.join("plugins", "android", "build"),
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


# Build app image on launch
tutor_hooks.Filters.IMAGES_BUILD_REQUIRED.add_item("android-app")


# Mount custom edx-app-android repo at build time
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _build_custom_android_app(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == "edx-app-android":
        # Bind-mount repo at build-time
        mounts.append(("android", "edx-app-android"))
    return mounts


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_android_app_public_hosts(
    hostnames: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "local":
        hostnames.append("{{ ANDROID_APP_HOST }}")
    else:
        hostnames.append("{{ ANDROID_APP_HOST }}:8321")
    return hostnames


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
