import scrapy
import hashlib
import json
import os
from dotenv import load_dotenv

from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
RECEIVER_PHONE_NUMBER = os.getenv("RECEIVER_PHONE_NUMBER")

class SihSpider(scrapy.Spider):
    name = "sih_spider"
    start_urls = [
        'https://sih.gov.in/',
        # 'https://sih.gov.in/screeningresult',
        # 'https://sih.gov.in/screeningresult_batch_two'
        ]

    def parse(self, response):
        # Example: Extract page content and compute its hash to detect changes
        page_content = response.xpath("//body//text()").getall()
        page_text = ''.join(page_content)
        page_hash = hashlib.md5(page_text.encode()).hexdigest()

        # Save hash to a file
        if os.path.exists("page_hash.json"):
            with open("page_hash.json", "r") as f:
                data = json.load(f)
            if data['hash'] != page_hash:
                # If hash is different, trigger an alert and update the hash file
                self.send_alert("SIH website content has changed!")
                data['hash'] = page_hash
                with open("page_hash.json", "w") as f:
                    json.dump(data, f)
        else:
            # Initialize with the current hash
            with open("page_hash.json", "w") as f:
                json.dump({'hash': page_hash}, f)

    def send_alert(self, message):
        # Twilio WhatsApp credentials
        account_sid = TWILIO_SID
        auth_token = TWILIO_AUTH_TOKEN

        print("\n\n\n\n",message,"\n\n\n\n")
        # client = Client(account_sid, auth_token)

        # # # Send message to WhatsApp
        # try:
        #     client.messages.create(
        #         from_='whatsapp:+14155238886',  # Twilio sandbox WhatsApp number
        #         body=message,
        #         to=RECIEVER_PHONE_NUMBER
        #     )
        #     self.log("WhatsApp alert sent successfully.")
        # except Exception as e:
        #     self.log(f"Failed to send WhatsApp alert: {e}")
