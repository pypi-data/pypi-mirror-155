=====
Usage
=====

To use Logging Utility for InfluxDB in a project::

    import log2influx

    ## initialize log2influx
    conf = json.load(open("./conf/settings.json","r"))
    log2 = Log2Influx(conf)
    user = os.environ.get("SHINYPROXY_USERNAME","unkonwn")

    # write login event
    log2.event_login(user)

    # Data loading process
    try:
        data = ...
        # log data load process
        log2.event_data_load(user,success=True)        
    except Exception as ex:
        # log data load process
        log2.event_data_load(user,success=False)
        # todo show data load error


Configuration::
    
    Configuration is a dict. Example:

.. code-block:: json

    {
        "url": "https://influxdb.swarm.edmonton.ca",
        "org": "coe",
        "bucket": "shiny_app_stats",
        "token": "pYNiUhqlfH3oc_2_BYHl9QF_p3r6EyZqBTJEG7HNbnOhoWUo0H5uoMDV2RMed35_9dX6CReSI7GzWONW_OEMgA==",
        "app_id": "needle_collection_data"
    }