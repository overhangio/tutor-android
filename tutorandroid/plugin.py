from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutor.types import Config, get_typed

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__


config: t.Dict[str, t.Dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        "APP_HOST": "mobile.{{ LMS_HOST }}",
        "APP_ID": "org.openedx.app",
        "APP_REPOSITORY": "https://github.com/openedx/openedx-app-android.git",
        "APP_VERSION": '{% if OPENEDX_COMMON_VERSION == "master" %}main{% else %}{{ OPENEDX_COMMON_VERSION }}{% endif %}',  # noqa: E501
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-android:{{ ANDROID_VERSION }}",  # noqa: E501
        "APP_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-android-app:{{ ANDROID_VERSION }}",  # noqa: E501
        "ENABLE_RELEASE_MODE": False,
        "RELEASE_STORE_PASSWORD": "android store password",
        "RELEASE_KEY_PASSWORD": "android release key password",
        "RELEASE_KEY_ALIAS": "android release key alias",
        # tutor.yaml: top-level app settings
        "ENVIRONMENT_DISPLAY_NAME": "tutor",
        "URI_SCHEME": "",
        "FAQ_URL": "",
        "OAUTH_CLIENT_ID": "android",
        "PLATFORM_FULL_NAME": "{{ PLATFORM_NAME }}",
        "THEME_DIRECTORY": "openedx",
        "TOKEN_TYPE": "JWT",
        # Agreement URLs (leave empty to hide the corresponding setting)
        "PRIVACY_POLICY_URL": "",
        "COOKIE_POLICY_URL": "",
        "DATA_SELL_CONSENT_URL": "",
        "TOS_URL": "",
        "EULA_URL": "",
        "SUPPORTED_LANGUAGES": [],
        # Discovery
        "DISCOVERY_TYPE": "native",
        "DISCOVERY_WEBVIEW_BASE_URL": "",
        "DISCOVERY_WEBVIEW_COURSE_DETAIL_TEMPLATE": "",
        "DISCOVERY_WEBVIEW_PROGRAM_DETAIL_TEMPLATE": "",
        # Program
        "PROGRAM_TYPE": "native",
        "PROGRAM_WEBVIEW_PROGRAM_URL": "",
        "PROGRAM_WEBVIEW_PROGRAM_DETAIL_URL_TEMPLATE": "",
        # Firebase
        "FIREBASE_ENABLED": False,
        "FIREBASE_ANALYTICS_SOURCE": "",
        "FIREBASE_CLOUD_MESSAGING_ENABLED": False,
        "FIREBASE_PROJECT_NUMBER": "",
        "FIREBASE_PROJECT_ID": "",
        "FIREBASE_APPLICATION_ID": "",
        "FIREBASE_API_KEY": "",
        # Segment.io
        "SEGMENT_IO_ENABLED": False,
        "SEGMENT_IO_WRITE_KEY": "",
        # Braze
        "BRAZE_ENABLED": False,
        "BRAZE_PUSH_NOTIFICATIONS_ENABLED": False,
        # Social: Google
        "GOOGLE_ENABLED": False,
        "GOOGLE_CLIENT_ID": "",
        # Social: Microsoft
        "MICROSOFT_ENABLED": False,
        "MICROSOFT_CLIENT_ID": "",
        "MICROSOFT_PACKAGE_SIGNATURE": "",
        # Social: Facebook
        "FACEBOOK_ENABLED": False,
        "FACEBOOK_APP_ID": "",
        "FACEBOOK_CLIENT_TOKEN": "",
        # Branch
        "BRANCH_ENABLED": False,
        "BRANCH_KEY": "",
        "BRANCH_URI_SCHEME": "",
        "BRANCH_HOST": "",
        "BRANCH_ALTERNATE_HOST": "",
        # Feature flags
        "WHATS_NEW_ENABLED": False,
        "SOCIAL_AUTH_ENABLED": False,
        "COURSE_NESTED_LIST_ENABLED": False,
        "COURSE_UNIT_PROGRESS_ENABLED": False,
    },
    "unique": {
        "OAUTH2_SECRET": "{{ 24|random_string }}",
    },
}

with open(
    os.path.join(
        str(importlib_resources.files("tutorandroid") / "templates"),
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
def _add_remote_android_app_image_iff_customized(
    images: list[tuple[str, str]], user_config: Config
) -> list[tuple[str, str]]:
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
    image_tag = get_typed(user_config, "ANDROID_APP_DOCKER_IMAGE", str, "")
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
    if path_basename == "openedx-app-android":
        # Bind-mount repo at build-time
        mounts.append(("android", "openedx-app-android"))
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


# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorandroid") / "templates")
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
        str(importlib_resources.files("tutorandroid") / "patches"),
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
