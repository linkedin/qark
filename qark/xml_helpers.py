from xml.etree import ElementTree

def write_key_value_to_xml(key, value, path):
    """
    Checks if `key` exists in the parsed XML `path`, if it does not it creates a new
    element and appends it to the XML tree and then updates the file.

    :param key:
    :param value:
    :param path: Union[str, pathlib.Path, FileObject]
    :return:
    """
    try:
        xml_to_write = ElementTree.parse(path)
    except IOError:
        log.exception("Strings file for exploit APK does not exist")
        raise SystemExit("Strings file for exploit APK does not exist")

    if not xml_to_write.find(key):
        new_element = ElementTree.SubElement(xml_to_write.getroot(), "string", attrib={"name": key})
        new_element.text = value

        xml_to_write.write(path)


def write_key_value_to_string_array_xml(array_name, value, path):
    """
    Checks if `array_name` is name of a `string-array`, if it does not exist it creates a new
    element and appends it to the XML tree and then updates the file, if it exists it updates the existing element.

    :param array_name:
    :param value:
    :param path: Union[str, pathlib.Path, FileObject]
    """
    try:
        strings_xml = ElementTree.parse(path)
    except IOError:
        log.exception("Extra keys file for exploit APK does not exist")
        raise SystemExit("Extra keys file for exploit APK does not exist")

    # attempt to update the entry if it exists
    for string_array in strings_xml.findall("string-array"):
        if string_array.attrib.get("name") == array_name:
            sub_element_item = ElementTree.SubElement(string_array, "item")
            sub_element_item.text = value

            strings_xml.write(path)
            return

    # write the entry as it does not exist
    new_string_array = ElementTree.SubElement(strings_xml.getroot(), "string-array", attrib={"name": array_name})
    sub_element_item = ElementTree.SubElement(new_string_array, "item")
    sub_element_item.text = value

    strings_xml.write(path)