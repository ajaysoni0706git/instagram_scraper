import getpass
import time
import os
from modules.insta_fetchUrl import get_latest_instagram_post
from modules.insta_fetchCapImage import get_postCapImage
from modules.caption_tweet import summarize_with_chatgpt
from modules.post_tweet import post_tweet


def main():
    try:
        # taking user input
        target_username = input("Enter the Instagram username to fetch the latest post: ").strip()

        twitter_acc_login = input("Do you want to use your X.com (Twitter) account for posting? (y/n): ").strip().lower()
        if twitter_acc_login == "y":
            twitter_username = input("Enter your X.com (Twitter) username: ").strip()
            twitter_password = getpass.getpass("Enter your X.com (Twitter) password: ").strip()
        else:
            twitter_username = "abc_test12345"  #this is a dummy account for testing
            twitter_password = "Test@1234567890"
        
        if not target_username or not twitter_username or not twitter_password:
            print("Error: All fields are required!")
            return
        
        # Step 1: Fetch latest Instagram post URL
        print("Fetching the latest Instagram post...")
        post_url = get_latest_instagram_post(target_username)
        
        if not post_url:
            print("Failed to retrieve the latest Instagram post.")
            return
        print(f"Latest post URL: {post_url}")
        
        # Step 2: Extract caption and image from the post
        print("Extracting caption and image...")
        caption = get_postCapImage(post_url)
        image_path = "latest_instagram_post.jpg"
        
        if not os.path.exists(image_path):
            print("Image download failed!")
            return
        
        if not caption:
            print("No caption found. Using default text.")
            caption = "New Instagram post! Check it out!"
        elif caption == "No caption found.":
            print("No caption found. Using default text.")
            caption = "New Instagram post! Check it out!"    
        print(f"Caption Extracted: {caption}")
        
        # Step 3: Summarize caption for a tweet
        print("Summarizing caption for Twitter...")
        tweet = summarize_with_chatgpt(caption)
        
        if not tweet or "Error:" in tweet:
            print("Failed to generate a tweet. Using original caption.")
            tweet = caption[:280]  # Ensure it fits within 280 characters
        print(f"Tweet: {tweet}")
        
        # Step 4: Post tweet with image
        print("Posting tweet...")
        response = post_tweet(twitter_username, twitter_password, tweet, image_path)
        
        if response:
            print("Tweet posted successfully!")
        else:
            print("Failed to post the tweet.")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        time.sleep(2)
        print("Process completed.")

if __name__ == "__main__":
    main()
