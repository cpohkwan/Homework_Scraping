#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# ## **Exercise 1**
# 
# Scrape the following into CSV files. Each one is broken up into multiple tiers – the more you scrape the tougher it is!
# Scrape https://www.congress.gov/members (Links to an external site.)
# Tier 1: Scrape their name and full profile URL, and additional
# Tier 2: Separate their state/party/etc into separate columns
# Advanced: Scrape each person's actual data from their personal project

# In[3]:


response = requests.get("https://www.congress.gov/members")
doc = BeautifulSoup(response.text)


# In[4]:


doc


# In[5]:


# doc.select(".result-heading") - This returns two rows of the same result

congress_members = []

members = doc.find_all("li", class_="expanded")

for member in members:
    name = member.find("span", class_="result-heading")
    url = member.find("a")["href"]
    
    #print(name.text, "https://www.congress.gov" + url)
    
    congress_member = {
        "name": name.text,
        "url": "https://www.congress.gov" + url
    }

    congress_members.append(congress_member)
    
congress_members


# In[6]:


congress_members = []

members = doc.find_all("li", class_="expanded")

for member in members:
    name = member.find("span", class_="result-heading")
    url = member.find("a")["href"]
    state = member.select_one("#main > ol > li:nth-child(n) > div.quick-search-member > div.member-profile.member-image-exists > span:nth-child(n) > span")
    party = member.select_one("#main > ol > li:nth-child(n) > div.quick-search-member > div.member-profile.member-image-exists > span:nth-last-child(2) > span")
    
    congress_member = {
        "name": name.text,
        "url": "https://www.congress.gov" + url,
        "state": state.text,
        "party": party.text
    }

    congress_members.append(congress_member)

congress_members


# In[7]:


df = pd.DataFrame(congress_members)
df


# In[8]:


urls = []

for member in members:
    url = member.find("a")["href"]
    url = "https://www.congress.gov" + url
    
    urls.append(url)
    
urls


# In[9]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[10]:


# Getting errors while trying to scrape all URLs:

# for url in urls:
    # response = requests.get(url)
    # doc = BeautifulSoup(response.text)
    
# ConnectionError: HTTPSConnectionPool(host='www.congress.gov', port=443): Max retries exceeded with url: /member/daniel-akaka/A000069 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x1183aeb30>: Failed to establish a new connection: [Errno 50] Network is down'))

# So, ended up scraping just the **first url** to test the code


# In[11]:


response = requests.get("https://www.congress.gov/member/james-abdnor/A000009")
doc = BeautifulSoup(response.text)
doc


# In[12]:


# name = doc.select_one(".legDetail")
# print(name)

# <h1 class="legDetail">Senator James Abdnor<span class="birthdate"> (1923 - 2012)</span><span>In Congress 1973 - 1987</span></h1>

# Can't isolate the senator's name when I go with doc.select_one(".legDetail") or doc.find("h1", {"class":"legDetail"})
# Tried doc.select_one(".legDetail h1:first-child" and many other variations of this code but got "None" when printing name


# In[13]:


name = doc.find("title")
name = name.text.replace(" | Congress.gov | Library of Congress", "")
name


# In[14]:


birthdate = doc.select_one("#content > div.featured > h1 > span.birthdate")
birthdate = birthdate.text.strip().replace("(", "").replace(")", "")
birthdate


# In[15]:


in_congress = doc.select_one("#content > div.featured > h1 > span:nth-child(2)")
in_congress = in_congress.text.replace("In Congress", "").strip()
in_congress 


# In[16]:


# to run the following to scrape the members' details in all urls 

# profiles = []

# for url in urls:
    # name = doc.find("title").text.replace(" | Congress.gov | Library of Congress", "")
    # birthdate = doc.select_one("#content > div.featured > h1 > span.birthdate").text.strip().replace("(", "").replace(")", "")
    # in_congress = doc.select_one("#content > div.featured > h1 > span:nth-child(2)").text.replace("In Congress", "").strip()
    
    # profile = {
        # "name": name,
        # "birthdate": birthdate,
        # "in_congress": in_congress
    # }

    # profiles.append(profile)
    
# df = pd.DataFrame(profiles)

# Help! please show the smarter, faster way to get this done!


# ## **Exercise 2**
# 
# Scrape https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx (Links to an external site.)
# Tier 1: Scrape the date, URL to agenda, URL to board minutes
# Tier 2: Download agenda items to an "agendas" folder and board minutes to a "minutes" folder

# In[341]:


response = requests.get("https://www.marylandpublicschools.org/stateboard/Pages/Meetings-2018.aspx")
doc = BeautifulSoup(response.text)
doc


# In[219]:


pd.read_html(response.text, flavor="html5lib", skiprows=1, header=0)[0]


# In[107]:


table = doc.find("table")
print(table.prettify())


# In[322]:


# I tried scraping this table by row using the cells[0] method but couldn't get it right, so I have to borrow your method. 
# And I'm not sure why it doesn't work when I tried table.select("tbody a"). 

urls = doc.select("table a")

rows = []
for url in urls:
    row = {
        "date": url.text.replace("Board", " "),
        "url": url["href"]
        }
                                  
    rows.append(row)

df = pd.DataFrame(rows)
df


# In[434]:


meeting_dates = []

dates = doc.select("tr strong")
for date in dates:
    date = date.text.replace("Board Agenda", "")
    date = date.replace("Board Minutes", "")
    print(date)
    
    meeting_dates.append(date)

del meeting_dates[0]

meeting_dates


# In[435]:


agenda_urls = doc.select("table a[href*=meeting-agendas]")
minute_urls = doc.select("table a[href*='minutes']")


# In[436]:


agenda_full_urls = ["https://www.marylandpublicschools.org" + url['href'] for url in agenda_urls if url["href"] != '/stateboard/Pages/meeting-agendas/2016-02-11.aspx']
minute_full_urls = ["https://www.marylandpublicschools.org" + url['href'] for url in minute_urls]

agenda_full_urls


# In[437]:


table = {
    "meeting_dates": meeting_dates,
    "agenda_urls": agenda_full_urls,
    "minute_urls": minute_full_urls
}

table


# In[439]:


df = pd.DataFrame(table)
df


# In[442]:


df.to_csv("state_board_2018_meetings", index=False)


# In[449]:


# Don't really understand the syntax here. What's f for?

with open("agenda_urls.txt", "w") as f:
    f.write('\n'.join(agenda_full_urls))
    
with open("minute_urls.txt", "w") as f:
    f.write('\n'.join(minute_full_urls))


# In[450]:


get_ipython().system('wget --no-verbose -i agenda_urls.txt -P agendas')


# In[451]:


get_ipython().system('wget --no-verbose -i minute_urls.txt -P agendas')


# **Exercise 3**
# 
# Scrape http://www.nvmcsd.org/our-school-board/meetings/agendas (Links to an external site.)
# Tier 1: Scrape the name of the link and the URL
# Tier 2: Add a column for the date (you'll need to manually edit some, probably [but using pandas!])
# Tier 3: Download the PDFs but name them after the date

# In[452]:


response = requests.get("http://www.nvmcsd.org/our-school-board/meetings/agendas")
doc = BeautifulSoup(response.text)
doc

# blocked


# In[456]:


import requests

cookies = {
    '_gid': 'GA1.2.1537398196.1658161435',
    '_ga_D6KJ33W4L0': 'GS1.1.1658161435.1.1.1658161734.0',
    '_ga': 'GA1.2.1941387291.1658161435',
}

headers = {
    'authority': 'nvmcsd.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_gid=GA1.2.1537398196.1658161435; _ga_D6KJ33W4L0=GS1.1.1658161435.1.1.1658161734.0; _ga=GA1.2.1941387291.1658161435',
    'dnt': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

response = requests.get('https://nvmcsd.org/our-school-board/meetings/agendas', cookies=cookies, headers=headers)


# In[459]:


doc = BeautifulSoup(response.text)
print(doc.prettify())


# In[552]:


datapoints = doc.select(".kt-accordion-panel-inner a")
datapoints


# In[553]:


for item in datapoints:
    file_name = item.text
    link = item["href"]


# In[512]:


items = []

for item in datapoints:
    item = {
        "file_name": item.text,
        "url": item["href"]
    }

    items.append(item)

df = pd.DataFrame(items)
df


# In[554]:


# add date column

df["date"] = df.file_name.str.extract("(.* \d\d\d\d)")
df["date"] 
# remove cells with no dates

new_df = df[df.date.notnull()]


# checking to see if the second, third urls in the same cells (e.g. May 31, 2022 Special School Board Meeting; Item #2; Item #3) are scraped 
pd.options.display.max_colwidth

new_df

# So, looks like only the first URL in every cell is scraped.


# In[574]:


# Tried updating "anuary 5, 2022" in row 17 to "January 5" but couldn't do so. 

new_df["date"].values[17] == "January 5, 2022"
new_df["date"].values[17]
new_df


# In[571]:


# Tried updating "anuary 5, 2022" in row 17 to "January 5" with another method but couldn't do so. 

new_df["date"].values[17] = "January 5, 2022"
new_df.iat[17,2] = "January 5, 2022"
new_df


# In[575]:


get_ipython().system('mkdir -p mineral-school-board-meeting-minutes')


# In[581]:


# Just copying

for index, row in new_df.iterrows():
    url = row['url']
    
    clean_date = row['date'].lower().replace(",", "").replace(" ", "-")
    filename = f"mineral-school-board-meeting-minutes/{clean_date}.pdf"

    print("Saving", url)
    
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
        
    # don't understand with open, wb (binary?), and f


# **Exercise 4**
# 
# Scrape https://rocktumbler.com/blog/rock-and-mineral-clubs/ (Links to an external site.)
# Tier 1: Scrape all of the name and city
# Tier 2: Scrape the name, city, and URL
# Tier 3: Scrape the name, city, URL, and state name (you'll probably need to learn about "parent" nodes)

# In[582]:


response = requests.get("https://rocktumbler.com/blog/rock-and-mineral-clubs/")
doc = BeautifulSoup(response.text)


# In[583]:


doc


# In[586]:


doc.select("table a")


# In[605]:


rows = doc.find_all("tr", bgcolor="#FFFFFF")
print(rows)


# In[638]:


clubs = []

for row in rows:

    club_name = row.find("a").text
    url = row.find("a")["href"]
    city = row.find("td", width="40%").text
    
    club = {
    "club_name": club_name,
    "url": url,
    "city": city    
    }
    
    clubs.append(club)

df = pd.DataFrame(clubs)
df


# In[657]:


clubs = []

for row in rows:

    club_name = row.find("a").text
    url = row.find("a")["href"]
    city = row.find("td", width="40%").text
    state = row.find_parent("section").find("h3").text
    
    club = {
    "club_name": club_name,
    "url": url,
    "city": city,
    "state": state
    }
    
    clubs.append(club)

df = pd.DataFrame(clubs)
df


# In[660]:


df["state"] = df.state.str.replace("Rock and Mineral Clubs", "")


# In[661]:


df


# In[ ]:




