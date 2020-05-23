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

# All of the BookOfReddit code by @shaunakg is
# copyright (c) @shaunakg under the GNU GPLv3 License.

# All of the parts of this program using Calibre and Kovid Goyal's work 
# are copyright (c) Kovid Goyal. Check the license for Calibre at
# https://github.com/kovidgoyal/calibre for more information.

# COMMAND LINE USAGE
# python bookofreddit.py (url) (file name without extension) [extension] [can download from web] 

__developer__ = "@shaunakg"
__version__ = "0.4.3"

# Start logging before everything
import datetime
start_mstime = str(datetime.datetime.now().timestamp())
logfilename = "logs/" + start_mstime +"-logfile.log"
logfile = open(logfilename,"a+")
logfile.write(f"\n>>> Start BOR Logfile at {datetime.datetime.now()} <<<\n")
def lw(writetext, printAlso=False):
	logfile.write(f"[{str(datetime.datetime.now())}] {writetext}\n")
	if printAlso:
		print(writetext)
	return(f"[{str(datetime.datetime.now())}] {writetext}\n")

# Import useful modules
import sys
import codecs
import praw # Use praw
import re
import subprocess
import platform
import os
from random import randint

from dotenv import load_dotenv
try:
	load_dotenv(dotenv_path="config.env")
	lw("loaded environment file")
except:
	exit(lw("fatal: unable to load environment file. exiting."))

canDownloadFromWeb = True
try:
	from modules import md_download_to_urls
	lw("successfully imported URL download module.")
except Exception as e:
	lw("couldn't find URL download module, won't download from web.")
	canDownloadFromWeb = False
	print("!!! You need the file md_download_to_urls.py to enable the download of links from the web. Get it at: git.io/fA2dt (note: BOR will still work, it will just use urls.md/txt)\n")
exists = os.path.exists

# setup rich text
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
console = Console()

def print_markdown(t):
	console.print(Markdown(t))

if len(sys.argv)==1:
	lw("no command line options specified on startup")
	print("\nRunning BOR with user input. If you want to run automated, use the following command next time:")
	print("$ python bookofreddit.py (url) (file name without extension) [extension]\n")

if os.name != 'nt':
	lw(f"User is running {platform.platform()}, not Windows/NT.")
	print("You are running a non-windows system. Some conversion commands may not work.")

starttext = f"""\
reddit post compendium made by BookOfReddit (https://git.io/fA2dt)
version {__version__} by {__developer__}
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
by {__developer__} on Github.

I cannot guarantee great
formatting as Reddit is
weird. However the original
Markdown is preserved as
well as the links to the
posts.

Enjoy, and happy reading!

{__developer__},
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

print_markdown(f"# BookOfReddit version {__version__} by {__developer__}")
print_markdown(f"saving log for this run to **{logfilename}**")

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
			md_download_to_urls.get(url_to_get, lw)
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

exts = ["pdf",
	"azw3",
	"epub",
	"mobi",
	"html",
	"",
	"cf_disabled"
] # < Add more (TODO)

try:
	ext = sys.argv[3].replace(".","")
	lw("started with cmd extension argument " + sys.argv[3])
except IndexError:
	lw("no cmd extension. asking user...")
	ext = input("Enter a file extension for conversion (or leave blank) [azw3/epub/mobi/html]: ")
	while ext not in exts:
		lw(f"user entered {ext} which isn't valid")
		ext = input("Invalid input. Enter a file extension for conversion (or leave blank) [azw3/epub/mobi/html]:")
	lw(f"got final user input extension > {ext}")

if ext == "":
	ext = "cf_disabled"

if ext not in exts:
	lw(f"{ext} wasn't a valid extension. disabling conversion.")
	print(f"{ext} is not a valid extension. Disabling conversion.")
	ext = "cf_disabled"

print("\n- starting automated process (use CTRL-C to exit) -\n")

try:

	# Makes folders so it's cleaner
	folder_name = f"{name}-{start_mstime}"

	os.makedirs(f"./outputs/{folder_name}/")
	name = f"{folder_name}/{name}"

	filename = "outputs/" + name+".md"
	lw("Full output path: " + filename)

	write_file = codecs.open(filename,'w+',"utf-8")
	write_file.close()
	write_file = codecs.open(filename,'a+','utf-8')
	write_file.write(starttext)

except Exception as e:

	lw(f"An unknown exception occurred: {e}. Raising and exiting.")
	raise e
	exit()

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

write_file.write("\n**Compendium by BookOfReddit (https://git.io/fA2dt), " + str(len(urls)) + " posts included**\n")
write_file.write(f"[original url link]({url_to_get})\n[ebook generation feedback](https://git.io/fAoaw)\n\n")

try:
	links = urls
	for link in track(links, description = "Downloading..."):
		link_list.append(link)
		try:
			submission = reddit.submission(url=link)
		except praw.exceptions.InvalidURL as e:
			lw(f"PRAW InvalidURL Exception: {e}")
			pass
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
			write_file.write(("\n<h2 class=\"chapter\">" + submission.title.replace("[","(").replace("]",")")) + "</h2>\n") # Using semantic HTML to get Calibre to recognise it.
			write_file.write(submission.selftext) # .replace("‽", "?!")
			lw(f"[Processed #{links.index(link)}] {submission.title}")

		except UnicodeEncodeError:

			lw("UnicodeEncodeError on " + str(submission.title) + ", at: " + link)
			# Error writing block
			write_file.write(("\n<h2 class=\"chapter\">(error) " + submission.title.replace("[","(").replace("]",")")) + "</h2>\n") # Using semantic HTML to get Calibre to recognise it.
			write_file.write("[There was an error parsing the content at " + link + ".]")
			write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			write_file.write("[Error information (submit this): " + str(e) + "]")

		except Exception as e:
			try:
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
	write_file.write('\n<h2 class="chapter">Compendium metadata</h2>\n')
	write_file.write("List of posts compiled:\n")
	write_file.write("\n<ol>\n")
	for submission in compendium:
		write_file.write(f'<li><a href="https://reddit.com{submission.permalink}">{submission.title}</a> by u/{submission.author.name} in r/{submission.subreddit.name}</li>')
	write_file.write("</ol>\n")
	write_file.close()
	if ext in exts and ext != "cf_disabled": # Conversion and Metadata write code

		lw("starting calibre conversion...")

		# conversion command assembly
		new_filename = "outputs/" + name + "." + ext
		conversion_command = ["ebook-convert", filename, new_filename, "--input-encoding", "utf-8", "--asciiize"]

		if ext=="mobi":
			conversion_command.append("--mobi-file-type")
			conversion_command.append("new")

		lw("autogenerated conversion command: " + ' '.join(conversion_command))
		lw(f"conversion output will be written to {new_filename}")

		# metadata command assembly
		lw("generating metadata command")
		metadata_write_command = ["ebook-meta", new_filename, "-t", name, "-a", '&'.join(list(set(authors))), "-k", "BookOfReddit (https://git.io/fA2dt)", "--publisher", "BookOfReddit (https://git.io/fA2dt)", "-c", ebook_desc, "--to-opf", "outputs/" + name + "-metadata.opf"]
		lw(f"generated metadata command: {metadata_write_command}")

		# Ebook polishing command assembly
		covers = [
			"covers/light/1.jpg",
			"covers/light/2.jpg",
			"covers/light/3.jpg",
			"covers/light/4.jpg",
			"covers/dark/1.jpg",
			"covers/dark/2.jpg",
			"covers/dark/3.jpg",
			"covers/dark/4.jpg",
			"covers/dark/5.jpg",
		]
		coverfile = covers[randint(0,8)]
		cover_write_command = ["ebook-polish", new_filename, "--cover", coverfile]

		# Excecuting commands
		errors = 0
		for command in track([conversion_command, metadata_write_command, cover_write_command], description = "Converting..."):
			lw(f"Excecuting {command}")
			if subprocess.call(command, stdout=logfile):
				lw("Error!!")
				error = errors + 1

		errorcode = False if errors==0 else True
		if errorcode:
			lw("system error while trying to convert formats.")
			print("Error while trying to convert formats.\nYou probably don't have Calibre (https://github.com/kovidgoyal/calibre) installed.")
			exit()
		
		lw("Removing non-polished book.")
		os.remove(new_filename)
		lw("Renaming to normal book.")
		os.rename(new_filename.replace(f".{ext}","") + f"_polished.{ext}", new_filename)
		
		lw("-\nFinished converting.\n")
		print(f"Your file was downloaded and converted into .{ext} format. Recommended actions:")
		print(" - go into calibre and change title to actual series title")
		print(" - go into calible and change synopsis")
		print(" - go into calibre and generate a cover")
		print(" - enjoy.\n")

		exit()

	elif ext=="cf_disabled":
		conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"' + name + '.'+'[mobi/epub/pdf/azw3]"'
		lw("user chose to not convert book.")
		lw("conversion command: " + ' '.join(conversion_command))
		print("Cannot convert book, conversion functionality disabled. If you want to convert the book later, use the Calibre GUI or run:")
		print(conversion_command)
		print("Finished processing, thank you for using BookOfReddit.")
		exit()
	else:
		conversion_command = "ebook-convert " + '"' + filename + '"' + " " + '"' + name + '.'+'[mobi/epub/pdf/azw3]"'
		print("\n\nYou didn't put an extension to convert into. BookOfReddit will not automatically convert your file, however, if you have Calibre ebook manager (https://calibre-ebook.com) installed, you can run:\n")
		print(conversion_command)
		print("\nto convert your book into the format of your choice.\n")
		print("\nFinished processing, thank you for using BookOfReddit.\n\n")
		logfile.close()
		exit()

