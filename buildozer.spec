[app]

# (str) Title of your application
title = Vocabulary

# (str) Package name
package.name = vocabulary

# (str) Package domain
package.domain = dev.vocabulary

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = db, kv, png, py

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements (comma separated e.g. requirements = sqlite3, kivy)
requirements = python3, kivy==2.1.0, kivymd==0.104.2, pillow, sdl2_ttf==2.0.15, sqlite3, android

# (str) Presplash of the application
presplash.filename = %(source.dir)s/img.png

# (str) Icon of the application
icon.filename = %(source.dir)s/img.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# OSX Specific
#

# Change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (string) Presplash background color
android.presplash_color = #311B92

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = False

# (str) The android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

#
# Python for android (p4a) specific
#

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
# ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
