# A python script that writes a example json to a xml-file and saves it to a file
import xml.etree.ElementTree as ET

json_data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

root = ET.Element("root")
for key, value in json_data.items():
    ET.SubElement(root, key).text = str(value)

tree = ET.ElementTree(root)
tree.write("test.xml")
