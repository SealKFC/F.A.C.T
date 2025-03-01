import requests
from bs4 import BeautifulSoup

def create_tile(image_path):
    # URL of the server where you want to send the image
    url = "https://www.imgonline.com.ua/eng/make-seamless-texture-result.php"

    # Path to the image file
    # image_path = "C:\\Users\\tyrar\\OneDrive\\Desktop\\Hackathon2025\\flowers.jpg"

    # Custom boundary
    boundary = "geckoformboundary9b7308782dea9d879bdb671f408b1f00"

    # Form data
    form_data = {
        "efset3": "2",
        "efset4": "1",
        "efset6": "4",
        "cropleft": "0",
        "croptop": "0",
        "cropbottom": "0",
        "cropright": "0",
        "efset2": "0",
        "efset": "5",
        "outformat": "2",
        "jpegtype": "1",
        "jpegqual": "92"
    }

    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Referer": "https://www.imgonline.com.ua/eng/make-seamless-texture.php"
    }

    # Read the image file
    with open(image_path, "rb") as image_file:
        files = {"uploadfile": (image_path, image_file, "image/png")}
        # Send the request
        response = requests.post(url, headers=headers, files=files, data=form_data)

    # Print response
    # print(response.status_code)
    # print(response.text)

    #tml_content = "response.text"

    #parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find the link that contains the text "Tile to check texture seamlessness"
    link = soup.find('a', string="Tile to check texture seamlessness")

    # Extract the href attribute (the link)
    if link:
        link_href = link.get('href')
        
        if link_href[:2] == "..":  # Check if the first two characters are ".."
            link_href = "https://imgonline.com.ua" + link_href[2:]  # Replace ".." with "imgonline.com.ua"
    
        print("new Link: " + link_href)
    else:
        print("Link not found")

    # download image from link
    response = requests.get(link_href)
    with open("Resources/tile_image.png", "wb") as f:
        f.write(response.content)


