import requests




def requester(str):
    url = "azapi.cloudns.ph/api/" + str
    page = requests.get(url=url)
    jsonPage = page.json()

    price = jsonPage["price"]
    productCode = jsonPage["Product Code"]
    name = jsonPage["name"] 
    urlRe = jsonPage["url"]
    return price, name,productCode,urlRe
