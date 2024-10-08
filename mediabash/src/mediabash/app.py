import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

VIDEO_DIR = "saved_videos"  # Directory to save videos

# Ensure the video directory exists
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

class MediaBash(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.show_main_page()

    def show_main_page(self, widget=None):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color='#f0f0f0'))
        label = toga.Label("Select a website to search for videos:", style=Pack(padding=5, font_size=16))
        main_box.add(label)

        vidbinge_button = toga.Button("Browse VidBinge", on_press=self.show_vidbinge_search_page,
                                      style=Pack(padding=10, background_color='#007bff', color='white', font_size=14))
        main_box.add(vidbinge_button)

        self.main_window.content = main_box
        self.main_window.show()

    def show_vidbinge_search_page(self, widget=None):
        search_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color='#f0f0f0'))
        label = toga.Label("Enter a search term (e.g., 'rick'):", style=Pack(padding=5, font_size=16))
        self.search_input = toga.TextInput(placeholder="Enter search term", style=Pack(padding=10))
        search_button = toga.Button("Search", on_press=self.show_search_results,
                                    style=Pack(padding=10, background_color='#28a745', color='white', font_size=14))

        # Trigger search on Enter key
        self.search_input.on_submit = search_button.on_press

        search_box.add(label)
        search_box.add(self.search_input)
        search_box.add(search_button)

        self.main_window.content = search_box

    def show_search_results(self, widget=None):
        search_term = self.search_input.value
        if not search_term:
            return

        results_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color='#f0f0f0'))
        results_label = toga.Label(f"Search results for: {search_term}", style=Pack(padding=5, font_size=18))
        results_box.add(results_label)

        scroll_container = toga.ScrollContainer(style=Pack(flex=1))
        results_list_box = toga.Box(style=Pack(direction=COLUMN, padding=5))

        # Fetch VidBinge search results
        self.fetch_vidbinge_results(search_term, results_list_box)

        scroll_container.content = results_list_box
        results_box.add(scroll_container)

        back_button = toga.Button("Back to Search", on_press=self.show_vidbinge_search_page,
                                  style=Pack(padding=10, background_color='#ffc107', color='black', font_size=14))
        home_button = toga.Button("Home", on_press=self.show_main_page,
                                  style=Pack(padding=10, background_color='#007bff', color='white', font_size=14))

        results_box.add(back_button)
        results_box.add(home_button)

        self.main_window.content = results_box

    def fetch_vidbinge_results(self, search_term, results_list_box):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            # Enable the DevTools Protocol
            driver.execute_cdp_cmd('Network.enable', {})

            # Set up request interception
            driver.request_interceptor = lambda request: self.log_request(request)

            driver.get(f"https://www.vidbinge.com/browse/{search_term}")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid.grid-cols-2.gap-6.sm\\:grid-cols-3.md\\:grid-cols-4 a.tabbable"))
            )

            video_elements = driver.find_elements(By.CSS_SELECTOR, "div.grid.grid-cols-2.gap-6.sm\\:grid-cols-3.md\\:grid-cols-4 a.tabbable")

            if not video_elements:
                results_list_box.add(toga.Label("No results found.", style=Pack(padding=5)))
            else:
                for video in video_elements:
                    title = video.text.strip()
                    link = video.get_attribute("href")

                    video_card = toga.Box(style=Pack(direction=COLUMN, padding=10, background_color='#e9ecef'))
                    title_label = toga.Label(title, style=Pack(padding=5, font_weight='bold', font_size=16))
                    watch_button = toga.Button("Watch", on_press=lambda w, url=link: self.play_video(url),
                                               style=Pack(padding=5, background_color='#007bff', color='white'))
                    download_button = toga.Button("Download", on_press=lambda w, url=link: self.download_video(url),
                                                  style=Pack(padding=5, background_color='#28a745', color='white'))

                    video_card.add(title_label)
                    video_card.add(watch_button)
                    video_card.add(download_button)
                    results_list_box.add(video_card)

        except Exception as e:
            results_list_box.add(toga.Label("An error occurred while fetching results.", style=Pack(padding=5)))
            print("Error:", str(e))
        finally:
            driver.quit()

    def log_request(self, request):
        # Log only requests that contain specific keywords (like "hls")
        if 'hls' in request['url']:
            print(f"Network Request: {request['url']}")

    def play_video(self, url):
        video_box = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # Create a WebView to display the video
        web_view = toga.WebView(url=url, style=Pack(flex=1))

        # JavaScript to request full-screen
        js_fullscreen = """
        const videoElement = document.getElementById('video-element');
        if (videoElement) {
            videoElement.requestFullscreen().catch(err => {
                console.log('Error attempting to enable full-screen mode:', err.message);
            });
        }
        """

        # Load the video URL
        web_view.on_load = lambda w: w.evaluate(js_fullscreen)

        video_box.add(web_view)

        # Add back and home buttons
        back_button = toga.Button("Back to Results", on_press=self.show_vidbinge_search_page,
                                  style=Pack(padding=10, background_color='#ffc107', color='black', font_size=14))
        home_button = toga.Button("Home", on_press=self.show_main_page,
                                  style=Pack(padding=10, background_color='#007bff', color='white', font_size=14))

        video_box.add(back_button)
        video_box.add(home_button)

        self.main_window.content = video_box

    def download_video(self, url):
        # Fetch the actual video URL using Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video#video-element"))
            )
            video_element = driver.find_element(By.CSS_SELECTOR, "video#video-element")
            video_url = video_element.get_attribute('src')

            # Start the download process
            self.save_video(video_url)

        except Exception as e:
            print("Error fetching video URL for download:", str(e))
        finally:
            driver.quit()

    def save_video(self, video_url):
        response = requests.get(video_url, stream=True)
        video_file_path = os.path.join(VIDEO_DIR, 'downloaded_video.mp4')

        with open(video_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        toga.MessageBox("Download Complete", f"Video has been downloaded to: {video_file_path}")

def main():
    return MediaBash()
