# Silverblue tools

A toolbox of scripts for [toolbox](https://github.com/containers/toolbox/),
[Silverblue](https://silverblue.fedoraproject.org/), [flatpak](https://github.com/flatpak/flatpak), and [rpm-ostree](https://github.com/coreos/rpm-ostree).

Python requirements are in `requirements.txt`

``` sh
pip install -r requirements.txt
```

## toolbox-export

Export application metadata outside of a toolbox container.

#### Usage

``` sh
$ toolbox-export foo
installed: ~/.local/share/applications/foo.desktop
installed: ~/.local/share/icons/hicolor/32x32/apps/foo.png
installed: ~/.local/share/icons/hicolor/64x64/apps/foo.png
installed: ~/.local/share/icons/hicolor/128x128/apps/foo.png
installed: ~/.local/share/icons/hicolor/scalable/apps/foo.svg
installed: ~/.local/share/appdata/foo.appdata.xml
```
Results in correct desktop entries
``` sh
[Desktop Entry]
Name=foo
Exec=toolbox run foo %f
TryExec=toolbox
Icon=foo
Type=Application
Terminal=false
Categories=Foo;Bar
```

## flatpak-curl

Quickly generate modules for your flatpak manifest.

#### Usage

``` sh
$ flatpak-curl https://domain.org/foo-version.tar.gz
{
    "name": "foo-version",
    "buildsystem": "simple",
    "build-commands": [],
    "sources": [
        {
            "type": "archive",
            "url": "https://domain.org/foo-version.tar.gz",
            "sha256": "88d3b735e43f6f16a0181a8fec48847693fae80168d5f889fdbdeb962f1fc804"
        }
    ]
}
```

# Future ideas

## TODO flatpak-alias and toolbox-alias

Quickly create alias to flatpak and toolbox applications.

#### Usage

``` sh
$ flatpak-alias gcc --command=gcc org.freedesktop.Sdk
Created alias gcc="flatpak run --command=gcc org.freedesktop.Sdk"
```

``` sh
$ toolbox-alias dnf
Created alias bar="toolbox run dnf"
```

## TODO ostree-history

List recent commits by date to facilitate rollbacks.

``` sh
$ ostree-history 4
History of fedora:fedora/32/x86_64/silverblue:
Jul 2 f0df14c641d2090b69f4860aa312a9098d9e5eb6a3c8f1d37327fd62293d916b
Jul 3 7402ccb7488428235c332ce1eaf94d836737bdeccf57b98fa2757d53b1f87985
Jul 5 7402ccb7488428235c332ce1eaf94d836737bdeccf57b98fa2757d53b1f87985
Jul 11 6e670d9a4cb48d15c8e2a8ab64246a5051148981da417b970e15b57290c34d82
```
To deploy: `$ rpm-ostree deploy COMMIT`, to compare `rpm-ostree db diff COMMIT`.

## TODO ostree-copr

Enable copr repos in silverblue. Requires root permissions.

#### Usage

``` sh
ostree-copr enable user/repository
```

``` sh
ostree-copr disable user/repository
```
