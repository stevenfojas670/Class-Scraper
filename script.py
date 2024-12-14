import requests
import os

cwd = os.getcwd()

# Headers
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.7",
    "cookie": "CloudFront-Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vZW1lcmdpbmd0YWxlbnQuY29udGVudGNvbnRyb2xsZXIuY29tL3ZhdWx0L2RhNjZjMmRiLWVkOWQtNDhiMS1iMTc5LTQzODg2NzU3MDljNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzM0MTQ2MjY4fX19XX0_; CloudFront-Signature=lPGM4Oud6TrVL9oDUq7DRa9rPD7L5RFoXgTVM650qDfvWsXwSvrWtl2HiE62~6afwnQ8GnfTwkAmvr2vL4uqZl~3pzoew1M6iFfR1oXedLDNPQDvG13brwlIWbctw0dQofrnTTjKYaO5F0fi2zfegHXQZsBKjlLCoJZ3PPc8BlPaestBE6X4b6~K-GCAwThSu9a6WbtYPINy5b2YPBWONu2BnlxxIzgbmnaIwcwQ08v6gKGTNxlJeN5mnS7AM4nQEoQOQPU705-twq2h-33bMlb2daM5oB2a9PVz6ChCqQtgk5tXfDmuu9ijbRqz8R3D02u8HrZcqHhvcEHnIEx4hg__; CloudFront-Key-Pair-Id=APKAIA3TVUCWOFBI6GMA",
    "priority": "u=1, i",
    "referer": "https://emergingtalent.contentcontroller.com/ScormEngineInterface/defaultui/player/cmi5-au/1.0/html/cmi5-mediaFile.html?actor=%7B%22name%22%3A%220815286c81c0a2b10ca38fcc85bb966b9dab29baeb5d2b1286adc5b831f443ed%20eb045d78d273107348b0300c01d29b7552d622abbc6faf81b3ec55359aa9950c%22%2C%22objectType%22%3A%22Agent%22%2C%22account%22%3A%7B%22name%22%3A%22a088a88d7cda3e34200ec61ac489dcee7b530c69b2ac0ed00183d2811b44eeff%22%2C%22homePage%22%3A%22https%3A%2F%2Femergingtalent.contentcontroller.com%22%7D%7D&activityId=https%3A%2F%2Femergingtalent.contentcontroller.com%2Fcmi5%2Flms-id%2F553665d846e4ff906642e51b6311bd591d5be9bb%2Fa671e3bd-c9b7-43fd-88c9-14bedb73e65f&endpoint=https%3A%2F%2Femergingtalent.contentcontroller.com%2FScormEngineInterface%2FTCAPI%2Fe3dde401-3796-49f8-9a58-859cba2168f5%2F&fetch=https%3A%2F%2Femergingtalent.contentcontroller.com%2FScormEngineInterface%2Fcmi5Fetch.jsp%3Fsession%3Db4ee56aa-a04f-44f7-ba2a-f546420d69ed%26extCfg%3DAccountId%257C6%2521ContentVaultPath%257C%252Fvault%252Fda66c2db-ed9d-48b1-b179-4388675709c4%2521EngineTenantName%257Ce3dde401-3796-49f8-9a58-859cba2168f5%2521InjectPathMediaFile%257Ctrue&registration=0498143b-693c-4fb2-9069-9d554613128c",
    "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

def download_file(url):
    try:
        # Make the request
        response = requests.get(url, headers=headers, stream=True)
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

        # Derive filename from URL
        filename = os.path.basename(url).split("?")[0]

        # Save to a file
        with open(f'{cwd}\\{filename}', "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"File downloaded successfully as '{filename}'")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    while True:
        # Take user input
        url = input('Enter link to download content: ')
        download_file(url)