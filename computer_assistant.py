# importing libraries

import speech_recognition as sr 
import os
from gtts import gTTS as voice_converter
import datetime 
import warnings
import calendar
import random
import wikipedia
import webbrowser
from playsound import playsound
import cv2


#ignore any warnings messages 
warnings.filterwarnings('ignore')

#record the audio and return it as a string 
def recordfoldername():
	
	#recording the audoo
	r = sr.Recognizer()  #creating a recognizer object

	#open the microphone and start recording
	with sr.Microphone() as source:
		# print('Say something!!!')
		audio = r.listen(source)

	#use google speech recognition
	folder_name = ''
	try:
		folder_name = r.recognize_google(audio)
		string_name = str(folder_name)
		feedback = 'proposed folder name is '+string_name
		assistantResponse(feedback)
		cv2.waitKey(2000)
		
	except sr.UnknownValueError: #check for unknown errors
		print('Google Speech Recognition could not understand the audio, unknown error')
	except sr.RequestError as e:
		print('Request results from google speech recognition service error')

	return folder_name

#record the audio and return it as a string 
def recordAudio():
	
	#recording the audoo
	r = sr.Recognizer()  #creating a recognizer object

	#open the microphone and start recording
	with sr.Microphone() as source:
		print('Say something!!!')
		audio = r.listen(source)

	#use google speech recognition
	data = ''
	try:
		data = r.recognize_google(audio)
		print('You said:'+data)
	except sr.UnknownValueError: #check for unknown errors
		print('Google Speech Recognition could not understand the audio, unknown error')
	except sr.RequestError as e:
		print('Request results from google speech recognition service error')

	return data

#A function to get virtual assistant response
def assistantResponse(text):

	print(text)

	#convert the text to speech
	myobj = voice_converter(text=text, lang='en', slow=False) #slow allows the computer read more slowly

	#save the converted audio to a file
	myobj.save('assistant_response.mp3')

	# playsound('assistant_response.mp3')

	#removing the file
	# os.remove('assistant_response.mp3')

	#play the converted file
	os.system('start assistant_response.mp3')


#a function for wake words or phrase
def wakeWord(text):
	WAKE_WORDS = ['hey assistant','hello assistant']

	#converting all the text into lowercase
	text = text.lower()

	#check to see if the user command contains a wake word or phrase
	for phrase in WAKE_WORDS:
		if phrase in text:
			return True

	#if the wake word is not found in the text, it returns false
	return False


#a functon to get the current date
def getDate():

	now = datetime.datetime.now()
	my_date = datetime.datetime.today()
	weekday = calendar.day_name[my_date.weekday()] #example friday
	monthNum = now.month
	dayNum = now.day 

	#a list of months 
	month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

	#list of ordinal numbers
	ordinalNumbers = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th','31st']

	return 'Today is '+weekday+' '+month_names[monthNum-1]+' the '+ordinalNumbers[dayNum-1]+'.'



#a function to return a random greeting response
def greeting(text):

	#greeting inputs
	GREETING_INPUTS = ['hi','hey','hello','hola','greetings','what\'s up']
	# GREETING_INPUTS = ['assalaamwaalikum','sasriyaakaal','namaste','holaamigo','kaymchho','what\'s up']


	#greeting responses
	GREETING_RESPONSES = ['how you doin?','hello','hey there!','whats good']

	#if the users input is a greeting then return a randomly chosen greeting response
	for word in text.split():
		if word.lower() in GREETING_INPUTS:
			return random.choice(GREETING_RESPONSES) + '.'

	#if no greeting were detected then return an empty response
	return ''


# a function to get a person's first and last name from the text
def getPerson(text):

	wordList = text.split() #splitting the text into a list of words

	for i in range (0, len(wordList)):
		if i+3 <= len(wordList)-1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
			return wordList[i+2]+' '+wordList[i+3]


#a function to get a place location details
def getInfo(text):
	
	listing_words = text.split() #splitting text into a list of words


	for i in range(0, len(listing_words)):
		if i+3 <= len(listing_words)-1 and listing_words[i].lower() == 'tell' and listing_words[i+1].lower() == 'me' and listing_words[i+2].lower() == 'something':
			info_about = ' '
			for j in range(i+4, len(listing_words)):
				info_about = info_about + listing_words[j]
			return info_about.lower()


def visit_site(text):

	wordList = text.split()

	for i in range (0, len(wordList)):
		if i+1 <= len(wordList)-1 and wordList[i].lower() == 'open':
			return wordList[i+1].lower()+'.com'

if __name__ == "__main__":


	while True:

		#record the audio
		text = recordAudio()

		#an empty string for appending all of the responses together and convert it to audio
		response = ''

		#check for the wake words/phrases
		if(wakeWord(text) == True):

			#check for the greetings by the user
			response = response + greeting(text)

			#check to see if the user said anything having to do with the date
			if('date' in text):
				get_date = getDate()
				response = response +' '+get_date

			
			#check to see if the user said anything having to do with the time
			if('time' in text):
				now = datetime.datetime.now()
				meridiem = ''
				if now.hour>=12:
					meridiem = 'p.m' #post meridiem i.e after mid day
					hour = now.hour-12
				else:
					meridiem = 'a.m' #pre meridiem i.e. before mid day
					hour = now.hour

				#convert minute into proper string
				if now.minute<10:
					minute = '0'+str(now.minute)
				else:
					minute = str(now.minute)

				response = response+' '+'It is' +str(hour)+':'+minute+' ' +meridiem+'.'


			#check to see is the user said 'who is'
			if ('who is' in text):
				person = getPerson(text)
				wiki = wikipedia.summary(person, sentences=2)
				response = response +' '+wiki

			#opening gmail site
			if ('open' in text):
				data = visit_site(text)
				chrome_path ='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
				webbrowser.get(chrome_path).open(data)
				

			#check to see where a place lies
			if ('tell me something' in text):
				place = getInfo(text)
				wiki = wikipedia.summary(place, sentences=2)
				response = response+' '+wiki

			#creating a new folder
			if ('create new folder' in text):
				assistantResponse(response)
				folder_created_response = 'New folder created'
				folder_inquiry_response = 'What should be the folder name?'
				assistantResponse(folder_inquiry_response)
				fold_name = recordfoldername()
				created_foldername = ' '
				created_foldername = str(fold_name)
				# feedback = 'proposed folder name is '+fold_name
				# assistantResponse(feedback)
				os.mkdir(created_foldername)
				assistantResponse(folder_created_response)
				
				response = 'I am happy to have been useful. '


			#have the assistant respond back using audio and the text from the response
			assistantResponse(response)

		if('shutdown computer' in text):
			os.system("shutdown /s /t 1");

		if('restart computer' in text):
			os.system("shutdown /r /t 1");

		#check to see if the user said 'terminate'
		if ('terminate' in text):
				exit()




































































































