import time
import random
import requests
import os
import re
import threading
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

username = os.environ.get('username')
password = os.environ.get('password')

cwd = os.getcwd()

class Browser:
    browser, options = None, None
    request_data = None
    directory: str = None
    download_flag: bool = None

    def __init__(self, directory: str, download_flag: bool):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.options.page_load_strategy = 'normal'
        self.browser = webdriver.Chrome(options=self.options)
        self.request_data = {}
        self.directory = directory
        self.download_flag = download_flag
        os.makedirs(self.directory, exist_ok=True) # Creating root directory
 
    def open_page(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        for character in text:
            field.send_keys(character)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        wait = WebDriverWait(self.browser, timeout=2)
        wait.until(lambda d : button.is_displayed())
        actions = ActionChains(self.browser)
        actions.move_to_element(button).pause(2).click().perform()

    def login_awsacademy(self, username: str, password: str):
        self.wait_random_time()
        self.add_input(by=By.ID, value='pseudonym_session_unique_id', text=username)
        self.wait_random_time()
        self.add_input(by=By.ID, value='pseudonym_session_password', text=password)
        self.wait_random_time()
        self.click_button(by=By.NAME, value='commit')

    def traverse_page(self):
        try:
            
            modules_container = self.browser.find_element(by=By.CLASS_NAME, value='ig-list')
            module_sections = modules_container.find_elements(By.XPATH, ".//div[starts-with(@aria-label, 'Module')]")

            for div in module_sections:
                module_name = div.get_attribute('aria-label')
                print(f'Processing: {module_name}')
                content_div = div.find_element(by=By.CLASS_NAME, value='content')
                modules_list = content_div.find_element(by=By.TAG_NAME, value='ul')
                module_items = modules_list.find_elements(by=By.TAG_NAME, value='li')

                original_window = self.browser.current_window_handle

                assert len(self.browser.window_handles) == 1

                for item in module_items:
                    try:
                        link_type_element = item.find_element(by=By.CLASS_NAME, value="type_icon")
                        link_title = link_type_element.get_attribute('title')

                        if link_title == 'External Tool':
                            link = item.find_element(by=By.XPATH, value=".//a[@class='ig-title title item_link']")
                            title = link.get_attribute("title")
                            second_page = link.get_attribute("href")
                            self.browser.execute_script("window.open()")
                            self.wait_random_time()
                            windows = self.browser.window_handles
                            self.browser.switch_to.window(windows[-1])
                            self.browser.get(second_page)
                            self.get_request_information('https://emergingtalent.contentcontroller.com/vault', module_name, title)
                            self.wait_random_time()
                            self.browser.close()
                            self.browser.switch_to.window(original_window)
                    except Exception as e:
                        print(f'No link found in this {item.id}')

        except Exception as e:
            print(f"An error occurred: {e}")

        return self.request_data

    def get_request_information(self, link: str, directory: str, filename: str):

        pattern = re.compile(rf"{re.escape(link)}.*\.(pdf|mp4)$")

        while True:
            for request in self.browser.requests:
                if pattern.search(request.url):
                    self.request_data = {
                        "directory": directory,
                        "url": request.url,
                        "headers": request.headers,
                        "filename": filename
                    }
                    del self.browser.requests

                    if self.download_flag == True:
                        self.download()

                    return
        
    def download(self):

        url = self.request_data['url']
        headers = self.request_data['headers']
        name = self.request_data['filename']
        directory = self.request_data['directory']

        try:
            # Make the request
            response = requests.get(url=url, headers=headers, stream=True)
            response.raise_for_status()

            # Get content type and infer file extension
            content_type = response.headers.get("Content-Type", "")
            file_extension = {
                "text/vtt": ".vtt",
                "application/pdf": ".pdf",
                "text/plain": ".txt",
                "application/json": ".json",
            }.get(content_type, ".bin")  # Default to ".bin" if unknown

            if file_extension == '.bin':
                file_extension = '.mp4'

            directory = self.remove_illegal_characters(directory)
            name = self.remove_illegal_characters(name)

            # Make directory titled after module name
            os.makedirs(f'{self.directory}\\{directory}', exist_ok=True)

            # Save to a file
            with open(f'{cwd}\\{self.directory}\\{directory}\\{name}{file_extension}', "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"File downloaded successfully as '{cwd}\\{self.directory}\\{directory}\\{name}\\{file_extension}'")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    # Utility functions 
    def wait_random_time(self):
        time.sleep(random.random())

    def find_specific_request(self, keyword: str):
        for request in self.browser.requests:
            if request.method == 'GET' and keyword in request.url:
                print

    def remove_illegal_characters(self, input_string: str):
        # Define the regex pattern for illegal characters
        illegal_chars = r'[<>:"/\\|?*]'
        
        # Replace illegal characters with an empty string
        sanitized_string = re.sub(illegal_chars, '', input_string)
        
        # Strip trailing spaces or periods
        sanitized_string = sanitized_string.rstrip(' .')
        
        return sanitized_string
    
def run_multiple_drivers(directory: str, url: str, download_flag: bool):
    print(f'{directory} thread starting!')
    
    browser = Browser(directory=directory, download_flag=download_flag)
    browser.open_page('https://awsacademy.instructure.com/login/canvas')
    browser.login_awsacademy(username, password)
    time.sleep(8)
    browser.open_page(url)
    time.sleep(8)
    browser.traverse_page()


if __name__ == '__main__':

    # Run thread with True to download files
    foundations = threading.Thread(target=run_multiple_drivers, args=('AWS Cloud Foundations', 'https://awsacademy.instructure.com/courses/91362/modules', False))
    foundations.start()
    foundations.join()