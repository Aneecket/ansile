import boto3
import sys
import json

class ags:
    def __init__(self,Region_Name):
        try:
            self.ip_list=[]
            self.ags_client=boto3.client('autoscaling',region_name=Region_Name)
            self.ec2_client=boto3.resource('ec2',region_name=Region_Name)
        except ClientError as e:
            print(("ConnectionError: %s" % e))
        self.protected_ins = 0
    def autoscaling_status(self,ags_name):
        self.response = self.ags_client.describe_auto_scaling_groups(AutoScalingGroupNames=[ags_name])
        for i  in self.response['AutoScalingGroups']:
            self.current_running_server=i['DesiredCapacity']
            self.current_minimum_server=i['MinSize']
            self.current_maximum_server=i['MaxSize']
            for instance in  i['Instances']:
                self.ip_list.append(self.ec2_client.Instance(instance['InstanceId']).private_ip_address)
        #print ("Current Running Desired Server: {}" .format(self.current_running_server))
        #print ("Current Running Minimum Server: {}" .format(self.current_minimum_server))
        #print ("Current Running Maximum Server: {}" .format(self.current_maximum_server))
        #self.private_ip =( ", ".join( repr(e) for e in self.ip_list ) )
        self.private_ip = ("".join( ", ".join( repr(e) for e in self.ip_list ) ))
        #print  self.private_ip
        return json.dumps({ 'min': self.current_minimum_server , 'max': self.current_maximum_server , 'des':self.current_running_server ,'ip': self.private_ip})
ob=ags('ap-south-1')
print(ob.autoscaling_status(sys.argv[1]))
