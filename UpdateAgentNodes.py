from jenkinsapi.jenkins import Jenkins
import xml.etree.ElementTree as ET
import getpass
print ("Please provide the details below:")
# Initialize the Jenkins API object
jenkins_url = input('Enter your controller url: ')
username = input('Enter your UserName: ')
password = getpass.getpass('Enter your Password: ')
ElementToUpdate = input('Enter the Element you want to update: ')
NewValue = input('Enter the new value: ')
jenkins = Jenkins(jenkins_url, username=username, password=password)
# Get the list of all nodes
nodes = jenkins.nodes
# Update the description element of the config.xml file for each node and save the changes
for node_name, node_obj in nodes.items():
    if (node_name != "Built-In Node"):
        # Parse the XML file
        tree = ET.parse(f'/var/lib/jenkins/nodes/{node_name}/config.xml')
        root = tree.getroot()
        element_to_update = root.find(f'.//{ElementToUpdate}')
        element_to_update.text = NewValue
        tree.write (f'/var/lib/jenkins/nodes/{node_name}/config.xml', xml_declaration=True, encoding='UTF-8', method="xml")
        print (f'Node - {node_name} element {ElementToUpdate} is now updated to {NewValue}')
print ('Changes will take effect after either a restart or reload configuration from disk')                                                                                             
