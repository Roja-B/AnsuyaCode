## from pybing import Bing
## import urllib

## bing=Bing('<E6C1E113773ED242B82E03F49740BACD17FDAA36>')
## response=bing.search_web('global street fashion')
## print response['SearchResponse']['Web']['Total']

from pybing.query import WebQuery
query=WebQuery('E6C1E113773ED242B82E03F49740BACD17FDAA36',query='global street fashion')
results=query.execute()
for result in results[:3]:
    print repr(result.title)
