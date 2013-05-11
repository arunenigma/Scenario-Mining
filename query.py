__author__ = 'arun'


class QuerySearch(object):
    def __init__(self):
        pass

    def enterSearchQuery(self):
        query = raw_input('Enter search query: ')
        query_words = query.split(' ')
        print query_words

if __name__ == '__main__':
    q = QuerySearch()
    q.enterSearchQuery()


