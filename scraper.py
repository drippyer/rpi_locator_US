from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
parser = "html.parser"

import json

from email.mime.text import MIMEText
import smtplib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def sparkfun_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        row = soup.find("div", {"class": "product-title"})
        stock = row.find("span", {"class": "visuallyhidden"}).string.strip()
    except:
        stock = ""
    available = False if stock == "Out of stock" else True
    return available


def vilros_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        row = soup.find("div", {"class": "payment-buttons"})
        stock = row.find("span").string.strip()
    except:
        stock = ""
    available = False if stock == "Sold Out" else True
    return available


def chidist_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        stock = soup.find("span", {"class": "sold_out"}).string.strip()
    except:
        stock = ""
    available = False if stock == "Sold Out" else True
    return available


def adafruit_single(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}))
    soup = BeautifulSoup(page, parser)
    try:
        stock = soup.find("div", {"class": "oos-header"}).string.strip()
    except:
        stock = ""
    available = False if stock == "Out of stock" else True
    return available


def okdo_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        row = soup.find("div", {"id": "product-main"})
        stock = row.find("span", {"class": "c-stock-level"}).string.strip()
    except:
        stock = ""
    available = False if stock == "Out of stock" else True
    return available


def pishop_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        row = soup.find("input", {"id": "form-action-addToCart"})
        stock = row["value"].strip()
    except:
        stock = ""
    available = False if stock == "Out of stock" else True
    return available


def canakit_single(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, parser)
    try:
        row = soup.find("div", {"id": "ProductAddToCartDiv"})
        stock = row.find("a").string.strip()
    except:
        stock = ""
    available = False if stock == "Sold Out" else True
    return available


def site_search(site_dict):
    site = site_dict["name"]
    abbr = site_dict["short"]
    url_base = site_dict["url"]
    id_dict = site_dict["ids"]

    print(f"Scraping {site} {' ' * 11}")

    if abbr == "spark":
        output = {k: {"available": sparkfun_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "vil":
        output = {k: {"available": vilros_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "chi":
        output = {k: {"available": chidist_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "ada":
        output = {k: {"available": adafruit_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "okdo":
        output = {k: {"available": okdo_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "pishop":
        output = {k: {"available": pishop_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    elif abbr == "cana":
        output = {k: {"available": canakit_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items() if k not in ignore}
    else:
        output = {"error": "UNCAUGHT"}
    
    print(f"Scraped {site} {' ' * 12}")
    return output


def main():
    stock = {sites[k]["name"]: site_search(sites[k]) for k, v in sites.items()}

    sender = creds["username"]
    gmail_pass = creds["password"]
    recipients = creds["recipients"]

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(sender, gmail_pass)

    for k, v in stock.items():
        for k2, v2 in v.items():
            if v2["available"] is True:
                subject = f"[!] {pi_names[k2]} at {k}!"
                msg = MIMEText(v2['url'])
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = recipients[0]
                s.sendmail(sender, recipients, msg.as_string())
            else:
                subject = f"{pi_names[k2]} not at {k}..."
            print(subject)

    s.quit()

with open("pi_names.json") as json_file:
    pi_names = json.load(json_file)

with open("sites.json") as json_file:
    sites = json.load(json_file)

with open("credentials.json") as json_file:
    creds = json.load(json_file)

with open("device_ignore.json") as json_file:
    device_ignore = json.load(json_file)
    ignore = device_ignore["ignore"]


main()
