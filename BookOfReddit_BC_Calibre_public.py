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

# COMMAND LINE USAGE
# python bookofreddit.py (url) (file name without extension) [extension] [can download from web] 

import sys
import datetime

if len(sys.argv)==1:
	lw("no command line options specified on startup")
	print("Running BOR with user input. If you want to run automated, use the following command next time:")
	print("python bookofreddit.py (url) (file name without extension) [extension]")

logfile = open("logs/" + str(datetime.datetime.now().timestamp())+"-logfile.log","a+")

logfile.write("\n\n^^^ THE ABOVE IS CONSOLE GENERATED OUTPUT ^^^\n\n")
logfile.write(f"\n>>> Start BOR Logfile at {datetime.datetime.now()} <<<\n")

def lw(writetext, printAlso=False):
	logfile.write(f"[{str(datetime.datetime.now())}] {writetext}\n")
	if printAlso:
		print(writetext)
	return(f"[{str(datetime.datetime.now())}] {writetext}\n")

canDownloadFromWeb = True

try:
	ext = sys.argv[3].replace(".","")
	lw("started with cmd extension argument " + sys.argv[3])
except IndexError:
	lw("no cmd extension. disabling conversion.")
	ext = "cf_disabled"

exts = ["pdf","azw3","epub","mobi","","cf_disabled"] # < Add more (TODO)

if ext not in exts:
	lw(f"{sys.argv[3]} wasn't a valid extension. disabling conversion.")
	print(f"{ext} is not a valid extension. Disabling conversion.")
	ext = "cf_disabled"

from dotenv import load_dotenv

try:
	load_dotenv(dotenv_path="config.env")
	lw("loaded environment file")
except:
	exit(lw("fatal: unable to load environment file. exiting."))

import codecs
import praw # Only use praw if we're using the web.

try:
	from modules import md_download_to_urls
	lw("successfully imported URL download module.")
except Exception as e:
	lw("couldn't find URL download module, won't download from web.")
	canDownloadFromWeb = False
	print("!!! You need the file md_download_to_urls.py to enable the download of links from the web. Get it at: git.io/fA2dt (note: BOR will still work, it will just use urls.md/txt)\n")

import subprocess
import os

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

reddit = praw.Reddit(client_id=os.getenv("reddit_client"),
                     client_secret=os.getenv("reddit_secret"),
                     user_agent=os.getenv("reddit_useragent"))

lw("initialised praw")

compendium = []
link_list = []
authors = []

print(">>> Welcome to Book of Reddit (CONVERTER/DOWNLOADER EDITION) <<<")

if canDownloadFromWeb:
	while True:

		try:
			url_to_get = sys.argv[1] 
			lw("cmd argument for reddit url: " + sys.argv[1])
		except IndexError:
			lw("no cmd argument. querying using input()")
			url_to_get = input("Enter a reddit URL to parse (or just <ENTER> to get existing urls.md): ")
			lw(f"user entered {url_to_get}")
		
		if url_to_get == "":
			lw("user did not enter a string.")
			break
		elif "http" in url_to_get:
			lw("downloading urls...")
			md_download_to_urls.get(url_to_get)
			break
		else:
			lw("user did not enter a valid URL")
			print("Enter a valid url (with \"http\") or press <ENTER>!")

try:
	name = sys.argv[2]
	lw("cmd spec write filename is " + sys.argv[2])
except IndexError:
	lw("no filename specified in command line arguments, querying using input()")
	name = input("Filename to save into (without extension): ")
	lw("inputted filename: " + name)

print("\n")
print("(Use CTRL-C to exit or 'wipe' to wipe the file)")
filename = "outputs/" + name+".txt"
lw("Full output path: " + filename)

try:
	write_file = codecs.open(filename,'w+',"utf-8")
	write_file.close()
	write_file = codecs.open(filename,'a+','utf-8')
	write_file.write(starttext)
except FileNotFoundError:
	print("Folder not found. BookOfReddit cannot create folders, please use a existing path.")
	exit(lw("user entered a filename with folders in it. Oh no!"))

if not exists("urls.md"):
	if not exists("urls.txt"):
		print("To use this program, please put Markdown with urls in 'urls.md' or normal urls in 'urls.txt' (Or setup the downloader from the Github repo)")
		exit(lw("Did not find urls.md or urls.txt, exiting now..."))

import re
lw("Imported regex module to parse links")

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

	lw("-Starting Parsing stage 4-")
	for i in urls:
		if not "redd" in i:
			urls.remove(i)

	lw("URLS TO PROCESS:")
	for i in urls:
		lw(i)
	lw("\nStarting Processing...")
except:
	urls = codecs.open("urls.txt","r+","utf-8").read().split("\n")
	if len(urls) < 2:
		urls = urls[1].split(",")

write_file.write("\n#Compendium by BookOfReddit (https://git.io/fA2dt), " + str(len(urls)) + " posts included\n")
write_file.write(f"[original url link]({url_to_get})\n\n")

try:
	links = urls
	for link in links:
		link_list.append(link)
		# print("Trying : " + link)
		try:
			submission = reddit.submission(url=link)
		except Exception as e:
			print(str(e))
			lw("[Exception] " + str(e))
			# Error writing block
			write_file.write("\n##" + submission.title + " (ERROR)\n")
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")
		compendium.append(submission)
		try:
			authors.append(str(submission.author.name))
			write_file.write("\n##" + submission.title.replace("[","(").replace("]",")") + "\n") # Added the '#' instead of normal '>>> ??? <<<' because then Calibre will detect it as a chapter.
			write_file.write(submission.selftext) # .replace("‽", "?!")
			print("Processed: " + submission.title)
			lw("Processed: " + submission.title)
		except UnicodeEncodeError:
			print("UnicodeEncodeError on " + str(submission.title))
			lw("UnicodeEncodeError on " + str(submission.title) + ", at: " + link)
			# Error writing block
			write_file.write("\n## " + submission.title + " (ERROR) \n")
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")
		except Exception as e:
			try:
				print(str(e))
				lw("Exception while writing " + link + " to file: " + str(e))
				# Error writing block
				write_file.write("\n>>> " + submission.title + " (ERROR) <<<\n")
				write_file.write("[There was an error parsing the content at " + link + ".]")
				write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
				write_file.write("[Error information (submit this): " + str(e) + "]")
			except:
				lw(link + " : NOT A POST")
				compendium.remove(submission)
				pass

	raise KeyboardInterrupt	# This probably violates a lot of coding conventions and maritime laws

except KeyboardInterrupt:
	ebook_desc = "This is a Reddit compendium created by a program called BookOfReddit. The program is available at https://git.io/fA2dt and is licensed under GNU GPLv3 or later. Check last part of book for more information."
	write_file.write("\n\n>>> End Compendium (with " + str(len(links)) + " posts), Metadata Below <<<\n")
	write_file.write("List of books in format ([TITLE], by [AUTHOR] in [SUBREDDIT]):\n")
	for submission in compendium:
		write_file.write('> "' + submission.title+'", by u/' + submission.author.name + " in r/" + str(submission.subreddit)+"\n")
		# ebook_desc = ebook_desc + ", " + submission.title
	write_file.close()
	if ext in exts and ext != "cf_disabled": # Conversion and Metadata write code

		lw("starting calibre conversion...")

		#conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"outputs/' + name + '.'+ext+'"'
		conversion_command = ["ebook-convert", filename, 'outputs/' + name + '.' +ext]
		lw("autogenerated conversion command: " + ' '.join(conversion_command))

		new_filename = "outputs/" + name + "." + ext
		lw(f"conversion output will be written to {new_filename}")

		print("--- converting to calibre please wait ---")
		lw('EXECUTING ' + ' '.join(conversion_command), True)
		print("Starting CALIBRE ebook conversion service (if installed)...")
		errors = 0
		if subprocess.call(conversion_command, stdout=logfile) != 0: # Probably a better way of doing this
			errors = errors+1
		print("Starting CALIBRE ebook metadata write (if installed)...")
		
		# Metadata command assembly (That sounds complicated, but it is way more than just that)
		lw("starting metadata write", True)
		metadata_write_command = ["ebook-meta", new_filename, "-t", name, "-a", '&'.join(list(set(authors))), "-k", "BookOfReddit (https://git.io/fA2dt)", "-c", ebook_desc, "--to-opf", "outputs/" + name + "-metadata.opf"]
		
		# for i in compendium:
		# 	metadata_write_command = metadata_write_command+i.author.name+'&'
		#metadata_write_command = metadata_write_command+'" -t "' + name  + '" -a "' + '&'.join(list(set(authors))) + ' " -k "BookOfReddit (https://git.io/fA2dt)" -c "' + ebook_desc + '" --to-opf "outputs/' + name + '-metadata.opf"'
		
		lw("autogenerated metadata write command: " + ' '.join(metadata_write_command))
		print("Excecuting metadata write command (not shown because it's too large)")

		if subprocess.call(conversion_command, stdout=logfile) != 0: # Probably a better way of doing this
			errors = errors+1
		if subprocess.call(metadata_write_command, stdout=logfile) != 0: # Probably a better way of doing this
			errors = errors+1
		errorcode = False if errors==0 else True

		if errorcode:
			lw("system error while trying to convert formats.")
			print("Error while trying to convert formats.\nYou probably don't have Calibre (https://github.com/kovidgoyal/calibre) installed.")
			exit()
		
		print("-\nFinished converting. Exiting...")

	elif ext=="cf_disabled":
		conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"' + name + '.'+'[mobi/epub/pdf/azw3]"'
		lw("user chose to not convert book.")
		lw("conversion command: " + ' '.join(conversion_command))
		print("Cannot convert book, conversion functionality disabled. If you want to convert the book later, use the Calibre GUI or run:")
		print(conversion_command)
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

