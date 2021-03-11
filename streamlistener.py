import tweepy
import traceback

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    
    
    def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            return
        with open("bot_words.txt", "r", encoding="utf-8") as bot_words_file:
            file_contents = bot_words_file.read()
            bot_words = file_contents.splitlines()
        with open("unfavorable_descriptions.txt", "r", encoding="utf-8") as red_flag_words_file:
            file_contents = red_flag_words_file.read()
            red_flag_words = file_contents.splitlines()
        bot_chance = 0
        unfavorable_description = 0
        found_words = []
        unfavorable_words = []
        if tweet.user.description is not None:
            for word in bot_words:
                if word.lower() in tweet.user.description.lower():
                    bot_chance += 20
                    found_words.append(word)
            for word in red_flag_words:
                if word.lower() in tweet.user.description.lower():
                    unfavorable_description += 20
                    unfavorable_words.append(word)
        if bot_chance >= 60:
            bot_string = f"{tweet.user.screen_name} is likely a bot! Reason: Bot chance is at {bot_chance}% with words: {found_words} in description: {tweet.user.description}\n"
            print(bot_string)
            print("\n=====================================\n")
            f = open("bots_found.txt", "a", encoding="utf-8")
            r = open("bots_found.txt", "r", encoding="utf-8")
            current_file = r.read()
            if tweet.user.description not in current_file:
                f.write(bot_string)
            return
        if unfavorable_description >= 60:
            unfavored_string = f"{tweet.user.screen_name} has an unfavorable description and unlikely to produce good content! Words {unfavorable_words} in description: {tweet.user.description}\n"
            print(unfavored_string)
            print("\n=====================================\n")
            f = open("unfavorable_accounts.txt", "a", encoding="utf-8")
            r = open("unfavorable_accounts.txt", "r", encoding="utf-8")
            current_file = r.read()
            if tweet.user.description not in current_file:
                f.write(unfavored_string)
            return
        if not tweet.favorited:
            try:
                tweet.favorite()
                print("Tweet favorited!")
            except Exception as e:
                print("Error while favoriting tweet")
        if not tweet.retweeted:
            try:
                tweet.retweet()
                print("Tweet retweeted!")
            except:
                print("Tweet retweetion failed")
        print("\n=====================================\n")

    def on_error(self, status):
        print(f"Error detected: {status}")
        if status_code == 327:
            return True