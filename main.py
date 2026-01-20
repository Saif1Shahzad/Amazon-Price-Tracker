from playwright.sync_api import sync_playwright
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

def fetch_page(url):
    """
    Fetches the page content using Playwright with a real browser.
    This approach is more reliable for GitHub Actions and automated environments.
    """
    try:
        with sync_playwright() as p:
            # Launch browser in headless mode
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            # Navigate to the URL
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            
            # Wait a bit for dynamic content to load
            page.wait_for_timeout(2000)
            
            # Get the page content
            content = page.content()
            
            # Close browser
            browser.close()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            return soup
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
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
    
    if soup is None:
        print("Failed to fetch the page. Exiting...")
        exit(1)
    price_whole = int(soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-whole').get_text().replace(',', '').replace('.', '').strip())
    price_fraction = int(soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-fraction').get_text())
    product_total_price = price_whole + price_fraction / 100
    product_price_symbol = soup.select_one('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-symbol').get_text().strip()
    product_name = soup.find(name="span", class_="a-size-large product-title-word-break").get_text().split()
    product_name = " ".join(product_name).strip()
    print(f"The price of the Product is: {product_price_symbol} {product_total_price:.2f}")
    print(f"Product Name: {product_name}")

    if (product_price_symbol == "$" and product_total_price < 500.00) or (product_price_symbol == "PKR" and product_total_price < 140000.00):
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
        body = f'The price of the product "{product_name}" has dropped to {product_price_symbol} {product_total_price:.2f}.\nCheck it out at:\n {url}'
        send_email(smtp, from_address, to_address, subject, body)
        smtp.quit()
