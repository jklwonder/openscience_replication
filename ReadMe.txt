

Replication Guide for Science of Open Communication Science Manuscript (JOC)

Coder: Yepeng Jin (yjin225@wisc.edu), incoming PhD student at School of Business (2021 - ), University of Wisconsin-Madison
Date: June 2021

--------------------------------------------------------------------------------------

Preface

1. Scholars are encouraged to replicate the result based on the code and data we provided. One attention point is that the scripts are written based on the HTML structure of various journal submission guide websites in June 2020. As the website content and structure may change in the future, the crawling script needs to be adjusted. Scholars can use data from "instruction text.csv" to check the result based on the website crawled in June 2020. Details can be found in Description on Programming Scripts 1.B.   

2: Considering the complexity of crawling and the aesthetic requirement of plotting, we used python(main.py) to crawl website content and store the processed dataset, and RStudio(plot.R) to plot the result based on dataset we constructed("work count and journal count_comm.csv" and "final_plot.csv").
   
   Please run 'main.py' and 'r_plot.r' to reproduce the two figures [Figure 2 and Figure 3] in the manuscript. Table S3 could also be reproduced based on column "journal count" in "word count and journal count_allfields.csv". Notice 'r_plot.r' is just for checking and plotting data in R, while the main data collecting & analyses process(e.g. scraping data, removing patterns and calculating the frequency) is done in 'main.py'.

3: Before running 'main.py', you should check 
	a. the regular expression of openscience phrases in column G in 'lexicon-draft-1.xlsx'. Notice column F represents the selected openscience related phrases and column G represents the regular expression of these phrases. 
	b. the folder named 'journal'. It contains the four csv files where you can find the interested journals names for communication field, political science, psych and social psych.

4: We use the regular expression to match the openscience phrases. First we got the word stem of each phrases, then use ".?" to match multiple word connection conditions(blank, no blank, underline, hyphen etc.) For example, the regular expression "open.?data" can match "open data","opendata","open_data" and "open-data".

5: The python script is tested in Python 3.8.10 (default, May 19 2021, 13:12:57) [MSC v.1916 64 bit (AMD64)], Anaconda Individual Edition. You may need to install magic-google and selenium packages from PyPI.

Description on Programming Scripts

1: 'main.py' is the script that imports functions from crawl_website.py to create five spread sheets and Figure 2

	A-- It uses column G (the regular expression of "open science phrases" ) in "lexicon-draft-1.xlsx" and generates the below five spreadsheets: 
		
		a. 'submissionlink.csv': the links of the interested journals and whether the submission instruction is a website or a hyperlink to [PDF,WORD...]. If it is a hyperlink, you need to go to the website and copy the text to the 'guide txt' folder manually.

		b. 'instruction text.csv': the text of the author guideline instruction. Most of them are from the python crawling. Some of them are from the txt files you manually stored in step 'a'.
		
		c. 'word count and journal count_comm.csv': It contains the number of open science phrases mentions in Communication journals (word count) and number of Communication journals containing the open science phrases (journal count). This spreadsheet contains the same information as Figure 2.  

		d. 'word count and journal count_all.csv': It contains the number of open science phrases mentions in All Three Fields journals (word count) and number of All Three Fields journals containing the open science phrases (journal count).   It is the csv to generate Table S1: Total Journal Counts of Each Key Word (Among 389 Journal Guidelines Across Three Fields) in the supplementary material.
		
		e:'final_plot.csv': it is used for r_plot.r to generate Figure 3.

	B-- As the content of the journal submission guide webistes may change in the future, scholars can simply run get_word_count_and_journal_count() and get_single_rep_word() in main.py to check the result.
		Attention! You need the "instruction text.csv" to run these two functions. Make sure it is in the default folder.

2: 'crawl_website.py'

	-- This is the functional script that contains the functions to crawl the journal author guideline web pages [submissionlink.csv, instruction text.csv] and to construct the datasets for plot purpose [word count and journal count_comm.csv, final_plot.csv].
 
3: 'r_plot.r':

	-- This is the R script to generate Figure 3.
--------------------------------------------------------------------------------------

Description on Datasets


A: Open-science lexicon

 1. "Lexicon-draft-1.xlsx"
 --It contains the open science related phrases.


B: The dataset that contains information crawled from the author guideline website: (Generated by 'main.py')

	2. "submissionlink.csv"
	--It contains the hyperlink of each journal's submission instruction. 

	3. "instruction text.csv"
	--It contains the html texts from the author guideline page of each journal.

C:The dataset after processing and ready for plot and analysis: (Generated by 'main.py'）

	4. "work count and journal count_comm.csv"
	--It represents the "Number of phrases mentions in Communication journals (word count) and number of Communication journals containing the word (journal count)". This spreadsheet contains the same information as Figure 2 does.

	5. "work count and journal count_all.csv"
	--It represents the "Number of phrases mentions in All Three Fields journals (word count) and number of All Three Fields journals containing the word (journal count)". This spreadsheet is used to generate Table S1: Total Journal Counts of Each Key Word (Among 389 Journal Guidelines Across Three Fields) in the supplementary material.

	6. "final_plot.csv"
	--It is designed for r_plot.r to plot Figure 3. This spreadsheet contains the same information as Figure 3 does.


--------------------------------------------------------------------------------------


Folder "journal"
-- It contains the spreadsheets that store the names of our interested journals that were downloaded in June 2020 from the Web of Science, Journal Citation Report.

Folder "guide txt"
-- It contains the author submission instruction (i.e, author guideline) texts of those journals whose submission instruction is not a typical website but an hyper-link for another document format such as Word or PDF. 
