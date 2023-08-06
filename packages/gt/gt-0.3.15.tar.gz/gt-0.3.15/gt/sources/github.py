import requests
from gt.sources.base import GitSource

# API Token can be generated here
# https://github.com/settings/tokens/new
# 'repo' and 'delete_repo' permissions must be checked.

class GitHub(GitSource):
    def __init__(self, api_token):
        self._http = requests.Session()
        self._http.headers.update({
            "Authorization": "token " + api_token
        })

    @property
    def _user(self):
        if not hasattr(self, "_user_val"):
            self._user_val = self._http.post('https://api.github.com/graphql',
                                        json={'query': 'query { viewer { login } }'}).json()\
                                        ['data']\
                                        ['viewer']\
                                        ['login']

        return self._user_val

    def git_url(self, name):
        return "ssh://git@github.com:/{0}/{1}".format(self._user, name)

    def delete(self, name):
        result = self._http.delete('https://api.github.com/repos/{0}/{1}'\
                                   .format(self._user, name))

        if result.status_code < 200 or result.status_code >= 300:
            raise Exception(result.content)

    def create(self, name, is_private=True):
        result = self._http.post('https://api.github.com/user/repos',
                               json={'name': name, 'private': is_private}).json()
        err = result.get('errors')
        message = result.get('message')

        if err or message:
            raise Exception(err or message)

    @property
    def repos(self):
        #Yo dawg I heard you like abstraction...
        query_template = '''query {
          viewer {
            repositories(first: 100 %s) {
              nodes {
                name
                  url: sshUrl
                  isPrivate
              }
              pageInfo {
                endCursor
                  hasNextPage
              }
            }
          }
      }'''

        if not hasattr(self, '_repos'):
            self._repos = []
            token = ""
            while True:
                query = query_template % token

                resp = self._http.post('https://api.github.com/graphql',
                        json={'query': query}).json()['data']\
                             ['viewer']\
                             ['repositories']

                self._repos.extend([ (r['name'], r['isPrivate']) for r in resp['nodes'] ])

                if not resp['pageInfo']['hasNextPage']:
                        break;

                token = "after: \"%s\"" % resp['pageInfo']['endCursor']

        return self._repos
