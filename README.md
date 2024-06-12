
# eBay Web Scraper - Telegram Bot 🤖🛍️

#### By Antonio Bertolini (Code in Place 2024, Stanford University)




## Introduction
My project is a Python script that employs the requests library for communicating with the Telegram API and the BeautifulSoup library for parsing HTML content during web scraping of eBay. Additionally, it utilizes the os and dotenv libraries for handling environment variables, ensuring secure access to sensitive data like API tokens. These libraries collectively enable the script to receive user queries from a Telegram channel, search eBay for relevant products, and then share the most cost-effective findings back to the same Telegram channel. The goal is to offer users a streamlined way to discover budget-friendly items on eBay without manual browsing.



## Features

- Real-time scraping of eBay search results.
- Filtering and sorting of items based on price.
- Automatic sending of search results to a specified Telegram chat.
- Sanitization of user input to prevent injection attacks.
- Continuous monitoring of Telegram messages to respond promptly.


## How It Works

#### 1. Loading Environment Variables
The bot loads the Telegram bot token, chat ID, and email from a .env file using os and dotenv.
#### 2. Receiving Messages
The bot continuously monitors Telegram for new messages using the requests library.
#### 3. Sanitizing Input
User input is sanitized using regular expressions to ensure safe and valid search queries.

#### 4. Scraping eBay
The bot scrapes eBay search results using requests and BeautifulSoup, filtering and sorting items based on price.

#### 5. Sending Results
The best deal found is sent to the user via Telegram using the requests library.
## Getting Started
#### Quick guide

### 1. Create a Telegram Bot with BotFather

To create a Telegram bot, you'll need to use BotFather, a special bot that helps you create and manage your own bots.

#### Start a chat with BotFather:
   - Open Telegram and search for `BotFather`.
   - Start a chat with BotFather by clicking on the `Start` button.

**Create a new bot:**
   - Send the `/newbot` command to BotFather.
   - Follow the instructions to choose a name and username for your bot.
   - Once created, BotFather will provide you with a token. This token is needed to        interact with the Telegram API.

**Copy the Bot Token:**
   - Save the token provided by BotFather. You'll need to add this token to your `.env` file.

### 2. Clone the Repository:
#### git clone 
- https://github.com/tonyisdoingResearch/eBay-Scraper-Bot-for-Telegram.git

### 3. Create a .env File:
#### .env file content

- BOT_TOKEN=your_telegram_bot_token
- CHAT_ID=your_telegram_chat_id
- EMAIL=your_email_address

### 4. Install Dependencies
#### Install all Dependencies in one go
- pip install requests beautifulsoup4 python-dotenv
#### requests
- pip install requests
#### BeautifulSoup
- pip install beautifulsoup4
#### dotenv
- pip install python-dotenv
## Libraries and Technologies Used
#### requests
The requests library is used to handle HTTP requests. It simplifies the process of making GET and POST requests, which are essential for interacting with eBay and Telegram APIs.

#### Why requests?
- Easy to use and well-documented.
- Provides a simple interface for sending HTTP requests and handling responses.
- Supports HTTPS connections.

#### BeautifulSoup
BeautifulSoup is a library used for parsing HTML and XML documents. It helps in extracting data from web pages, making it easier to navigate and search through HTML elements.

#### Why BeautifulSoup?
- Intuitive API for parsing HTML.
- Robust and flexible, allowing for easy data extraction.
- Handles different types of HTML documents and can work with various parsers.

#### os
The os module provides a way to interact with the operating system. In this project, it is used to manage environment variables securely.

#### Why os?
- Facilitates interaction with the underlying operating system.
- Provides a simple way to handle environment variables.

#### dotenv
dotenv is used to read environment variables from a .env file. This is crucial for keeping sensitive information such as API keys and tokens secure.

#### Why dotenv?
- Keeps configuration separate from code.
- Simplifies the management of environment variables.

#### re
The re module provides support for regular expressions in Python. It is used for sanitizing user input to prevent injection attacks.

#### Why re?
- Powerful pattern matching capabilities.
- Essential for text processing and validation.

#### Why time?
- Provides various functions for working with time.
- Useful for adding delays and measuring execution time.



## License

[MIT](https://choosealicense.com/licenses/mit/)

