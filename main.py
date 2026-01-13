import requests
from bs4 import BeautifulSoup
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import datetime
from dotenv import load_dotenv
import os
import time
import random
load_dotenv()

# Enhanced headers to mimic real browser behavior
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
    "DNT": "1"
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    
import datetime

def send_email(smtp, from_addr, to_addr, subject, body):
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    sender_name = "Amazon Price Tracker" 
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr((str(Header(sender_name, "utf-8")), from_addr))
    msg["To"] = to_addr
    msg["Date"] = date
    msg["Subject"] = Header(subject, "utf-8")

    smtp.send_message(msg) 
    
if __name__ == "__main__":
    url = "https://www.amazon.com/PlayStation-PS5-Console-Ragnar%C3%B6k-Bundle-5/dp/B0BHC395WW/ref=sr_1_7?crid=3IOXEW6U1L08F&dib=eyJ2IjoiMSJ9.woHqMsxNaFAYceP9UBfhRaTo67iyX0jgtD-Og3_0W5b8qlc6tygxiWbVEKq2aoBdnKg-UGiIpTbdfEvf2c8MVD8TWG3CkB_P9BUaNjS6_vCr4GcwGVFXJWJyHOlKYdFa9M1SJcUdpnP94W8umcUuvyfqTGOV3m8N3zXITCPiDUBK0oX_eNjeq52CgpFRS8ECyeelSg937dN-wA8csWSXSNz9Rygc8B_NV81XDsW69Xc.wINPOsWMLYY_oQnspj7zqKdRA6bOWBOeWsh8NdCrChM&dib_tag=se&keywords=ps5+pro&qid=1768162326&sprefix=ps5%2Caps%2C840&sr=8-7"
    soup = fetch_page(url)
    price_whole = int(soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-whole').get_text().replace(',', '').replace('.', '').strip())
    price_fraction = int(soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-fraction').get_text())
    product_total_price = price_whole + price_fraction / 100
    product_price_symbol = soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-symbol').get_text().strip()
    product_name = soup.find(name="span", class_="a-size-large product-title-word-break").get_text().split()
    product_name = " ".join(product_name).strip()
    print(f"The price of the Product is: {product_price_symbol}{product_total_price:.2f}")
    print(f"Product Name: {product_name}")

    if product_total_price < 164000.00:
        debuglevel = 0
        gmail_email = os.getenv("SENDER_EMAIL")
        gmail_password = os.getenv("SENDER_PASSWORD")
        receiver_email = os.getenv("RECIEVER_EMAIL")
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT"))
        if not gmail_email or not gmail_password:
            raise ValueError("SENDER_EMAIL and SENDER_PASSWORD must be set in environment variables.")
        smtp = SMTP(smtp_host, smtp_port)
        smtp.set_debuglevel(debuglevel)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(gmail_email, gmail_password)
        from_address = gmail_email
        to_address = 'saifshahzad901@gmail.com'
        subject = f'Amazon Price Alert!'
        body = f'The price of the product "{product_name}" has dropped to {product_price_symbol}{product_total_price:.2f}.\nCheck it out at {url}'
        send_email(smtp, from_address, to_address, subject, body)
        smtp.quit()
