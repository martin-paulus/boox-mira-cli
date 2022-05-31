.. _appimage-analysis:

AppImage analysis
=================
Besides the built-in buttons the Onyx Boox Mira can also be configured through an `application`__. For Linux the distribution format is AppImage. The current version contains a flaw where the application attempts to write to its own path, which is read only, rather than the user's home directory.

.. __: https://help.boox.com/hc/en-us/articles/4408324394772-Mira-Software-Download

Inspecting the AppImage
-----------------------
In order to find out what causes the errors the AppImage outputs you have to look inside. AppImage files are filesystem images and can therefore be mounted. The `Mira-latest.AppImage`__ is in AppImage version 2 format, so it supports the ``--appimage-mount`` parameter. When run like this, the filesystem is mounted without launching the application: ``./Mira-latest.AppImage --appimage-mount``. This command outputs the mountpoint. The contents are now available for browsing.

.. __: https://static.send2boox.com/monitor-pc/linux/Mira-latest.AppImage

.. tip:: Copy the files at the mountpoint to a writable path to launch the application from (e.g. ``cp -R "$mountpoint" ~/Mira-latest``). When invoked from a writable path the application outputs fewer errors, and the *Export configuration* feature works properly. But the sources of the application are not visible at this stage.

Extracting the ASAR
-------------------
The sources to the Electron application that is contained in the AppImage are packaged into an Atom Shell Archive Format file: ``resources/app.asar``. Use the `asar`__ package to extract this file (e.g. ``asar extract ~/Mira-latest/resources/app.asar ~/Mira-latest-asar``). Now the source files are visible inside the extraction path. However, the JavaScript files are minified, making them difficult to read (e.g. ``js/app.913389d7.js``).

.. __: https://www.npmjs.com/package/asar

Extracting the source map
-------------------------
Use the `source-from-sourcemaps`__ package to extract the source map (e.g ``source-from-sourcemaps  ~/Mira-latest-asar/js/app.913389d7.js.map``). The readable sources can be found in the extraction path (e.g. ``sources-gen/src/``).

.. __: https://www.npmjs.com/package/source-from-sourcemaps
