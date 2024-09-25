import os
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
from shutil import which
from xdg.BaseDirectory import xdg_cache_home, xdg_data_home


def main():
    user_binaries = os.listdir("/var/lib/flatpak/exports/bin/")
    system_binaries = os.listdir(f"{xdg_data_home}/flatpak/exports/bin/")
    binaries = user_binaries + system_binaries
    command = ["flatpak", "info", "-m"]

    initial = [
        "PATH=$PATH:/var/lib/flatpak/exports/bin:${XDG_DATA_HOME}/flatpak/exports/bin"
    ]
    aliases = []

    print("Creating alias for:")
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
                print(f"{cmd} for {appid}")

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
