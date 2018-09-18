# How to use BookOfReddit

### 1. Running the program
There are different ways to do this:
  - Double-click the file in Finder or Explorer
  - Open in Terminal:
    - You must be in the directory with [urls.md/txt](#DontClickThis) (if applicable) to do this! 
    - Example:
      ```
      C:\Users\XXX\BookOfReddit\> dir
      Volume in drive C is Windows
      Volume Serial Number is C812-E8FD

       Directory of C:\Users\XXX\BookOfReddit\

      18/09/2018  01:39 PM    <DIR>          .
      18/09/2018  01:39 PM    <DIR>          ..
      18/09/2018  01:39 PM              329 urls.md
      18/09/2018  01:39 PM              145 BookOfReddit_BULK_v020.py
      18/09/2018  01:39 PM    <DIR> 7783281 definetaly_homework
                     1 File(s)              474 bytes
                    0 Dir(s)  378,609,623,040 bytes free
      C:\Users\XXX\BookOfReddit\> python BookOfReddit_BULK_v020.py
      (BOOK OF REDDIT STARTS)
      ...
      ```
    - Do not run something like `python C:\Users\XXX\BookOfReddit\BookOfReddit_BULK_v020.py` unless [urls.md/txt](#DontClickThis) is in the current folder
    
### Interlude: Using urls.md/txt
urls.md and urls.txt have different purposes. Urls in urls.md will be processed as Markdown, so if you have a long list of urls in Reddit Markdown format, the program will automatically parse them. However, plaintext urls such as `https://reddit.com/r/SUBREDDITNAME/comments/xby23a` will not be processed, they go in the urls.txt file. **The program will always prioritise urls.txt over urls.md**, so if you have both files full only urls.txt will be processed (this will be optimised in a later version).

Example of urls.md:
```
***0:[The Kevin Jenkins Experience Part 1.1](http://www.reddit.com/r/HFY/comments/2ftcpy/)***
 
***0:[The Kevin Jenkins Experience Part 1.2](http://www.reddit.com/r/HFY/comments/2ftdrl/text_the_kevin_jenkins_experience_chapter_1_part/)***
 
***0:[The Kevin Jenkins Experience Part 2](http://www.reddit.com/r/HFY/comments/2ftevq/text_the_kevin_jenkins_experience_chapter_2/)***
 
***0:[The Kevin Jenkins Experience Part 3](http://www.reddit.com/r/HFY/comments/2ftfyo/text_the_kevin_jenkins_experience_chapter_3/)***
```
From the above file, the program will parse:
```
http://www.reddit.com/r/HFY/comments/2ftcpy/
http://www.reddit.com/r/HFY/comments/2ftdrl/text_the_kevin_jenkins_experience_chapter_1_part/
http://www.reddit.com/r/HFY/comments/2ftevq/text_the_kevin_jenkins_experience_chapter_2/
http://www.reddit.com/r/HFY/comments/2ftfyo/text_the_kevin_jenkins_experience_chapter_3/
```

**TL;DR and Warning: URLs inside Markdown go in urls.md, plaintext urls go in urls.txt, seperated by line break. If you put plaintext in the .md file, no URLs will be processed, if you put Markdown in the .txt file, the program will crash.**
