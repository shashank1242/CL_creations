from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import urllib.parse

# --- Configuration ---
phone_numbers = ["+918050767472"]  # Replace with actual numbers
message = "Hello! This is an automated message."

options = webdriver.ChromeOptions()
# options.binary_location = "/usr/bin/google-chrome" # Uncomment if strictly needed for your Linux setup
options.add_argument("--user-data-dir=/home/shashankp/.config/whatsapp-bot")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# Initialize Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")

print("⏳ Waiting for WhatsApp to load...")

try:
    # Wait for the main layout to load (indicates successful login)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )
    print("✅ WhatsApp loaded successfully!")
except Exception as e:
    print("❌ WhatsApp took too long to load or login failed. Please check your session.")
    driver.quit()
    exit()

# --- Message Sending Loop ---
for number in phone_numbers:
    print(f"🔄 Processing number: {number}...")
    encoded_msg = urllib.parse.quote(message)
    driver.get(f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}")

    try:
        # We look for the main chat area ('id="main"') and then the editable text box inside it.
        # This is much more reliable than looking for the send button.
        msg_box_locator = (By.XPATH, '//*[@id="main"]//div[@contenteditable="true"]')

        # Wait until the message box is loaded and clickable
        msg_box = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(msg_box_locator)
        )

        # A tiny pause ensures WhatsApp has fully pasted the text from the URL into the box
        time.sleep(1.5)

        # AUTOSEND: Simulate pressing the 'Enter' key inside the text box
        msg_box.send_keys(Keys.ENTER)
        print(f"✅ Message automatically sent to {number}")

        # Wait a few seconds for the message to actually fire off before the next iteration
        time.sleep(3)

    except Exception as e:
        print(f"❌ Failed to autosend to {number}. The number might be invalid.")
        print(f"Error details: {e}")

# Clean up
driver.quit()
print("🎉 All tasks completed!")
