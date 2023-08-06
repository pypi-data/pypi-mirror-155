import os
import os.path
import sys

from shutil import copyfile
from string import Template

from .abstract_folder_mgr import Templatelternative
from .plugin_info import PluginInfo

plugin_tpl_path = '/../../tpls/plugin'

def _copy_file(src, dst, local_tpl: bool = True):
    if os.path.exists(dst):
        print("<%s> exists and skipped" % dst)
        return

    if (local_tpl):
        root_path = os.path.abspath(__file__ + plugin_tpl_path)
        copyfile(os.path.realpath(root_path + "/" + src), dst)
    else:
        copyfile(src, dst)


def _generate_config_file(src, dst, info: PluginInfo, delimiter="#"):
    if os.path.exists(dst):
        print("<%s> exists and skipped" % dst)
        return

    print("Generate <%s>" % dst)

    root_path = os.path.abspath(__file__ + plugin_tpl_path)

    with open(root_path + "/" + src) as f_in:
        content = f_in.read()

    if delimiter == "#":
        t = Templatelternative(content)
    else:
        t = Template(content)
    #if (date_time == ""):
    #    new_content = t.substitute(COMPONENT=component, VERSION=version)
    #else:
    new_content = t.substitute(
        COMPONENT = info.name, 
        VERSION = info.eb_version, 
        YEAR = info.year,
        AUTHOR = info.author,
        COMPANY = info.company,
        MAJOR = info.major, 
        MINOR = info.minor,
        PATCH = info.patch,
        AR_MAJOR = info.ar_major,
        AR_MINOR = info.ar_minor,
        AR_PATCH = info.ar_patch,
        AR_PACKAGE = info.ar_package,
        VENDOR_ID = info.vendor_id,
        DATE_TIME = info.date_time, 
        TRESOS_ROOT = info.tresos_root, 
        GEN_FILES_TEXT = info.gen_files_text,
        SRC_FILES_TEXT = info.src_files_text
    )

    with open(dst, 'w') as f_out:
        f_out.write(new_content)

def _generate_plugin_file(src, dst, info: PluginInfo):
    if os.path.exists(dst):
        print("<%s> exists and skipped" % dst)
        return

    print("Generate <%s>" % dst)

    root_path = os.path.abspath(__file__ + plugin_tpl_path)

    with open(root_path + "/" + src) as f_in:
        content = f_in.read()

    t = Templatelternative(content)
    new_content = t.substitute(
        COMPONENT = info.name, 
        VERSION = info.eb_version, 
        YEAR = info.year,
        AUTHOR = info.author,
        COMPANY = info.company,
        MAJOR = info.major, 
        MINOR = info.minor,
        PATCH = info.patch,
        AR_MAJOR = info.ar_major,
        AR_MINOR = info.ar_minor,
        AR_PATCH = info.ar_patch,
        AR_PACKAGE = info.ar_package,
        VENDOR_ID = info.vendor_id
    )

    with open(dst, 'w') as f_out:
        f_out.write(new_content)

def eb_plugin_look_for_template(info: PluginInfo):
    if (info.header_file_tpl != ""):
        if (not os.path.exists(info.header_file_tpl)):
            print("<%s> does not exist." % info.header_file_tpl)
            sys.exit(1)

    if (info.source_file_tpl != ""):
        if (not os.path.exists(info.source_file_tpl)):
            print("<%s> does not exist." % info.source_file_tpl)
            sys.exit(1)

def eb_plugin_create(cfg_file):

    info = PluginInfo()
    info.parse(cfg_file)

    print("Generate %s (%d.%d.%d)" % (info.name, info.major, info.minor, info.patch))

    eb_plugin_look_for_template(info)

    create_folders(root_path = info.root_path)

    _generate_plugin_file('plugin.xml.tpl', '%s/plugin.xml' % info.root_path, info = info)

    _generate_config_file('doc/user_manual.md', '%s/doc/%s_um.md' % (info.root_path, info.name), info = info, delimiter='$')
    _generate_config_file('config/template.xdm.tpl', '%s/config/%s.xdm' % (info.root_path, info.name), info = info)

    _generate_config_file('.project.tpl', '%s/.project' % info.root_path, info = info)
    _generate_config_file("META-INF/MANIFEST.MF.tpl", '%s/META-INF/MANIFEST.MF' % info.root_path,  info = info)
    _generate_config_file("component.ant.tpl",'%s/%s.ant' % (info.root_path, info.name),  info = info)

    _generate_config_file("make/defs.mak", '%s/make/%s_defs.mak' % (info.root_path, info.name), info = info, delimiter='$')
    _generate_config_file("make/rules.mak", '%s/make/%s_rules.mak' % (info.root_path, info.name), info = info, delimiter='$')

    _generate_config_file("generate_swcd/swcd/Bswmd.arxml", '%s/generate_swcd/swcd/%s_Bswmd.arxml' % (info.root_path, info.name), info = info)
    _generate_config_file("generate_swcd/swcd/swc_interface.arxml", '%s/generate_swcd/swcd/%s_swc_interface.arxml' % (info.root_path, info.name), info = info)
    _generate_config_file("generate_swcd/swcd/swc_internal.arxml", '%s/generate_swcd/swcd/%s_swc_internal.arxml' % (info.root_path, info.name), info = info)
    
    _copy_file(".classpath.tpl", '%s/.classpath' % info.root_path)
    _copy_file("build.properties.tpl", '%s/build.properties' % info.root_path)

    for h_file in info.header_files:
        if info.header_file_tpl == "":
            _copy_file("header.h.tpl", "%s/include/%s" % (info.root_path, h_file))
        else:
            _copy_file(info.header_file_tpl, "%s/include/%s" % (info.root_path, h_file), False)

    for c_file in info.source_files:
        if info.source_file_tpl == "":
            _copy_file("source.c.tpl", "%s/src/%s" % (info.root_path, c_file))
        else:
            _copy_file(info.source_file_tpl, "%s/src/%s" % (info.root_path, c_file), False)


def create_folders(root_path):
    os.makedirs(root_path, exist_ok=True)
    os.makedirs(root_path + "/config", exist_ok=True)
    os.makedirs(root_path + "/META-INF", exist_ok=True)
    os.makedirs(root_path + "/doc", exist_ok=True)
    os.makedirs(root_path + "/generate", exist_ok=True)
    os.makedirs(root_path + "/generate/include", exist_ok=True)
    os.makedirs(root_path + "/generate/src", exist_ok=True)
    os.makedirs(root_path + "/generate_swcd", exist_ok=True)
    os.makedirs(root_path + "/generate_swcd/swcd", exist_ok=True)
    os.makedirs(root_path + "/include", exist_ok=True)
    os.makedirs(root_path + "/make", exist_ok=True)
    os.makedirs(root_path + "/src", exist_ok=True)
