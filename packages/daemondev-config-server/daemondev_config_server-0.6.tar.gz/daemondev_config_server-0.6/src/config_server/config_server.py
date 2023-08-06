from core.request import request
import os
import base64
import logging
import sys
import yaml
import re
from colors import Colors as colors   ### Run in local
from attribute_dict import AttributeDict
#from config_server.colors import Colors as colors  ### Run installed

#import colors as C
#colors = C.Colors

#from dotenv import load_dotenv
#load_dotenv()

logging.basicConfig(filename='/tmp/daemondev-config-server.log', format='%(asctime)s-daemondev-config-server> %(levelname)s-%(message)s', level=logging.INFO)
_logger = logging.getLogger(__name__)
h = logging.StreamHandler(sys.stdout)
h.flush = sys.stdout.flush
h.setLevel(logging.DEBUG)                   #h.setFormatter(CustomFormatter())
_logger.addHandler(h)

K8S = os.getenv("KUBERNETES_PORT", None )
envConfig = f"{os.getcwd()}/.configserver"

def readfile(filename, is_yaml=False):
    content = ""
    with open(filename, "r") as f:
        if is_yaml:
            content = yaml.load(f, Loader=yaml.FullLoader)
        else:
            content = f.read().strip()
    return content

if os.path.exists(envConfig):
    envs = readfile(envConfig)
    for l in envs.split("\n"):
        key, val = l.split("=")
        os.environ[key.strip()] = val.strip()

configFilesDir = f"{os.path.dirname(os.path.realpath(__file__))}"
repo_name = os.path.basename(os.popen("git rev-parse --show-toplevel").read().strip()) if not K8S else "dummy"
environment = os.getenv("ENVIRONMENT", "local")
debug = os.getenv("DEBUG", False)
config_files_folder = os.getenv("LOCAL_CONFIG_DIR", os.getenv("GLOBAL_CONFIG_DIR", configFilesDir))
allowed_debugable_environmets = ["local", "development", "staging"]

schema = os.getenv("CONFIG_SCHEMA", "https")
config_server = f"{os.getenv('CONFIG_SERVER','config.wecourier4u.com')}"
obj = None
final_local_yaml = ""
project = os.getenv("APPLICATION", os.getenv("PROJECT_NAME", repo_name or "dummy"))
yamlfile = f"{config_files_folder}/{project}-{environment}"
check_env_var_mode_re = r"\${.+}"
inner_content_re = r"(?<=\${)[^{\}].+(?=})"
executionMessage = ""

if os.path.exists(configFilesDir) and os.getcwd() == "/app":
    executionMessage = f"{colors.bggreen}{colors.fgblack}>>> Running in {colors.bgmagenta}\"docker-mode\"{colors.reset}"

if environment in allowed_debugable_environmets and debug:
    ENV_VARS=f" APPLICATION: {project}\n ENVIRONMENT: {environment}\n LOCAL_CONFIG_DIR: {config_files_folder}"
    _logger.info(f"{colors.bgmagenta}{colors.fgblack}ENV VARS:{executionMessage if executionMessage != '' else ''}{colors.reset}{colors.bgyellow}\n{ENV_VARS}{colors.reset}")

def interpolate(obj, key):
    final = obj[key]
    if re.match(check_env_var_mode_re, final):
        env_var_name = re.findall(inner_content_re, final)
        _default = ""
        if "," in final:
            splitted = env_var_name[0].split(",")
            env_var_name = splitted[0].strip()
            _default = splitted[1].strip()
        final = f"{os.getenv(env_var_name, _default)}"
    return final

def iterator(obj):
    for k in obj.keys():
        if isinstance(obj[k], dict):
            iterator(obj[k])
        elif isinstance(obj[k], str):
            obj[k] = interpolate(obj, k)

if K8S is None:
    schema = "http"
    config_server = "localhost:5000"

for ext in ["yaml", "yml"]:
    final_local_yaml =  f"{yamlfile}.{ext}"
    if os.path.exists(final_local_yaml):
        obj = readfile(final_local_yaml, True)

if obj is None:
    auth = f"{os.getenv('CONFIG_USERNAME', 'w4u')}:{os.getenv('CONFIG_PASSWORD','w4u')}".encode("ascii")
    auth = base64.b64encode(auth).decode("utf-8")
    url = f"{schema}://{config_server}/{project}-{environment}"

    custom_headers = {
        "Content-Type": "application/json",
        'Authorization': f"Bearer {auth}"
    }
    obj = request(url, {}, custom_headers, method="GET")
    _logger.info(f"{colors.bggreen}>>> Successful load from request: {colors.bgmagenta}[{url}]!!!{colors.reset}")
else:
    _logger.info(f"{colors.bggreen}{colors.fgblack}>>> Successful load from local directory: {colors.bgmagenta}[{final_local_yaml}]{colors.reset}")


if debug and environment in allowed_debugable_environmets:
    import json
    _logger.info(f"{colors.bgblue}")
    _logger.info(json.dumps(obj,  indent=4, sort_keys=True))
    _logger.info(f"{colors.reset}")

iterator(obj)

def objectify(obj):
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = objectify(v)
    return AttributeDict(obj)

config = objectify(obj)

#print(f">>> obj: [{config.database.name}]")
