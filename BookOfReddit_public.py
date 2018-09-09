# YOU NEED TO REPLACE CLIENT ID AND SECRET BELOW, OR ELSE IT WILL NOT WORK

import praw #Makes sure we can use the module

starttext = """\
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
--------------------------
"""


reddit = praw.Reddit(client_id='<YOUR CLIENT ID>',
                     client_secret='<YOUR CLIENT SECRET>')

compendium = []
link_list = []

print("--- Welcome to Book of Reddit, enter a URL ---")
print("(Use CTRL-C to exit or 'wipe' to wipe the file)")
link = str(input("URL: "))
link_list.append(link)
submission = reddit.submission(url=link)
compendium.append(submission)
write_file = open(submission.title+".txt",'w+')
write_file.close()
write_file = open(submission.title+".txt",'a+')
write_file.write(starttext)
write_file.write("\n--- " + submission.title + " ---\n")
write_file.write(submission.selftext)

try:
	while True:
		link = str(input("URL: "))
		if link=="wipe":
			f.truncate(0)
			print("Wipe OK, links previously in file: " + link_list)
		link_list.append(link)
		submission = reddit.submission(url=link)
		compendium.append(submission)
		write_file.write("\n--- " + submission.title + " ---\n")
		write_file.write(submission.selftext)
		print("Write OK, CTRL-C to exit, 'wipe' to wipe file.\n")
except KeyboardInterrupt:
	write_file.write("\n\n------ End Compendium, Metadata Below ------\n")
	write_file.write("List of books in format ([TITLE], by [AUTHOR] in [SUBREDDIT]):\n")
	for submission in compendium:
		write_file.write('"' + submission.title+'", by ' + submission.author.name + " in " + str(submission.subreddit)+"\n")