[app]
title = Youtube Video Downloader
package.name = youtube.videodownloader
package.domain = org.jubito
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# ✅ Cleaned and corrected requirements
requirements = python3,kivy==2.2.1,kivymd,yt-dlp,requests,android,libffi

# ✅ Platform configuration
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.release_artifact = apk  # Instead of aab

# ✅ Correct SDK/NDK paths (set in GitHub Actions)
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

# ✅ Release signing (ensure your keystore is present or set this via GitHub Secrets)
#android.release_keystore = keystore/myapp.keystore
#android.release_store_password = key@123
#android.release_key_alias = key0
#android.release_key_password = key@123

# ✅ Use the latest stable python-for-android branch
p4a.branch = develop
# p4a.fork =  # Leave blank unless you have a custom fork

[buildozer]
build_dir = C:\Buildozer_Outputs
