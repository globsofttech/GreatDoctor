import json
import re
from html import unescape
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BROCADE_URL = "https://brocadeofficial.com/collections/tshirts?limit=250"
HUBA_URL = "https://www.hubanepal.com/men"
REQUEST_TIMEOUT = 20


def _price_value(value):
    if value is None:
        return None
    match = re.search(r"\d[\d,]*(?:\.\d+)?", str(value))
    if not match:
        return None
    return float(match.group(0).replace(",", ""))


def _product(product_id, name, price, url, source):
    if price is None or not name:
        return None
    return {
        "id": f"{source}:{product_id or url or name}",
        "name": unescape(str(name)).strip(),
        "price": float(price),
        "url": url,
        "source": source,
    }


def _fetch(url):
    response = requests.get(
        url,
        headers={"User-Agent": "GreatDoctor price monitor/1.0"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.text


def _brocade_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.select("product-card[data-product-id]"):
        title_node = card.select_one("[data-product-title]")
        price_node = card.select_one("product-price")
        link_node = card.select_one("a.product-card__link[href]")
        if not title_node or not price_node:
            continue
        prices = [_price_value(text) for text in price_node.stripped_strings]
        prices = [price for price in prices if price is not None]
        product = _product(
            card.get("data-product-id"),
            title_node.get("data-product-title"),
            min(prices) if prices else None,
            urljoin("https://brocadeofficial.com", link_node["href"])
            if link_node
            else BROCADE_URL,
            "brocade",
        )
        if product:
            products.append(product)
    return products


def _huba_products(html):
    marker = '"productsWithMetaData":{"list":'
    start = html.find(marker)
    if start < 0:
        raise ValueError("Hubanepal product metadata was not found")

    list_start = start + len(marker)
    products, _ = json.JSONDecoder().raw_decode(html[list_start:])
    result = []
    for item in products:
        if "t-shirt" not in item.get("name", "").lower() and "tee" not in item.get(
            "name", ""
        ).lower():
            continue
        discount = item.get("itemDiscount") or {}
        price = discount.get("priceAfterDiscountAmount") or item.get("price")
        product = _product(
            item.get("id"),
            item.get("name"),
            price,
            urljoin(HUBA_URL, f"/product-page/{item.get('urlPart', '')}"),
            "huba",
        )
        if product:
            result.append(product)
    return result


def fetch_products():
    return _brocade_products(_fetch(BROCADE_URL)) + _huba_products(_fetch(HUBA_URL))
