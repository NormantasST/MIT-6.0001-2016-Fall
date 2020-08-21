# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Normantas
# Collaborators: None
# Time: 4-7hours

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import copy
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        """Initializes NewsStory Object"""
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def  get_guid(self):
        """Returns string, Global unique identifier of NewsStory Object"""
        return self.guid
    
    def get_title(self):
        """Returns string, title of NewsStory Object"""
        return self.title
    
    def get_description(self):
         """Returns string, decription of NewsStory Object"""
         return self.description
         
    def get_link(self):
        """Returns string, link of NewsStory Object"""
        return self.link
         
    def get_pubdate(self):
        """Returns shallow copy of DateTime object, Date of published of NewsStory Object"""
        return copy.copy(self.pubdate)
    
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    
    def __init__(self, phrase):
        """Initializes Phrase Trigger
        input: phrase (string)"""
        self.phrase = phrase.lower()
        PhraseTrigger.regex_splitter = "(^|$|\s+)"
        
    def build_regex(self):
        regex = r"" + PhraseTrigger.regex_splitter
        for word in self.phrase.split():
            regex += word + PhraseTrigger.regex_splitter
        return regex
    
    @staticmethod
    def create_empty_space_lines_for_str_translate(word):
        """Creates empty lines to be used to replace letters or symbols
        with whitespace: "ABC" => "   ", "!@" => "  "
        """
        output = ""
        for letter in word:
            output += " "
        return output
    
    def is_phrase_in(self, text):
        """Returns True if phrase is in text
        returns False if phrase is not in text"""
        text = text.lower()
        text = text.translate(str.maketrans(string.punctuation, PhraseTrigger.create_empty_space_lines_for_str_translate(string.punctuation)))
        return bool(re.search(self.build_regex(), text))

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """Initializes TitleTrigger"""
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, news_story):
        """Evaluates if a trigger should be raised"""
        return self.is_phrase_in(news_story.get_title())
    
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """Initializes TitleTrigger"""
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, news_story):
        """Evaluates if a trigger should be raised"""
        return self.is_phrase_in(news_story.get_description())


class TimeTrigger(Trigger):
    def __init__(self, time):
        """Initializes TimeTrigger object
        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S"."""
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        time = time.replace(tzinfo=pytz.timezone("EST"))
            
        self.time = time
        
    def update_story(story):
        story_date = story.get_pubdate()
        story_date = story_date.replace(tzinfo=pytz.timezone("EST"))
        return story_date
    
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):   
        """Initializes BeforeTrigger Object"""
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        story_date = TimeTrigger.update_story(story)
        return bool(story_date < self.time)
    
class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        """Initializes AfterTrigger Object"""
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        story_date = TimeTrigger.update_story(story)
        return bool(story_date > self.time)


    # COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, opposite_trigger):
        """The trigger is being called
        when it reason to be called is opposite to another trigger"""
        self.trigger = opposite_trigger
    
    def evaluate(self, story):
        """Only being called if the given trigger is false"""
        return not self.trigger.evaluate(story)
    
class AndTrigger(Trigger):
    def __init__(self,first_trigger, second_trigger):
        """Trigger takes in 2 triggers"""
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger
    
    def evaluate(self, story):
        """Is being called when the both given triggers are returned True"""
        return self.first_trigger.evaluate(story) and self.second_trigger.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self,first_trigger, second_trigger):
        """Trigger takes in 2 triggers"""
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger
    
    def evaluate(self, story):
        """Returns True if ANY of 2 given triggers in the constructor returns True"""
        return self.first_trigger.evaluate(story) or self.second_trigger.evaluate(story)
    
#======================
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    trigered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                trigered_stories.append(story)
                continue;
    return trigered_stories



#======================
# User-Specified Triggers
#======================



def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    n-complexity
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    trigger_dict = {}
    trigger_list = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
            
            #Creates a trigger
            line_elements = line.split(",")
            trigger = None
            if line_elements[0] == "ADD":
                for element_index in range(1, len(line_elements)):
                    trigger_list.append(trigger_dict[line_elements[element_index]])
            else:
                if line_elements[1] == "TITLE":
                    trigger = TitleTrigger(line_elements[2])
                    
                elif line_elements[1] == "DESCRIPTION":
                    trigger = DescriptionTrigger(line_elements[2])
                    
                elif line_elements[1] == "AFTER":
                    trigger = AfterTrigger(line_elements[2]) 
                    
                elif line_elements[1] == "BEFORE":
                    trigger = BeforeTrigger(line_elements[2]) 
                    
                elif line_elements[1] == "OR":
                    trigger = OrTrigger(trigger_dict[line_elements[2]], trigger_dict[line_elements[3]])
                    
                elif line_elements[1] == "NOT":
                    trigger = NotTrigger(trigger_dict[line_elements[2]])
                    
                elif line_elements[1] == "AND":
                    trigger = AndTrigger(trigger_dict[line_elements[2]], trigger_dict[line_elements[3]])
                    
            trigger_dict[line_elements[0]] = trigger
            
    print(lines) # for now, print it so you see what it contains!
    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

