# Requirements
 - require .env file with these contents

```
CONFIG_SERVER=localhost | config.wecourier4u.com
CONFIG_SCHEMA=https | http
CONFIG_USERNAME=xxx
CONFIG_PASSWORD=xxxxxxxxxxxxxxxxxxxxxxxx
ENVIRONMENT=local | production
LOCAL_CONFIG_DIR=/path/to/my/config-files/repo/dir  #Optional
DEBUG=1                                             #Optional
```

 - (Optional): create .configserver file in root project and set LOCAL_CONFIG_DIR
 - (Optional): export GLOBAL_CONFIG_DIR in your .*rc file

```
#~/.bashrc
export GLOBAL_CONFIG_DIR=/path/to/config-files/dir

#$PROJECT_ROOT/.configserver
LOCAL_CONFIG_DIR=/path/to/config-files/dir
```
 - Append this commands to package.json in ```scripts``` section

```
#package.json
...
    "install": "docker run -it --rm --name nest -v $(pwd):/app node:14.19-alpine3.14 sh -c 'cd /app && npm install'",
    "docker": "docker run -it --rm --name nest -p ${PORT:-3000}:${PORT:-3000} -e PORT=${PORT} -v ${GLOBAL_CONFIG_DIR}:/app/config-files -e DEBUG=${DEBUG} -v $(pwd):/app node:14.19-alpine3.14 sh -c 'cd /app && npm run start'",
...
```
