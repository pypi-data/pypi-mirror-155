import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post165"
version_tuple = (0, 4, 0, 165)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post165")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post23"
data_version_tuple = (0, 4, 0, 23)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post23")
except ImportError:
    pass
data_git_hash = "b58b7f77b166bc69116f2ead9edf03fbeeb8820a"
data_git_describe = "0.4.0-23-gb58b7f77"
data_git_msg = """\
commit b58b7f77b166bc69116f2ead9edf03fbeeb8820a
Merge: d01b22ca 3c77dac6
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Jun 14 16:26:05 2022 +0200

    Merge pull request #585 from Silabs-ArjanB/ArjanB_dbgg1
    
    Explained which addresses are used as compare values for execute/load…

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
