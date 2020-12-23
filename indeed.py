import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  last_page = int(pagination.find_all("a")[-2].string)

  return last_page

def extract_job(html):
  title = html.find("h2", {"class":"title"}).find("a")["title"]

  company = html.find("span", {"class":"company"})
  if company:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = company_anchor.get_text(strip=True)
    else:
      company = company.get_text(strip=True)
  else:
    company = None

  location = html.find("div", {"class", "recJobLoc"})['data-rc-loc']
  job_id = html['data-jk']

  return {'title':title, 'company':company, 'location':location, 'link':f"https://kr.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
  jobs = []

  for page in range(last_page):
    print(f"Scraping indeed page {page+1}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for result in results:
      job = extract_job(result)
      jobs.append(job)

  return jobs

def get_indeed_jobs():
  last_page = extract_indeed_pages()
  jobs = extract_indeed_jobs(last_page)

  return jobs