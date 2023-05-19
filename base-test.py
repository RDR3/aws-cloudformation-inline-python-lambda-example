---
AWSTemplateFormatVersion: 2010-09-09
Description: >
    An example Lambda deployment using CloudFormation. Includes a DynamoDB table for the function to interact with.
    https://github.com/aws-samples/aws-cloudformation-inline-python-lambda-example
Parameters:
  LambdaFunctionName:
    Type: String
    MinLength: '1'
    MaxLength: '64'
    AllowedPattern: '[a-zA-Z][a-zA-Z0-9_-]*'
    Description: The name of the Lambda function to be deployed
    Default: Lambda-DynamoDB-Function-CFNExample
  LambdaRoleName:
    Type: String
    MinLength: '1'
    MaxLength: '64'
    AllowedPattern: '[\w+=,.@-]+'
    Description: The name of the IAM role used as the Lambda execution role
    Default: Lambda-Role-CFNExample
  LambdaPolicyName:
    Type: String
    MinLength: '1'
    MaxLength: '128'
    AllowedPattern: '[\w+=,.@-]+'
    Default: Lambda-Policy-CFNExample
  DynamoDBTableName:
    Type: String
    MinLength: '3'
    MaxLength: '255'
    AllowedPattern: '[a-zA-Z0-9_.-]+'
    Description: The name of the DynamoDB table to be deployed
    Default: DynamoDB-Table-CFNExample
  DynamoDBPKName:
    Type: String
    MinLength: '1'
    MaxLength: '255'
    AllowedPattern: '[a-zA-Z][a-zA-Z0-9_-]*'
    Description: The name of the primary key that will exist in the DynamoDB table
    Default: itemId
    
Resources:
  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Ref LambdaRoleName
      Description: An execution role for a Lambda function launched by CloudFormation
      ManagedPolicyArns:
        - !Ref LambdaPolicy
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action:
          - 'sts:AssumeRole'
      
  LambdaPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      ManagedPolicyName: !Ref LambdaPolicyName
      Description: Managed policy for a Lambda function launched by CloudFormation
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 'dynamodb:PutItem'
            Resource: !Sub 'arn:${AWS::Partition}:dynamodb:${AWS::Region}:${AWS::AccountId}:table/${DynamoDBTable}'
          - Effect: Allow
            Action:
              - 'logs:CreateLogStream'
              - 'logs:PutLogEvents'
            Resource: !Join ['',['arn:', !Ref AWS::Partition, ':logs:', !Ref AWS::Region, ':', !Ref AWS::AccountId, ':log-group:/aws/lambda/', !Ref LambdaFunctionName, ':*']]
          - Effect: Allow
            Action:
              - 'logs:CreateLogGroup'
            Resource: !Sub 'arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:*'
        
  LogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Join ['',['/aws/lambda/', !Ref LambdaFunctionName]]
      RetentionInDays: 30
            
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      Description: Adds a random string value to the specified DynamoDB table
      FunctionName: !Ref LambdaFunctionName
      Handler: index.lambda_handler
      MemorySize: 128
      Runtime: python3.8
      Role: !GetAtt 'LambdaRole.Arn'
      Timeout: 240
      Environment:
        Variables:
          TableName: !Ref DynamoDBTableName
          KeyName: !Ref DynamoDBPKName
      Code:
        ZipFile: |
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
    
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - 
          AttributeName: !Ref DynamoDBPKName
          AttributeType: "S"
      BillingMode: PROVISIONED
      KeySchema:
        -
          AttributeName: !Ref DynamoDBPKName
          KeyType: HASH
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      TableName: !Ref DynamoDBTableName
        
Outputs:
  CLI:
    Description: Use this command to invoke the Lambda function
    Value: !Sub |
        aws lambda invoke --function-name ${LambdaFunction} --payload '{"null": "null"}' lambda-output.txt --cli-binary-format raw-in-base64-out
