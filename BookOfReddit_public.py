# --- Welcome to BookOfReddit ---
# This edition of BookOfReddit will (singularly) write reddit posts to a file 
# only using Windows/Unix formatting. If you don't know what that means, you 
# should use the BULK_CODECS file for general purposes.

import praw #Makes sure we can use the module

starttext = """\
reddit post compendium made by BookOfReddit (https://git.io/fA2dt)
options: bulk, UTF-8 ONLY
--------------------------
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
--------------------------
"""


reddit = praw.Reddit(client_id='<YOUR CLIENT ID>',
                     client_secret='<YOUR CLIENT SECRET>')

compendium = []
link_list = []

print("--- Welcome to Book of Reddit, enter a file name ---")
filename = input("Filename to save into (without extension): ")
print("\n")
print("(Use CTRL-C to exit or 'wipe' to wipe the file)")
write_file = open(filename+".txt",'w+')
write_file.close()
write_file = open(filename+".txt",'a+')
write_file.write(starttext)

try:
	while True:
		links = str(input("URLs (seperated by commas): ")).split(",")
		if "wipe" in links:
			f.truncate(0)
			print("Wipe OK, links previously in file: " + link_list)
		for link in links:
			link_list.append(link)
			submission = reddit.submission(url=link)
			compendium.append(submission)
			write_file.write("\n--- " + submission.title + " ---\n")
			write_file.write(submission.selftext.replace("‽", "?!"))
			print("Processed: " + submission.title)
except KeyboardInterrupt:
	write_file.write("\n\n------ End Compendium, Metadata Below ------\n")
	write_file.write("List of books in format ([TITLE], by [AUTHOR] in [SUBREDDIT]):\n")
	for submission in compendium:
		write_file.write('> "' + submission.title+'", by u/' + submission.author.name + " in r/" + str(submission.subreddit)+"\n")