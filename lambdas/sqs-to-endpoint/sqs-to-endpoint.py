import json
import boto3
import random 

print('Loading function')
telefones = ['05511', '055119', '05511', '055119']
pinpoint = boto3.client('pinpoint')
projectid = ''
name = 'aws'
source = 'now'

def validate_number(): 
    # validar o numero e retornar se é ok ou nao
    for row in telefones: 
        print(row)
        data = pinpoint.phone_number_validate(
            NumberValidateRequest={
                'IsoCountryCode': 'US',
                'PhoneNumber': row
            }
        )
        if (data['NumberValidateResponse']['PhoneTypeCode'] == 0):
            create_endpoint(data)
        else:
            print(' Os telefones nao sao validos')

def create_endpoint(data):
    destinationNumber = data['NumberValidateResponse']['CleansedPhoneNumberE164']
    endpointid = data['NumberValidateResponse']['CleansedPhoneNumberE164']

    response = pinpoint.update_endpoint(
        ApplicationId=projectid,
        EndpointId=data['NumberValidateResponse']['CleansedPhoneNumberE164'],
        EndpointRequest={
            'Address': destinationNumber,
            'Attributes': {
                'Source': [
                    source,
                ]
            },
            'ChannelType':'SMS',
            'Location': {
                'City': data['NumberValidateResponse']['City'],
                'Country': data['NumberValidateResponse']['CountryCodeIso2'],
                'PostalCode': '11',
            },
            'OptOut': 'NONE',
            'User': {
                'UserAttributes': {
                    'Nome': [
                        name,
                    ]
                },
            }
        }
    )
    print(response)

def lambda_handler(event, context):
    validate_number()

