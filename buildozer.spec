[app]
android.sdk_path = /home/runner/android-sdk  # Correct for GitHub Actions
title = Youtube Video Downloader
package.name = youtube.videodownloader
package.domain = org.jubito
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Updated requirements
requirements = python3,kivy==2.2.1,kivymd,yt-dlp,requests,android,libffi==local_path_to_custom_recipe

# Keystore (relative path or GitHub Secrets)
android.release_keystore = keystore/myapp.keystore
android.release_store_password = key@123
android.release_key_alias = key0
android.release_key_password = key@123

# Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# API Levels
android.api = 33
android.minapi = 21

# Archs
android.archs = arm64-v8a, armeabi-v7a
