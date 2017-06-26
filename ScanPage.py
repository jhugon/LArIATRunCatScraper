
import re, requests, json,csv

current_tag   = "mid_f_mc7an"
energy_tag    = "mid_f_mcenrg"
polarity_tag  = "mid_f_mc7anb"

r = requests.get('http://lariat-wbm.fnal.gov/wbm/servlet/LariatRunSummary?RUN=9094')
text = r.text
print text
print text.find(current_tag )
print text.find(energy_tag  )
print text.find(polarity_tag)
print r.encoding
