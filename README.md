# LArIATRunCatScraper

Description of this Package:
This python script retrieves the run conditions from the LArIAT run catalogue, given a csv containing
run, subrun, event number. 

What does this package contain?

<ol>
  <li>README.md</li>
  <li>ScanPage.py</li>      
  <li>test.csv</li>
</ol>


<b> So, I'm done with my analysis and want to know which portion of my data comes from which run condition... what do I need?</b>

<ol>
<li> Download this package. And you can do so by 
 > git clone  https://github.com/ElenaGramellini/LArIATRunCatScraper
</li>
<li> Whatever your favorite way of doing an analysis in LArIAT is, make your analyzer spit out a text file in the following format:
</br>
run, subrun, event
</br>
One line per each event that passes your cuts
</li>
<li> Run
 > python.py ScanPage.py <input.csv>
</li>
</ol>

