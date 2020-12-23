import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class":"s-pagination"})
  pages = pagination.find_all("a")
  last_page = int(pages[-2].get_text(strip=True))
  
  return last_page

def extract_job(html):
  title = html.find("h2", {"class":"mb4"}).get_text(strip=True)
  company_row = html.find("h3").find_all("span")
  company = company_row[0].get_text(strip=True)
  location = company_row[1].get_text(strip=True)
  job_id = html["data-jobid"]

  return {'title':title, 'company':company, 'location':location, 'link':f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scraping stackoverflow page {page+1}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})

    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs

def get_so_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs