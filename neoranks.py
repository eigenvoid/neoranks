from bs4 import BeautifulSoup, SoupStrainer
from urllib import request
import re, sys

# Filter for obtaining usernames from search results
results = SoupStrainer('li', id = re.compile('username'))
    
# Calculate site rank for given tag and sorting method
def ranksBySort(sortBy, tag, username):
    print('Sorting by ' + sortBy + '...')

    # Sort and tag components of search URL
    sortPhrase = 'sort_by=' + sortBy
    if sortBy == 'followers':
        sortPhrase = ''
    tagPhrase = 'tag=' + tag
    if tag == 'all':
        tagPhrase = ''

    page = 1
    rank = 0
    # Stops after first 100 pages of search results. User may wish to change this number
    while page <= 100:

        # Page number component of search URL
        pagePhrase = 'page=' + str(page)
        if page == 1:
            pagePhrase = ''
        # Determine how many components (out of sort, tag and page number) are empty
        empty = 0
        phrases = [sortPhrase, tagPhrase, pagePhrase]
        for p in phrases:
            if p == '':
                empty += 1

        # Based on how many components are empty, set symbols to separate them
        del1 = ''
        if empty < 3:
            del1 = '?'
        del2 = ''
        if empty < 2:
            del2 = '&'
        del3 = ''
        if empty < 1:
            del3 = '&'

        # Build search URL and obtain webpage
        searchUrl = 'https://neocities.org/browse' + del1 + sortPhrase + del2 + tagPhrase + del3 + pagePhrase
        with request.urlopen(searchUrl) as f:
            htmlBytes = f.read()
            htmlStr = htmlBytes.decode('utf8')

        # Parse webpage using filter
        soup = BeautifulSoup(htmlStr, 'html.parser', parse_only = results)

        # If username not in results, get next page
        if soup.find_all(id = re.compile(username)) == []:
            page += 1
        # Calculate position of site in results by counting sites until it is reached
        else:
            position = 0
            for site in soup.find_all(True, recursive = False):
                position += 1
                if site == soup.find(id = re.compile(username)):
                    # Calculate rank, given that there are 100 sites per page
                    rank = position + ((page - 1) * 100)
            break

    if rank != 0:
        rankStr = str(rank)
    # If search ends before site is found, rank is unknown
    else:
        rankStr = '?'

    # Write rank for this tag and sorting method to ranks.txt
    with open('ranks.txt', 'a') as f:
        f.write('tag: ' + tag + ', sort by: ' + sortBy + ', rank: ' + rankStr + '\n')

# Site username, passed as command line argument
username = sys.argv[1]

# Obtain site tags from user profile
profileUrl = 'https://neocities.org/site/' + username
with request.urlopen(profileUrl) as f:
    htmlBytes = f.read()
    htmlStr = htmlBytes.decode('utf-8')
getTags = SoupStrainer('a', class_ = 'tag')
tagSoup = BeautifulSoup(htmlStr, 'html.parser', parse_only = getTags)

# Transfer tags to list and display list
tags = []
for tag in tagSoup.find_all(True):
    tags.append(tag.get_text())
tags.append('all')
print(username + "'s tags:")
print(tags)

# Create ranks.txt, or overwrite it if it exists
f = open('ranks.txt', 'w')
f.write(username + "'s rankings:\n\n")
f.close()

# All the ways it may be useful to sort websites. User can remove some of these
sorts = ['followers', 'hits', 'last_updated', 'newest', 'oldest', 'special_sauce', 'views']

# For each tag, get ranks for each sorting method and write to ranks.txt
for t in tags:
    print('\nSearching "' + t + '"...')
    for s in sorts:
        ranksBySort(s, t, username)
    with open('ranks.txt', 'a') as f:
        f.write('\n')
print('\nDone')
