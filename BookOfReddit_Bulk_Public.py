# --- Welcome to BookOfReddit ---
# This edition of BookOfReddit will (BULK) write reddit posts to a file 
# only using Windows/UNIX formatting. If you don't know what that means, you 
# should use the BULK-CODECS file for general purposes.

# YOU NEED TO REPLACE CLIENT ID AND SECRET BELOW, OR ELSE IT WILL NOT WORK

import praw #Makes sure we can use the module
import os

exists = os.path.exists

starttext = """\
reddit post compendium made by BookOfReddit (https://git.io/fA2dt)
options: bulk, no UTF-8
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

NOTE: Due to the nature of
the program used to create
this, certain characters
such as the interrobang
(which is the '?' and '!'
characters mixed together)
have been replaced with
appropriate counterparts.
For example, the interro-
bang would have been
replaced with '?!'.
__________________________
"""

reddit = praw.Reddit(client_id='<YOUR CLIENT ID>',
                     client_secret='<YOUR CLIENT SECRET>')

compendium = []
link_list = []

print(">>> Welcome to Book of Reddit_BULK, enter a file name <<<")
filename = input("Filename to save into (without extension): ")
print("\n")
print("(Use CTRL-C to exit or 'wipe' to wipe the file)")
write_file = open(filename+".txt",'w+')
write_file.close()
write_file = open(filename+".txt",'a+')
write_file.write(starttext)

logfile = open("logfile-"+filename+".txt","a+")
logfile.write(">>> Start Logfile <<<n")

def lw(writetext):
	logfile.write(writetext+"\n")

if not exists("urls.md"):
	if not exists("urls.txt"):
		lw("Did not find urls.md or urls.txt, exiting now...")
		print("To use this program, please put Markdown with urls in 'urls.md' or normal urls in 'urls.txt'")
		exit(2)

import re
lw("Imported re module to parse links")

try:
	url = open("urls.md","r+").read()

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
	urls = open("urls.txt","r+").read().split("\n")
	if len(urls) < 2:
		urls = urls[1].split(",")

write_file.write("\n>>> Compendium by BookOfReddit (https://git.io/fA2dt), " + str(len(compendium)) + " posts included <<<\n")

try:
	while True:
		links = urls
		for link in links:
			link_list.append(link)
			try:
				submission = reddit.submission(url=link)
			except Exception as e:
				print(str(e))
				lw("Exception while getting Reddit submission for " + link + ": " + str(e))
			compendium.append(submission)
			try:
				write_file.write("\n>>> " + submission.title + " <<<\n")
				write_file.write(submission.selftext.replace("‽", "?!").encode('utf-8'))
				print("Processed: " + submission.title)
				lw("Processed: " + submission.title)
			except UnicodeEncodeError:
				print("UnicodeEncodeError on " + str(submission.title))
				lw("UnicodeEncodeError on " + str(submission.title) + ", at: " + link)
				write_file.write("\n>>> " + submission.title + " (ERROR) <<<\n")
				write_file.write("[There was an error parsing the content at " + link + ".]")
				write_file.write("[Please submit an error report at https://git.io/fAoaw.]")
			except Exception as e:
				print(str(e))
				lw("Exception while writing " + link + " to file: " + str(e))
except KeyboardInterrupt:
	write_file.write("\n\n>>> End Compendium (with " + str(len(links)) + " posts), Metadata Below <<<\n")
	write_file.write("List of books in format ([TITLE], by [AUTHOR] in [SUBREDDIT]):\n")
	for submission in compendium:
		write_file.write('> "' + submission.title+'", by u/' + submission.author.name + " in r/" + str(submission.subreddit)+"\n")