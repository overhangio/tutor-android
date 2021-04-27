from glob import glob
import os
import pkg_resources

from .__about__ import __version__
from .cli import android as android_command


templates = pkg_resources.resource_filename("tutorandroid", "templates")


config = {
    "add": {"OAUTH2_SECRET": "{{ 24|random_string }}"},
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-android:{{ ANDROID_VERSION }}",
        "RELEASE_STORE_PASSWORD": "android store password",
        "RELEASE_KEY_PASSWORD": "android release key password",
        "RELEASE_KEY_ALIAS": "android release key alias",
    },
}

hooks = {"build-image": {"android": "{{ ANDROID_DOCKER_IMAGE }}"}, "init": ["lms"]}


command = android_command


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutorandroid", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
