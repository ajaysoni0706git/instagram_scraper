Instagram Scraper & Auto-Poster

Setup & Run Instructions

First make sure to have latest python version 3.13 

Follow the steps below to set up and run the project in VS Code PowerShell Terminal:

**Skip First Step(Step 1)

Step 1: Create and Activate a Virtual Environment

    Open VS Code and run the following commands in the PowerShell Terminal:

    python -m venv venv                              # Create a virtual environment
    Set-ExecutionPolicy Unrestricted -Scope Process  # Allow script execution
    venv\Scripts\activate                            # Activate the virtual environment
**Skip First Step(Step 1)


Step 2: Install Required Libraries

    Once the virtual environment is activated, install the necessary dependencies by running:

    pip install -r requirements.txt

    This command will install all required libraries for Instagram scraping.

Step 3: Run the Main Script

    After installing the dependencies, execute the script by running:

    python main.py

Step 4: Provide Input for Scraping & Posting

    The script will prompt you to enter the Instagram account username from which you want to scrape the latest post.

    Next, it will ask whether you want to post the scraped content to your own Instagram account:

    If you choose "Yes", it will prompt you to enter your login credentials (password input is hidden for security).

    If you choose "No", it will proceed using a dummy test account created specifically for testing.

Step 5: Automatic Image Update

    The latest Instagram post image will be saved in the project folder as:

    latest_instagram_post.jpg

    This file will automatically update each time you run the script with the most recent post image from the specified Instagram account.

Project Features

    Scrapes the latest post image and caption from any Instagram account. Option to automatically post the content to another Instagram account. Uses secure credential input (password is hidden). Dummy account available for testing purposes. The latest image is automatically updated in latest_instagram_post.jpg.

Project Structure & File Descriptions

    This project is divided into five main scripts, each handling a specific functionality:

    insta_fetchUrl.py

        Fetches the latest Instagram post URL from the specified account.

        Uses Selenium to navigate Instagram and extract the post link.  

    insta_fetchCapImage.py

        Extracts the caption and image URL from the latest post.

        Uses Selenium to dismiss the login popup and retrieve post details.

        Downloads the image and saves it as latest_instagram_post.jpg.

    caption_tweet.py

        Cleans and processes the extracted caption.

        Removes extra spaces, line breaks, and emojis for better readability.

    post_tweet.py

        Posts the cleaned caption and image to Twitter/X.

    main.py

        The central script that runs all the above functionalities in sequence.

        Prompts the user for an Instagram account to scrape.

        Asks whether to post on Instagram and collects login credentials if needed.


