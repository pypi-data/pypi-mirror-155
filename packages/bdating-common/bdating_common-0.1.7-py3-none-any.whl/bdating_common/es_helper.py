"""
Elastic Helper for Bdating.
"""


def es_get_result_to_dict(es_result: dict) -> dict:
    """
    A typical es result
    {
    "_index": "local-bdating",
    "_id": "0x7bf572eF922A79d5e01d064506f682caaCa0abCd:producer",
    "_version": 1,
    "_seq_no": 0,
    "_primary_term": 1,
    "found": true,
    "_source": {
      "type": "producer",
      "wallet": "0x7bf572eF922A79d5e01d064506f682caaCa0abCd",
      "address": "10809 Mercedes Loaf Apt. 552\nNancyborough, ID 01277",
      "location": [
        -38.1355732927354,
        145.21265948643753
      ],
      "name": "Julie Simmons",
      "bio": "Number next prepare possible generation among arm."
    }
  }
    """
    return es_result.get('_source', {})


def es_search_result_to_dict(es_result: dict) -> dict:
    '''
    A typical es result
    {
  "took" : 6,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10,
      "relation" : "eq"
    },
    "max_score" : 0.020639554,
    "hits" : [
      {
        "_index" : "local-bdating",
        "_id" : "0x7bf572eF922A79d5e01d064506f682caaCa0abCd:slot",
        "_score" : 0.020639554,
        "_source" : {
          "type" : "slot",
          "wallet" : "0x7bf572eF922A79d5e01d064506f682caaCa0abCd",
          "address" : """Unit 9190 Box 6681


DPO AP 42608""",
          "location" : {
            "lat" : -37.977931083798815,
            "lon" : 145.07269918572806
          },
          "name" : "Zachary Powers",
          "bio" : "Type seat some agent.",
          "rate_aud" : 150,
          "slot_id" : 2022062623
        }
      },
      ...
    ]
  }
}

  }
    '''
    result = {
        'results': [
            r.get('_source')
            for r in es_result.get('hits', {})['hits']
        ]
    }
    if es_result.get('hits', {}).get('total', {}).get('value') is not None:
        result['total_size'] = es_result.get(
            'hits', {}).get('total', {}).get('value')
    result['size'] = len(result['results'])
    return result


def validate_slot_id(slot_id: int):
    if slot_id % 100 > 47:
        raise HTTPException(
            status_code=400, detail="slot id hour part must be between 0-47")
    if slot_id / 100 % 100 < 1 or slot_id / 100 % 100 > 31:
        raise HTTPException(
            status_code=400, detail="slot id day part must be between 1-31")
    if slot_id / 10000 % 100 < 1 or slot_id / 10000 % 100 > 12:
        raise HTTPException(
            status_code=400, detail="slot id month part must be between 1-12")
    if slot_id / 1000000 < 2020 or slot_id / 1000000 > 4000:
        raise HTTPException(
            status_code=400, detail="slot id year part must be resonable")


# def limit_query_condition(query_condition=None):
#     if query_condition:
#         return {
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "wallet": TODO_DELETE_ME
#                             }
#                         },
#                         {
#                             "match": {
#                                 "type": TYPE
#                             }
#                         },
#                         query_condition
#                     ]
#                 }
#             }
#         }
#     else:
#         return {
#             "query": {
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "wallet": TODO_DELETE_ME
#                             }
#                         },
#                         {
#                             "match": {
#                                 "type": TYPE
#                             }
#                         },
#                     ]
#                 }
#             }
#         }
