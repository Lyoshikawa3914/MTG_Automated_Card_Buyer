"""
Purpose:
    create a bot that automatically buys cards of a edh deck from the internet
    select the deck based on the cost

What the bot will do:
    open webbrowser to edhrec
    search for the specified card
    select the deck based on the price
    take you to cardkingdom to buy the cards
    add cards from the deck to shopping card based on price

    incoporate binary search algorimth

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random as rd
import time

class card_buying_bot:
    def __init__(self, name, price):
        self.name = name
        self.price = price


#get the path of chromedriver to make the program work
        self.PATH = "C:\Program Files (x86)\chromedriver.exe"

#set the webdriver up
        self.driver = webdriver.Chrome(self.PATH)


#automate driver to go to weblink
        self.link = self.driver.get("https://edhrec.com/")
        time.sleep(2)

#selects the search bar on website, enters self.name, then clicks the name on the bar
        self.search = self.driver.find_element_by_xpath('/html/body/div/div/nav/div/div[2]/ul[2]/form/span/div/div[1]/'
                                                        'input')
        time.sleep(2)
        self.search.send_keys(self.name)
        self.driver.find_element_by_xpath('/html/body/div/div/nav/div/div[2]/ul[2]/form/span/div/ul').click()
        time.sleep(4)

#selects the link "more decks..." on the page
        self.driver.find_element_by_link_text('More decks...').send_keys(Keys.RETURN)
        time.sleep(3)

#program presses the key down once, to 25
        self.entry = self.driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/div/div[3]/div/span/div/'
                                                       'div[1]/div[1]/div/label/select')
        self.entry.send_keys(Keys.RETURN)
        time.sleep(2)

        self.entry.send_keys(Keys.ARROW_DOWN)
        self.entry.send_keys(Keys.RETURN)
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/div/div[3]/div/span/div/div[2]/div/table/'
                                          'thead/tr/th[3]').send_keys(Keys.RETURN)

        self.table = self.driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/div/div[3]/div/span/div/'
                                                       'div[2]/div/table/tbody')

        self.random_selection_to_nextpage(self.table)
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/div/div[3]/div/span/a[1]').click()

#Entering Cardkingdom website and switching handles to Cardkingdom.com
        time.sleep(5)
        self.current = self.driver.current_window_handle
        self.handles = self.driver.window_handles # get all the handle values of opened browser windows

        for handle in self.handles:
            self.driver.switch_to.window(handle)
            if handle == self.current:
                self.driver.close()

# This will uncheck the box for lower prices
        time.sleep(2)
        self.checkbox = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/form/div[1]/div/div[2]'
                                          '/ul/li/input').is_selected()
        if self.checkbox:
            self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/form/div[1]/div/div[2]'
                                          '/ul/li/input').click()


        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/form/button[1]').click()

# call to the method to select the lowest price card
        #the div tag
        self.data = self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/form/div[2]')
        self.select_low_price_card(self.data)
        time.sleep(14)

    def random_selection_to_nextpage(self, data):
        # gather the data from self.table, add them to a list 'decks',
        # then randomly choose the decks based on self.price
        # the program will go to the page of the chosen deck

        decks = []
        count = 0
        rows = data.find_elements_by_tag_name('tr')
        for row in rows:
            #print(row.text)
            row_price = row.find_element_by_class_name('sorting_1')
            alt_price = row_price.text.replace('$', '')

            if int(alt_price) <= int(self.price):
                decks.append(row.text)
                count += 1

        #print(count)
        #print(decks)

        random_choice = rd.choice(decks)
        #print(random_choice)
        for i in rows:
            if random_choice == i.text:
                choice = i.find_element_by_link_text('View Decklist')
                choice.click()
                break
        return

    def select_low_price_card(self, data):

        count = 0
        panels = data.find_elements_by_class_name('panel-default')
        for i in panels:
            count += 1
            print(i.text)
            print()
        print(count)








bot1 = card_buying_bot('Golos, Tireless Pilgrim', 100)