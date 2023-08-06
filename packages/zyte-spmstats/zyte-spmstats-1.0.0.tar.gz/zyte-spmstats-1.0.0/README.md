## Zyte-spmstats

It is a small python module for interacting with Zyte Smart Proxy Manager Stats API

### Documentation

[Zyte SPM Stats API Documentation](https://docs.zyte.com/smart-proxy-manager/stats.html)

### Installation

`pip install zyte-spmstats`

### Usage

1. For a single domain/netloc:

`python -m zyte.spmstats <ORG-API> amazon.com 2022-06-15T18:50:00 2022-06-17T23:00`

Output:

`
      {
         "failed": 0,
         "clean": 29,
         "time_gte": "2022-06-10T18:55:00",
         "concurrency": 0,
         "domain": "amazon.com",
         "traffic": 3865060,
         "total_time": 1945
      },
`

2. For a multiple domain/netloc:

`python -m zyte.spmstats <ORG-API> amazon.com,pharmamarket.be 2022-06-15T18:50:00 2022-06-17T23:00`

Output:

`"results": [
      {
         "failed": 88,
         "clean": 230,
         "time_gte": "2022-06-13T07:50:00",
         "concurrency": 1,
         "domain": "pharmamarket.be",
         "traffic": 3690976,
         "total_time": 2386
      },
      {
         "failed": 224,
         "clean": 8497,
         "time_gte": "2022-06-16T01:45:00",
         "concurrency": 80,
         "domain": "amazon.com",
         "traffic": 2280046474,
         "total_time": 1373
      }]`
