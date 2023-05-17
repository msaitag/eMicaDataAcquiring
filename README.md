# eMicaDataAcquiring

I'am explainng this repository in short.

this repository consists of the python sheets which I used on my Master's Thesis for data acquisition from hotel website's html structure 
with python web crawling libraries (Beautifulsoup, Selenium etc.).

sheet named 'link Detector.by' is collecting in-links from websites which will be evaluated. broken links doesn't getting into the inlinks file 'hotelinlinks.json'. 
I'm eliminating them in the code block as you can see.

sheet named 'eMicaItemDedector.py' is it contains all functions for every criteria of eMICA website evaluation scale.

sheet named 'python.py' is launching all functions one by one (depends to search for which criteria you want), 
gathering datas from websites and posting them to results file 'results.json', and from there to excel file.
