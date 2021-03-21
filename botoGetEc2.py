import boto3
import botocore
import time


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
            print("instance running -", instance)
        else:
            print("instance terminated - ", instance)
            instance.terminate()


#TODO: finsh this
# run on all EC2 instances and create AMI from the first one that is running
ec2 = boto3.resource('ec2')

try:
    for instance in ec2.instances.all():
        if(instance.state['Name'] == 'running'):
            running_instance = instance
            break

    image = running_instance.create_image(InstanceId=running_instance.id, NoReboot=True, Name="abc22")


    # instance_ami = running_instance
    # print("id for ami creation", instance_ami.id)
    # running_instance.create_image(InstanceId=running_instance.id, NoReboot=True, Name="abc12")
    # print("sleep for 20 sec")
    # time.sleep(20)
    # print("Created image from instance", running_instance.id)
    # # images = ec2.describe_images(Owners=['self'])
    # images = ec2.images.filter(Owners=['self'])
    # print("My images:")
    # for ami in images:
    #     print(ami)
    # print("Image Created ", running_instance.id)
except Exception as e:
    print("You have no instances")
    print(e)