# FreeBSD Scriptorium

The native FreeBSD upstream is https://github.com/kjwat/scriptorium-freebsd.
It selects https://github.com/kjwat/simplesuite-freebsd by default. Linux and
macOS retain https://github.com/kjwat/scriptorium and its original SimpleSuite
upstream. The entry points reject the wrong checkout for the running OS.

Clone into the canonical directory so the existing writing and backup tools
find it:

```sh
git clone https://github.com/kjwat/scriptorium-freebsd.git ~/scriptorium
cd ~/scriptorium
./install.sh
```

This port is in progress. The complete native installer and application release
checks must pass before this is described as a working FreeBSD distribution.
The installer supports both a clean native Git checkout and the complete
hash-checked SimpleSuite source bundled with a preinstalled SimpleOS image.
It does not replace that source with the Linux repository.

The full native suite is built through `gmake full` / `install-full`, including
SimpleTerm, SimplePlay and SimplePDF. Existing release tests remain required.
The native SID compatibility library is built by SimpleSuite's own bootstrap;
no parent porting workspace is required by a standalone clone.

Calibre remains a required ebook conversion dependency. The installer checks
the official latest binary catalogue through a temporary repository directory,
using latest only for that package while normal system updates retain quarterly.
If the binary package is unavailable, the helper uses `deskutils/calibre` in the
Ports Collection. It never substitutes a Linux binary or omits ebook conversion.

SimpleCheck, SimpleTrident, aliases, reminders and normal writing configuration
remain part of the installation. The checked-in defaults are sanitized release
defaults; personal calendar data, browser history, cookies, keys, credentials
and the original repository's personal dotfiles are excluded from this new
repository's initial history.
