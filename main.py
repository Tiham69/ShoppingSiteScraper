import requests, os, schedule, smtplib, time
from bs4 import BeautifulSoup
from replit import db
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 

def sendMail(priceTag, product_url, nameTag):
  username = os.environ['mailUsername']
  password = os.environ['mailPassword']
  email = f"""
  <p>Price droped to {priceTag} on your favorite outware.<a href="{product_url}"> click here </a> 
  """
  server = "smtp.gmail.com"
  port = 587
  s = smtplib.SMTP(host=server, port=port)
  s.starttls()
  s.login(username, password)

  msg = MIMEMultipart()
  msg['To'] = username
  msg['From'] = username
  msg['Subject'] = nameTag
  msg.attach(MIMEText(email, 'html'))
  s.send_message(msg)
  del msg
  

def getItemPrice(product_url):
  
  response = requests.get(product_url)
  # print(response)
  html = response.text
  # print(html)
  soup = BeautifulSoup(html, "html.parser")
  # print(soup)
  nameTag = soup.find_all("h4", {"class": "tiny-margin"})
  priceTag = soup.find_all("span", {"class": "price_field"})
  # print(nameTag[0].text, priceTag[0].text)
  nameTag = nameTag[0].text
  priceTag = priceTag[0].text
  keys = db.keys()
  for key in keys:
    # print(key, db[key])
    try:
      # print("try", key, nameTag)
      if key == nameTag:
        # print("2nd", db[key], priceTag)
        if db[key] < priceTag:
          # print("ok")
          sendMail(priceTag, product_url, nameTag)
          return True
        else:
          # print("not so")
          return False
    except:
      # print("error")
      return 1
    
  db[nameTag] = priceTag

def scheduleSend():
  product_url = "https://fabrilife.com/product/72744-mens-chino-pant-tan"
  
  print("Checking URL...\n")
  time.sleep(1)
  print("Found Product 👍\n")
  time.sleep(1)
  print("Sending Mail...\n")
  if getItemPrice(product_url):
    print("Sent")
  else:   
    print("🚫  Not Sent  🚫")
    time.sleep(1)

schedule.every(24).hours.do(scheduleSend)

while True:
  schedule.run_pending()
  time.sleep(3600)
  os.system("clear")



# https://fabrilife.com/product/72461-premium-cuban-shirt-petra