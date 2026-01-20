# Amazon Price Tracker

Automated price monitoring for Amazon products with email alerts when prices drop below your threshold.

## Prerequisites

- Python 3.13+ (tested with the bundled `venv`)
- PowerShell (for Windows automation via Task Scheduler)
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
playwright install chromium
```

Note: The `playwright install chromium` command downloads the Chromium browser needed for web scraping. This is required for both local and GitHub Actions environments.

3. Configure environment variables in a `.env` file at the project root

```
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_app_password
RECIEVER_EMAIL=destination@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

4. Test manually first

```powershell
python main.py
```

## Automation

This workflow is designed to run automatically on a schedule. Set up automation using:

### Windows Task Scheduler

1. Open Task Scheduler (`taskschd.msc`)
2. Create a new Basic Task
3. Set trigger (e.g., daily at specific time, or every few hours)
4. Action: **Start a program**
   - Program: `C:\Users\YourUser\AppData\Local\Programs\Python\Python313\python.exe` (adjust path)
   - Arguments: `"d:\Portfolio Projects\Amazon-Price-Tracker\main.py"`
   - Start in: `d:\Portfolio Projects\Amazon-Price-Tracker`
5. Save and test the task

### Alternative: GitHub Actions (Cloud-based)

Add `.github/workflows/price-check.yml` with a cron schedule to run in the cloud without keeping your PC on.

Example workflow file:

```yaml
name: Amazon Price Check

on:
  schedule:
    - cron: "0 */6 * * *" # Every 6 hours
  workflow_dispatch: # Allows manual trigger

jobs:
  price-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps chromium

      - name: Run price checker
        env:
          SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
          SENDER_PASSWORD: ${{ secrets.SENDER_PASSWORD }}
          RECIEVER_EMAIL: ${{ secrets.RECIEVER_EMAIL }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
        run: python main.py
```

Remember to add your environment variables as GitHub Secrets in your repository settings.

## How it works

- Uses Playwright to fetch the product page with a real Chromium browser (headless mode).
- This approach is more reliable than requests library, especially in automated environments like GitHub Actions.
- Parses price, currency symbol, and product name with `BeautifulSoup`.
- Prints the current price to the console/log.
- Sends an email alert if the price drops below your configured threshold.
- Runs automatically on your chosen schedule without manual intervention.

## Configuration

- **Product URL:** Edit `url` inside `main.py`.
- **Price threshold:** Adjust the comparison value (currently `< 164000.00`) to your target.
- **Email sender/receiver:** Set via `.env` (`SENDER_EMAIL`, `RECIEVER_EMAIL`). For Gmail, use an App Password and keep 2FA enabled.
- **SMTP host/port:** Defaults to Gmail STARTTLS (`smtp.gmail.com:587`). Change if you use another provider.
- **Schedule frequency:** Configure in Task Scheduler or workflow file based on how often you want to check prices.

## Notes and troubleshooting

- If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before `./venv/Scripts/Activate.ps1`.
- Amazon markup can change; if selectors break, update the CSS selectors in `main.py`.
- Respect Amazon’s Terms of Service and rate limits when scraping.
