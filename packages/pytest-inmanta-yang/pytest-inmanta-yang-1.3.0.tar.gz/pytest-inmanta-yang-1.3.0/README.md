# pytest-inmanta-yang

Common fixtures used in inmanta yang related modules


Installation
------------

    pip install pytest-inmanta-yang


Usage
-----


1. You can specify workspace folder and device access parameters

```bash
export WORKSPACE=/tmp/workspace
export YANG_DEVICE_HOST="sros-1.ci.ii.inmanta.com"
export YANG_DEVICE_PORT="830"
export YANG_DEVICE_USERNAME="admin"
export YANG_DEVICE_PASSWORD="admin"
```

2. The override the base config (that will be deployed to the device before each test), override the fixture `netconf_device_initial_config_path_file` to return the path to the file containing the base config