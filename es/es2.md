# Source filtering 
```js 
GET /_search
{
    "_source": false,
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

GET /_search
{
    "_source": "obj.*",
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

GET /_search
{
    "_source": [ "obj1.*", "obj2.*" ],
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

GET /_search
{
    "_source": {
        "includes": [ "obj1.*", "obj2.*" ],
        "excludes": [ "*.description" ]
    },
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
```

# Fields 
```js 
GET /_search
{
    "stored_fields" : ["user", "postDate"],
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

GET /_search
{
    "stored_fields" : [],
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}

GET /_search
{
    "stored_fields": "_none_",
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
```
# Script Fields 
```js 
GET /_search
{
    "query" : {
        "match_all": {}
    },
    "script_fields" : {
        "test1" : {
            "script" : {
                "lang": "painless",
                "source": "doc['price'].value * 2"
            }
        },
        "test2" : {
            "script" : {
                "lang": "painless",
                "source": "doc['price'].value * params.factor",
                "params" : {
                    "factor"  : 2.0
                }
            }
        }
    }
}

GET /_search
{
  "query": {
    "match_all": {}
  },
  "script_fields": {
    "test1": {
      "script": "params['_source']['message']"
    }
  }
}
```

# Post Filter 
```js
PUT /shirts
{
  "mappings": {
    "_doc": {
      "properties": {
        "brand": {
          "type": "keyword"
        },
        "color": {
          "type": "keyword"
        },
        "model": {
          "type": "keyword"
        }
      }
    }
  }
}

PUT /shirts/_doc/1?refresh
{
  "brand": "gucci",
  "color": "red",
  "model": "slim"
}

GET /shirts/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "color": "red"
          }
        },
        {
          "term": {
            "brand": "gucci"
          }
        }
      ]
    }
  }
}

GET /shirts/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "color": "red"   }},
        { "term": { "brand": "gucci" }}
      ]
    }
  },
  "aggs": {
    "models": {
      "terms": { "field": "model" } 
    }
  }
}

GET /shirts/_search
{
  "query": {
    "bool": {
      "filter": {
        "term": { "brand": "gucci" } 
      }
    }
  },
  "aggs": {
    "colors": {
      "terms": { "field": "color" } 
    },
    "color_red": {
      "filter": {
        "term": { "color": "red" } 
      },
      "aggs": {
        "models": {
          "terms": { "field": "model" } 
        }
      }
    }
  },
  "post_filter": { 
    "term": { "color": "red" }
  }
}
```
# Scroll
```js
POST /twitter/_search?scroll=1m
{
    "size": 100,
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}

POST /_search/scroll 
{
    "scroll" : "1m", 
    "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==" 
}

DELETE /_search/scroll
{
    "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
}

DELETE /_search/scroll
{
    "scroll_id" : [
      "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==",
      "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB"
    ]
}

DELETE /_search/scroll/_all

DELETE /_search/scroll/DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ==,DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAABFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAAAxZrUllkUVlCa1NqNmRMaUhiQlZkMWFBAAAAAAAAAAIWa1JZZFFZQmtTajZkTGlIYkJWZDFhQQAAAAAAAAAFFmtSWWRRWUJrU2o2ZExpSGJCVmQxYUEAAAAAAAAABBZrUllkUVlCa1NqNmRMaUhiQlZkMWFB

GET /twitter/_search?scroll=1m
{
    "slice": {
        "id": 0, 
        "max": 2 
    },
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}

GET /twitter/_search?scroll=1m
{
    "slice": {
        "id": 1,
        "max": 2
    },
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}

GET /twitter/_search?scroll=1m
{
    "slice": {
        "field": "date",
        "id": 0,
        "max": 10
    },
    "query": {
        "match" : {
            "title" : "elasticsearch"
        }
    }
}

```
# Explain 
```js
GET /_search
{
    "explain": true,
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
```

