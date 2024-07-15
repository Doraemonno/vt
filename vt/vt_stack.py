from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    custom_resources as cr
)


class VtStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # next 10 lines of code is only for creating table
        table = dynamodb.Table(self, "MyDynamoDBTable",
        partition_key=dynamodb.Attribute(
            name="id",
            type=dynamodb.AttributeType.STRING
        ),
        billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        removal_policy=cdk.RemovalPolicy.DESTROY
        )

        
        # next 20 lines of code is for inserting data in table
         
        init_handler = _lambda.Function(self, "InitLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="init_lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Grant the init Lambda function write permissions on the DynamoDB table
        table.grant_write_data(init_handler)

        # Define a custom resource to invoke the init Lambda function
        my_provider = cr.Provider(self, "MyProvider",
            on_event_handler=init_handler
        )

        cdk.CustomResource(self, "InitCustomResource",
            service_token=my_provider.service_token
        )


     # Define the Lambda function
        handler = _lambda.Function(self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="fetch_lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Grant the Lambda function read/write permissions on the DynamoDB table
        table.grant_read_write_data(handler)

        # Define the API Gateway
        api = apigateway.RestApi(self, "MyApiGateway",
            rest_api_name="MyApi",
            description="API Gateway for DynamoDB data retrieval"
        )

        # Define the Lambda integration
        integration = apigateway.LambdaIntegration(handler)

        # Define the API Gateway resource and method
        api_resource = api.root.add_resource("data")
        api_resource.add_method("GET", integration) 