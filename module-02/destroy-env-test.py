import boto3
import json
import requests
import hashlib
import sys
import datetime

clientec2 = boto3.client('ec2')
response = clientec2.describe_instances()

print("Begin tests for destroy-env.sh module 2...")
destroyTestResults = []

# Check for empty response or no EC2 instances
if 'Reservations' not in response or len(response['Reservations']) == 0:
    sys.exit("No EC2 instances are listed or available - did you mean to run this destroy test?")

# Loop through reservations and instances
for reservation in response.get('Reservations', []):
    for instance in reservation.get('Instances', []):
        state = instance['State']['Name']
        if state not in ['pending', 'shutting-down', 'terminated', 'stopping', 'stopped']:
            print(f"EC2 instance {instance['InstanceId']} has an incorrect state: {state}.")
            destroyTestResults.append(False)
        else:
            print(f"EC2 instance {instance['InstanceId']} has a correct state: {state}.")
            destroyTestResults.append(True)

# Calculate grand total
grandtotal = 1 if False not in destroyTestResults else 0
print(f"Your result is: {grandtotal} out of 1 points.")

# Create and write the results to a file
assessmentName = "module-2-assessment-destroy-test"
dt = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
resultToHash = (assessmentName + str(grandtotal) + dt)
h = hashlib.new('sha256')
h.update(resultToHash.encode())

resultsdict = {
    'Name': assessmentName,
    'gtotal': grandtotal,
    'datetime': dt,
    'sha': h.hexdigest()
}

with open('destroy-env-module-02-results.txt', 'w', encoding="utf-8") as f:
    json.dump(resultsdict, f)

print("Write successful! Ready to submit your assessment.")
