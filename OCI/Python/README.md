# Introduction
This README file serves as a guide for users and contributors of the project. It contains information on how to run, install, and contribute to the project.

# Project Description
The project consists of a Python script named main.py that creates Virtual Cloud Network (VCN) Infrastructure in Oracle Cloud Infrastructure (OCI). The script uses the OCI Python SDK to interact with OCI services and mimics the VCN Wizard in the OCI web console to create a complete VCN infrastructure with an Internet Gateway, Route Table, Security List, and Subnet. The script can be executed from the command line and accepts command-line arguments such as VCN name, CIDR block, and region.

# Installation
To install the project, please follow these steps:

- Clone the repository using the command git clone https://github.com/<username>/<repository>.git
- Install the OCI Python SDK using the command pip install oci
- Set up your OCI credentials. Refer to the OCI SDK documentation for more information.
- Open the main.py file and modify the compartment_id variable to match your desired compartment ID.
- Run the script using the command python main.py --vcn-name <vcn_name> --cidr-block <cidr_block> --region <region>, where <vcn_name> is the desired name of the VCN, <cidr_block> is the CIDR block for the VCN, and <region> is the desired region (optional).


# Resources in an OCI VCN

In an OCI Virtual Cloud Network (VCN), there are several resources that can be created. Here's a brief definition of each resource:

1. **VCN (Virtual Cloud Network)**: The VCN is the foundation of your network infrastructure in OCI. It is a logically isolated virtual network that you own and configure. It allows you to launch compute instances, connect to other Oracle Cloud Infrastructure services, and control traffic flow.

2. **Subnet**: A subnet is a subdivision of a VCN. It is a range of IP addresses in your VCN that you can use to deploy your resources. You can create public subnets, private subnets, or both. You can associate security lists and route tables to subnets to control traffic flow.

3. **Internet Gateway**: An Internet Gateway is a virtual router that provides a path for traffic between your VCN and the internet. You can use an Internet Gateway to connect to the internet, launch public-facing instances in your public subnets, and allow inbound traffic.

4. **NAT Gateway**: A NAT (Network Address Translation) Gateway is a virtual device that enables instances in your private subnet to initiate outbound internet connections while preventing inbound connections from the internet. You can use a NAT Gateway to allow instances in your private subnet to access the internet without exposing them to the public.

5. **Route Table**: A route table is a set of rules, called routes, that determine where network traffic is directed. Each subnet in your VCN must be associated with a route table. You can configure different routes to control traffic flow between subnets in your VCN or to the internet.

6. **Security List**: A security list acts as a virtual firewall for your instances. It is a set of ingress and egress rules that control traffic to and from your instances. Each subnet in your VCN must be associated with a security list.

7. **DHCP Options**: DHCP (Dynamic Host Configuration Protocol) options specify the settings that are provided to instances when they boot up. You can configure DHCP options to assign custom DNS servers, domain names, and search domains to instances in your VCN.

These are the main resources that you can create and configure within a VCN in OCI. Depending on your use case, you may need to create additional resources such as Load Balancers, VPN Connections, or FastConnect Circuits.



# Contribution
- Contributions are welcome! To contribute to the project, please follow these steps:

- Fork the repository
- Create a new branch with a descriptive name (git checkout -b my_new_feature)
- Make your changes and commit them (git commit -am 'Add new feature')
- Push your changes to your fork (git push origin my_new_feature)
- Create a pull request
- Please make sure to write clear commit messages and follow the code style of the project.

