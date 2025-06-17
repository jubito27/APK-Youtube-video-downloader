from kivymd.app import MDApp # type: ignore
from kivymd.uix.screen import MDScreen # type: ignore
from kivymd.uix.button import MDRaisedButton # type: ignore
from kivymd.uix.textfield import MDTextField # type: ignore
from kivymd.uix.dialog import MDDialog # type: ignore
from kivymd.uix.boxlayout import MDBoxLayout # type: ignore
from kivymd.uix.label import MDLabel # type: ignore
from kivymd.uix.progressbar import MDProgressBar # type: ignore
from kivy.clock import Clock # type: ignore 
from kivy.utils import platform # type: ignore
from kivy.properties import StringProperty # type: ignore
import yt_dlp # type: ignore
import os
import glob
import threading
from pathlib import Path

class YouTubeDownloader(MDApp):
    download_status = StringProperty("")
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        
        self.screen = MDScreen()
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding="40dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.8))
        
        self.title_label = MDLabel(
            text="YouTube Video Downloader",
            halign="center",
            font_style="H4",
            theme_text_color="Primary")
        
        self.url_input = MDTextField(
            hint_text="Enter YouTube video link",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            helper_text="Example: https://youtu.be/L5CV53wCW00",
            helper_text_mode="persistent")
        
        self.download_btn = MDRaisedButton(
            text="Download",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color=self.theme_cls.primary_color)
        self.download_btn.bind(on_release=self.start_download)
        
        self.progress_bar = MDProgressBar(
            type="indeterminate",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9)
        self.progress_bar.opacity = 0
        
        self.status_label = MDLabel(
            text=self.download_status,
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp")
        
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.download_btn)
        self.layout.add_widget(self.progress_bar)
        self.layout.add_widget(self.status_label)
        
        self.screen.add_widget(self.layout)
        return self.screen
    
    def get_downloads_folder(self):
        """Returns the system's default downloads folder path"""
        if platform == 'win':
            import ctypes
            from ctypes import windll, wintypes
            CSIDL_PERSONAL = 5  # My Documents
            CSIDL_DOWNLOADS = 0x0011  # Downloads
            
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DOWNLOADS, None, 0, buf)
            return buf.value
        elif platform == 'linux':
            return str(Path.home() / "Downloads")
        elif platform == 'macosx':
            return str(Path.home() / "Downloads")
        else:
            return str(Path.home())  # Fallback to home directory
    
    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.show_dialog("Error", "Please enter a YouTube link.")
            return
        
        self.progress_bar.opacity = 1
        self.progress_bar.start()
        self.download_btn.disabled = True
        self.update_status("Starting download...")
        
        threading.Thread(target=self.download_video, args=(url,)).start()
    
    def download_video(self, url):
        try:
            downloads_folder = self.get_downloads_folder()
            output_template = os.path.join(downloads_folder, '%(title)s.%(ext)s')
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("Downloading video...")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                self.update_status(f"Download complete: {os.path.basename(filename)}")
                Clock.schedule_once(lambda dt: self.show_download_complete(filename))
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            Clock.schedule_once(lambda dt: self.show_dialog("Error", f"Download failed: {str(e)}"))
        finally:
            Clock.schedule_once(self.reset_ui)
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if '_percent_str' in d:
                Clock.schedule_once(lambda dt: self.update_status(f"Downloading... {d['_percent_str']}"))
            elif 'eta' in d:
                Clock.schedule_once(lambda dt: self.update_status(f"Downloading... ETA: {d['eta']}s"))
    
    def update_status(self, message):
        self.download_status = message
        self.status_label.text = message
    
    def show_download_complete(self, file_path):
        filename = os.path.basename(file_path)
        self.dialog = MDDialog(
            title="Download Complete!",
            text=f"Video saved to your Downloads folder:\n{filename}",
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

if __name__ == "__main__":
    YouTubeDownloader().run()
