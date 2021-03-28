from datetime import datetime
import boto3
import botocore


# open a list of tags from an s3 bucket and copy it to local
s3 = boto3.resource('s3')

try:
    s3.Bucket('tags-list').download_file('tags.txt', 'local_tags.txt')
    with open('local_tags.txt') as f:
        contents = f.read()

    print("The content of the tags file:")
    print(contents)
    print("EOF")

except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise


# run on all EC2 instances tag's and terminate if the tag is not on the list
ec2 = boto3.resource('ec2')

for instance in ec2.instances.all():
    for tag in instance.tags:
        print("*****************")
        print(tag['Key'], " -", tag['Value'])
        if tag['Key'] in contents or tag['Value'] in contents:
            print("instance remaining -", instance)
        else:
            print("instance terminated - ", instance)
            instance.terminate()


# run on all EC2 instances and create AMI from the first one that is running
ec2 = boto3.resource('ec2')

try:
    for instance in ec2.instances.all():
        if(instance.state['Name'] == 'running'):
            running_instance = instance
            print(instance)
            break

    create_ami = running_instance.create_image(InstanceId=running_instance.id,
                                               BlockDeviceMappings=[{'DeviceName': '/dev/sda1',
                                                                    'Ebs': {'DeleteOnTermination': True}}, ],
                                               NoReboot=True, Name="abc255")
    create_ami.wait_until_exists(Filters=[{'Name': 'state', 'Values': ['available']}])
    print('success: ami now available')
    print(datetime.now())
except Exception as e:
    print("You have no instances")
    print(e)