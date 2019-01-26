import json
import boto3
import copy


def lambda_handler(event, context):
  
  #Declaring global variables
  global image
  image = {
    "LinuxwindowsImageId": {
      "us-east-2": {
        "linux": "ami-0f65671a86f061fcd",
        "windows": "ami-0a0772f0c61374aa5"
      },
      "us-east-1": {
        "linux": "ami-0ac019f4fcb7cb7e6",
        "windows": "ami-0c96d9489fa933423"
      },
      "us-west-1": {
        "linux": "ami-063aa838bd7631e0b",
        "windows": "ami-00dc63564bd128515"
      },
      "us-west-2": {
        "linux": "ami-0bbe6b35405ecebdb",
        "windows": "ami-06ab3380600711ab2"
      },
      "ap-south-1": {
        "linux": "ami-0d773a3b7bb2bb1c1",
        "windows": "ami-064f73035abc59315"
      },
      "ap-northeast-2": {
        "linux": "ami-06e7b9c5e0c4dd014",
        "windows": "ami-01b645ac8525ebd19"
      },
      "ap-southeast-1": {
        "linux": "ami-0c5199d385b432989",
        "windows": "ami-0077b703cac9baa12"
      },
      "ap-southeast-2": {
        "linux": "ami-07a3bd4944eb120a0",
        "windows": "ami-0869e4e50ff1a4ae5"
      },
      "ap-northeast-1": {
        "linux": "ami-07ad4b1c3af1ea214",
        "windows": "ami-02e903e6b943a4d23"
      },
      "ca-central-1": {
        "linux": "ami-0427e8367e3770df1",
        "windows": "ami-079c6702a8f78abed"
      },
      "eu-central-1": {
        "linux": "ami-0bdf93799014acdc4",
        "windows": "ami-0bd3cc88ca8ae88f5"
      },
      "eu-west-1": {
        "linux": "ami-00035f41c82244dab",
        "windows": "ami-046ad87f7b7598d2e"
      },
      "eu-west-2": {
        "linux": "ami-0b0a60c0a2bd40612",
        "windows": "ami-0d87cfd2257ebac55"
      },
      "eu-west-3": {
        "linux": "ami-08182c55a1c188dee",
        "windows": "ami-0ed99320453c5d6dc"
      },
      "eu-north-1": {
        "linux": "ami-0bc14f75",
        "windows": "ami-0a52617c75a47c7a9"
      },
      "sa-east-1": {
        "linux": "ami-03c6239555bb12112",
        "windows": "ami-05e76da9721569df6"
      }
    }
  }
  global instance
  instance = {
    "EC2instance": {
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "InstanceType": "",
        "ImageId": {"Fn::FindInMap": ["LinuxwindowsImageId",{"Ref": "AWS::Region"},""]},
        "SecurityGroupIds": [
          {
            "Ref": ""
          }
        ],
        "BlockDeviceMappings": [
          {
            "DeviceName": "",
            "Ebs": {
              "VolumeSize": "",
              "VolumeType": ""
            }
          }
        ],
        "SubnetId": {
          "Ref": ""
        },
        "KeyName": "",
        "Tags": [
          {
            "Key": "Name",
            "Value": ""
          }
        ]
      }
    }
  }
  global vpc
  vpc = {
    "Vpc" : {
      "Type" : "AWS::EC2::VPC",
      "Properties" : {
        "CidrBlock" : "10.0.0.0/16"
      }
    }
  }
  global subnet
  subnet = {
    "subnet" : {
      "Type" : "AWS::EC2::Subnet",
      "Properties" : {
        "VpcId" : {
          "Ref" : "Vpc",
        },
        "CidrBlock" : "",
        "MapPublicIpOnLaunch" : "true"
      }
    }
  }
  global vpcGatewayAttachment
  vpcGatewayAttachment = {
    "VPCGatewayAttachment":{
      "Type":"AWS::EC2::VPCGatewayAttachment",
      "Properties":{
        "VpcId": {
          "Ref" : "Vpc",
        },
        "InternetGatewayId":{
          "Ref":""
        }
      }
    }
  }
  global InternetGateway
  InternetGateway = {
    "InternetGateway":{
      "Type":"AWS::EC2::InternetGateway"
    }
  }
  global PubicRoutetable
  PubicRoutetable = {
    "PublicRouteTable": {
      "Type": "AWS::EC2::RouteTable",
      "Properties": {
        "VpcId": {
          "Ref": "Vpc"
        }
      }
    }
  }
  global RouteTable
  RouteTable = {
    "PublicRoute": {
      "Type": "AWS::EC2::Route",
      "DependsOn": "VPCGatewayAttachment",
      "Properties": {
        "RouteTableId": {
          "Ref": ""
        },
        "DestinationCidrBlock": "0.0.0.0/0",
        "GatewayId": {
          "Ref": ""
        }
      }
    }
  }
  global PublicSubnetRouteTableAssociation
  PublicSubnetRouteTableAssociation = {
    "PublicSubnetRouteTableAssociation": {
      "Type": "AWS::EC2::SubnetRouteTableAssociation",
      "Properties": {
        "SubnetId": {
          "Ref": ""
        },
        "RouteTableId": {
          "Ref": ""
        }
      }
    }
  }
  global PublicSubnetNetworkAclAssociation
  PublicSubnetNetworkAclAssociation = {
    "PublicSubnetNetworkAclAssociation": {
      "Type": "AWS::EC2::SubnetNetworkAclAssociation",
      "Properties": {
        "SubnetId": {
          "Ref": ""
        },
        "NetworkAclId": {
          "Ref": "NetworkAcl"
        }
      }
    }
  }
  global NetworkAcl
  NetworkAcl = {
    "NetworkAcl": {
      "Type": "AWS::EC2::NetworkAcl",
      "Properties": {
        "VpcId": {
          "Ref": "Vpc"
        }
      }
    }
  }
  global InstanceSecurityGroup
  InstanceSecurityGroup = {
    "InstanceSecurityGroup": {
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "GroupDescription" : "Enable SSH access via port 22",
        "VpcId": {
          "Ref": "Vpc"
        },
        "SecurityGroupIngress": [
          {
            "IpProtocol": "tcp",
            "FromPort": "22",
            "ToPort": "22",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "3389",
            "ToPort": "3389",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "443",
            "ToPort": "443",
            "CidrIp": "0.0.0.0/0"
          },
          {
            "IpProtocol": "tcp",
            "FromPort": "80",
            "ToPort": "80",
            "CidrIp": "0.0.0.0/0"
          }
        ]
      }
    }
  }
  global winchrome
  winchrome = {
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
          ]
        ]
      }
    }
  }
  global linchrome
  linchrome ={
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
            "#!/bin/bash",
            "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
            "sudo dpkg -i google-chrome-stable_current_amd64.deb",
            "sudo apt-get update"
          ]
        ]
      }
    }
  }
  global linfirefox
  linfirefox = {
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
            "#!/bin/bash",
            "sudo apt install firefox",
            "sudo apt-get update"
          ]
        ]
      }
    }
  }
  global winfirefox
  winfirefox = {
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
          ]
        ]
      }
    }
  }
  global linopera
  linopera = {
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
            "#!/bin/bash",
            "wget -qO- https://deb.opera.com/archive.key | sudo apt-key add -",
            "sudo add-apt-repository deb [arch=i386,amd64] https://deb.opera.com/opera-stable/ stable non-free",
            "sudo apt-get update",
            "sudo apt-get install -y opera-stable",
            "sudo apt-get update"
          ]
        ]
      }
    }
  }
  global winopera
  winopera = {
    "UserData": {
      "Fn::Base64": {
        "Fn::Join": [
          "\n",
          [
          ]
        ]
      }
    }
  }
  global loadbalncer
  loadbalncer = {
    "LoadBalancer": {
      "Type": "AWS::ElasticLoadBalancing::LoadBalancer",
      "Properties": {
        "LoadBalancerName": "LoadBalancer",
        "Listeners": [
          {
            "InstancePort": "80",
            "InstanceProtocol": "HTTP",
            "LoadBalancerPort": "80",
            "Protocol": "HTTP"
          }
        ],
        "Scheme": "internet-facing",
        "HealthCheck": {
          "Target": {
            "Fn::Join": ["",["HTTP:","80", "/healthchecker.php"]]
          },
          "HealthyThreshold": "10",
          "UnhealthyThreshold": "5",
          "Interval": "20",
          "Timeout": "10"
        },
        "SecurityGroups": [
          {
            "Ref": ""
          }
        ],
        "Subnets": [
          {
            "Ref": ""
          }
        ]
      }
    }
  }
  global AutoScaling
  AutoScaling = {
    "AutoScaling": {
      "Type": "AWS::AutoScaling::AutoScalingGroup",
      "Properties": {
        "VPCZoneIdentifier": [
          {
          "Ref": ""
          }
        ],
        "LaunchConfigurationName": {
          "Ref": ""
        },
        "MinSize": "1",
        "MaxSize": "10",
        "Tags": [
          {
            "Key": "Name",
            "Value": "",
            "PropagateAtLaunch": "true"
          }
        ]
      }
    }
  }
  global launchconfiguration
  launchconfiguration = {
    "LaunchConfig" : {
      "Type" : "AWS::AutoScaling::LaunchConfiguration",
      "Properties" :{
        "InstanceType": "",
        "ImageId": { "Fn::FindInMap" : [ "LinuxwindowsImageId", { "Ref" : "AWS::Region" }, ""]},
        "BlockDeviceMappings": [
          {
            "DeviceName": "",
            "Ebs": {
              "VolumeSize": "",
              "VolumeType": ""
            }
          }
        ],
        "SecurityGroups": [
          {
            "Ref": ""
          }
        ],
        "KeyName": ""
      },
      "DependsOn": "VPCGatewayAttachment"
    }
  }
  
  Cloud = boto3.resource('cloudformation')
  s3 = boto3.resource('s3')
  
  '''
  #when getting mail from the bucket
  #getting bucket and key
   
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = event['Records'][0]['s3']['object']['key']
  
  #Reading the JSon Template 
  template = s3_resource.Object('infra-mail', 'template.json')
  file_content = template.get()['Body'].read().decode('utf-8')
  ******_template = json.loads(file_content)
  
  #Reading email content
  file = s3.get_object(Bucket=bucket, Key=key)
  email_content = email.message_from_string(file['Body'].read().decode('utf-8'))
  attachment = base64.b64decode(email_content.get_payload()[1].get_payload()).decode('utf-8')
  lines = []
  
  for line in attachment.split('\r\n'):
        lines.append(line.split(','))
        
    '''
  
  instances = {}
  Public_Subnet = {}
  public_vpcGateway = {}
  Route_Table = {}
  PublicSubnet_RouteTableAssociation = {}
  PublicSubnet_NetworkAclAssociation = {}
  Auto_Scaling = {}
  launch_configuration = {}
  load_balncer ={}
  
  #Creating template
  
  stack_temp = {'Mappings' : {},'Resources' : {} }
  
  #Creating vpc Gateway
  
  public_vpcGateway['VPCGatewayAttachment'] = copy.deepcopy(vpcGatewayAttachment['VPCGatewayAttachment'])
  public_vpcGateway['VPCGatewayAttachment']['Properties']['InternetGatewayId']['Ref'] = 'InternetGateway'
  
  #Creating Route table
  
  Route_Table['PublicRoute'] = copy.deepcopy(RouteTable['PublicRoute'])
  Route_Table['PublicRoute']['Properties']['RouteTableId']['Ref'] = 'PublicRouteTable'
  Route_Table['PublicRoute']['Properties']['GatewayId']['Ref'] = 'InternetGateway'
  
  stack_temp['Mappings'].update(image) 
  stack_temp['Resources'].update(vpc)
  stack_temp['Resources'].update(InternetGateway)
  stack_temp['Resources'].update(public_vpcGateway)
  stack_temp['Resources'].update(NetworkAcl)
  stack_temp['Resources'].update(PubicRoutetable)
  stack_temp['Resources'].update(Route_Table)
  stack_temp['Resources'].update(InstanceSecurityGroup)


  row = ['linux','t2.micro','','','','chrome','10','gp2']
  for  i in range(1,3):
    
    
      #Creaating Instance resource
      
      instances['EC2instance' + str(i)] = copy.deepcopy(instance['EC2instance'])
      instances['EC2instance' + str(i)]['Properties']['InstanceType'] = row[1]
      instances['EC2instance' + str(i)]['Properties']['ImageId']['Fn::FindInMap'][2] = row[0]
      instances['EC2instance' + str(i)]['Properties']['KeyName'] = 'new'
      instances['EC2instance' + str(i)]['Properties']['SecurityGroupIds'][0]['Ref'] = 'InstanceSecurityGroup'
      instances['EC2instance' + str(i)]['Properties']['SubnetId']['Ref'] = 'subnet' +str(i)
      instances['EC2instance' + str(i)]['Properties']['Tags'][0]['Value'] = 'insta' + str(i)
      instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['Ebs']['VolumeSize'] = row[6]
      instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['Ebs']['VolumeType'] = row[7]
      
      #Creating Autoscaling 
      
      Auto_Scaling['AutoScaling' + str(i)] = copy.deepcopy(AutoScaling['AutoScaling'])
      Auto_Scaling['AutoScaling' + str(i)]['Properties']['VPCZoneIdentifier'][0]['Ref'] = 'subnet' + str(i)
      Auto_Scaling['AutoScaling' + str(i)]['Properties']['LaunchConfigurationName']['Ref'] = 'LaunchConfig' + str(i)
      Auto_Scaling['AutoScaling' + str(i)]['Properties']['Tags'][0]['Value'] = 'AutoScaling Instance for' + str(i)
      
      #Creating Launchconfiguration
      
      launch_configuration['LaunchConfig' + str(i)] = copy.deepcopy(launchconfiguration ['LaunchConfig'])
      launch_configuration['LaunchConfig' + str(i)]['Properties']['InstanceType'] = row[1]
      launch_configuration['LaunchConfig' + str(i)]['Properties']['ImageId']['Fn::FindInMap'][2] = row[0]
      launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['Ebs']['VolumeSize'] = row[6]
      launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['Ebs']['VolumeType'] = row[7]
      launch_configuration['LaunchConfig' + str(i)]['Properties']['KeyName'] = 'new'
      launch_configuration['LaunchConfig' + str(i)]['Properties']['SecurityGroups'][0]['Ref'] = 'InstanceSecurityGroup'
        
      #creating a loadbalancer
      
      load_balncer['LoadBalancer'] = copy.deepcopy(loadbalncer['LoadBalancer'])
      load_balncer['LoadBalancer']['Properties']['SecurityGroups'][0]['Ref'] = 'InstanceSecurityGroup'
      load_balncer['LoadBalancer']['Properties']['Subnets'][0]['Ref'] = 'subnet' + str(i)
  
      
        #updating user data for instaling chrome,firefox,opera    
        
      if row[0].lower() == 'windows' and row[5].lower() == 'chrome':
        
        instances['EC2instance' +str(i)]['Properties'].update(winchrome)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(winchrome)
        
      elif row[0].lower() == 'windows' and row[5].lower() == 'firefox':
        
        instances['EC2instance' +str(i)]['Properties'].update(winfirefox)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(winfirefox)
        
      elif row[0].lower() == 'windows' and row[5].lower() == 'opera':
        
        instances['EC2instance' +str(i)]['Properties'].update(winopera)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(winopera)
        
      elif row[0].lower() == 'linux' and row[5].lower() == 'chrome':
        
        instances['EC2instance' +str(i)]['Properties'].update(linchrome)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(linchrome)
        
      elif row[0].lower() == 'linux' and row[5].lower() == 'firefox':
        
        instances['EC2instance' +str(i)]['Properties'].update(linfirefox)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(linfirefox)
       
      elif row[0].lower() == 'linux' and row[5].lower() == 'opera':
        
        instances['EC2instance' +str(i)]['Properties'].update(linopera)
        instances['EC2instance' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties']['BlockDeviceMappings'][0]['DeviceName'] = '/dev/sda1'
        launch_configuration['LaunchConfig' + str(i)]['Properties'].update(linopera)
        
        
      
      #Creating Publicsubnet
      
      Public_Subnet['subnet' + str(i)] = copy.deepcopy(subnet['subnet']) 
      Public_Subnet['subnet' + str(i)]['Properties']['CidrBlock'] = '10.0.'+str(i)+'.0/24'
      
      #Creating Public Subnet Route Table Association 
    
      PublicSubnet_RouteTableAssociation['PublicSubnetRouteTableAssociation' + str(i)] = copy.deepcopy(PublicSubnetRouteTableAssociation['PublicSubnetRouteTableAssociation'])
      PublicSubnet_RouteTableAssociation['PublicSubnetRouteTableAssociation' + str(i)]['Properties']['SubnetId']['Ref'] = 'subnet' + str(i)
      PublicSubnet_RouteTableAssociation['PublicSubnetRouteTableAssociation' + str(i)]['Properties']['RouteTableId']['Ref'] = 'PublicRouteTable'
      
      #creation Public Subnet Network Acl Association
      
      PublicSubnet_NetworkAclAssociation['PublicSubnetNetworkAclAssociation' + str(i)] = copy.deepcopy(PublicSubnetNetworkAclAssociation['PublicSubnetNetworkAclAssociation'])
      PublicSubnet_NetworkAclAssociation['PublicSubnetNetworkAclAssociation' + str(i)]['Properties']['SubnetId']['Ref'] = 'subnet' + str(i)
      
      stack_temp['Resources'].update(instances)
      stack_temp['Resources'].update(Public_Subnet)
      stack_temp['Resources'].update(PublicSubnet_RouteTableAssociation)
      stack_temp['Resources'].update(PublicSubnet_NetworkAclAssociation)
      stack_temp['Resources'].update(load_balncer)
      stack_temp['Resources'].update(Auto_Scaling)
      stack_temp['Resources'].update(launch_configuration)

  #uploding template to s3 bucket
  
  obt = s3.Object('inframindsolution','Test.json')
  obt.put(Body = json.dumps(stack_temp))
  objt = json.dumps(stack_temp)
  
  #pushing into stack
  
  try:
    stack = Cloud.create_stack(StackName='Test2',TemplateURL= 'https://s3-us-west-2.amazonaws.com/inframindsolution/Test.json')
  except Exception as e:
    print(e) 
    
    
  print(stack_temp)
  print('success')  
    
  