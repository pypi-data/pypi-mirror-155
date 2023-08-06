# pipus
**pip** helper for **u**ser **s**ite packages

*pipus* is a very simple wrapper around pip to help you manage the installation
of Python packages in your user directory.

pip lacks the ability to keep track of which packages were manually installed
and which came as dependencies. When installing packages in your home, this
quickly becomes an issue if you ever want to update the packages you installed
and do not care about updating the dependency packages if the dependent ones
did not receive any update.

*pipus* fixes this by maintaning a file, similar to the familiar
requirements.txt file, in which the manually installed packages are listed.
*pipus* will then only update those packages when you attempt to run a global
update.

Packages are always installed to your local site and never globally: pipus
calls `pip install --user` internally. This avoids conflict with your OS'
distributed Python packages and is the recommended way to install Python
packages not required by your system components.


## Commands

- Installing a package:  
  `pipus packagename`  
  or manually editing `pipus.txt` and adding the package to it, then running
  `pipus` (or `pipus --update`)

- Updating all packages installed with pipus:  
  `pipus` (or `pipus --update`)

- Uninstalling a package:  
  `pipus -R packagename`  
  or manually editing `pipus.txt` and removing the package from it, then running
  `pipus --refresh`


- Removing all local packages, then installing pipus ones (AKA migrating to
  pipus):  
  `pipus --refresh`

For details, see `pipus --help`.
