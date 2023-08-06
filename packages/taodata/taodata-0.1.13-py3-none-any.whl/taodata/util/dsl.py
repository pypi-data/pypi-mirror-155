class BodyHelper:

    must_clause = 'must'
    must_not_clause = 'must_not'
    should_clause = 'should_clause'

    def __init__(self):
        self.__bool_query = {
            'bool': {
                'must': [],
                'must_not': [],
                'should': []
            }
        }
        self.__from = 0
        self.__size = 10
        self.__sort = []

    # match phrase query
    def match_phrase(self, field, value, clause='must'):
        query = {
          "match_phrase": {
            field: value
          }
        }
        self.__append_query(clause, query)
        return self

    # match all query
    def match_all(self, clause='must'):
        query = {
          "match_all": {
          }
        }
        self.__append_query(clause, query)
        return self

    # term query
    def term(self, field, value, clause='must'):
        query = {
          'term': {
            field: {
              'value': value
            }
          }
        }
        self.__append_query(clause, query)
        return self

    # terms query
    def terms(self, field, values, clause='must'):
        query = {
          "terms": {
            field: values
          }
        }
        self.__append_query(clause, query)
        return self

    def set_minimum_should_match(self, minimum_should_match):
        self.__bool_query['bool']['minimum_should_match'] = minimum_should_match
        return self

    #
    def exists(self, field, clause='must'):
        query = {
            "exists": {
              "field": field
            }
        }
        self.__append_query(clause, query)

    def set_size(self, __size):
        self.__size = __size
        return self

    def set_from(self, __from):
        self.__from = __from
        return self

    def sort(self, field, order='asc'):
        self.__sort.append(
            {
                field: {
                    'order': order
                }
            }
        )
        return self

    # range query
    # format yyyy-MM-dd HH:mm:ss
    def range(self, field, gte=None, lte=None, gt=None, lt=None, format=None, clause='must'):
        if gte is None and lte is None and gt is None and lt is None:
            return

        query = {
          'range': {
            field: {
            }
          }
        }

        if gte:
            query['range'][field]['gte'] = gte

        if lte:
            query['range'][field]['lte'] = lte

        if gt:
            query['range'][field]['gt'] = gt

        if lt:
            query['range'][field]['lt'] = lt

        if format:
            query['range'][field]['format'] = format

        self.__append_query(clause, query)
        return self

    def __append_query(self, clause, query):
        if clause == 'must':
            self.__bool_query['bool']['must'].append(query)
        elif clause == 'should':
            self.__bool_query['bool']['should'].append(query)
        elif clause == 'must_not':
            self.__bool_query['bool']['must_not'].append(query)

    def to_json(self):
        # 构建 bool_query
        body = {
            'query': self.__bool_query,
            'from': self.__from,
            'size': self.__size,
            'sort': self.__sort
        }

        return body


if __name__ == '__main__':
    helper = BodyHelper()
    helper.match_phrase('blog.raw_text','战争','should').term('blog.id','12345').set_size(20).set_from(100).sort('blog.id')
    json1 = helper.to_json()
    print(json1)

    helper1 = BodyHelper()
    helper1.range(field='blog.status_count', lte=100).match_all()
    json2 = helper1.to_json()
    print(json2)

