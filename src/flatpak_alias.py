import os
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from shutil import which
from xdg.BaseDirectory import xdg_cache_home


def main():
    binaries = os.listdir("/var/lib/flatpak/exports/bin/")
    command = ["flatpak", "info", "-m"]

    initial = ["PATH=$PATH:/var/lib/flatpak/exports/bin"]
    aliases = []

    for binary in binaries:
        appid = os.path.basename(binary)
        try:
            proc = subprocess.run(command + [appid], check=True, capture_output=True)
            # This might be overkill
            parser = ConfigParser(interpolation=ExtendedInterpolation())
            parser.read_string(proc.stdout.decode("utf-8"))
            cmd = os.path.basename(parser["Application"]["command"]).replace(
                "-wrapper", ""
            )
            if not which(cmd):
                aliases.append("alias {}={}".format(cmd, appid))
        except Exception as e:
            print(f"skiping: {appid}: {e}")

    path = os.path.join(xdg_cache_home, "flatpak-aliases")

    contents = [x + "\n" for x in initial + aliases]
    with open(path, "w+") as f:
        f.writelines(contents)

    print(
        """Add

    if [ -f "${XDG_CACHE_HOME}"/flatpak-aliases ] && ! [ "$HOSTNAME" == "toolbox" ] && [[ -z "${FLATPAK_ID}" ]]; then
        . "${XDG_CACHE_HOME}"/flatpak-aliases
    fi

    to your ~/.bashrc file."""
    )


if __name__ == "__main__":
    main()
