###############################################################################
# Copyright (C) 2021 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################
import ctypes
import os
import subprocess
import sys

def _call_lib_api_ret_char(api_call):
    api_call.restype = ctypes.c_char_p
    api_call.argtypes = []
    return api_call().decode("utf-8")


def _call_lib_api_ret_int(api_call):
    api_call.restype = ctypes.c_int
    api_call.argtypes = []
    return api_call()


def _read_version_info(lib_to_read_version_info):
    import tensorflow # habana_device requires tf libs to be loaded in the process, hence import
    lib = ctypes.cdll.LoadLibrary(lib_to_read_version_info)
    retVal = ",".join([_call_lib_api_ret_char(lib.VERSION),
                       _call_lib_api_ret_char(lib.VERSION_HASH),
                       _call_lib_api_ret_char(lib.BUILD_DATE),
                       _call_lib_api_ret_char(lib.VERSION_TF)])
    retVal += ",dirty" if _call_lib_api_ret_int(lib.BUILD_DIRTY) == 1 else ""
    print(retVal, end="")


def get_version_dict(lib_to_read_version_info):
    # inception warning: calling this script in a subprocess to avoid loading habana_device in main process
    env = dict(os.environ)
    # suppress all INFO logs comming from TF
    env['TF_CPP_MIN_LOG_LEVEL'] = "10"
    output = subprocess.check_output(
        [sys.executable, __file__, lib_to_read_version_info], env=env, encoding="ascii")
    output = output.split(",")
    out_dict = {"VERSION": output[0], "VERSION_HASH": output[1],
                "BUILD_DATE": output[2], "VERSION_TF": output[3]}
    if len(output) == 5:
        out_dict["BUILD_DIRTY"] = output[4]
    return out_dict


def concat_version_dict(version_dict):
    out = "_".join([version_dict["VERSION"], version_dict["VERSION_HASH"],
                   version_dict["BUILD_DATE"], version_dict["VERSION_TF"]])
    if "BUILD_DIRTY" in version_dict:
        out += "_dirty"
    return out


if __name__ == '__main__':
    _read_version_info(str(sys.argv[1]))
