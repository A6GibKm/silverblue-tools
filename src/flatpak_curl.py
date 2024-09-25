__license__ = "MIT"

import argparse
import json
import hashlib
import os
import ruamel.yaml
import shutil
import sys
import tempfile
import urllib.request

from collections import OrderedDict
from ruamel.yaml.representer import RoundTripRepresenter


def download(url: str, tempdir: str) -> str:
    with urllib.request.urlopen(url) as response:
        file_path = os.path.join(tempdir, url.split("/")[-1])
        with open(file_path, "x+b") as tar_file:
            shutil.copyfileobj(response, tar_file)
    return file_path


def get_file_hash(filename: str) -> str:
    sha = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            data = f.read(1024 * 1024 * 32)
            if not data:
                break
            sha.update(data)
        return sha.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument(
        "-y",
        "--yaml",
        action="store_true",
        help="generate in yaml format",
    )
    opts = parser.parse_args()
    url = opts.url

    filename = url.split("/")[-1]

    name, extension = os.path.splitext(filename)
    name = name.replace(".tar", "")

    prefix = "flatpak-curl-generator"
    with tempfile.TemporaryDirectory(prefix=prefix) as tempdir:
        filename = download(url, tempdir)
        sha256 = get_file_hash(filename)
        if extension in [".gz", ".zip", ".xz", ".bz2"]:
            file_type = "archive"
        else:
            file_type = "file"
    source = OrderedDict([("type", file_type), ("url", url), ("sha256", sha256)])
    module = OrderedDict(
        [
            ("name", name),
            ("buildsystem", "simple"),
            ("build-commands", []),
            ("sources", [source]),
        ]
    )
    if opts.yaml:
        print_yaml(module)
    else:
        print(json.dumps(module, indent=4))


def print_yaml(module: OrderedDict) -> None:
    class MyRepresenter(RoundTripRepresenter):
        pass

    ruamel.yaml.add_representer(
        OrderedDict, MyRepresenter.represent_dict, representer=MyRepresenter
    )

    yaml = ruamel.yaml.YAML()
    yaml.Representer = MyRepresenter
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.dump(module, sys.stdout)


if __name__ == "__main__":
    main()
