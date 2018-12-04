import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

class Commenter:
	"""docstring for Commenter"""
	def __init__(self, username, password):
		super(Commenter, self).__init__()
		self.username = username
		self.password = password
		self.driver = webdriver.Firefox()
		self.driver.set_window_size(750, 900)

	#close browser
	def closeBrowser(self):
		self.driver.close()
	
	#login function
	def login(self):
		driver = self.driver
		driver.get("https://www.instagram.com/")
		time.sleep(5)
		login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
		login_button.click()
		time.sleep(5)
		user_name_elem =driver.find_element_by_xpath("//input[@name='username']")
		user_name_elem.clear()
		user_name_elem.send_keys(self.username)
		password_elem = driver.find_element_by_xpath("//input[@name='password']")
		password_elem.clear()
		password_elem.send_keys(self.password)
		password_elem.send_keys(Keys.RETURN)
		time.sleep(2)

	#getting pictures on a hastag page
	def get_pictures_on_page(self, hashtag, scrolls=int):
		self.driver.get("https://www.instagram.com/explore/tags/"+ hashtag +"/")
		time.sleep(5)
		
		#gathering photos
		pic_hrefs = []
		for i in range(1,scrolls):
			try:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(5)

				#get tags
				hrefs_in_view = self.driver.find_elements_by_tag_name('a')
				#finding relevant hrefs
				hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if hashtag in elem.get_attribute('href')]
				#building list of unique photos
				[pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
				#print("Check: pic href length " + str(len(pic_hrefs)))
			except Exception:
				continue
		return pic_hrefs

	#write comment in text area using lambda function
	def write_comment(self, comment_text):
		try:
			comment_button = lambda: self.driver.find_element_by_xpath("//span[@aria-label='Comment']")
			comment_button().click()
		except NoSuchElementException as e:
			print(e)
			pass
			
		try:
			comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
			comment_box_elem().send_keys('')
			comment_box_elem().clear()
			for letter in comment_text:
				comment_box_elem().send_keys(letter)
				time.sleep((random.randint(1, 7) / 30))

			return comment_box_elem
		except (StaleElementReferenceException, NoSuchElementException) as e:
			print(e)
			return False

	#post a comment
	def post_comment(self, comment_text):
		time.sleep(random.randint(1, 5))

		comment_box_elem = self.write_comment(comment_text)
		if comment_text in self.driver.page_source:
			comment_box_elem().send_keys(Keys.ENTER)
			try:
				post_button = lambda: self.driver.find_element_by_xpath("button[@type='Post']")
				post_button().click()
				print('clicked post button')
			except NoSuchElementException:
				pass

		time.sleep(random.randint(4, 6))
		self.driver.refresh()
		if comment_text in self.driver.page_source:
			return True
		return False

	#grab comments
	def get_comments(self):
		#load more comments if button exists
		time.sleep(3)

		try:
			#k59kT & gElp9 these values can change time to time
			#look up <ul> & <li> tag
			comment_block = self.driver.find_element_by_class_name('k59kT')
			comments_in_block = comment_block.find_elements_by_class_name('gElp9')
			comments = [x.find_element_by_tag_name('span') for x in comments_in_block]
			user_comment = re.sub(r"#.\w*", "", comments[0].text)

		except NoSuchElementException:
			return ''
		return user_comment

	#have bot comment on pic
	def comment_on_picture(self):
		bot = ChatBot('YouTubeChatBot')
		bot.set_trainer(ListTrainer)
		picture_comment = self.get_comments()
		#user's comment and bot's response
		response = bot.get_response(picture_comment).__str__()
		print("User's Comment", picture_comment)
		print("Bot's Response", response)
		return self.post_comment(response)

com = Commenter(username='usman9104', password='Nigga@123')
com.login()
# pictures_on_page = com.get_pictures_on_page(hashtag='photoshop', scrolls=3)[1:]
# print(pictures_on_page)
time.sleep(3)
com.driver.get('https://www.instagram.com/p/BqaQodwgpx_yCPzNHj5r34WeyAb8vsNaoUgNd00/')
time.sleep(3)
# com.write_comment('test')
# com.post_comment('test')
print(com.get_comments())
print("posted Comment", com.comment_on_picture())