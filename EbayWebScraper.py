import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
import re




"""

 ______     ______     ______     __  __        __     __     ______     ______        ______     ______     ______     ______     ______   ______     ______    
/\  ___\   /\  == \   /\  __ \   /\ \_\ \      /\ \  _ \ \   /\  ___\   /\  == \      /\  ___\   /\  ___\   /\  == \   /\  __ \   /\  == \ /\  ___\   /\  == \   
\ \  __\   \ \  __<   \ \  __ \  \ \____ \     \ \ \/ ".\ \  \ \  __\   \ \  __<      \ \___  \  \ \ \____  \ \  __<   \ \  __ \  \ \  _-/ \ \  __\   \ \  __<   
 \ \_____\  \ \_____\  \ \_\ \_\  \/\_____\     \ \__/".~\_\  \ \_____\  \ \_____\     \/\_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\    \ \_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/\/_/   \/_____/      \/_/   \/_/   \/_____/   \/_____/      \/_____/   \/_____/   \/_/ /_/   \/_/\/_/   \/_/     \/_____/   \/_/ /_/ 

By Antonio Bertolini (CODE IN PLACE 2024/Standford University)            
"""


# Load environment variables from the data.env file
load_dotenv('data.env')

# Retrieve the bot token, chat ID, and email from environment variables
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
email = os.getenv('EMAIL')

# Print environment variables, masking sensitive information
print(f"BOT_TOKEN: {'*' * len(bot_token)}")
print(f"CHAT_ID: {'*' * len(str(chat_id))}")
print(f"EMAIL: {'*' * len(email)}")

# Define the headers for HTTP requests
# Including an appropriate User-Agent to avoid being blocked by the website during scraping
headers = {
    "User-Agent": f"TelegramBot/0.1 ({email})"
}

# Function to sanitize user input by removing non-alphanumeric characters
# This helps prevent injection attacks and ensures the search query is URL-compatible
def sanitize_input(text):
    sanitized_text = re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()
    return sanitized_text

# Function to send a message to the Telegram bot
def send_message_to_telegram(text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        'parse_mode': 'Markdown'  # Use Markdown format for the message
    }
    # Make a POST request to the Telegram API to send the message
    response = requests.post(url, data=data)
    return response.json()  # Return the JSON response

# Function to get the latest message received by the Telegram bot
# Using offset helps avoid receiving duplicate messages
def get_latest_message(offset=None):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {'offset': offset} if offset else {}  # Add offset to parameters if it exists
    response = requests.get(url, params=params)  # Make a GET request to the Telegram API
    if response.status_code == 200:  # Check if the request was successful
        data = response.json()  # Convert the response to JSON
        if 'result' in data and data['result']:  # Check if there are results in the response
            latest_update = data['result'][-1]  # Get the latest update
            message_id = latest_update['update_id']  # Get the message ID
            message_text = latest_update['message'].get('text')  # Get the message text
            return message_id, message_text  # Return the message ID and text
    return None, None  # Return None if there are no messages

# Function to scrape search results from eBay for a given query
def scrape_ebay_search(query):
    # Keywords excluded from search results
    # These terms are common in sponsored results and are not relevant to the user
    excluded_keywords = ["Shop on eBay", "....", "...."]  
    sanitized_query = sanitize_input(query)  # Sanitize the user's query
    url = f"https://www.ebay.com/sch/i.html?_nkw={sanitized_query}"
    response = requests.get(url, headers=headers)  # Make a GET request to the eBay search page

    if response.status_code == 200:  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content with BeautifulSoup
        items = soup.select(".s-item")  # Select elements that represent search results
        item_list = []

        for item in items:
            title = item.select_one(".s-item__title")  # Get the item's title
            price = item.select_one(".s-item__price")  # Get the item's price
            link = item.select_one(".s-item__link")  # Get the item's link

            if title and price and link:  # Check if title, price, and link are present
                item_title = title.get_text(strip=True)  # Get the text of the title
                if any(excluded_keyword.lower() in item_title.lower() for excluded_keyword in excluded_keywords):
                    continue  # Skip this item if it contains any of the excluded keywords

                # Remove dollar signs and commas from the price and convert to float
                # Some prices can be ranges (e.g., "10 to 20"), so take only the first value
                price_text = price.get_text(strip=True).replace("$", "").replace(",", "")
                if "to" in price_text:
                    price_text = price_text.split("to")[0].strip()  # Take only the first price if there are two
                try:
                    price_value = float(price_text)
                    item_list.append({
                        "title": item_title,
                        "price": price_value,
                        "link": link['href']
                    })
                except ValueError:
                    continue  # Skip this item if the price is not valid

        # Filter and sort items by price
        item_list = [item for item in item_list if item['price'] > 0]  # Exclude items with invalid prices
        item_list.sort(key=lambda x: x['price'])  # Sort items by price in ascending order

        if item_list:  # If there are valid items
            # Calculate the average price of the items
            average_price = sum(item['price'] for item in item_list) / len(item_list)
            
            # Find the cheapest item that is at least 40% of the average price
            # So that the item is not an outlier with an unusually low price (e.g., a scam, fake item, etc.) [Optional]
            cheapest_item = next((item for item in item_list if item['price'] >= average_price * 0.4), None)

            if cheapest_item:  # If a valid item was found
                # Prepare the message in Markdown format for Telegram
                message = f"{cheapest_item['title']}\nPrice: ${cheapest_item['price']}\n[Link to the item]({cheapest_item['link']}) 💰"
                response = send_message_to_telegram(message)  # Send the message to Telegram
                if response.get('ok'):
                    print("Message sent to Telegram")
                else:
                    print(f"Error sending message to Telegram: {response}")
            else:
                print("No items found or all items have invalid prices.")
        else:
            print("No valid items found.")
            # Send a message to Telegram if no valid items were found
            send_message_to_telegram("No valid items found. Please try again with a different search query. 🛒🔍")
    else:
        print(f"Request error: {response.status_code}")

# Main function to continuously monitor messages on Telegram and respond
def main():

    counter = 0
    last_update_id = None
    # Send a welcome message to the user
    send_message_to_telegram("Welcome to the eBay Web Scraper Bot! 🤖🛍️\n\nPlease enter the product title you want to search for on eBay. 🔍")

    while True:
        latest_message_id, latest_message_text = get_latest_message(last_update_id)
        if latest_message_id:
            # Update the last processed message ID to avoid processing duplicate messages
            last_update_id = latest_message_id + 1

            if latest_message_text:
                print(f"Received message from user: {latest_message_text}")  # Debugging print
                scrape_ebay_search(latest_message_text)  # Start the eBay search with the received message text
                time.sleep(1)  # Wait for a second to avoid rate limiting by Telegram's API
        else:
            # Print a message every 10 iterations to indicate the bot is running
            counter += 1
            if counter % 10 == 0:
                print("No new messages.")  # Debugging print

if __name__ == "__main__":
    main()
