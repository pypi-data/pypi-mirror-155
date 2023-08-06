from urllib.request import urlopen, Request  ### from urllib.parse import urlencode
from urllib.error import HTTPError
import json


def request(url, data={}, headers={}, method="POST"):
    rq = Request(url, json.dumps(data).encode("ascii"), headers, method=method)
    data = {}
    try:
        response = urlopen(rq)
        data = json.load(response)
    except HTTPError as e:
        raise e
    return data

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK) and os.path.isfile(fpath)

    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            for candidate in ext_candidates(exe_file):
                if is_exe(candidate):
                    return candidate

    return None
