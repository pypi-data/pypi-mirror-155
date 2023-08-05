import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post163"
version_tuple = (0, 4, 0, 163)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post163")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post21"
data_version_tuple = (0, 4, 0, 21)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post21")
except ImportError:
    pass
data_git_hash = "d01b22ca894152467faaaa56a3084683ab0abb8a"
data_git_describe = "0.4.0-21-gd01b22ca"
data_git_msg = """\
commit d01b22ca894152467faaaa56a3084683ab0abb8a
Merge: e36832a5 a0edb6a9
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Jun 14 15:54:15 2022 +0200

    Merge pull request #584 from Silabs-ArjanB/ArjanB_dbgg0
    
    Made dcsr.EBREAKM descriptions specific to machine mode. Expanded ins…

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
