# manage-AWS-EC2-tags

## Prerequesits:
AWS-CLI configured in your cli 

## Overall
This file consist of 3 part

Part 1: code lines 6-22
 in this part a file named 'tags.txt' is downloaded to a local file named 'local_tags.txt' from a private s3 bucket for the second part 
 and we do have an example file here under the same name 'local_tags.txt'
 
Part 2: code lines 25-36
  in this part we get all our EC2 instances and prints their tags, key and value.
  we compare every key and value from the tags to the content of the 'local_tags.txt' file we got from part 1 
  in case the key or value mach to a word from the tags list text file then the instace is left unchanged otherwise the instance get terminated
  
Part 3: code lines 39-58
 in this final part we get all our EC2 instances again and serach fo the first running instance, if there isnt one the code ends
 if we do find one we just create an AMI (Amazon Machine Image) from it and call a waiter and wait until the ami is exists
