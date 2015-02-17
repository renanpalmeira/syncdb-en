# Syncdb (Synchronization between ElasticSearch and Cassandra)

#### About:

Description:
* Technical challenge (https://www.dropbox.com/s/k6lf1c4greuirqs/Desafio_T%C3%A9cnico_Simbiose_Sincroniza%C3%A7%C3%A3o_ElasticSearch_Cassandra.pdf)

Modules:
* Cassandra-Driver (https://github.com/datastax/python-driver)
* Cqlengine (https://cqlengine.readthedocs.org)
* ElasticSearch-Py (http://www.elasticsearch.org/guide/en/elasticsearch/client/python-api/current/)
* Elasticsearch DSL (http://elasticsearch-dsl.readthedocs.org/)

Supported Databases (yet):
* ElasticSearch
* Cassandra

# Installation
* Python
    * Version: 2.7.x;
    * If you do not have the modules, just "run" on your command line ``sudo pip install -r requirements.txt ``
* Cassandra
    * http://cassandra.apache.org/
    * http://cassandra.apache.org/download/
    * https://wiki.apache.org/cassandra/GettingStarted
    * *Note*: Do not forget to create a keyspace in Cassandra `` CREATE keyspace simbiose_challenge `` (http://www.datastax.com/documentation/cql/3.0/cql/cql_reference/create_keyspace_r.html)
* ElastichSearch
    * http://www.elasticsearch.org/
    * http://www.elasticsearch.org/overview/elkdownloads/
    * http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/getting-started.html

# Getting Started

1. To start `` sudo python sync_daemon.py start ``
    * Stop `` sudo python sync_daemon.py stop ``
    * Restart `` sudo python sync_daemon.py restart ``
2. `` python start_test.py ``
    * In file (``start_test.py``) has some examples of how to *insert's*, *get's*, *updated's*;
3. (Final) Open the 2 databases, and they sync station.
    * ***suggestion***:
        * To "open" Cassandra, the cqlsh itself, is already good use;
        * For the Elastic, the suggestion is the Postman - REST Client (http://www.getpostman.com/), Google Chrome extension, but it runs as an application outside the browser;

# Running syncdb
1. After taking the test, he will be performing in the form of "daemon", ie syncdb periodically checks for changes in the bank (default: 10 seconds), but if you want to run at a certain time, just change the seconds sycn_daemon.py (`` daemon_app = DaemonApp (10) ``), rather than 10, set the desired time (in seconds);

#Read More
* https://elasticsearch-py.readthedocs.org/en/master/api.html?highlight=get#elasticsearch.Elasticsearch.get
* http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html
* https://elasticsearch-py.readthedocs.org/en/master/
* https://github.com/elasticsearch/elasticsearch-py
* https://elasticsearch-py.readthedocs.org/en/master/api.html?highlight=update#elasticsearch.Elasticsearch.update
* https://pypi.python.org/pypi/python-daemon/
* http://nanvel.name/weblog/python-unix-daemon/
* http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
* http://planetcassandra.org/getting-started-with-cassandra-and-python/
* https://datastax.github.io/python-driver/installation.html
* http://joelabrahamsson.com/elasticsearch-101/
* http://www.datastax.com/documentation/developer/python-driver/1.0/common/drivers/introduction/introArchOverview_c.html