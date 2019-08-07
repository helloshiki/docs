# Update
## Operation Type 
```js
PUT twitter/_doc/2?op_type=create
{
  "user": "kimchy",
  "post_date": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}

PUT twitter/_doc/1/_create
{
  "user": "kimchy",
  "post_date": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}
```
## Automatic ID Generation 
```js
POST twitter/_doc/
{
  "user": "kimchy",
  "post_date": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}
```
## Routing 
```js
POST twitter/_doc?routing=kimchy
{
  "user": "kimchy",
  "post_date": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}
```
## Timeout 
```js
PUT twitter/_doc/1?timeout=5m
{
  "user": "kimchy",
  "post_date": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}
```
## Versioning 
```js
PUT twitter/_doc/1?version=2&version_type=external
{
  "message": "elasticsearch now has versioning support, double cool!"
}
```

# Query 
## Get Api 
```js
GET twitter/_doc/1

HEAD twitter/_doc/1
```
## Source filtering
```js
GET twitter/_doc/1?_source=false

GET twitter/_doc/1?_source_includes=*.id&_source_excludes=entities
GET twitter/_doc/1?_source=*.id,retweeted
```
## Store Fields
```js
DELETE twitter
PUT twitter
{
  "mappings": {
    "_doc": {
      "properties": {
        "counter": { "type": "integer", "store": false },
        "tags": { "type": "keyword", "store": true }
      }
    }
  }
}

PUT twitter/_doc/1
{
  "counter": 1,
  "tags": [ "red" ]
}

GET twitter/_doc/1

GET twitter/_doc/1?stored_fields=tags,counter

PUT twitter/_doc/2?routing=user1
{
  "counter": 1,
  "tags": [ "white" ]
}

GET twitter/_doc/2?routing=user1&stored_fields=tags,counter
```
## Getting  the _source directly
```js
GET twitter/_doc/1/_source

GET twitter/_doc/1/_source?_source_includes=*.id&_source_excludes=entities

GET twitter/_doc/2?routing=user1
```

# Delete 
## Delete Api
```js
DELETE /twitter/_doc/1
DELETE /twitter/_doc/1?routing=kimchy
DELETE /twitter/_doc/1?timeout=5m
```
## Delete by Query Api 
```js
POST twitter/_delete_by_query
{
  "query": {
    "match": {
      "message": "some message"
    }
  }
}

POST twitter/_doc/_delete_by_query?conflicts=proceed
{
  "query": {
    "match_all": {}
  }
}

POST twitter/_delete_by_query?routing=1
{
  "query": {
    "range": {
      "age": {　"gte": 10 }
    }
  }
}

POST twitter/_delete_by_query?scroll_size=5000
{
  "query": {
    "term": {　"user": "kimchy" }
  }
}
```

# Update 
## Scripted Updates 
```js
POST test/_doc/1/_update
{
  "script": {
    "source": "ctx._source.counter += params.count",
    "lang": "painless",
    "params": { "count": 4 }
  }
}

POST test/_doc/1/_update
{
  "script": {
    "source": "ctx._source.tags.add(params.tag)",
    "lang": "painless",
    "params": { "tag": "blue" }
  }
}

POST test/_doc/1/_update
{
  "script": {
    "source": "if (ctx._source.tags.contains(params.tag)) { ctx._source.tags.remove(ctx._source.tags.indexOf(params.tag)) }",
    "lang": "painless",
    "params": { "tag": "blue" }
  }
}

POST test/_doc/1/_update
{
  "script": "ctx._source.new_field = 'value_of_new_field'"
}

POST test/_doc/1/_update
{
  "script": {
    "source": "if (ctx._source.tags.contains(params.tag)) { ctx.op = 'delete' } else { ctx.op = 'none' }",
    "lang": "painless",
    "params": { "tag": "green" }
  }
}
```
## Updates With A Partial Document
```js
POST test/_doc/1/_update
{
  "doc": {
    "name": "new_name"
  }
}

POST test/_doc/1/_update
{
  "doc": {
    "name": "new_name"
  },
  "detect_noop": false
}
```
## Scripted Upserts
```js
POST test/_doc/1/_update
{
  "script": {
    "source": "ctx._source.counter += params.count",
    "lang": "painless",
    "params": { "count": 4 }
  },
  "upsert": { "counter": 1 }
}

POST test/_doc/1/_update
{
  "doc": {
    "name": "new_name"
  },
  "doc_as_upsert": true
}

```
## Update by query 
```js
POST twitter/_update_by_query?conflicts=proceed
POST twitter/_doc/_update_by_query?conflicts=proceed

POST twitter/_update_by_query?conflicts=proceed
{
  "query": {
    "term": { "user": "kimchy" }
  }
}

POST twitter/_update_by_query
{
  "script": {
    "source": "ctx._source.likes++",
    "lang": "painless"
  },
  "query": {
    "term": { "user": "kimchy" }
  }
}

POST twitter,blog/_doc,post/_update_by_query
POST twitter/_update_by_query?routing=1
POST twitter/_update_by_query?scroll_size=100
```

# Multi Get Api
## Mget
```js
GET /_mget
{
  "docs": [
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "1"
    },
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "2"
    }
  ]
}

GET /test/_mget
{
  "docs": [
    {
      "_type": "_doc",
      "_id": "1"
    },
    {
      "_type": "_doc",
      "_id": "2"
    }
  ]
}

GET /test/_doc/_mget
{
  "docs": [
    {
      "_id": "1"
    },
    {
      "_id": "2"
    }
  ]
}

GET /test/_doc/_mget
{
  "ids": [ "1", "2" ]
}
```
## Source filtering 
```js
GET /_mget
{
  "docs": [
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "1",
      "stored_fields": [ "field1", "field2" ]
    },
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "2",
      "stored_fields": [ "field3", "field4" ]
    }
  ]
}

GET /test/_doc/_mget?stored_fields=field1,field2
{
  "docs": [
    {
      "_id": "1"
    },
    {
      "_id": "2",
      "stored_fields": [ "field3", "field4" ]
    }
  ]
}
```
## Routing 
```js
GET /_mget?routing=key1
{
  "docs": [
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "1",
      "routing": "key2"
    },
    {
      "_index": "test",
      "_type": "_doc",
      "_id": "2"
    }
  ]
}

```
# Bulk Api
## Bulk Update 
```js
POST _bulk
{"index":{"_index":"test","_type":"_doc","_id":"1"}}
{"field1":"value1"}
{"delete":{"_index":"test","_type":"_doc","_id":"2"}}
{"create":{"_index":"test","_type":"_doc","_id":"3"}}
{"field1":"value3"}
{"update":{"_id":"1","_type":"_doc","_index":"test"}}
{"doc":{"field2":"value2"}}

POST _bulk
{"update":{"_id":"1","_type":"_doc","_index":"index1","retry_on_conflict":3}}
{"doc":{"field":"value"}}
{"update":{"_id":"0","_type":"_doc","_index":"index1","retry_on_conflict":3}}
{"script":{"source":"ctx._source.counter += params.param1","lang":"painless","params":{"param1":1}},"upsert":{"counter":1}}
{"update":{"_id":"2","_type":"_doc","_index":"index1","retry_on_conflict":3}}
{"doc":{"field":"value"},"doc_as_upsert":true}
{"update":{"_id":"3","_type":"_doc","_index":"index1","_source":true}}
{"doc":{"field":"value"}}
{"update":{"_id":"4","_type":"_doc","_index":"index1"}}
{"doc":{"field":"value"},"_source":true}
```

# Reindex Api
```js 
POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter",
    "version_type": "internal"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter",
    "version_type": "external"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter",
    "op_type": "create"
  }
}

POST _reindex
{
  "conflicts": "proceed",
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter",
    "op_type": "create"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter",
    "type": "_doc",
    "query": {
      "term": {
        "user": "kimchy"
      }
    }
  },
  "dest": {
    "index": "new_twitter"
  }
}

POST _reindex
{
  "source": {
    "index": [ "twitter", "blog" ],
    "type": [ "_doc", "post" ]
  },
  "dest": {
    "index": "all_together",
    "type": "_doc"
  }
}


POST _reindex
{
  "size": 1,
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter"
  }
}

POST _reindex
{
  "size": 10000,
  "source": {
    "index": "twitter",
    "sort": { "date": "desc" }
  },
  "dest": {
    "index": "new_twitter"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter",
    "_source": ["user", "_doc"]
  },
  "dest": {
    "index": "new_twitter"
  }
}

POST _reindex
{
  "source": {
    "index": "twitter"
  },
  "dest": {
    "index": "new_twitter",
    "version_type": "external"
  },
  "script": {
    "source": "if (ctx._source.foo == 'bar') {ctx._version++; ctx._source.remove('foo')}",
    "lang": "painless"
  }
}

POST _reindex
{
  "source": {
    "index": "source",
    "query": {
      "match": {
        "company": "cat"
      }
    }
  },
  "dest": {
    "index": "dest",
    "routing": "=cat"
  }
}

POST _reindex
{
  "source": {
    "index": "source",
    "size": 100
  },
  "dest": {
    "index": "dest",
    "routing": "=cat"
  }
}

POST _reindex
{
  "source": {
    "remote": {
      "host": "http://otherhost:9200",
      "username": "user",
      "password": "pass"
    },
    "index": "source",
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "dest"
  }
}

POST _reindex
{
  "source": {
    "remote": {
      "host": "http://otherhost:9200"
    },
    "index": "source",
    "size": 10,
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "dest"
  }
}

POST _reindex
{
  "source": {
    "remote": {
      "host": "http://otherhost:9200",
      "socket_timeout": "1m",
      "connect_timeout": "10s"
    },
    "index": "source",
    "query": {
      "match": {
        "test": "data"
      }
    }
  },
  "dest": {
    "index": "dest"
  }
}
```
# Search Apis 
```js 
POST /twitter/_doc?routing=kimchy
{
  "user": "kimchy",
  "postDate": "2009-11-15T14:12:12",
  "message": "trying out Elasticsearch"
}

POST /twitter/_search?routing=kimchy
{
  "query": {
    "bool": {
      "must": {
        "query_string": {
          "query": "some query string here"
        }
      },
      "filter": {
        "term": {
          "user": "kimchy"
        }
      }
    }
  }
}

GET /twitter/_search?q=user:kimchy

GET /kimchy,elasticsearch/_search?q=tag:wow

GET /_all/_search?q=tag:wow

GET twitter/_search?q=user:kimchy
```
* q 
  * The query string (maps to the query_string query, see Query String Query for more details).
* df 
  * The default field to use when no field prefix is defined within the query.
* analyzer 
  * The analyzer name to be used when analyzing the query string.
* analyze_wildcard 
  * Should wildcard and prefix queries be analyzed or not. Defaults to false.
* batched_reduce_size
  *  The number of shard results that should be reduced at once on the coordinating node. This value should be used as a protection mechanism to reduce the memory overhead per search request if the potential number of shards in the request can be large.
* default_operator 
  * The default operator to be used, can be AND or OR. Defaults to OR.
* lenient 
  * If set to true will cause format based failures (like providing text to a numeric field) to be ignored. Defaults to false.
* explain 
  * For each hit, contain an explanation of how scoring of the hits was computed.
* _source 
  * Set to false to disable retrieval of the _source field. You can also retrieve part of the document by using _source_includes & _source_excludes (see the request body documentation for more details)
* stored_fields 
  * The selective stored fields of the document to return for each hit, comma delimited. Not specifying any value will cause no fields to return.
* sort 
  * Sorting to perform. Can either be in the form of fieldName, or fieldName:asc/fieldName:desc. The fieldName can either be an actual field within the document, or the special _score name to indicate sorting based on scores. There can be several sort parameters (order is important).
* track_scores
  * When sorting, set to true in order to still track scores and return them as part of each hit.
* track_total_hits 
  * Set to false in order to disable the tracking of the total number of hits that match the query. (see Index Sorting for more details). Defaults to true.
* timeout 
  * A search timeout, bounding the search request to be executed within the specified time value and bail with the hits accumulated up to that point when expired. Defaults to no timeout.
* terminate_after 
  * The maximum number of documents to collect for each shard, upon reaching which the query execution will terminate early. If set, the response will have a boolean field terminated_early to indicate whether the query execution has actually terminated_early. Defaults to no terminate_after.
* from 
  * The starting from index of the hits to return. Defaults to 0.
* size 
  * The number of hits to return. Defaults to 10.
* search_type 
  * The type of the search operation to perform. Can be dfs_query_then_fetch or query_then_fetch. Defaults to query_then_fetch. See Search Type for more details on the different types of search that can be performed.
* allow_partial_search_results 
  * Set to false to return an overall failure if the request would produce partial results. Defaults to true, which will allow partial results in the case of timeouts or partial failures. This default can be controlled using the cluster-level setting search.default_allow_partial_results.

# Sort 
```js 
PUT /my_index
{
    "mappings": {
        "_doc": {
            "properties": {
                "post_date": { "type": "date" },
                "user": {
                    "type": "keyword"
                },
                "name": {
                    "type": "keyword"
                },
                "age": { "type": "integer" }
            }
        }
    }
}

GET /my_index/_search
{
    "sort" : [
        { "post_date" : {"order" : "asc"}},
        "user",
        { "name" : "desc" },
        { "age" : "desc" },
        "_score"
    ],
    "query" : {
        "term" : { "user" : "kimchy" }
    }
}
```
