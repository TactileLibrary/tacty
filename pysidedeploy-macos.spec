[app]

# title of your application
title = tacty

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = run.py

# directory where the executable output is generated
exec_directory = dist

# path to the project file relative to project_dir
project_file =

# application icon
icon = src/tacty/resources/icons/tl.png

[python]

# python path
# python_path =
# python packages to install
packages = Nuitka==2.7.11

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
qml_files =

# excluded qml plugin binaries
excluded_qml_plugins =

# qt modules used. comma separated
modules = Core,Gui,Widgets

# qt plugins used by the application.
plugins = accessiblebridge,generic,iconengines,imageformats,platforminputcontexts,platforms,styles

[android]

# path to pyside wheel
wheel_pyside =

# path to shiboken wheel
wheel_shiboken =

# plugins to be copied to libs folder of the packaged application. comma separated
plugins =

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# add permissions here if your app accesses the microphone, camera, etc.
macos.permissions =

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = standalone

# specify any extra nuitka arguments
extra_args = --assume-yes-for-downloads --noinclude-qt-translations --include-package=pydantic --include-package=pandas --nofollow-import-to=*.tests --nofollow-import-to=*.pytest --macos-create-app-bundle

[buildozer]

# build mode
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir =

# path to extra qt android .jar files to be loaded by the application
jars_dir =

# if empty, uses default ndk path downloaded by buildozer
ndk_path =

# if empty, uses default sdk path downloaded by buildozer
sdk_path =

# other libraries to be loaded at app startup. comma separated.
local_libs =

# architecture of deployed platform
arch =
