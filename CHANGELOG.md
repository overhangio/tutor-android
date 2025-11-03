# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-21.0.0'></a>
## v21.0.0 (2025-11-03)

- [Improvement] Migrate from pylint and black to ruff. (by @Abdul-Muqadim-Arbisoft)
- [Improvement] Test python package distribution build when running make test. (by @Abdul-Muqadim-Arbisoft)

- 💥[Feature] Upgrade to Ulmo. (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-20.0.0'></a>
## v20.0.0 (2025-06-10)

- [Improvement] Migrate packaging from setup.py/setuptools to pyproject.toml/hatch. (by @Abdul-Muqadim-Arbisoft)
  - For more details view tutor core PR: https://github.com/overhangio/tutor/pull/1163

- [Improvement] Add hatch_build.py in sdist target to fix the installation issues (by @dawoudsheraz)

- 💥[Feature] Upgrade to teak. (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-19.0.0'></a>
## v19.0.0 (2024-12-09)

- 💥[Feature] Upgrade to Sumac (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-18.0.1'></a>
## v18.0.1 (2024-11-28)

- [Bugfix] Fix legacy warnings during Docker build. (by @regisb)
- 💥[Feature] Update android image to use Ubuntu `24.04` as base OS. (by @Abdul-Muqadim-Arbisoft)
- 💥 [Deprecation] Drop support for python 3.8 and set Python 3.9 as the minimum supported python version. (by @Abdul-Muqadim-Arbisoft)
- 💥[Improvement] Rename Tutor's two branches (by @DawoudSheraz):
  * Rename **master** to **release**, as this branch runs the latest official Open edX release tag.
  * Rename **nightly** to **main**, as this branch runs the Open edX master branches, which are the basis for the next Open edX release.

<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-06-20)

- 💥[Feature] Upgrade to redwood (by @dawoudsheraz)
- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)
- 💥[Feature] Upgrade the deprecated [edx-app-android](https://github.com/openedx-unsupported/edx-app-android) to [openedx-app-android](https://github.com/openedx/openedx-app-android). (by @hamza-56)
- [Feature] Update the tutor.yaml configuration to align with the new app’s default settings. See the default configuration here: [default_config/prod/config.yaml](https://github.com/openedx/openedx-app-android/blob/main/default_config/prod/config.yaml) (by @cmltawt0).
- [Feature] Enhanced `ANDROID_APP_VERSION` logic to dynamically set the version based on `OPENEDX_COMMON_VERSION`: for nightly builds, `ANDROID_APP_VERSION` is set to main. For other builds, `ANDROID_APP_VERSION` is set to the value of `OPENEDX_COMMON_VERSION`. (by @hamza-56)


<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-09)

- 💥 [Feature] Upgrade to Quince (by @muhammadali286).
    - The nightly branch will now build the master branch of the edx-app-android repository. (by @regisb)
- [Improvement] Added Typing to code, Makefile and test action to the repository and formatted code with Black and isort. (by @CodeWithEmad)

<a id='changelog-16.0.0'></a>
## v16.0.0 (2023-06-14)

- 💥[Feature] Upgrade to Palm. (by @regisb)
- [Improvement] Add a scriv-compliant changelog. (by @regisb)

