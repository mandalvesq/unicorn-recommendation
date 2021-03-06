# Unicorn Recommendation

Sistema de recomendação de produto financeiro baseado em ML. 

# Deploy da Solução

Para fazer o deploy da solução em uma conta AWS, siga os procedimentos abaixo.

## IAM 
- Crie todas as policies e roles para os respectivos serviços necessários para criar todos os recursos da POC.

- Lambda csv-to-dynamo-sqs-role:
    - Permissoes:
        - SQS
        - S3
        - DynamoDB
        - CloudWatch Log
        - SNS
        
- Lambda sqs-to-endpoint:
    - Permissoes:
      - SQS 
      - Pinpoint
      - CloudWatch Log
      - SNS

- Glue Job:
    - Permissoes:
      - S3

- SageMaker:
    - Permissoes:
      - S3

## Criação de recursos AWS

- Criar todos os recursos da arquitetura 

### Lambda Functions:


- csv-to-dynamo-sqs:
    
    ```
        create-function --function name csv-to-dynamo-sqs \
        --runtime python3.7 \
        --role csv-to-dynamo-sqs-role \
        --handler lambda_function.lambda_handler
        --code s3://bucket/caminhodoarquivo.py
    ```

- sqs-to-endpoint:

    ```
        create-function --function name sqs-to-endpoint \
        --runtime python3.7 \
        --role csv-to-dynamo-sqs-role \
        --handler lambda_function.lambda_handler
        --code s3://bucket/caminhodoarquivo.py
    ```

### Glue

- etl-job

      
      aws glue create-job --name recommend_clean_data \    
      --role glue_s3 \
      --command '{"Name" :  "pythonshell", "PythonVersion" : "3", 
      "ScriptLocation" : "s3://glue-recommend/scripts/clean_data.py"}
      
### S3

- datalake

``` 
aws s3api create-bucket --bucket datalake-unicorn-recommendations --region us-east-1
```

### DynamoDB

- inference-results
```
  aws dynamodb create-table \
    --attribute-definitions ID=string,Result=string \
    --table-name inference-results \
    --key-schema AttributeName=ID,KeyType=Hash,AttributeName=Result,KeyType=Range
```

### SQS

```
aws sqs create-queue --queue-name sistema-recomendacao
```


## Códigos

Os respectivos códigos da solução estão versionados nas pastas: glue, lambdas e notebook.


Versão: `python3.7` 

## Machine Learning

Para criar o notebook para executar o notebook, siga os seguintes passos: 

- TDB
