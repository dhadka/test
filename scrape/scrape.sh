# do actual google scholar scraping
python3 scrape.py 

# compose index.html
cat top.txt bib.txt bottom.txt > ./../index.html