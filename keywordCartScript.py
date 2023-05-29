import requests
import time

siteUrl = "https://[DOMAIN].com"           #domain of site that will be monitored
discordWebhook = "YOUR DISCORD WEBHOOK URL"             #discord webhook url where embed will be sent
keyWords = ['Keyword 1','Keyword 2','Keyword 3']        #keywords which script will look for
monitorDelay = 3                                        #delay for checking endpoint
quantity = 2                                            #quantity of each item that will be carted


def sendDiscord(cartLink):                                  #Sends 'Add to Cart' Link to desired Discord Channel
    print("Sending Discord Webhook.")

    embed = {
        "embeds": [
            {
                "color": 3946197,
                "fields": [
                    {
                        "name": "Shopify Scraper Product Found!",
                        "value": f"{cartLink}"
                    }
                ]
            }
        ],
        "attachments": []
    }

    try:
        webhookResponse = requests.post(url=discordWebhook,json=embed)
        if webhookResponse.ok == True:
            print(f"Webhook Sent Successfully [{webhookResponse.status_code}]")
        else:
            print(f"Webhook Sent Failed [{webhookResponse.status_code}]")

    except:
        print("Request timed out")

def addToCartLink(pidArray):                                #creates 'add to cart' link by using domain, product IDs and quantity.
    print("Creating Cart Link")

    cartLink = f"{siteUrl}/cart/"

    for item in pidArray:
        cartLink += (str(item) + f':{quantity},')

    print(cartLink)
    return cartLink

def scrape():

    productsFound = False

    while (productsFound == False):                         #Loops until product is found.


        print("Attempting Check End Point.")
        try:
            endpoint = requests.get(f"{siteUrl}/products.json")         #GET request to check shopify product page endpoint.

            if endpoint.ok == False:
                print(f"Password Page Up/Rate Limited [{endpoint.status_code}]")

            else:

                pidArray = []

                print(f"Password Page Down [{endpoint.status_code}]")
                products = endpoint.json()['products']

                for z in products:
                    foundHandle = z['title']

                    for x in keyWords:
                        if x in foundHandle:                        #Compares Keywords to product names found.
                            pid = z['variants'][0]['id']
                            print(f"Product Found! PID: {pid}")
                            pidArray.append(pid)

                        else:
                            pass

            if len(pidArray) == 0:                                 #If product is not found yet, delay is applied then loop will continue
                print("Product Not Found. Retrying.")
                time.sleep(monitorDelay)

            else:
                productsFound = True                               #When product/s is found loop will stop
                print(f"PIDS Found. {pidArray}")
                return pidArray

        except:
            print("Request timed out. Retrying.")
            time.sleep(monitorDelay)
            
def start():                                        #Start function which prints out all keywords provided and monitor delay.
    print("Keywords:")
    for x in keyWords:
        print(f"{x}")
    print(f"Monitor Delay: {monitorDelay}(s)\n")


#---------------------------------Start-------------------------------------------

if __name__ == "__main__":
    start()
    pidArray = scrape()
    cartLink = addToCartLink(pidArray)
    sendDiscord(cartLink)

