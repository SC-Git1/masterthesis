from types import prepare_class
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
from webdriver_manager.chrome import ChromeDriverManager

# set up headless Chrome browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.headless = True
wd = webdriver.Chrome('chromedriver',options=chrome_options)

with open("/drive/MyDrive/masterthesis/CECT_with_Genome2.tsv", "w") as f:
    # note: genome accessions are initially extracted for use in manual annotation
    f.write("Name" + "\t" + "Strain" + "\t" + "Temp" + "\t" + "Source_ID" + "\t"
            "Genome" + "\n")

    # all IDs appear to be within this range
    for i in range(20000):

        Source_ID = "CECT " + str(i)
        Name = ""
        Temp = ""
        Genome = ""
        Strain = ""

        # go to the url for ID i
        wd.get("https://www.cect.org/vstrn.php?lan=en&cect=" + str(i))
        # wait 5 seconds for the page to load
        wd.implicitly_wait(5)
        # set timeout for a page to load to 50 seconds
        wd.set_page_load_timeout(50)
        
        try:
          # if a table is present (i.e., a record is present)
          table = wd.find_element(By.ID, "fichacepa")
          body = table.find_elements(By.TAG_NAME, "tr")

          for bEl in body:
            # get current name
            if "Name" in bEl.text and "Name changes" not in bEl.text:
              Name = " ".join(bEl.text.split(" ")[1:3])
            if "Strain designation" in bEl.text:
              Strain = re.search("Strain designation (.*)", bEl.text).group(1)
            # capture temperatures in the following format: temperature (in °C): 'number'
            if "temperature (in °C):" in bEl.text:
              Temp = re.search("temperature \(in °C\): (\d+)", bEl.text).group(1)
            if "Genetic data" in bEl.text:
              try: 
                # capture NCBI genome assembly accessions (start with GCA_ or GCF_) in the following format: Complete genome sequence: 'accession'
                Genome = re.search("Complete genome sequence: (GC[AF]_[_AGCF0-9;. ]+)", 
                                   bEl.text).group(1)
              except:
                Genome = ""
          # keep the information only if temperature annotation is available
          if Temp != "":
            f.write(Name + "\t" + Strain + "\t"  + Temp + "\t" + Source_ID + "\t" + Genome + "\n")
            f.flush()
        except:
          pass
