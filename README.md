# rpi_locator_US

### Instructions for Use:
- clone this repo 
  -  `git clone https://github.com/drippyer/rpi_locator_US`
- navigate to the created directory
  - `cd rpi_locator_US` 
- copy sample credentials to usable filename
  - `cp credentials_SAMPLE.json credentials.json`
- modify created file to reflect your own Gmail credentials
  - `nano credentials.json`
- execute script
  - `python3 scraper.py`

#### CRON
It is heavily recommended to use Cron to automatically run this script on a schedule.

Example: `*/3 * * * *   pi    cd /home/pi/rpi_locator_US && python3 scraper.py`


### Note:
In theory, this should be able to handle any product on the following (US) web stores:
- PiShop
- Vilros
- Chicago Distribution
- Adafruit
- SparkFun
- OKDO
- CanaKit (currently unstable)

To extend this tool's functionality, you are able to add products to specific sites.
