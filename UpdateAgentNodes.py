from jenkinsapi.jenkins import Jenkins
import xml.etree.ElementTree as ET
import getpass
print ("Please provide the details below:")
jenkins_url = input('Enter your controller url: ')
username = input('Enter your UserName: ')
password = getpass.getpass('Enter your Password: ')
jenkinsHome = input('Abosulte path for your jenkins home (example - /var/lib/jenkins/): ')
elementToUpdate = input('Enter the Element you want to update: ')
newValue = input('Enter the new value: ')
jenkins = Jenkins(jenkins_url, username=username, password=password)
# Get the list of all nodes
nodes = jenkins.nodes
# Update the element of the config.xml file for each node and save the changes
for node_name, node_obj in nodes.items():
    if (node_name != "Built-In Node"):
        # Parse the XML file
        tree = ET.parse(f'{jenkinsHome}nodes/{node_name}/config.xml')
        root = tree.getroot()
        element_to_update = root.find(f'.//{elementToUpdate}')
        element_to_update.text = newValue
        tree.write (f'{jenkinsHome}nodes/{node_name}/config.xml', xml_declaration=True, encoding='UTF-8', method="xml")
        print (f'Node - {node_name} element {elementToUpdate} is now updated to {newValue}')
print ('Changes will take effect after either a restart or reload configuration from disk')
