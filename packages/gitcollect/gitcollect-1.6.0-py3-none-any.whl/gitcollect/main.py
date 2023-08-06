from bs4 import BeautifulSoup
import requests, datetime, sys

def repo_desc(repo_link):
  """
  Gets the repo's description
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_="f4 my-3").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def repo_stargazers(repo_link):
  """
  Gets the number of stargazers
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_="Counter js-social-count").get_text()
    print(f"{e} stargazers ⭐")
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def issues_open(repo_link):
  """
  Gets the number of issues open
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find_all(class_='Counter')[3].get_text()
    print(f"{e} issues open 🟢")
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def issues_closed(repo_link):
  """
  Gets the number of issues open
  """
  try:
    if repo_link.endswith("/"):
      page = requests.get(f"{repo_link}issues?q=is%3Aissue+is%3Aclosed") #hmmm
    else:
      page = requests.get(f"{repo_link}/issues?q=is%3Aissue+is%3Aclosed")
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_='btn-link selected').get_text()
    print(f"{e} (issues) 🔴") #don't know why there's so many blank space hmmmm
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")


def pr_open(repo_link):
  """
  Gets the number of pull requests open
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find_all(class_='Counter')[4].get_text()
    print(f"{e} pull requests open 🟩")
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def pr_closed(repo_link):
  """
  Gets the number of pull requests open
  """
  try:
    if repo_link.endswith("/"):
      page = requests.get(f"{repo_link}pulls?q=is%3Apr+is%3Aclosed")
    else:
      page = requests.get(f"{repo_link}/pulls?q=is%3Apr+is%3Aclosed")
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_='btn-link selected').get_text()
    print(f"{e} pull requests closed 🟥") #blank space go brrr
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def branches(repo_link):
  """
  Gets how many branches a repo has
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "Link--primary no-underline").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def tags(repo_link):
  """
  Gets how many tags a repo has
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "ml-3 Link--primary no-underline").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def recent_commit(repo_link):
  """
  Gets the date, commit name, and the user who commited the most recent commit to the repo

  If the date is today, that means the commit was made less than 24 hours ago
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "d-flex flex-auto flex-justify-end ml-3 flex-items-baseline").get_text()
    f = soup.find(class_ = "css-truncate css-truncate-overflow color-fg-muted ").get_text()
    print(f"{e}{f}")
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def license(repo_link):
  """
  Gets the license type
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "Link--muted").get_text()
    if "Readme" in e: #lol
      print("This repo has no license :P")
    else:
      print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def forks(repo_link):
  """
  Gets the forks for the repo
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "BorderGrid-cell").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def default_branch(repo_link):
  """
  Gets the default branch for the repo
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "btn css-truncate").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")

def commits(github_user, year):
  """
  It gets your contributions during a specific year
  """
  try:
    current_year = datetime.datetime.today().year
    if year > current_year:
      print("Hey! Trying to look into the future I see...")
      sys.exit()
    page = requests.get(f"https://github.com/{github_user}?tab=overview&from={year}-12-01&to={year}-12-31")
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "f4 text-normal mb-2").get_text()
    print(e)
  except AttributeError:
    print("Hmm, did you enter the github username correctly?")

def releases(repo_link):
  """
  Gets the number of releases for a repo
  """
  try:
    page = requests.get(repo_link)
    soup = BeautifulSoup(page.content, 'html.parser')
    e = soup.find(class_ = "h4 mb-3").get_text()
    print(e)
  except AttributeError:
    print("Hmm, you are probably trying to detect a private repo or a repo that does not exist.")