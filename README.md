# neoranks
A program to calculate how a Neocities website ranks against other Neocities websites in [Neocities search results](https://neocities.org/browse).

## Installation
[Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup) must be installed in order to run `neoranks.py`.

## Usage
Run:

```
python3 neoranks.py <username>
```

where `<username>` is the Neocities username of the site being ranked. To rank `https://example.neocities.org`, run `python3 neoranks.py example`.

The program will calculate ranks per sorting method per tag used by the site. Sorting methods include `followers`, `hits`, `last_updated`, `newest`, `oldest`, `special_sauce` and `views`. To remove a sorting method, one can alter the following line in `neoranks.py`:

```py
sorts = ['followers', 'hits', 'last_updated', 'newest', 'oldest', 'special_sauce', 'views']
```

The program will analyse the first 100 pages of search results at most. One can change this number by altering the following line in `neoranks.py`:

```py
while page <= 100:
```

The rank data is saved to the file `ranks.txt`. If a search ends before the site is found in the results, the corresponding rank is recorded as unknown, represented by `?`.

### Notes
1. If the site is ranked low in the search results for a certain tag and sorting method, the runtime of the program may be very long as it will fetch up to 100 pages of search results before moving on to the next search.
2. `neoranks.py` cannot obtain tags for sites whose Neocities profiles are disabled. If a site's profile is disabled, the script will calculate its ranks against all sites only.
