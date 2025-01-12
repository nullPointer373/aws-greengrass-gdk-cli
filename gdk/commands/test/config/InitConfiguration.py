import semver
from gdk.common.config.GDKProject import GDKProject
import logging
import requests


class InitConfiguration(GDKProject):
    def __init__(self, _args) -> None:
        super().__init__()
        self._args = _args
        self._otf_releases_url = "https://github.com/aws-greengrass/aws-greengrass-testing/releases"
        self.otf_version = self._get_otf_version()

    def _get_otf_version(self):
        _version_arg = self._args.get("otf_version", None)
        if _version_arg:
            logging.info("Using the OTF version provided in the command %s", _version_arg)
            return self._validated_otf_version(_version_arg)
        logging.info("Using the OTF version provided in the GDK test config %s", self.test_config.otf_version)
        return self._validated_otf_version(self.test_config.otf_version)

    def _validated_otf_version(self, version) -> str:
        _version = version.strip()

        if not _version:
            raise ValueError(
                "OTF version cannot be empty. Please specify a valid OTF version in the GDK config or in the command argument."
            )

        if not semver.Version.is_valid(_version):
            raise ValueError(
                f"OTF version {_version} is not a valid semver. Please specify a valid OTF version in the GDK config or in"
                " the command argument."
            )

        if not self._otf_version_exists(_version):
            raise ValueError(
                f"The specified Open Test Framework (OTF) version '{_version}' does not exist. Please"
                f" provide a valid OTF version from the releases here: {self._otf_releases_url}"
            )

        return _version

    def _otf_version_exists(self, _version) -> bool:
        _testing_jar_url = "https://github.com/aws-greengrass/aws-greengrass-testing/releases/tag/v" + _version
        head_response = requests.head(_testing_jar_url, timeout=10)
        return head_response.status_code == 200
