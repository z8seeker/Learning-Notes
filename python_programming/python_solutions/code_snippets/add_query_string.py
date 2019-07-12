try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

# 为跳转 url 添加 push_id 信息
query = 'push_id={}&source=push_subscription'.format(push_id)
parsed_url = urlparse(tm.url)
if parsed_url.query:
    query += '&' + parsed_url.query
    
url = urlunparse(parsed_url._replace(query=query))
