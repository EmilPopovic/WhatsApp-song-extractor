from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def read_video_urls(_=None):
    with open('extracted.csv', 'r') as f:
        contents = f.read()

    entries = contents.split('\n')

    urls = []

    for entry in entries[1:]:
        splt = entry.split(',')
        url = splt[4]
        urls.append(url)

    return urls


def main():
    # Read the text file containing video URLs
    video_urls = read_video_urls()
    
    # Create a new Chrome browser instance
    driver = webdriver.Chrome()
    
    # Go to YouTube and sign in to your account
    driver.get("https://www.youtube.com")
    # Perform necessary actions to sign in to your YouTube account manually
    # (e.g., entering credentials and clicking the sign-in button)
    # Make sure to stay signed in during the script execution
    time.sleep(60)
    
    # Create a new playlist
    driver.get("https://www.youtube.com/playlist?list_type=playlist")
    time.sleep(2)  # Add a delay to ensure the page is loaded properly
    playlist_title = "My Playlist"
    playlist_title_input = driver.find_element("name", "title")
    playlist_title_input.send_keys(playlist_title)
    playlist_title_input.send_keys(Keys.RETURN)
    
    # Add videos to the playlist
    for video_url in video_urls:
        driver.get("https://www.youtube.com/watch?v=" + video_url)
        time.sleep(2)  # Add a delay to ensure the page is loaded properly
        driver.find_element("xpath", "//button[contains(text(),'Save to playlist')]").click()
        time.sleep(2)  # Add a delay to ensure the action is performed properly
        driver.find_element("xpath", "//div[contains(text(), 'My Playlist')]").click()
        time.sleep(2)  # Add a delay to ensure the action is performed properly
    
    driver.quit()
    print(f"Playlist '{playlist_title}' created successfully!")


if __name__ == "__main__":
    main()
