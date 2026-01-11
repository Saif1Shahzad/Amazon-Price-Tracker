# Amazon Price Tracker

Track a single Amazon product, print its current price, and email yourself when it drops below your threshold.

## Prerequisites

- Python 3.13+ (tested with the bundled `venv`)
- PowerShell (for the activation command examples)
- An email account with SMTP access (Gmail app password recommended)

## Setup

1. Create and activate a virtual environment (PowerShell)

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure environment variables in a `.env` file at the project root

```
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_app_password
RECIEVER_EMAIL=destination@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

4. Run the scraper

```powershell
python main.py
```

## How it works

- Fetches the product page with a desktop User-Agent to reduce blocking.
- Parses price, currency symbol, and product name with `BeautifulSoup`.
- Prints the current price to the console.
- Sends an email alert if the price is below your configured threshold in `main.py`.

## Configuration

- **Product URL:** Edit `url` inside `main.py`.
- **Price threshold:** Adjust `product_total_price < 100000.00` to your target.
- **Email sender/receiver:** Set via `.env` (`SENDER_EMAIL`, `RECIEVER_EMAIL`). For Gmail, use an App Password and keep 2FA enabled.
- **SMTP host/port:** Defaults to Gmail STARTTLS (`smtp.gmail.com:587`). Change if you use another provider.

## Notes and troubleshooting

- If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before `./venv/Scripts/Activate.ps1`.
- Amazon markup can change; if selectors break, update the CSS selectors in `main.py`.
- Respect Amazon’s Terms of Service and rate limits when scraping.
