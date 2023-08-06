import datetime
import re

class AbstractInfo:
    def __init__(self) -> None:
        self.name = ""
        self.author = ""
        self.company = ""
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.ar_major = 0
        self.ar_minor = 0
        self.ar_patch = 0
        self.year = datetime.datetime.now().strftime("%Y")
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    @property
    def eb_version(self) -> str:
        if (self.major == 0 and self.minor == 0 and self.patch == 0):
            raise ValueError("Invalid EB version (%d.%d.%d)" % (self.major, self.minor, self.patch))
        return "TxDxM%dI%dR%d" % (self.major, self.minor, self.patch)

    @property
    def ar_version(self) -> str:
        if (self.ar_major == 0 and self.ar_minor == 0 and self.ar_patch == 0):
            raise ValueError("Invalid AR version (%d.%d.%d)" % (self.ar_major, self.ar_minor, self.ar_patch))
        return "%d.%d.%d" % (self.ar_major, self.ar_minor, self.ar_patch)

    @property
    def root_path(self) -> str:
        if (self.name == ""):
            raise ValueError("Invalid Plugin Name (%s)" % (self.name))
        return "%s_TS_%s" % (self.name, self.eb_version)

    @property
    def uppercase_name(self) -> str:
        return self.name.upper()

    def _parse_version(self, version):
        m = re.match(r'^(\d+)\.(\d+).(\d+)$', version)
        if (m):
            return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        else:
            raise ValueError("Invalid version %s" % version)

    def _parse_toml_data(self, data):
        self.name = data['component']['name']
        self.author = data['component']['author']
        self.company = data['component']['company']
        (self.major, self.minor, self.patch) = self._parse_version(data['component']['version'])
        (self.ar_major, self.ar_minor, self.ar_patch) = self._parse_version(data['component']['ar_version'])

    def dump(self):
        print("Name           : %s" % self.name)
        print("Version        : %d.%d.%d" % (self.major, self.minor, self.patch))
        print("AUTOAR Version : %d.%d.%d" % (self.ar_major, self.ar_minor, self.ar_patch))