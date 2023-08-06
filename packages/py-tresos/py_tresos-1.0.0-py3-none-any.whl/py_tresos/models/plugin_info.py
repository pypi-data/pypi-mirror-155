import toml
import sys

from .abstract_info import AbstractInfo

class PluginInfo(AbstractInfo):
    def __init__(self) -> None:
        super().__init__()
        self.tresos_root = ""
        self.header_files = []
        self.source_files = []
        self.gen_header_files = []
        self.gen_source_files = []
        self.header_file_tpl = ""
        self.source_file_tpl = ""
        self.ar_package = ""
        self.vendor_id = "0x0000"

    @property
    def gen_files_text(self) -> str:
        lines = []
        for name in self.gen_header_files:
            lines.append("\t$(%s_OUTPUT_PATH)/include/%s" % (self.name, name))
        for name in self.gen_source_files:
            lines.append("\t$(%s_OUTPUT_PATH)/src/%s" % (self.name, name))
        
        return " \\\n".join(lines)

    @property
    def src_files_text(self) -> str:
        lines = []
        #for name in self.header_files:
        #    lines.append("\t$(%s_CORE_PATH)/include/%s" % (self.name, name))
        for name in self.source_files:
            lines.append("\t$(%s_CORE_PATH)/src/%s" % (self.name, name))
        
        return " \\\n".join(lines)

    def _parse_toml_data(self, data):
        super()._parse_toml_data(data)
        self.tresos_root = data['component']['tresos_root']
        for file in data['component']['header_files']:
            self.header_files.append(file)
        for file in data['component']['source_files']:
            self.source_files.append(file)
        for file in data['component']['gen_header_files']:
            self.gen_header_files.append(file)
        for file in data['component']['gen_source_files']:
            self.gen_source_files.append(file)
        self.ar_package = data['component']['ar_package']
        self.vendor_id = data['component']['vendor_id']
        if 'template' in data:
            if 'source_file' in data['template']:
                self.source_file_tpl = data['template']['source_file']
            if 'header_file' in data['template']:
                self.header_file_tpl = data['template']['header_file']
        

        #self.dump()

    def parse(self, filename):
        parsed_toml = toml.load(filename)
        self._parse_toml_data(parsed_toml)

    def dump(self):
        super().dump()

        print("Header Files:")
        for name in self.header_files:
            print("  %s" % name)
        print("  -- cfg --")
        for name in self.gen_header_files:
            print("  %s" % name)

        print("Source Files:")
        for name in self.source_files:
            print("  %s" % name)
        print("  -- cfg --")
        for name in self.gen_source_files:
            print("  %s" % name)

        print("Source File Template:")
        print("  %s" % self.source_file_tpl)

        print("Header File Template:")
        print("  %s" % self.header_file_tpl)

        sys.exit(2)