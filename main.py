# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 20:43:09 2020

@author: Yepeng Jin
"""
# This is the central script that calls for functions from crawl_website.py to generate four spreadsheets we described in our ReadMe.txt.


from crawl_website import * # note: crawl_website.py contains all major functions used to scrape author guidelins, doing data-preprocessing, and generating datasets for plotting


#Input: 'lexicon-draft-1.xlsx', the folder named 'journal' which contains 4 csv files where you can find the interested journals names
# Need Selenium and goodle driver to run get_submission_link function
# Output: a csv file named 'journal submission link.csv' in the current path
get_submission_link()

#Input: 'journal submission link.csv'
# Output: a csv file named 'instruction text.csv' in the current path, this spreadsheet contains the text for these 389 journals
get_text()

#Input: 'instruction text.csv' 
#Output: 
#---1:'word count and journal count_allfields.csv': 
#        the number of open science word mentions across All Three Fields journals (word count)
#            and the number of All Three Fields journals containing the open science word (journal count)
#---2:'word count and journal count_comm.csv': 
#        the number of open science word mentions across Communication journals (word count)
#            and the number of Communication journals containing the open science word (journal count)
get_word_count_and_journal_count("comm")
get_word_count_and_journal_count("all")

#Input: 'instruction text.csv'
#Output: final_plot.csv
get_single_rep_word()