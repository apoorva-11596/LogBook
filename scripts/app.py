import sys
import logging
import rds_config
import pymysql
import json
#rds settings
rds_host  = "boomerang-server-integration.cluster-cpql5egydm6u.us-west-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
   # encodedEvent=event.encode("utf-8")
    logger.info("Event="+str(event['params']['querystring']));
    username=event['params']['querystring']['username'];
    startTime=event['params']['querystring']['startTime'];
    endTime=event['params']['querystring']['endTime'];

  #  requestParams=json.loads(encodedEvent);
    item_count = 0

    with conn.cursor() as cur:
        if startTime and endTime:
            queryToExecute="select * from logbook where user_name='%s' and event_ingestion_time_utc>'%s' and event_ingestion_time_utc<'%s' group by order by event_ingestion_time_utc "%(username,startTime,endTime);
        else:
            queryToExecute="select * from logbook where user_name='%s' gruup by order by event_ingestion_time_utc  "%(username);
        logger.info("queryToExecute="+queryToExecute);

        cur.execute(queryToExecute)
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
       	return json.dumps(json_data)
