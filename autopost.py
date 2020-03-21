import facebook
import tweepy
from selenium import webdriver
import pandas as pd
from os.path import abspath

class AutoPost:
    def __init__(self):
        self.image_path = ""
        self.image_desc = ""
        self.url = ""
    def user_input(self):
        # Enter path image from a internet source or from your local device from the current directory
        self.image_path = input("Enter Path Of The Image (E.g. thor.jpg) : ")
        self.image_desc = input("Write Description Of The Image : ")
        # Enter A Valid URL starting from https or http.
        self.url = input("Enter The URL : ")

    def post_to_facebook(self):
        self.user_input()
        # Enter the access page token of your fb page generated from Graph API of Facebook Developers Site(https://developers.facebook.com/tools/). Token must enclosed between quotes as a string.
        token = 'EAAPaKfEyiSABAKtzmZBai64TdqZAQ56RW2cOsPQRruzOxrOtQWIUB3rvuoV227I5F2pJCP64ZBGTI7lOEC9vPdIgg0ubvnJee7rTx8DZBIJRPxhefRU95pIYg80m4hRPZChYPj5eBUCPcthAlkZADnYWpjvUriZCYhdYkeSjtZAwcgZDZD' #Enter access page token inside these blank quotes.
        fb = facebook.GraphAPI(access_token = token)
        fb.put_photo(image = open(self.image_path, 'rb'), message = self.image_desc + '\n' + self.url)
        print("Successfully Posted Content On Your Facebook Page!!")

    def post_to_twitter(self):
        self.user_input()
        # Enter consumer key, consumer secret key, access token and access secret token of your Twitter handle. Get it from the https://apps.twitter.com/
        # Make sure to put all the token values inside the blank double quotes.
        consumer_key = "o0iBjVWuidJu9WsNofA5q6uWA"
        consumer_secret = "fv5sq7TsBAa4hqg6fM4t8Iuj1RCuKlCxCYdNNz9oaHPHOMIQqA"
        access_token = "966334170539503617-dpwTiliYyRRKMob54qGUHZtJ8Os3BCA"
        access_token_secret = "SePvdqq7ITBhs2a8yFtWhILkmwTF7oopONlia4LmOCrI2"
        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # update the status
        tweet = self.image_desc + '\n' + self.url
        image_path = self.image_path
        status = api.update_with_media(image_path, tweet)
        api.update_status(status = tweet)
        print("Successfully Posted Content On Your Twitter Handle!!")

    def post_to_linkedin(self):
        self.user_input()
        driver = webdriver.Chrome("chromedriver")
        # reading csv file
        df = pd.read_csv("linkedin.csv", encoding='utf-8')
        # reading username
        myUsername = df.Username[0]
        # reading password
        myPassword = df.Password[0]
        absolute_file_path = abspath(self.image_path)
        # driver.get method() will navigate to a page given by the URL address
        driver.get("https://www.linkedin.com/login?")
        username = driver.find_element_by_name('session_key')
        username.send_keys(myUsername)
        password = driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(myPassword)
        log_in_button = driver.find_element_by_class_name('btn__primary--large')
        log_in_button.click()
        start_post = driver.find_element_by_class_name('share-box__trigger')
        start_post.click()
        text = driver.find_element_by_class_name('mentions-texteditor__content')
        # send_keys() to simulate key strokes
        text.send_keys(self.image_desc + "\n" + self.url)
        image = driver.find_element_by_xpath('//*[@data-control-name="share.select_image"]')
        image.click()
        photo = driver.find_element_by_xpath('//*[@data-control-name="select_photo"]').send_keys(absolute_file_path)
        next = driver.find_element_by_xpath('//*[@data-control-name="confirm_selected_photo"]')
        next.click()
        post = driver.find_element_by_xpath('//*[@data-control-name="share.post"]')
        post.click()
        print("Successfully Posted Content On Your LinkedIn Page!!")


if __name__ == '__main__':
    ap = AutoPost()
    while(True):
        app = input("Where do you want to post your content? (facebook, twitter, linkedin or exit)\n")
        if app == 'facebook':
            ap.post_to_facebook()
        elif app == 'twitter':
            ap.post_to_twitter()
        elif app == 'linkedin':
            ap.post_to_linkedin()
        elif app == 'exit':
            break
        else:
            print("\nInvalid Appname. Please Try Again!\n")
            continue
        ch = input("\nWanna Add More Content?(y/n)\n")
        if ch == 'n':
            break
