from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Iterable, Dict, Iterator, TYPE_CHECKING, Type

from pkm.api.dependencies.dependency import Dependency
from pkm.api.packages.package_installation_info import PackageInstallationInfo
from pkm.api.packages.package_metadata import PackageMetadata
from pkm.api.versions.version import Version, StandardVersion
from pkm.config.configclass import config, config_field, ConfigFile, ConfigFieldCodec, ConfigCodec
from pkm.config.configfiles import INIConfigIO, WheelFileConfigIO, CSVConfigIO
from pkm.utils.commons import UnsupportedOperationException
from pkm.utils.dicts import get_or_compute
from pkm.utils.entrypoints import EntryPoint, ObjectReference
from pkm.utils.files import path_to
from pkm.utils.hashes import HashSignature
from pkm.utils.ipc import IPCPackable
from pkm.utils.iterators import groupby
from pkm.utils.properties import cached_property

if TYPE_CHECKING:
    from pkm.api.packages.package import PackageDescriptor


class DistInfo(IPCPackable):

    def __init__(self, path: Path):
        self.path = path

    def __getstate__(self):
        return [self.path]

    def __setstate__(self, state):
        self.__init__(*state)

    @cached_property
    def package_name_by_dirname(self):
        """
        :return: the package name as can be computed from the dist-info file name. note that if the loaded dist-info
         path has non-standard, the return value of this method is undetermined
        """
        return self.path.name.split("-")[0]

    @cached_property
    def package_version_by_dirname(self):
        """
        :return: the package name as can be computed from the dist-info file name. note that if the loaded dist-info
         path has non-standard, the return value of this method is undetermined
        """
        return Version.parse(self.path.name.split("-")[1])

    def load_wheel_cfg(self) -> "WheelFileConfiguration":
        """
        loads and return the WHEEL configuration file
        :return: the loaded configuration file
        """
        return WheelFileConfiguration.load(self.wheel_path())

    def wheel_path(self) -> Path:
        """
        :return: the path to the WHEEL configuration file
        """
        return self.path / "WHEEL"

    def is_app_container(self) -> bool:
        """
        :return: True if this package dist-info is marked as an app-container
        """
        mode_info = self.load_installation_info()
        return mode_info and mode_info.containerized

    def load_entrypoints_cfg(self) -> "EntrypointsConfiguration":
        """
        load and return the entry_points.txt configurate file
        :return: the loaded configuration file
        """
        return EntrypointsConfiguration.load(self.path / "entry_points.txt")

    def load_installation_info(self) -> Optional[PackageInstallationInfo]:
        if self.installation_info_path().exists():
            return PackageInstallationInfo.load(self.installation_info_path())
        return None

    def save_installation_info(self, installation_mode: PackageInstallationInfo):
        self.installation_info_path().write_text(json.dumps(installation_mode.to_config()))

    def load_metadata_cfg(self) -> "PackageMetadata":
        """
        load and return the METADATA configuration file
        :return: the loaded configuration file
        """
        return PackageMetadata.load(self.metadata_path())

    def metadata_path(self) -> Path:
        """
        :return: the path to the METADATA configuration file
        """
        return self.path / "METADATA"

    def load_record_cfg(self) -> "RecordsFileConfiguration":
        """
        load and return the RECORD configuration file
        :return: the loaded configuration file
        """
        return RecordsFileConfiguration.load(self.record_path())

    def record_path(self) -> Path:
        """
        :return: the path to the RECORD configuration file
        """
        return self.path / "RECORD"

    def license_path(self) -> Path:
        """
        :return: the path to the LICENSE file
        """
        return self.path / "LICENSE"

    def installation_info_path(self) -> Path:
        """
        :return: the path to the pkm's added INSTALLATION_MODE file
        """
        return self.path / "INSTALLATION_MODE"

    def user_requested_path(self) -> Path:
        """
        :return: the path to the REQUESTED marker file
        """
        return self.path / "REQUESTED"

    def mark_as_user_requested(self, info: Dependency):
        """
        marks the given package as a user requested one, pkm will not consider it as an orphan package if no other
        package depends on it
        :param info: information about the user request
        """
        self.user_requested_path().write_text(str(info))

    def unmark_as_user_requested(self):
        """
        remove the "user request" mark from a package, pkm will consider it as an orphan package if no other
        package depends on it
        """
        self.user_requested_path().unlink(missing_ok=True)

    def is_user_requested(self) -> bool:
        """
        :return: True if this package dist-info is marked as user-requested
        """
        return self.user_requested_path().exists()

    def load_user_requested_dependency(self) -> Optional[Dependency]:
        try:
            return Dependency.parse(self.user_requested_path().read_text().strip())
        except:  # noqa
            return None

    @classmethod
    def load(cls, path: Path, non_standard_name_ok: bool = False) -> "DistInfo":
        """
        loads the given `path` as a distinfo
        :param path: the path to load, must be a directory
        :param non_standard_name_ok: if False and the name of the given path is not standard will raise a ValueError
        :return: the loaded distinfo
        """

        if path.exists() and not path.is_dir():
            raise ValueError(f"the given path is not a directory: {path}")

        if path.suffix != '.dist-info' and not non_standard_name_ok:
            raise ValueError(f"{str(path)} is not a properly named dist-info directory")

        return cls(path)

    @classmethod
    def scan(cls, path: Path) -> Iterator[DistInfo]:
        """
        scans a path for all its standard-named dist-info children, load and yield them.
        :param path: the path to scan
        :return: iterator over all the found dist-info children
        """
        for file in path.iterdir():
            if file.suffix == ".dist-info":
                yield DistInfo.load(file)

    @classmethod
    def expected_dir_name(cls, package: "PackageDescriptor") -> str:
        """
        :param package: the package to compute the expected directory name for
        :return: the name of the dist-info directory (last element in the path for the dist-info) that is expected to be
                 created for the given package
        """
        return f"{package.expected_src_package_name}-{str(package.version).replace('-', '_')}.dist-info"

    def installed_files(self) -> Iterator[Path]:
        """
        :return: paths to all the files that were installed to the environment via this package (taken from RECORD)
        """
        root = self.path.parent
        for record in self.load_record_cfg().records:
            file = Path(root, record.file).resolve()
            yield file

        yield self.record_path()


@dataclass
@config(io=INIConfigIO())
class EntrypointsConfiguration(ConfigFile):
    _data = config_field(leftover=True)

    @cached_property
    def entrypoints(self) -> Iterable[EntryPoint]:
        result: List[EntryPoint] = []

        for group_name, group in self._data.items():
            for entry_point, object_ref in group.items():
                result.append(EntryPoint(group_name, entry_point, ObjectReference.parse(object_ref)))

        return result

    @entrypoints.setter
    def entrypoints(self, entrypoints):
        self._data.clear()
        by_group: Dict[str, List[EntryPoint]] = groupby(entrypoints, key=lambda e: e.group)
        new_data = {group: {e.name: e.ref for e in entries} for group, entries in by_group.items()}
        self._data.update(new_data)


@dataclass
@config(io=WheelFileConfigIO())
class WheelFileConfiguration(ConfigFile):
    version: Version = config_field(key='Wheel-Version', default=Version.parse("1.0"))
    generator: str = config_field(key="Generator", default="")
    root_is_purelib: bool = config_field(key="Root-Is-Purelib", default=True)
    _leftovers = config_field(leftover=True)

    def validate_supported_version(self):
        if not isinstance(self.version, StandardVersion):
            raise UnsupportedOperationException(f"unknown wheel version: {self.version}")

        if self.version.release[0] != 1:
            raise UnsupportedOperationException(f"unsupported wheel version: {self.version}")
        if self.version.release[1] != 0:
            print(f'advanced wheel version: {self.version} detected, will be treated as version 1.0')

    @classmethod
    def create(cls, generator: str, purelib: bool):
        return WheelFileConfiguration(Version.parse("1.0"), generator, purelib)


class _RecordHashsignatureCodec(ConfigFieldCodec):

    def parse(self, parent: ConfigCodec, type_: Type, v: str) -> Optional[HashSignature]:
        return None if not v else HashSignature.parse_urlsafe_base64_nopad_encoded(v)

    def unparse(self, parent: ConfigCodec, type_: Type, v: Optional[HashSignature]) -> str:
        return '' if not v else str(v)


@dataclass
@config
class Record:
    file: str
    hash_signature: HashSignature
    length: int

    def absolute_path(self, dist_info: DistInfo) -> Path:
        return (dist_info.path / self.file).resolve()


@config(io=CSVConfigIO(
    "file", "hash_signature", "length",
    codec=ConfigCodec({HashSignature: _RecordHashsignatureCodec()})))
class RecordsFileConfiguration(ConfigFile):
    records: List[Record] = config_field(default_factory=list)

    def sign_files(self, files: Iterable[Path], root: Path,
                   precomputed_hashes: Optional[Dict[str, HashSignature]] = None) -> RecordsFileConfiguration:
        """
        add to the records in this file the signatures for the given `files`

        :param files: the files to sign
        :param root:
            a root directory to sign the files relative to, when signing, the record file path will be writen
            relative to this root
        :param precomputed_hashes:
            dictionary containing some or all of the given files precomputed hashes,
            its key is the relative path from root to each of the files
        :return: self (for chaining support)
        """

        precomputed_hashes = precomputed_hashes or {}
        records: List[Record] = self.records
        for file in files:
            if file.exists():
                if not file.is_dir():
                    path = str(path_to(root, file))

                    hash_sig = get_or_compute(
                        precomputed_hashes, path,
                        lambda: HashSignature.compute_urlsafe_base64_nopad_encoded('sha256', file))

                    records.append(Record(
                        path,
                        hash_sig,
                        file.lstat().st_size  # size
                    ))
            else:
                warnings.warn(f"requiring to sign non existing file - {file}, skipping it")

        return self

    def sign_recursive(self, content_root: Path) -> RecordsFileConfiguration:
        """
        add to the records in this file the signatures for files inside the `content_root`
        :param content_root: the content to sign
               (will recursively sign all files in the content root and add their signature to the created record file)
        :return: self (for chaining support)
        """
        return self.sign_files(content_root.rglob("*"), content_root)
