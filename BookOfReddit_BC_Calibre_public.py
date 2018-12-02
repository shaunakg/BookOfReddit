# --- BookOfReddit source code file ---
#
# This edition of BookOfReddit will:
# > Take text from urls[.md/.txt] OR from the web (need md_download_to_urls.py)
# > Parse it to get Reddit urls
# > Using PRAW, get the selftext of the Reddit posts in the urls
# > Encode it using UTF-8
# ├───	(This is due to the fact that the Windows-1252 encoding
# └───	fails with ereaders, Calibre and basically everything.)
# > Write it to a file (.txt)
# > Convert the file from TXT to mobi/epub/azw3/pdf:
# ├───	(I can't take credit for this, it uses Calibre by
# └───	Kovid Goyal which is a awesome tool that I did not create)

# All of the BookOfReddit code by @shaunakg/The_Removed is
# copyright (c) 2018 @shaunakg/The_Removed under the GNU GPLv3 License.

# All of the parts of this program using Calibre and Kovid Goyal's work 
# are copyright (c) 2018 Kovid Goyal. Check the license for Calibre at
# https://github.com/kovidgoyal/calibre for more information.

# YOU NEED TO REPLACE CLIENT ID AND SECRET BELOW, OR ELSE IT WILL NOT WORK

ConversionFunctionality = True # Switch to FALSE to not execute commands using CMD
# If you switch to FALSE, Calibre conversion will not work, however the program
# will not execute commands on the system

canDownloadFromWeb = False

import codecs
import praw #Makes sure we can use the module

try:
	import md_download_to_urls
	canDownloadFromWeb = True
except Exception as e:
	print("!!! You need the file md_download_to_urls.py to enable the download of links from the web. Get it at: git.io/fA2dt (Note: BookOfReddit will still work, however it will only read from urls.md)\n")


if ConversionFunctionality:
	import os # For executing Calibre commands only, see above to disable
else:
	print("\nBookOfReddit has been started with conversion functionality disabled.")
	print("This may be for security reasons, however, if you want to change it, go ")
	print("to the source code and change ConversionFunctionality to False.\n")
	print("While it is disabled, BookOfReddit cannot convert between file formats.\n")

exists = os.path.exists

starttext = """\
reddit post compendium made by BookOfReddit (https://git.io/fA2dt)
options: bulk, UTF-8 ONLY, Calibre Conversion Mode
_________________________
This is a compendium of
Reddit posts compiled by
a program. Please go to
the end of the file for
more information such as
the number and url of the
posts inside.

The program used to make
this compendium is called
BookOfReddit and is
available at:

https://git.io/fA2dt

It is made and maintained
by @shaunakg on Github
and u/The_Removed on
Reddit.

I cannot guarantee great
formatting as Reddit is
weird. However the original
Markdown is preserved as
well as the links to the
posts.

Enjoy, and happy reading!

u/The_Removed,
Creator of BookOfReddit
__________________________
"""

reddit = praw.Reddit(client_id='YOUR-CLIENT-ID',
                     client_secret='YOUR-CLIENT-SECRET', password='OPTIONAL-PASSWORD',
                     user_agent='BookOfReddit_V4', username='OPTIONAL-USERNAME')

compendium = []
link_list = []
exts = ["pdf","azw3","epub","mobi",""] # < Add more (TODO)

print(">>> Welcome to Book of Reddit (CONVERTER/DOWNLOADER EDITION) <<<")

if canDownloadFromWeb:
	while True:
		url_to_get = input("Enter a reddit URL to parse (or just <ENTER> to get existing urls.md): ")
		if url_to_get == "":
			break
		elif "http" in url_to_get:
			md_download_to_urls.get(url_to_get)
			break
		else:
			print("Enter a valid url (with \"http\") or press <ENTER>!")

name = input("Filename to save into (without extension): ")

ext = input("Enter a file extension to convert to (Calibre required for this part) or press ENTER:")
while ext not in exts:
	ext = input("!invalid extension, enter either pdf, azw3, epub or mobi\nEnter a file extension to convert to (Calibre required for this part) or press ENTER:")

ext = "cf_disabled" if not ConversionFunctionality else ext

print("\n")
print("(Use CTRL-C to exit or 'wipe' to wipe the file)")
filename = name+".txt"

try:
	write_file = codecs.open(filename,'w+',"utf-8")
	write_file.close()
	write_file = codecs.open(filename,'a+','utf-8')
	write_file.write(starttext)
except FileNotFoundError:
	print("Folder not found. BookOfReddit cannot create folders, please use a existing path.")
	exit()

logfile = open(filename+"-logfile.log","a+")
logfile.write(">>> Start Logfile <<<\n")

def lw(writetext):
	logfile.write(writetext+"\n")

if not exists("urls.md"):
	if not exists("urls.txt"):
		lw("Did not find urls.md or urls.txt, exiting now...")
		print("To use this program, please put Markdown with urls in 'urls.md' or normal urls in 'urls.txt' (Or setup the downloader from the Github repo)")
		exit(2)

import re
lw("Imported re module to parse links")

try:
	url = codecs.open("urls.md","r+").read()

	lw("Found file urls.md, parsing now")

	urls = re.findall('\(.*?\)',url)
	lw("Parsed stage 1, urls = urls/random text with brackets around.")
	lw("\n-Starting stage 2 parsing-")

	for i in urls:
		striped_i = i.strip("(").strip(")")
		urls[urls.index(i)] = striped_i
		lw("Removed brackets from " + i)
	lw("-END PARSING STAGE 2-\n")
	lw("-Starting parsing stage 3-")
	for i in urls:
		if "http" not in i:
			urls.remove(i)
			lw("Removed " + i + " from list, it is not a URL.")

	lw("-END PARSING STAGE 3-\n")
	lw("URLS TO PROCESS:")
	for i in urls:
		lw(i)
	lw("\nStarting Processing...")
except:
	urls = codecs.open("urls.txt","r+","utf-8").read().split("\n")
	if len(urls) < 2:
		urls = urls[1].split(",")

write_file.write("\n#Compendium by BookOfReddit (https://git.io/fA2dt), " + str(len(compendium)) + " posts included\n")

try:
	links = urls
	for link in links:
		link_list.append(link)
		try:
			submission = reddit.submission(url=link)
		except Exception as e:
			print(str(e))
			lw("Exception while getting Reddit submission for " + link + ": " + str(e))
			# Error writing block
			write_file.write("\n##" + submission.title + " (ERROR)\n")
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")
		compendium.append(submission)
		try:
			write_file.write("\n#" + submission.title.replace("[","(").replace("]",")") + "\n") # Added the '#' instead of normal '>>> ??? <<<' because then Calibre will detect it as a chapter.
			write_file.write(submission.selftext) # .replace("‽", "?!") #
			print("Processed: " + submission.title)
			lw("Processed: " + submission.title)
		except UnicodeEncodeError:
			print("UnicodeEncodeError on " + str(submission.title))
			lw("UnicodeEncodeError on " + str(submission.title) + ", at: " + link)
			# Error writing block
			write_file.write("\n>>> " + submission.title + " (ERROR) <<<\n")
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")
		except Exception as e:
			print(str(e))
			lw("Exception while writing " + link + " to file: " + str(e))
			# Error writing block
			write_file.write("\n>>> " + submission.title + " (ERROR) <<<\n")
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")

	raise KeyboardInterrupt	# This probably violates a lot of coding conventions and maritime laws	
except KeyboardInterrupt:
	ebook_desc = "This is a Reddit compendium created by a program called BookOfReddit. The program is available at https://git.io/fA2dt and is licensed under GNU GPLv3 or later. Check last part of book for more information."
	write_file.write("\n\n>>> End Compendium (with " + str(len(links)) + " posts), Metadata Below <<<\n")
	write_file.write("List of books in format ([TITLE], by [AUTHOR] in [SUBREDDIT]):\n")
	for submission in compendium:
		write_file.write('> "' + submission.title+'", by u/' + submission.author.name + " in r/" + str(submission.subreddit)+"\n")
		# ebook_desc = ebook_desc + ", " + submission.title
	write_file.close()
	if ext in exts: # Conversion and Metadata write code
		conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"' + name + '.'+ext+'"'
		new_filename = name+"."+ext
		os.system("echo off && cls")
		print("--- converting to calibre please wait ---")
		print('EXECUTING ' + conversion_command)
		print("\nStarting CALIBRE ebook conversion service (if installed)\n---\n")
		errors = 0
		if os.system(conversion_command) != 0: # Probably a better way of doing this
			errors = errors+1
		print("\nStarting CALIBRE ebook metadata write (if installed)\n---\n")
		
		# Metadata command assembly (That sounds complicated, but it is way more than just that)
		metadata_write_command = 'ebook-meta ' + new_filename + ' -a "BookOfReddit'
		# for i in compendium:
		# 	metadata_write_command = metadata_write_command+i.author.name+'&'
		metadata_write_command = metadata_write_command+'" -t "'+name+'" -p "BookOfReddit (https://git.io/fA2dt)" -c "' + ebook_desc
		print('EXECUTING ' + metadata_write_command)


		if os.system(conversion_command) != 0: # Probably a better way of doing this
			errors = errors+1
		if os.system(metadata_write_command) != 0: # Probably a better way of doing this
			errors = errors+1
		errorcode = False if errors==0 else True

		if errorcode:
			print("Error while trying to convert formats.\nYou probably don't have Calibre (https://github.com/kovidgoyal/calibre) installed.")
			exit()
		print("\n-\nFinished converting. Exiting...")
	elif ext=="cf_disabled":
		print("Cannot convert book, conversion functionality disabled.")
		print("Finished processing, thank you for using BookOfReddit.")
	else:
		conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"' + name + '.'+'[mobi/epub/pdf/azw3]"'
		print("\n\nYou didn't put an extension to convert into. BookOfReddit will")
		print("not automatically convert your file, however, if you have Calibre")
		print("ebook manager (https://calibre-ebook.com) installed, you can run:\n")
		print(conversion_command)
		print("\nto convert your book into the format of your choice.")
		print("\nFinished processing, thank you for using BookOfReddit.")
		exit()

