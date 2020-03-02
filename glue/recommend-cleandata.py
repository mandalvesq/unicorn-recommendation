# JOB Glue responsabilidades: 

# Baixar os datasets
# Baixar dataset de clientes que nao querem participar do S3
# fazer a remoção dos clientes que nao querem participar
# Ajustar os nomes das colunas 
# Quebrar entre datasets: treino, test e inferencia 
# Fazer o upload dos datasets pro S3

# Import libs e criação de variaveis

import pandas as pd 
import boto3
from zipfile import ZipFile

bucket = 'glue-recommend'
client = boto3.client('s3')

# Download Datasets

client.download_file(bucket, 'dataset/bank-additional.zip', '/tmp/bank-additional.zip')
client.download_file(bucket, 'dataset/outs.csv', '/tmp/outs.csv')
print("Downloading Datasets... ")

# Unzip dataset

with ZipFile('/tmp/bank-additional.zip', 'r') as zipObj:
   zipObj.extractall('/tmp/')

local_data_path = '/tmp/bank-additional/bank-additional-full.csv'
local_data_outs_path = '/tmp/outs.csv'
data = pd.read_csv(local_data_path)
outs = pd.read_csv(local_data_outs_path)

# Deletar usuarios que nao querem participar 

dataset = data.drop(outs.index)

# Separar Dataset em treino, test e inferencia.

train_data = dataset.sample(frac=0.5,random_state=200)

test_data = dataset.drop(train_data.index)

test_data = dataset.sample(frac=0.3,random_state=200)

inferencia_data = dataset.drop(test_data.index)


test_data_no_target = test_data.drop(columns=['y'])
inferencia_data_no_target = inferencia_data.drop(columns=['y'])

# Fazer upload dos datasets de treino, test e inferencia no S3

train_file = 'train_data.csv';
train_data.to_csv(train_file, index=True, header=True)
train_data_s3_path = client.upload_file(train_file, bucket,'/train/train_data.csv')
print('Train data uploaded to: /train/train_data.csv')

test_file = 'test_data.csv';
test_data_no_target.to_csv(test_file, index=True, header=False)
test_data_s3_path = client.upload_file(test_file, bucket,'/test/test_data.csv')
print('Test data uploaded to: /test/test_data.csv')

infer_file = 'infer_data.csv';
inferencia_data_no_target.to_csv(infer_file, index=True, header=False)
infer_data_s3_path = client.upload_file(infer_file, bucket, '/infer/infer_data.csv')
print('Infer data uploaded to: /infer/infer_data.csv')
