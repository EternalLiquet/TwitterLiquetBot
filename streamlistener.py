import tweepy
import traceback

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def return_divider(self):
        return "\n=====================================\n"

    def return_bot_string(self, tweet, bot_chance, found_words):
        return f"{tweet.user.screen_name} is likely a bot! Reason: Bot chance is at {bot_chance}% with words: {found_words} in description: {tweet.user.description}\n"

    def return_unfavorable_desc_string(self, tweet, unfavorability_index, found_words):
        return f"{tweet.user.screen_name} has an unfavorable description at {unfavorability_index} and unlikely to produce good content! Words {found_words} in description: {tweet.user.description}\n"

    def return_favorable_desc_string(self, tweet, favorability_index, found_words):
        return f"{tweet.user.screen_name} has a description score of {favorability_index}. Words {found_words} in description: {tweet.user.description}\n"

    def determine_bot_chance(self, tweet):
        bot_chance = 0
        found_words = []
        with open("bot_words.txt", "r", encoding="utf-8") as bot_words_file:
            file_contents = bot_words_file.read()
            bot_words = file_contents.splitlines()
        if tweet.user.description is not None:
            for word in bot_words:
                if word.lower() in tweet.user.description.lower():
                    bot_chance += 20
                    found_words.append(word)
        if bot_chance >= 60:
            print(self.return_bot_string(tweet, bot_chance, found_words))
            print(self.return_divider())
            with open("bots_found.txt", "a+", encoding="utf-8") as bots_found_file:
                bots_found_file.seek(0)
                current_file = bots_found_file.read()
                if tweet.user.description not in current_file:
                    bots_found_file.write(self.return_bot_string(tweet, bot_chance, found_words))
        return bot_chance
    
    def determine_unfavorability(self, tweet):
        unfavorability_index = 0
        found_words = []
        with open("red_flag_words.txt", "r", encoding="utf-8") as red_flag_words_file:
            file_contents = red_flag_words_file.read()
            red_flag_words = file_contents.splitlines()
        if tweet.user.description is not None:
            for word in red_flag_words:
                if word.lower() in tweet.user.description.lower():
                    unfavorability_index += 15
                    found_words.append(word)
        if unfavorability_index >= 60:
            print(self.return_unfavorable_desc_string(tweet, unfavorability_index, found_words))
            print(self.return_divider())
            with open("unfavorable_accounts.txt", "a+", encoding="utf-8") as unfavorable_acc_file:
                unfavorable_acc_file.seek(0)
                current_file = unfavorable_acc_file.read()
                if tweet.user.description not in current_file:
                    unfavorable_acc_file.write(self.return_unfavorable_desc_string(tweet, unfavorability_index, found_words))
            with open("unfavorable_descriptions_only.txt", "a+", encoding="utf-8") as descriptions_file:
                descriptions_file.seek(0)
                current_file = descriptions_file.read()
                if tweet.user.description not in current_file:
                    descriptions_file.write(f"{tweet.user.description}\n")
        return unfavorability_index

    def determine_favorability(self, tweet):
        favorability_index = 0
        found_words = []
        with open("favorable_words.txt", "r", encoding="utf-8") as favorable_words_file:
            file_contents = favorable_words_file.read()
            favorable_words = file_contents.splitlines()
        if tweet.user.description is not None:
            for word in favorable_words:
                if word.lower() in tweet.user.description.lower():
                    favorability_index += 10
                    found_words.append(word)
            print(self.return_favorable_desc_string(tweet, favorability_index, found_words))
            print(self.return_divider())
            if favorability_index >= 50:
                with open("favorable_descriptions.txt", "a+", encoding="utf-8") as favorable_desc_file:
                    favorable_desc_file.seek(0)
                    current_file = favorable_desc_file.read()
                    if tweet.user.description not in current_file:
                        favorable_desc_file.write(f"{tweet.user.description}\n")
        return favorability_index
    
    def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if (self.determine_bot_chance(tweet) >= 60):
            return
        if ((self.determine_unfavorability(tweet) - self.determine_favorability(tweet)) >= 60):
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
        print(self.return_divider())

    def on_error(self, status):
        print(f"Error detected: {status}")
        if status_code == 327:
            return True