# from kivymd.app import MDApp # type: ignore
# from kivymd.uix.screen import MDScreen # type: ignore
# from kivymd.uix.button import MDRaisedButton # type: ignore
# from kivymd.uix.textfield import MDTextField# type: ignore
# from kivymd.uix.dialog import MDDialog# type: ignore
# from kivymd.uix.boxlayout import MDBoxLayout# type: ignore
# from kivymd.uix.label import MDLabel# type: ignore
# from kivymd.uix.progressbar import MDProgressBar# type: ignore
# from kivy.clock import Clock# type: ignore
# from kivy.utils import platform# type: ignore
# from kivy.properties import StringProperty# type: ignore
# import yt_dlp# type: ignore
# import os
# import threading
# from pathlib import Path

# # Android-specific imports
# if platform == 'android':
#     from android.permissions import request_permissions, Permission# type: ignore
#     from android.storage import primary_external_storage_path# type: ignore
#     from jnius import autoclass# type: ignore

# class YouTubeDownloader(MDApp):
#     download_status = StringProperty("")
    
#     def build(self):
#         # Request Android permissions
#         if platform == 'android':
#             request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        
#         # KivyMD Dark Theme Setup
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Teal"
#         self.theme_cls.accent_palette = "Amber"
        
#         # UI Layout
#         self.screen = MDScreen()
#         self.layout = MDBoxLayout(
#             orientation="vertical",
#             padding="40dp",
#             spacing="20dp",
#             pos_hint={"center_x": 0.5, "center_y": 0.5},
#             size_hint=(0.8, 0.8)
#         )
        
#         # Title Label
#         self.title_label = MDLabel(
#             text="Video Downloader",
#             halign="center",
#             font_style="H4",
#             theme_text_color="Primary"
#         )
        
#         # Description label
#         self.desc_label = MDLabel(
#             text="Download any kind of  Youtube videos with one click without any signin or signup",
#             halign="center",
#             font_style="Subtitle1",
#             theme_text_color="Secondary",
#             size_hint_y=None,
#             height="60dp"
#         )
        
        
#         # URL Input Field
#         self.url_input = MDTextField(
#             hint_text="Enter YouTube video link",
#             mode="rectangle",
#             size_hint_x=0.9,
#             pos_hint={"center_x": 0.5},
#             helper_text="Example: https://youtu.be/L5CV53wCW00",
#             helper_text_mode="persistent"
#         )
        
#         # Download Button
#         self.download_btn = MDRaisedButton(
#             text="Download",
#             pos_hint={"center_x": 0.5},
#             size_hint_x=0.5,
#             md_bg_color=self.theme_cls.primary_color
#         )
#         self.download_btn.bind(on_release=self.start_download)
        
#         # Progress Bar
#         self.progress_bar = MDProgressBar(
#             type="indeterminate",
#             pos_hint={"center_x": 0.5},
#             size_hint_x=0.9
#         )
#         self.progress_bar.opacity = 0
        
#         # Status Label
#         self.status_label = MDLabel(
#             text=self.download_status,
#             halign="center",
#             theme_text_color="Secondary",
#             size_hint_y=None,
#             height="30dp"
#         )
        
#         # Add widgets to layout
#         self.layout.add_widget(self.title_label)
#         self.layout.add_widget(self.desc_label)
#         self.layout.add_widget(self.url_input)
#         self.layout.add_widget(self.download_btn)
#         self.layout.add_widget(self.progress_bar)
#         self.layout.add_widget(self.status_label)
        
#         self.screen.add_widget(self.layout)
#         return self.screen
    
#     def get_downloads_folder(self):
#         """Returns the correct Downloads folder for Android, Windows, Linux, or Mac."""
#         if platform == 'android':
#             downloads_path = os.path.join(primary_external_storage_path(), 'Download')
#             if not os.path.exists(downloads_path):
#                 os.makedirs(downloads_path)
#             return downloads_path
#         elif platform == 'win':
#             import ctypes
#             from ctypes import windll, wintypes
#             CSIDL_DOWNLOADS = 0x0011
#             buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
#             ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DOWNLOADS, None, 0, buf)
#             return buf.value
#         else:  # Linux/Mac
#             return str(Path.home() / "Downloads")
    
#     def start_download(self, instance):
#         url = self.url_input.text.strip()
        
#         # Check if URL is empty
#         if not url:
#             self.show_dialog("Error", "Please enter a video link.")
#             return
            
#         # Validate YouTube URL
#         if not self.is_valid_youtube_url(url):
#             self.show_dialog("Invalid Link", "Please enter a valid Video URL.\n\nExamples:\nhttps://youtu.be/dQw4w9WgXcQ\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ/nhttps://www.instagram.com/reel/DKOUYSPSX49/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==\nhttps://x.com/elonmusk/status/1234567890123456789\nhttps://www.facebook.com/watch?v=1234567890123456789")
#             return 
        
#         # Proceed with download if valid
#         self.progress_bar.opacity = 1
#         self.progress_bar.start()
#         self.download_btn.disabled = True
#         self.update_status("Starting download...")
        
#         threading.Thread(target=self.download_video, args=(url,)).start()

#     def is_valid_youtube_url(self, url):
#         """Check if the URL is a valid YouTube URL"""
#         youtube_domains = [
#             'www',
#             'http',
#             'https',
        
#         ]
        
#         # Basic check for YouTube domains
#         if not any(domain in url for domain in youtube_domains):
#             return False
        
#         # Run download in a background thread
#         threading.Thread(target=self.download_video, args=(url,)).start()
    
#     def download_video(self, url):
#         try:
#             downloads_folder = self.get_downloads_folder()
#             output_template = os.path.join(downloads_folder, '%(title)s.%(ext)s')
            
#             ydl_opts = {
#                 'format': 'best',
#                 'outtmpl': output_template,
#                 'progress_hooks': [self.progress_hook],
#                 'quiet': True,
#                 'no_warnings': True,
#             }
            
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 self.update_status("Downloading video...")
#                 info = ydl.extract_info(url, download=True)
#                 filename = ydl.prepare_filename(info)
                
#                 # Show Android notification when done
#                 if platform == 'android':
#                     self.show_android_notification("Download Complete", os.path.basename(filename))
                
#                 self.update_status(f"Download complete: {os.path.basename(filename)}")
#                 Clock.schedule_once(lambda dt: self.show_download_complete(filename))
            
#         except Exception as e:
#             self.update_status(f"Error: {str(e)}")
#             Clock.schedule_once(lambda dt: self.show_dialog("Error", f"Download failed: {str(e)}"))
#         finally:
#             Clock.schedule_once(self.reset_ui)
    
#     def show_android_notification(self, title, message):
#         """Shows a native Android notification when download is complete."""
#         PythonActivity = autoclass('org.kivy.android.PythonActivity')
#         Context = autoclass('android.content.Context')
#         NotificationManager = autoclass('android.app.NotificationManager')
#         NotificationBuilder = autoclass('android.app.Notification$Builder')
        
#         notification_service = PythonActivity.mActivity.getSystemService(Context.NOTIFICATION_SERVICE)
        
#         builder = NotificationBuilder(PythonActivity.mActivity)\
#             .setContentTitle(title)\
#             .setContentText(message)\
#             .setSmallIcon(PythonActivity.mActivity.getApplicationInfo().icon)\
#             .setAutoCancel(True)
        
#         notification_service.notify(0, builder.build())
    
#     def progress_hook(self, d):
#         if d['status'] == 'downloading':
#             if '_percent_str' in d:
#                 Clock.schedule_once(lambda dt: self.update_status(f"Downloading... {d['_percent_str']}"))
#             elif 'eta' in d:
#                 Clock.schedule_once(lambda dt: self.update_status(f"Downloading... ETA: {d['eta']}s"))
    
#     def update_status(self, message):
#         self.download_status = message
#         self.status_label.text = message
    
#     def show_download_complete(self, file_path):
#         filename = os.path.basename(file_path)
#         self.dialog = MDDialog(
#             title="✅ Download Complete!",
#             text=f"Video saved to:\n{filename}",
#             buttons=[
#                 MDRaisedButton(
#                     text="OK",
#                     on_release=lambda x: self.dialog.dismiss()
#                 ),
#                 MDRaisedButton(
#                     text="Open Downloads",
#                     on_release=lambda x: self.open_downloads_folder()
#                 )
#             ]
#         )
#         self.dialog.open()
    
#     def open_downloads_folder(self):
#         downloads_folder = self.get_downloads_folder()
#         if platform == 'win':
#             os.startfile(downloads_folder)
#         elif platform == 'linux':
#             os.system(f'xdg-open "{downloads_folder}"')
#         elif platform == 'macosx':
#             os.system(f'open "{downloads_folder}"')
#         elif platform == 'android':
#             # Android requires an Intent to open Downloads
#             Intent = autoclass('android.content.Intent')
#             Uri = autoclass('android.net.Uri')
#             PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
#             intent = Intent(Intent.ACTION_VIEW)
#             intent.setDataAndType(Uri.parse("file://" + downloads_folder), "resource/folder")
#             PythonActivity.mActivity.startActivity(intent)
        
#         self.dialog.dismiss()
    
#     def reset_ui(self, dt=None):
#         self.progress_bar.opacity = 0
#         self.progress_bar.stop()
#         self.download_btn.disabled = False
    
#     def show_dialog(self, title, text):
#         self.dialog = MDDialog(
#             title=title,
#             text=text,
#             buttons=[
#                 MDRaisedButton(
#                     text="OK",
#                     on_release=lambda x: self.dialog.dismiss()
#                 )
#             ]
#         )
#         self.dialog.open()
#         self.reset_ui()

# if __name__ == "__main__":
#     YouTubeDownloader().run()

from kivymd.app import MDApp # type: ignore
from kivymd.uix.screen import MDScreen # type: ignore
from kivymd.uix.button import MDRaisedButton # type: ignore
from kivymd.uix.button import MDFlatButton # type: ignore
from kivymd.uix.menu import MDDropdownMenu # type: ignore
from kivymd.uix.textfield import MDTextField# type: ignore
from kivymd.uix.dialog import MDDialog# type: ignore
from kivymd.uix.boxlayout import MDBoxLayout# type: ignore
from kivymd.uix.label import MDLabel# type: ignore
from kivymd.uix.progressbar import MDProgressBar# type: ignore
from kivy.clock import Clock# type: ignore
from kivy.utils import platform# type: ignore
from kivy.properties import StringProperty# type: ignore
import yt_dlp# type: ignore
import os
import shutil

import threading
from pathlib import Path

# Android-specific imports
if platform == 'android':
    from android.permissions import request_permissions, Permission# type: ignore
    from android.storage import primary_external_storage_path# type: ignore
    from jnius import autoclass# type: ignore

class MyLogger:
    def debug(self, msg):
        print(msg)
    def warning(self, msg):
        print("WARNING:", msg)
    def error(self, msg):
        print("ERROR:", msg)


class YouTubeDownloader(MDApp):
    download_status = StringProperty("")
    
    def build(self):
        # Request Android permissions
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        
        # KivyMD Dark Theme Setup
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        
        # UI Layout
        self.screen = MDScreen()
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding="40dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.8)
        )
        
        # Title Label
        self.title_label = MDLabel(
            text="Youtube Video Downloader",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        
        # Description label
        self.desc_label = MDLabel(
            text="Download any kind of Youtube videos with one click without any signin or signup",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="60dp"
        )
        
        
        # URL Input Field
        self.url_input = MDTextField(
            hint_text="Enter YouTube video link",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            helper_text="Example: https://youtu.be/L5CV53wCW00",
            helper_text_mode="persistent"
        )

        self.selected_quality = "720p"
        # self.quality_button.text = "Quality: 720p"
        self.quality_button = MDFlatButton(
            text="Quality: 720p",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5
        )

        self.quality_options = [
            {"text": "140p"}, {"text": "240p"}, {"text": "480p"},
            {"text": "720p"}, {"text": "1080p"}, {"text": "4K"}
        ]

        self.quality_menu = MDDropdownMenu(
            caller=self.quality_button,
            items=[
                {
                    "text": item["text"],
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=item["text"]: self.set_quality(x),
                } for item in self.quality_options
            ],
            width_mult=3
        )
        self.quality_button.bind(on_release=lambda *args: self.quality_menu.open())

        
        # Download Button
        self.download_btn = MDRaisedButton(
            text="Download",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color=self.theme_cls.primary_color
        )
        self.download_btn.bind(on_release=self.start_download)
        
        # Progress Bar
        self.progress_bar = MDProgressBar(
            type="indeterminate",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9
        )
        self.progress_bar.opacity = 0
        
        # Status Label
        self.status_label = MDLabel(
            text=self.download_status,
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp"
        )
        
        # Add widgets to layout
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.desc_label)
        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.quality_button)
        self.layout.add_widget(self.download_btn)
        self.layout.add_widget(self.progress_bar)
        self.layout.add_widget(self.status_label)
        
        self.screen.add_widget(self.layout)
        return self.screen
    
    def set_quality(self, quality_text):
        self.selected_quality = quality_text
        self.quality_button.text = f"Quality: {quality_text}"
        self.quality_menu.dismiss()
    
    def get_downloads_folder(self):
        """Returns the correct Downloads folder for Android, Windows, Linux, or Mac."""
        if platform == 'android':
            downloads_path = os.path.join(primary_external_storage_path(), 'Download')
            if not os.path.exists(downloads_path):
                os.makedirs(downloads_path)
            return downloads_path
        elif platform == 'win':
            import ctypes
            from ctypes import windll, wintypes
            CSIDL_DOWNLOADS = 0x0011
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DOWNLOADS, None, 0, buf)
            return buf.value
        else:  # Linux/Mac
            return str(Path.home() / "Downloads")
    
    def start_download(self, instance):
        url = self.url_input.text.strip()

        # Check if URL is empty
        if not url:
            self.show_dialog("Error", "Please enter a video link.")
            return

        # Validate YouTube URL
        if not self.is_valid_youtube_url(url):
            self.show_dialog("Invalid Link", "Please enter a valid YouTube video URL.\nExamples:\nhttps://youtu.be/dQw4w9WgXcQ\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")
            return
        if self.quality_button.text == "Select Quality":
            self.show_dialog("Select Quality", "Please select a video quality before downloading.")
            return

        # Proceed with download
        self.progress_bar.opacity = 1
        self.progress_bar.start()
        self.download_btn.disabled = True
        self.update_status("Starting download...")

        threading.Thread(target=self.download_video, args=(url,)).start()


    def is_valid_youtube_url(self, url):
        """Basic check if the URL looks like a YouTube link"""
        youtube_patterns = [
            "youtube.com/watch?v=",
            "youtu.be/",
            "youtube.com"
        ]
        return any(pattern in url for pattern in youtube_patterns)

        
    def check_ffmpeg_installed(self):
        if shutil.which("ffmpeg") is None:
            self.show_dialog("FFmpeg Not Found", "Please install FFmpeg to support HD downloads.")
            return False
        return True
    
    def download_video(self, url):
        try:
            downloads_folder = self.get_downloads_folder()
            output_template = os.path.join(downloads_folder, '%(title)s.%(ext)s')
            format_map = {
                "140p": "bestvideo[height<=144]+bestaudio",
                "240p": "bestvideo[height<=240]+bestaudio",
                "480p": "bestvideo[height<=480]+bestaudio",
                "720p": "bestvideo[height<=720]+bestaudio",
                "1080p": "bestvideo[height<=1080]+bestaudio",
                "4K": "bestvideo[height<=2160]+bestaudio",
            }

            selected_format = format_map.get(self.selected_quality, "bestvideo+bestaudio")


            ydl_opts = {
                'format': selected_format,  # Prefer HD video+audio
                'merge_output_format': 'mp4',  # Ensure merged file is mp4
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
                'ffmpeg_location': r"C:\FFMPEG\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin",
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'logger': MyLogger(),
              
                
                }

            # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #     self.update_status("Downloading video...")
            #     info = ydl.extract_info(url, download=True)
            #     filename = ydl.prepare_filename(info)
            #     resolution = info.get('format_note', 'Unknown quality')
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("Downloading video...")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # Use selected quality (e.g., "720p") directly
                resolution = self.selected_quality
                # Android notification
                if platform == 'android':
                    self.show_android_notification("Download Complete", os.path.basename(filename))

                self.update_status(f"Download complete: {os.path.basename(filename)} ({resolution})")
                Clock.schedule_once(lambda dt: self.show_download_complete(filename))

        except Exception as e:
            error_message = f"Download failed: {str(e)}"
            self.update_status(error_message)
            Clock.schedule_once(lambda dt: self.show_dialog("Error", error_message))

        finally:
            Clock.schedule_once(self.reset_ui)

    
    def show_android_notification(self, title, message):
        """Shows a native Android notification when download is complete."""
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        
        notification_service = PythonActivity.mActivity.getSystemService(Context.NOTIFICATION_SERVICE)
        
        builder = NotificationBuilder(PythonActivity.mActivity)\
            .setContentTitle(title)\
            .setContentText(message)\
            .setSmallIcon(PythonActivity.mActivity.getApplicationInfo().icon)\
            .setAutoCancel(True)
        
        notification_service.notify(0, builder.build())
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = int(downloaded / total * 100)
            Clock.schedule_once(lambda dt: self.update_status(f"Downloading... {percent}%"))

        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.update_status("Download finished. Processing..."))

    
    def update_status(self, message):
        self.download_status = message
        self.status_label.text = message
    
    def show_download_complete(self, file_path):
        filename = os.path.basename(file_path)
        self.dialog = MDDialog(
            title="✅ Download Complete!",
            text=f"Video saved to:\n{filename}",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Open Downloads",
                    on_release=lambda x: self.open_downloads_folder()
                )
            ]
        )
        self.dialog.open()
    
    def open_downloads_folder(self):
        downloads_folder = self.get_downloads_folder()
        if platform == 'win':
            os.startfile(downloads_folder)
        elif platform == 'linux':
            os.system(f'xdg-open "{downloads_folder}"')
        elif platform == 'macosx':
            os.system(f'open "{downloads_folder}"')
        elif platform == 'android':
            # Android requires an Intent to open Downloads
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(Uri.parse("file://" + downloads_folder), "resource/folder")
            PythonActivity.mActivity.startActivity(intent)
        
        self.dialog.dismiss()
    
    def reset_ui(self, dt=None):
        self.progress_bar.opacity = 0
        self.progress_bar.stop()
        self.download_btn.disabled = False
    
    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
        self.reset_ui()
    import shutil

    def check_ffmpeg_installed(self):
        if shutil.which("ffmpeg") is None:
            self.show_dialog("FFmpeg Not Found", "Please install FFmpeg to support HD downloads.")
            return False
        return True


if __name__ == "__main__":
    YouTubeDownloader().run()


