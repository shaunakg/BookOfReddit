# BookOfReddit
Creates a compendium of Reddit posts, useful for long, series length WritingPrompts. (Originally created for r/HFY)

## Usage instructions
There are two ways to use BookOfReddit.  
  
**Manual**
- Run `python bookofreddit.py` (or whatever the filename is)  
  
**Command-line arguments**
- Run `python bookofreddit.py (url) (file name without extension) [extension]`  
Options with (round brackets) are **required** while options with \[square brackets\] are **optional**

## Information about different files
### BookOfReddit_BC_Calibre_public.py
- Bulk writes reddit post selftexts to a compendium (reading from urls.md or urls.txt)
- **NEW: Gives the option to download and extract URLs from Reddit posts! Extremely useful for wiki pages or index pages (example: [this](https://www.reddit.com/r/HFY/wiki/ref/universes/jenkinsverse/chronological_reading_order) or [this](https://www.reddit.com/r/Selben/comments/60r5ps/timeline_for_tfts_stories/))**
- **Uses UTF-8 formatting** (This file is recommended to all users)

#### md_download_to_urls.py
- **Downloads wikis and index pages from reddit into urls.md**
- Required to download reddit wikis or index posts from the internet (doesn't use PRAW so it's standalone)
- Split into a different file to reduce code clutter (don't get used to it though)

## License
**BookOfReddit and all sub-programs are under the GNU GPLv3 license. You can do anything with them except commercialise or develop closed-source versions.**  
*The files that BookOfReddit makes are consisting of Reddit posts. Please review the Reddit content policy for more information.*  
