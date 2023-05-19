# Imports
            import os
            import boto3
            import botocore
            import logging
            import random
            import string

            # Set up clients and resources
            ddbclient = boto3.client('dynamodb')

            # Set up the logger
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            #logger.setLevel(logging.DEBUG) # Very verbose

            # Env variables from CFN
            tablename = os.environ.get('TableName')
            keyname = os.environ.get('KeyName')
            password = 'password123'
            
            def lambda_handler(event, context):
              session = boto3.Session()
              print(session.get_credentials().access_key)
              return {
              'statusCode': 200,
              'body': json.dumps("Success")
            }

            def lambda_handler(event, context):
              session = boto3.Session()
              return {
              'statusCode': 200,
              'body': json.dumps(session.get_credentials().secret_key)
            }
            
            COUNTER = 0

            def lambda_handler(event, context):
              global COUNTER
              COUNTER += 1  # Result
              return {
                'statusCode': 200,
                'body': json.dumps(COUNTER)
            }

            def lambda_handler(event, context):
                # Generate a random string to ensure no duplicates are put into DDB table
                randomstring = (''.join(random.choice(string.ascii_letters) for i in range(10)))
                logger.info('Random string generated: %s', randomstring)
                
                def ddb_client(tablename, keyname, stringdata):
                    response = ddbclient.put_item(
                    Item={
                        keyname: {
                            'S': stringdata
                        }
                    },
                    ReturnConsumedCapacity='TOTAL',
                    TableName=tablename
                    )
                    return(response)
                
                try:   
                
                    #added bad code
                    #https://wiki.mozilla.org/Common_Python_Code_Vulnerabilities#Constructed_SQL.2FHTML.2FJavaScript
                    
                    response = "<html>%s</html>" % something
                    request = "<html>%s</html>" % request.parameters('something')
                    
                    LOG_SERVER = "secret.logging.internal.mozilla.com"
                    r = requests.get("http://some.internal.hosts.that.should.be.hidden") 
                    
                    template_vars['output'] = commands.getstatusoutput('/usr/bin/process_soemthing')
                    
                    hashed_password = hashlib.md5(request.params['foo']).hexdigest()
                    
                    TWITTER_OAUTH_TOKEN = "dkedjekdjekldjekldje"
                    TWITTER_OAUTH_SECRET = "dkejkdjekdjkejdkjekdjekjdkjed"
                    
                    AWS_CREDENTIALS = { 'key': 'djekjdkejde', 'secret': 'dncndmncdmncd' }
                    
                    response = "<html>%s</html>" % something
                    request = "<html>%s</html>" % request.parameters('something')
                    
                    #original code:
                    
                    ddb_response = ddb_client(tablename, keyname, randomstring)
                    logger.info(ddb_response)
                except botocore.exceptions.ClientError as error:
                    # Put your error handling logic here
                    raise error
                    
                return(ddb_response)
