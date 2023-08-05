import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post161"
version_tuple = (0, 4, 0, 161)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post161")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post19"
data_version_tuple = (0, 4, 0, 19)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post19")
except ImportError:
    pass
data_git_hash = "e36832a5de2f05077829d82c8a3f1181b73ae0af"
data_git_describe = "0.4.0-19-ge36832a5"
data_git_msg = """\
commit e36832a5de2f05077829d82c8a3f1181b73ae0af
Merge: d5ed77f7 84e32533
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Jun 14 12:42:45 2022 +0200

    Merge pull request #583 from Silabs-ArjanB/ArjanB_ctrl6b
    
    Changed reset value of tdata1. Removed reset values for mcontrol6 and…

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
