#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging
import os
import uuid
from fnmatch import fnmatchcase

import attr
from commoncode import filetype
from commoncode.datautils import Boolean
from commoncode.datautils import Date
from commoncode.datautils import Integer
from commoncode.datautils import List
from commoncode.datautils import Mapping
from commoncode.datautils import String
from commoncode.datautils import choices
from commoncode.fileutils import as_posixpath
from packageurl import PackageURL
from packageurl import normalize_qualifiers

"""
Originally vendored from scancode-toolkit packagedcode.models

This module contain data models for package and dependencies, abstracting and
normalizing the small differences that exist across different package types
(aka. ecosystems), manifest file formats and tools.

A package is a unit of code that is provisioned and installable. More commonly a
package is stored in an archive and found in a package repository, though it can
be as simple as a single file such as a script or may be stored in a VCS
repository such as git.

A package contains:

 - package information and metadata in some "manifest" file,
 - a payload such as code, documentation, or data.


Structured package information come in three primary kinds:

- "metadata" such as a name, version or description,

- "dependencies" on other packages either potential with version requirements or
  resolved and locked with concrete versions), and

- "build" and packaging scripts and instructions.

Package types combine these in one or more manifest or script that we
collectively call datafiles. For instance a Maven POM XML file contains combined
metadata, dependencies and build instructions in an XML file while a pip
requirements.txt file contains only dependencies.

These package "data" files come in many different shapes:

- Manifest files proper such as a Maven POM, NPM package.json and several others.
- Dependency lockfiles such as pip requirements.txt or Go go.sum.
- Build scripts such as Makefile.
- Various structured or semi-structured metadata files in JSON, YAML or plain text
- Property files that supplement manifests such as a pom.properties
- Structured data headers or sections in binaries such as in an ELF, LKM or
  Windows PE; or the header of an RPM archive.
- Code tags or conventional variables such JavaDoc tags or Python __copyright__
  magic variables and variable in Yocto/Bitbake.
- In JSON datafiles (or similar) fetched from registry or package repository APIs.

We handle package information at two levels:

- First, we parse manifests or lockfiles in a common package data model.

- Second, we assemble lists of top-level Package and Dependency by aggregating
  the data from one or more parsed package datafiles.

The key models defined here are:

- PackageData: a class holding package data as parsed from a package datafile
  such as a manifest or lockfile.

- Package: a class for a top level package instance  with a UUID.
- Dependency: class used for a top level dependency instance with a UUID

- DatafileHandler: a base class for datafile handlers. Each handler can parse()
  manifest file format in PackageData and can optionally assemble() packages and
  dependencies. When implementing a new package type and manifest file format,
  subclass DatafileHandler and implement the parse() and assemble() methods for
  this package datafile format and package type. Then register this class in
  ``packagedcode.APPLICATION_PACKAGE_DATAFILE_HANDLERS`` if this is an
  application package or ``packagedcode.SYSTEM_PACKAGE_DATAFILE_HANDLERS`` if
  this is a system package.


Beyond these we have a few secondary models:

- ModelMixin: the base mixin for all models with generic creation and
  serialization to a dict methods.

- Party, DependentPackage, FileReference: lists of these objects used in PackageData

- IdentifiablePackageData: a base class for a Package-like class with a Package URL.
"""

SCANCODE_DEBUG_PACKAGE_API = os.environ.get("SCANCODE_DEBUG_PACKAGE_API", False)

TRACE = SCANCODE_DEBUG_PACKAGE_API
TRACE_UPDATE = SCANCODE_DEBUG_PACKAGE_API


def logger_debug(*args):
    pass


logger = logging.getLogger(__name__)

if TRACE or TRACE_UPDATE:
    import sys

    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(" ".join(isinstance(a, str) and a or repr(a) for a in args))


class ModelMixin:
    """
    Base mixin for all package models.
    """

    def to_dict(self, **kwargs):
        """
        Return a mapping of primitive Python types.
        """
        return attr.asdict(self)

    def to_tuple(self, **kwargs):
        """
        Return a hashable tuple of primitive Python types.
        """
        return to_tuple(self.to_dict(**kwargs))

    @classmethod
    def from_dict(cls, mapping):
        """
        Return an object built from ``kwargs`` mapping. Always ignore unknown
        attributes provided in ``kwargs`` that do not exist as declared attributes
        in the ``cls`` class.
        """
        known_attr = attr.fields_dict(cls)
        kwargs = {k: v for k, v in mapping.items() if k in known_attr}
        return cls(**kwargs)


def to_tuple(collection):
    """
    Return a tuple of basic Python values by recursively converting a mapping
    and all its sub-mappings.
    For example::
    >>> to_tuple({7: [1,2,3], 9: {1: [2,6,8]}})
    ((7, (1, 2, 3)), (9, ((1, (2, 6, 8)),)))
    """
    if isinstance(collection, dict):
        collection = tuple(collection.items())
    assert isinstance(collection, (tuple, list))
    results = []
    for item in collection:
        if isinstance(item, (list, tuple, dict)):
            results.append(to_tuple(item))
        else:
            results.append(item)
    return tuple(results)


party_person = "person"
# often loosely defined
party_project = "project"
# more formally defined
party_org = "organization"
PARTY_TYPES = (
    None,
    party_person,
    party_project,
    party_org,
)


@attr.attributes(slots=True)
class Party(ModelMixin):
    """
    A party is a person, project or organization related to a package.
    """

    type = String(
        repr=True,
        validator=choices(PARTY_TYPES),
        label="party type",
        help="the type of this party: One of: " + ", ".join(p for p in PARTY_TYPES if p),
    )

    role = String(
        repr=True,
        label="party role",
        help="A role for this party. Something such as author, "
        "maintainer, contributor, owner, packager, distributor, "
        "vendor, developer, owner, etc.",
    )

    name = String(repr=True, label="name", help="Name of this party.")

    email = String(repr=True, label="email", help="Email for this party.")

    url = String(repr=True, label="url", help="URL to a primary web page for this party.")


@attr.attributes(slots=True)
class IdentifiablePackageData(ModelMixin):
    """
    Identifiable package data object using purl as identifying attribute as
    specified here https://github.com/package-url/purl-spec.
    This base class is used for all package-like objects be they a manifest
    or an actual package instance.
    """

    type = String(
        repr=True,
        label="package type",
        help="A short code to identify what is the type of this "
        "package. For instance gem for a Rubygem, docker for container, "
        "pypi for Python Wheel or Egg, maven for a Maven Jar, "
        "deb for a Debian package, etc.",
    )

    namespace = String(repr=True, label="package namespace", help="Namespace for this package.")

    name = String(repr=True, label="package name", help="Name of the package.")

    version = String(repr=True, label="package version", help="Version of the package as a string.")

    qualifiers = Mapping(
        default=None,
        value_type=str,
        converter=lambda v: normalize_qualifiers(v, encode=False),
        label="package qualifiers",
        help="Mapping of key=value pairs qualifiers for this package",
    )

    subpath = String(
        label="extra package subpath",
        help="Subpath inside a package and relative to the root " "of this package",
    )

    @property
    def purl(self):
        """
        Return a compact Package URL string or None.
        """
        if self.name:
            return PackageURL(
                type=self.type,
                namespace=self.namespace,
                name=self.name,
                version=self.version,
                qualifiers=self.qualifiers,
                subpath=self.subpath,
            ).to_string()

    def set_purl(self, package_url):
        """
        Update this object with the ``package_url`` purl string or PackageURL if
        there is no pre-existing value for a given purl attribute.
        """
        if not package_url:
            return

        if not isinstance(package_url, PackageURL):
            package_url = PackageURL.from_string(package_url)

        for key, value in package_url.to_dict().items():
            self_val = getattr(self, key)
            if not self_val and value:
                setattr(self, attr, value)

    def to_dict(self, **kwargs):
        mapping = super().to_dict(**kwargs)
        mapping["purl"] = self.purl

        if self.qualifiers:
            mapping["qualifiers"] = normalize_qualifiers(
                qualifiers=self.qualifiers,
                encode=False,
            )

        return mapping


@attr.attributes(slots=True)
class DependentPackage(ModelMixin):
    """
    An identifiable dependent package package object.
    """

    purl = String(
        repr=True,
        label="Dependent package URL",
        help="A compact purl package URL. Typically when there is an "
        "unresolved requirement, there is no version. "
        "If the dependency is resolved, the version should be added to "
        "the purl",
    )

    extracted_requirement = String(
        repr=True,
        label="extracted version requirement",
        help="String for the original version requirements and constraints. "
        "Package-type specific and as found originally in a datafile.",
    )

    # ToDo: add `vers` support. See https://github.com/nexB/univers/blob/main/src/univers/version_range.py

    scope = String(
        repr=True,
        label="dependency scope",
        help="The scope of this dependency, such as runtime, install, etc. "
        "This is package-type specific and is the original scope string.",
    )

    is_runtime = Boolean(
        default=True,
        label="is runtime flag",
        help="True if this dependency is a runtime dependency.",
    )

    is_optional = Boolean(
        default=False,
        label="is optional flag",
        help="True if this dependency is an optional dependency",
    )

    is_resolved = Boolean(
        default=False,
        label="is resolved flag",
        help="True if this dependency version requirement has "
        "been resolved and this dependency url points to an "
        "exact version.",
    )

    resolved_package = Mapping(
        label="resolved package data",
        help="A mapping of resolved package data for this dependent package, "
        "either from the datafile or collected from another source. Some "
        "lockfiles for Composer or Cargo contain extra dependency data.",
    )

    # dependencies = List(
    #     item_type="DependentPackage",
    #     label="dependencies",
    #     help="A list of DependentPackage for this package.",
    # )


@attr.attributes(slots=True)
class Dependency(DependentPackage):
    """
    Top-level dependency instance from parsed package data collected from data
    files such as a package manifest or lockfile.
    """

    dependency_uid = String(
        label="Dependency unique id",
        help="A unique identifier for this dependency instance."
        "Consists of the dependency purl with a UUID qualifier.",
    )

    # TODO: should we also repeat the purl here: this may be redundant but this
    # would help avoid lookups
    for_package_uid = String(
        label="A Package unique id",
        help="The unique id of the package instance to which this dependency "
        "file belongs. This is the purl with a uuid qualifier.",
    )

    datafile_path = String(
        label="Path to datafile.",
        help="A POSIX path string to the package datafile that describes this " "dependency.",
    )

    datasource_id = String(
        label="datasource id", help="Datasource identifier for the source of these package data."
    )

    def __attrs_post_init__(self, *args, **kwargs):
        if not self.dependency_uid:
            self.dependency_uid = build_package_uid(self.purl)

    @classmethod
    def from_dependent_package(
        cls,
        dependent_package,
        datafile_path,
        datasource_id,
        package_uid=None,
    ):
        """
        Return a Dependency from a ``dependent_package`` DependentPackage object
        or mapping.
        """
        if isinstance(dependent_package, DependentPackage):
            dependent_package = dependent_package.to_dict()
        else:
            # make a copy
            dependent_package = dict(dependent_package)

        dependent_package["datafile_path"] = datafile_path
        dependent_package["datasource_id"] = datasource_id
        dependent_package["for_package_uid"] = package_uid

        return cls.from_dict(dependent_package)

    @classmethod
    def from_dependent_packages(
        cls,
        dependent_packages,
        datafile_path,
        datasource_id,
        package_uid=None,
    ):
        """
        Yield Dependency objects from a ``dependent_packages`` list of
        DependentPackage object or mappings found in the ``datafile_path`` with
        ``datasource_id`` for the ``package_uid``.
        """
        dependent_packages = dependent_packages or []
        for dependent_package in dependent_packages:
            if dependent_package.purl:
                yield Dependency.from_dependent_package(
                    dependent_package=dependent_package,
                    datafile_path=datafile_path,
                    datasource_id=datasource_id,
                    package_uid=package_uid,
                )
            else:
                if TRACE:
                    logger_debug(
                        f" Dependency.from_dependent_packages: dependent_package (does not have purl): {dependent_package}"
                    )
                pass


@attr.attributes(slots=True)
class FileReference(ModelMixin):
    """
    A reference to a file in a files listing from a manifest or data file.
    """

    path = String(
        label="Path of this file.",
        help="The file or directory POSIX path. The actual root for this path "
        "is specific to a datafile format. For instance it is the rootfs "
        "root for Linux system packages.",
        repr=True,
    )

    size = Integer(
        label="file size",
        help="size of the file in bytes",
        repr=False,
    )

    sha1 = String(
        label="SHA1 checksum",
        help="SHA1 checksum for this file in hexadecimal",
        repr=False,
    )

    md5 = String(
        label="MD5 checksum",
        help="MD5 checksum for this file in hexadecimal",
        repr=False,
    )

    sha256 = String(
        label="SHA256 checksum",
        help="SHA256 checksum for this file in hexadecimal",
        repr=False,
    )

    sha512 = String(
        label="SHA512 checksum",
        help="SHA512 checksum for this file in hexadecimal",
        repr=False,
    )

    extra_data = Mapping(
        label="extra data",
        help="A mapping of arbitrary extra file reference data.",
    )

    def update(self, other):
        """
        Update this reference with an other file reference only for non-empty
        values.
        """
        for name, value in other.to_dict().items():
            if not value:
                continue
            current = getattr(self, name, None)
            if not current:
                setattr(self, name, value)
        return self


@attr.attributes(slots=True)
class PackageData(IdentifiablePackageData):
    """
    The data of a given package type. This is the core model to store normalized
    package data parsed from package datafiles (such as a manifest) or stored in
    a top-level package.
    """

    primary_language = String(
        label="Primary programming language",
        help="Primary programming language",
    )

    description = String(
        label="Description",
        help="Description for this package. "
        "By convention the first should be a summary when available.",
    )

    release_date = Date(label="release date", help="Release date of the package")

    parties = List(
        item_type=Party,
        label="parties",
        help="A list of parties such as a person, project or organization.",
    )

    keywords = List(item_type=str, label="keywords", help="A list of keywords.")

    homepage_url = String(label="homepage URL", help="URL to the homepage for this package.")

    download_url = String(label="Download URL", help="A direct download URL.")

    size = Integer(
        default=None, label="download size", help="size of the package download in bytes"
    )

    sha1 = String(
        label="SHA1 checksum", help="SHA1 checksum for this package download in hexadecimal"
    )

    md5 = String(label="MD5 checksum", help="MD5 checksum for this package download in hexadecimal")

    sha256 = String(
        label="SHA256 checksum", help="SHA256 checksum for this package download in hexadecimal"
    )

    sha512 = String(
        label="SHA512 checksum", help="SHA512 checksum for this package download in hexadecimal"
    )

    bug_tracking_url = String(
        label="bug tracking URL", help="URL to the issue or bug tracker for this package"
    )

    code_view_url = String(label="code view URL", help="a URL where the code can be browsed online")

    vcs_url = String(
        help="a URL to the VCS repository in the SPDX form of: "
        "https://github.com/nexb/scancode-toolkit.git@405aaa4b3 "
        'See SPDX specification "Package Download Location" '
        "at https://spdx.org/spdx-specification-21-web-version#h.49x2ik5 "
    )

    copyright = String(
        label="Copyright", help="Copyright statements for this package. Typically one per line."
    )

    license_expression = String(
        label="license expression",
        help="The license expression for this package typically derived "
        "from its declared license or from some other type-specific "
        "routine or convention.",
    )

    declared_license = String(
        label="declared license",
        help="The declared license mention, tag or text as found in a "
        "package manifest. This can be a string, a list or dict of "
        "strings possibly nested, as found originally in the manifest.",
    )

    notice_text = String(label="notice text", help="A notice text for this package.")

    source_packages = List(
        item_type=str,
        label="List of related source code package purls",
        help='A list of related  source code Package URLs (aka. "purl") for '
        'this package. For instance an SRPM is the "source package" for a '
        "binary RPM.",
    )

    file_references = List(
        item_type=FileReference,
        label="referenced files",
        help="List of file paths and details for files referenced in a package "
        "manifest. These may not actually exist on the filesystem. "
        "The exact semantics and base of these paths is specific to a "
        "package type or datafile format.",
    )

    extra_data = Mapping(
        label="extra data",
        help="A mapping of arbitrary extra package data.",
    )

    dependencies = List(
        item_type=DependentPackage,
        label="dependencies",
        help="A list of DependentPackage for this package.",
    )

    repository_homepage_url = String(
        label="package repository homepage URL.",
        help="URL to the page for this package in its package repository. "
        "This is typically different from the package homepage URL proper.",
    )

    repository_download_url = String(
        label="package repository download URL.",
        help="download URL to download the actual archive of code of this "
        "package in its package repository. "
        "This may be different from the actual download URL.",
    )

    api_data_url = String(
        label="package repository API URL.",
        help="API URL to obtain structured data for this package such as the "
        "URL to a JSON or XML api its package repository.",
    )

    datasource_id = String(
        label="datasource id",
        help="Datasource identifier for the source of these package data.",
        repr=True,
    )

    def to_dict(self, with_details=True, **kwargs):
        mapping = super().to_dict(with_details=with_details, **kwargs)
        if not with_details:
            # these are not used in the Package subclass
            mapping.pop("file_references", None)
            mapping.pop("dependencies", None)
            mapping.pop("datasource_id", None)

        return mapping

    @classmethod
    def from_dict(cls, mapping):
        """
        Return an instance of PackageData built from a ``mapping`` native Python
        data. Known attributes that store a list of objects are also
        "rehydrated" (such as models.Party).

        Unknown attributes provided in ``mapping`` that do not exist as fields
        in the class are kept as items in the extra_data mapping. An Exception
        is raised if an "unknown attribute" name already exists as an extra_data
        name.
        """
        # TODO: consider using a proper library for this such as cattrs,
        # marshmallow, etc. or use the field type that we declare.

        # Each of these are lists of class instances tracked here, which are stored
        # as a list of mappings in scanc_data

        # these are computed attributes serialized on a package
        # that should not be recreated when de-serializing
        computed_attributes = set(
            [
                "purl",
            ]
        )

        fields_by_name = attr.fields_dict(cls)

        extra_data = mapping.get("extra_data", {}) or {}
        package_data = {}

        list_fields_by_item = {
            "parties": Party,
            "dependencies": DependentPackage,
            "file_references": FileReference,
        }

        for name, value in mapping.items():
            if not value:
                continue

            if name in computed_attributes:
                continue

            field = fields_by_name.get(name)
            if not field:
                # keep unknown fields as extra data
                if name not in extra_data:
                    extra_data[name] = value
                    continue
                else:
                    raise Exception(
                        f'Invalid package "scan_data" with duplicated name: {name!r}={value!r} '
                        f"present both as attribute AND as extra_data: {name!r}={extra_data[name]!r}"
                    )

            # re-hydrate lists of typed objects
            list_item_type = is_list_field = list_fields_by_item.get(name)

            if is_list_field:
                items = list(_rehydrate_list(cls=list_item_type, values=value))
                package_data[name] = items
            else:
                # this is a plain, non-nested field
                package_data[name] = value

        return super().from_dict(package_data)


def _rehydrate_list(cls, values):
    """
    Yield ``cls`` objects built from a ``values`` list of mappings.
    """
    # Since we have a list_item_type, value must be a list of mappings:
    # we transform it in a list of objects.
    base_msg = 'Invalid package "scan_data "with unknown data structure.'
    if not isinstance(values, list) and not all(isinstance(v, dict) for v in values):
        raise Exception(
            f"{base_msg}. Expected the value to be a list of dicts and not: "
            f"{type(values)!r} for class: {cls!r}"
        )

    for val in values:
        yield cls.from_dict(val)


class DatafileHandler:
    """
    A base handler class to handle any package manifests, lockfiles and data
    files. Each subclass handles a package datafile format to parse datafiles
    and assemble Package and Depdencies from these:

    - parses a datafile format and yields package data.

    - assembles this datafile package data in top-level packages and dependencies
    - assigns package files to their package
    """

    # A string to uniquely identify the datasource of this parser. Every parser
    # must fill this with a unique and descriptive string if (unique ignoring
    # case). Must be a valid Python identifier: must start with an ASCII letter,
    # can only contain ASCII letters, digits and underscore. Must be lowercase
    datasource_id = None

    # Sequence of known fnmatch-style case-insensitive glob patterns (e.g., Unix
    # shell style patterns) that apply on the whole POSIX path for package
    # datafiles recognized and parsed by this parser. See fnmatch.fnmatch().
    # *       matches everything
    # ?       matches any single character
    # Used by the default is_datafile() method. If not using this, a subclass
    # must override is_datafile()
    path_patterns = tuple()

    # Sequence of file types fragments: one of these must be contained in the
    # resource filetype
    filetypes = tuple()

    # Informational: Default package type for this parser. Some parsers may
    # yield more than one package type
    default_package_type = None

    # Informational: Default primary language for this parser.
    default_primary_language = None

    # Informational: Description of this parser
    description = None

    # Informational: URL that documents this file format
    documentation_url = None

    @classmethod
    def is_datafile(cls, location, filetypes=tuple(), _bare_filename=False):
        """
        Return True if the file at ``location`` is likely a package data file
        that this parser can handle. This implementation is based on:

        - matching the ``location`` as a whole with any one of the
          ``path_patterns`` sequence of patterns defined as a class attributes.
          The path patterns are for POSIX paths.

        - if defined, ensuring that the filetype of the file at ``location``
          contains any of the type listed in the ``filetypes`` class attribute.

        - ``_bare_filename`` is for testing using a bare path that does not
        point to real files.
        Subclasses can override to implement more complex data file recognition.
        """
        if filetype.is_file(location) or _bare_filename:
            loc = as_posixpath(location)
            if any(fnmatchcase(loc, pat) for pat in cls.path_patterns):
                filetypes = filetypes or cls.filetypes
                if not filetypes:
                    return True
        return False

    @classmethod
    def parse(cls, location):
        """
        Yield one or more PackageData objects given a package data file at
        ``location``.

        Subclasses must implement and are responsible for returning proper
        computed license fields and list of resources and files.
        """
        raise NotImplementedError


def build_package_uid(purl):
    """
    Return a purl string with a UUID qualifier given a ``purl`` string .
    """
    purl = PackageURL.from_string(purl)
    purl.qualifiers["uuid"] = str(uuid.uuid4())
    return str(purl)


def build_purl(mapping):
    """
    Return a PackageURL from a ``mapping`` or None if essential type and name
    fields are missing.
    """
    ptype = mapping.get("type")
    name = mapping.get("name")
    if not ptype or not name:
        return

    namespace = mapping.get("namespace")
    version = mapping.get("version")
    qualifiers = mapping.get("qualifiers") or {}
    subpath = mapping.get("subpath")
    return PackageURL(
        type=ptype,
        name=name,
        namespace=namespace,
        version=version,
        qualifiers=qualifiers,
        subpath=subpath,
    )


@attr.attributes(slots=True)
class Package(PackageData):
    """
    Top-level package instance assembled from parsed package data collected
    from one or more data files such as manifests or lockfiles.
    """

    package_uid = String(
        label="Package unique id",
        help="A unique identifier for this package instance."
        "Consists of the package purl with a UUID qualifier.",
    )

    datafile_paths = List(
        item_type=str,
        label="List of datafile paths",
        help="List of datafile paths used to create this package.",
    )

    datasource_ids = List(
        item_type=str,
        label="datasource ids",
        help="List of the datasource ids used to create this package.",
    )

    def __attrs_post_init__(self, *args, **kwargs):
        if not self.package_uid:
            self.package_uid = build_package_uid(self.purl)

    def to_dict(self):
        return super().to_dict(with_details=False)

    @classmethod
    def from_package_data(cls, package_data, datafile_path):
        """
        Return a Package from a ``package_data`` PackageData object
        or mapping. Or None.
        """
        if isinstance(package_data, PackageData):
            package_data_mapping = package_data.to_dict()
            dsid = package_data.datasource_id
        elif isinstance(package_data, dict):
            # make a copy
            package_data_mapping = dict(package_data.items())
            dsid = package_data["datasource_id"]
        elif package_data:
            raise Exception(f"Invalid type: {package_data!r}", package_data)

        package_data_mapping["datafile_paths"] = [datafile_path]
        package_data_mapping["datasource_ids"] = [dsid]

        return cls.from_dict(package_data_mapping)

    @classmethod
    def from_dict(cls, mapping):
        """
        Return an instance of Package built from a ``mapping`` of native Python
        data, typically a PackageData-like ``mapping``. Return None if there are
        not enough data to form a PackageURL from this data.

        See PackageData.from_dict() for other details.
        """
        if build_purl(mapping):
            return super().from_dict(mapping)

    def is_compatible(self, package_data, include_qualifiers=True):
        """
        Return True if the ``package_data`` PackageData is compatible with
        this Package, e.g. it is about the same package.
        """
        return (
            self.type == package_data.type
            and self.namespace == package_data.namespace
            and self.name == package_data.name
            and self.version == package_data.version
            and (include_qualifiers and self.qualifiers == package_data.qualifiers)
            and self.subpath == package_data.subpath
            and self.primary_language == package_data.primary_language
        )

    def update(self, package_data, datafile_path, replace=False):
        """
        Update this Package with data from the ``package_data`` PackageData.

        If a field does not have a value and the ``package_data`` field has a
        value, set this package field to the ``package_data`` field value.

        If there is a value on both side, update the value according to the
        ``replace`` flag.

        If ``replace`` is True, replace a value with the ``package_data`` value.
        Otherwise existing, non-empty values are left unchanged.

        List of values are merged, keeping the original order and avoiding duplicates.

        Return True if update is successful.

        Return False if there is a type, name or version mismatch between this
        package and the provided ``package_data``
        """
        if not package_data:
            return

        if isinstance(package_data, dict):
            package_data = PackageData.from_dict(package_data)

        if not self.is_compatible(package_data, include_qualifiers=False):
            if TRACE_UPDATE:
                logger_debug(f"update: {self.purl} not compatible with: {package_data.purl}")
            return False

        # always append these new items
        self.datasource_ids.append(package_data.datasource_id)
        self.datafile_paths.append(datafile_path)

        existing = self.to_package_data().to_dict()
        new_package_data = package_data.to_dict()

        # update for these means combining lists of items from both sides
        list_fields = set(
            [
                "parties",
                "dependencies",
                "file_references",
            ]
        )

        for name, value in existing.items():
            new_value = new_package_data.get(name)

            if TRACE_UPDATE:
                logger_debug(f"update: {name!r}={value!r} with new_value: {new_value!r}")

            if not new_value:
                if TRACE_UPDATE:
                    logger_debug("  No new value: skipping")
                continue

            if not value:
                if TRACE_UPDATE:
                    logger_debug("  set existing value to new")
                setattr(self, name, new_value)
                continue

            if replace:
                if TRACE_UPDATE:
                    logger_debug("  replace existing value to new")
                setattr(self, name, new_value)
                continue

            # here we do not replace... but we still merge lists/mappings
            if name == "extra_data":
                value.update(new_value)

            if name in list_fields:
                if TRACE_UPDATE:
                    logger_debug("  merge lists of values")
                merged = merge_sequences(list1=value, list2=new_value)
                setattr(self, name, merged)

            elif TRACE_UPDATE and value != new_value:
                if TRACE_UPDATE:
                    logger_debug("  skipping update: no replace")

        return True


def merge_sequences(list1, list2, **kwargs):
    """
    Return a new list of model objects merging the lists ``list1`` and
    ``list2`` keeping the original ``list1`` order and discarding
    duplicates.
    """
    list1 = list1 or []
    list2 = list2 or []
    merged = []
    existing = set()
    for item in list1 + list2:
        key = item.to_tuple(**kwargs)
        if not key in existing:
            merged.append(item)
            existing.add(key)
    return merged
