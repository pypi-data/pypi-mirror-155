import getopt
import sys

from ..models.plugin_folder_mgr import eb_plugin_create

def _usage(error: str):
    if error != "":
        print(error)
    print("eb_plugin [-c|--cfg name][-h|-help]")
    print("Create EB Plugin folder structure")
    print("   -c|--cfg name : The TOML configure file name")
    print("   -h            : Show the help information.")
    sys.exit(2)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hc:", ["help", "cfg"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        _usage("")

    cfg_name = ""
    for o, arg in opts:
        if o in ("-c", "--cfg"):
            cfg_name = arg
        elif o in ("-h", "--help"):
            _usage("")
        else:
            assert False, "unhandled option"

    if cfg_name == "":
        _usage("Please enter the TOML configure file name")

    try:
        eb_plugin_create(cfg_name)
    except Exception as e:
        # print(e)
        raise (e)


if __name__ == "__main__":
    main()
