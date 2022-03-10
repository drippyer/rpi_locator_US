from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import smtplib
from email.mime.text import MIMEText

import json
parser = "html.parser"

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


def site_search(site_dict):
    site = site_dict["name"]
    abbr = site_dict["short"]
    url_base = site_dict["url"]
    id_dict = site_dict["ids"]

    if abbr == "spark":
        output = {k: {"available": sparkfun_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    elif abbr == "vil":
        output = {k: {"available": vilros_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    elif abbr == "chi":
        output = {k: {"available": chidist_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    elif abbr == "ada":
        output = {k: {"available": adafruit_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    elif abbr == "okdo":
        output = {k: {"available": okdo_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    elif abbr == "pishop":
        output = {k: {"available": pishop_single(f"{url_base}{v}"),"url": f"{url_base}{v}"} for k, v in id_dict.items()}
    else:
        output = {"error": "UNCAUGHT"}
    
    print(f"Scraped {site} {' ' * 12}", end='\r')
    return output


def main():
    stock = {sites[k]["name"]: site_search(sites[k]) for k, v in sites.items()}

    sender = creds["username"]
    gmail_pass = creds["password"]
    recipient = creds["recipient"]
    #recipient = creds["recipient_test"]

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(sender, gmail_pass)

    for k, v in stock.items():
        for k2, v2 in v.items():
            if v2["available"] is True:
                subject = f"[!] {pi_names[k2]} at {k}!\n"
                msg = MIMEText(v2['url'])
                msg["Subject"] = subject
                msg["From"] = sender
                msg["To"] = recipient
                s.sendmail(sender, [recipient], msg.as_string())
            else:
                subject = f"{pi_names[k2]} not at {k}...\n"
            print(subject)

    s.quit()

with open("pi_names.json") as json_file:
    pi_names = json.load(json_file)

with open("sites.json") as json_file:
    sites = json.load(json_file)

with open("credentials.json") as json_file:
    creds = json.load(json_file)

main()

