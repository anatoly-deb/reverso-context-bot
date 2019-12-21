import requests
from bs4 import BeautifulSoup
def translate():
	languages_list = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
					  'portuguese', 'romanian', 'russian', 'turkish']
	default_lang = int(input("Hello, you're welcome to translator. Translator supports: \n1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n6. Hebrew\n7. Japanese\n8. Dutch\n9. Polish\n10. Portuguese\n11. Romanian\n12. Russian\n13. Turkish\nType number of your language: ").strip().lower())
	while 1 > default_lang or default_lang > 13:  # if default_lang incorrect type it again
		default_lang = int(input('Sorry, you typed incorrect number, please, rewrite it:'))

	language = int(input("Type number of language you want to traslate on: ").strip().lower())

	while language == default_lang or language < 0 or language > 13:
		language = int(input('Sorry, you typed incorrect number, please, rewrite it:'))
	if language != 0:
		default_lang = languages_list[default_lang - 1]
		languages_list = [languages_list[language - 1]]
	else:
		default_lang = languages_list.pop(default_lang - 1)

	word = input('Type word you want to translate: ')

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

	translation_text = ''
	for lang in languages_list:
		#  create request:
		URL = f'https://context.reverso.net/translation/{default_lang}-{lang}/' + word.replace(" ",
																							   "+").lower().replace("'",
																													"%27")
		# print(f'URL = {URL}')  #  if URL is correct, we will see it

		try:
			response = requests.get(URL, headers=headers)  # send request
			if response.status_code == 200:
				# print(response.status_code, 'OK')
				pass

		except requests.exceptions.ConnectionError:
			print('Something wrong with your internet connection')
			return False
		soup = BeautifulSoup(response.text, "html.parser")  # parse web page
		#  find translations with examples:
		translations_with_examples = soup.find_all(['div', 'a'], {"class": ['translation', 'src', 'trg']})
		#  find only translations of word:
		only_translations_of_word = soup.find_all(['div', 'a'], {"class": ['translation']})
		#  get text from html and format it:
		only_translations_list = []
		translations_with_examples_list = []
		for example in translations_with_examples:
			translations_with_examples_list.append(example.text.replace('\n', '').strip())
		for translation in only_translations_of_word:
			only_translations_list.append(translation.text.replace('\n', '').strip())
		#  we need see the result:
		# print(only_translations_list)
		#  format output for readable translations:
		translation_text = ''

		translations_with_examples_list = translations_with_examples_list[
										  translations_with_examples_list.index(only_translations_list[-1]) + 1:]
		translations_count = 0
		for translation in only_translations_list:
			if len(translation) > 0:
				if translation == 'Translation':
					translation = f'\n{lang} {translation.lower()}s:'.title()
				if language == 0 and translations_count < 2:
					translation_text += f'{translation}\n'
					translations_count += 1
				elif language != 0 and translations_count < 6:
					translation_text += f'{translation}\n'
					translations_count += 1

		example_count = 0
		example_text = f'{lang} examples:\n'.title() if language != 0 else f'{lang} example:\n'.title()
		for example in translations_with_examples_list:
			if example_count < 2:
				if len(example) > 0:
					if example_count % 2 == 0:
						example_text += example + ':\n'
					else:
						example_text += example + '\n'
					example_count += 1
			elif language != 0 and example_count < 10:
				if len(example) > 0:
					if example_count % 2 == 0:
						example_text += example + ':\n'
					else:
						example_text += example + '\n'
					example_count += 1


		print(translation_text + example_text)

translate()