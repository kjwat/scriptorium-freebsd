#!/usr/bin/env python3
"""Install native Calibre without changing the normal quarterly repositories."""
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile


def catalogue_has_calibre(pkg):
    result = subprocess.run([*pkg, 'search', '-q', 'calibre'], capture_output=True, text=True)
    if result.returncode not in {0, 1}:
        raise RuntimeError('Unable to query the Calibre package catalogue: ' + result.stderr.strip())
    return any(line.startswith('calibre-') for line in result.stdout.splitlines())


def install(ports=Path('/usr/ports')):
    if platform.system() != 'FreeBSD' or os.geteuid() != 0:
        raise RuntimeError('Native Calibre dependency installation requires administrator authentication on FreeBSD')
    if shutil.which('ebook-convert') and shutil.which('calibre-debug'):
        subprocess.run(['ebook-convert', '--version'], check=True)
        return
    # A private REPOS_DIR applies only to these processes. No configuration in
    # /etc/pkg or /usr/local/etc/pkg/repos is changed or added. Query latest
    # first and use it only for Calibre, leaving quarterly system updates intact.
    with tempfile.TemporaryDirectory(prefix='scriptorium-calibre-repo-') as temp:
        (Path(temp) / 'FreeBSD.conf').write_text('''Scriptorium-Calibre-latest: {
  url: "pkg+https://pkg.FreeBSD.org/${ABI}/latest",
  mirror_type: "srv",
  signature_type: "fingerprints",
  fingerprints: "/usr/share/keys/pkg",
  enabled: yes
}
''')
        pkg = ['pkg', '-o', 'REPOS_DIR=' + temp]
        subprocess.run([*pkg, 'update'], check=True)
        if catalogue_has_calibre(pkg):
            subprocess.run([*pkg, 'install', '-y', 'calibre'], check=True)
            subprocess.run(['ebook-convert', '--version'], check=True)
            return
    # Keep ebook conversion required when the latest binary catalogue lacks it.
    # Use the existing administrator-maintained Ports Collection when present.
    if not (ports / 'Mk/bsd.port.mk').is_file():
        if ports.exists() and any(ports.iterdir()):
            raise RuntimeError('/usr/ports is nonempty but is not a Ports Collection')
        subprocess.run(['git', 'clone', '--depth', '1',
                        'https://git.FreeBSD.org/ports.git', str(ports)], check=True)
    subprocess.run(['make', '-C', str(ports / 'deskutils/calibre'), 'BATCH=yes',
                    'USE_PACKAGE_DEPENDS=yes', 'install'], check=True)
    subprocess.run(['ebook-convert', '--version'], check=True)


if __name__ == '__main__':
    try:
        install()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        raise SystemExit('Scriptorium Calibre: ' + str(error))
