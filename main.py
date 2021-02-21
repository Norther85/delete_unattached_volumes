import boto3

ec2_client = boto3.client('ec2')

# ec2_client = boto3.client(
#     'ec2',
#     aws_access_key_id="xxxxxxxxxxxxxxxxxxxxxxxx",
#     aws_secret_access_key="xxxxxxxxxxxxxxxxxxxxxxxx"
# )

regions = [region['RegionName']
           for region in ec2_client.describe_regions()['Regions']]


def delete_unattached_volumes():
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region:", region)

        volumes = ec2.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )

        for volume in volumes:
            v = ec2.Volume(volume.id)
            print("Deleting EBS volume: ", v.id, v.size)
            v.delete()
