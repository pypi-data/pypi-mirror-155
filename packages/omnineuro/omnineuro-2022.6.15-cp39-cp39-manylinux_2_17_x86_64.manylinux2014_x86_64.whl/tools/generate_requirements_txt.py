#!/usr/bin/env python3
from os.path import abspath, dirname, join
from configparser import ConfigParser
from datetime import datetime

PROJECTDIR = dirname(abspath(dirname(__file__)))

setup_file = join(PROJECTDIR, "setup.cfg")
requirements_file = join(PROJECTDIR, "requirements.txt")


if __name__ == "__main__":
    config = ConfigParser()
    config.read(setup_file)
    requirements = config.get("options", "install_requires").strip().splitlines() + [""]
    requirements += config.get("options.extras_require", "all").strip().splitlines()

    with open(requirements_file, "w") as f:
        f.write("# Auto-generated on %s\n" % datetime.now().isoformat())
        for r in requirements:
            f.write("%s\n" % r)
