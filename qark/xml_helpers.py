from xml.etree import ElementTree

import logging

log = logging.getLogger(__name__)


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


def write_key_value_to_string_array_xml(array_name, value, path, add_id=True):
    """
    Checks if `array_name` is name of a `string-array`, if it does not exist it creates a new
    element and appends it to the XML tree and then updates the file, if it exists it updates the existing element.

    :param str array_name:
    :param str value:
    :param Union[str, pathlib.Path, FileObject] path:
    :param bool add_id: Whether or not to create an id like `value{id}` where `id` is an int
    """
    try:
        strings_xml = ElementTree.parse(path)
    except IOError:
        log.exception("Extra keys file for exploit APK does not exist")
        raise SystemExit("Extra keys file for exploit APK does not exist")

    if add_id:
        last_id = 0

    # attempt to update the entry if it exists
    for string_array in strings_xml.findall("string-array"):
        if string_array.attrib.get("name") == array_name:
            if add_id:
                for child in string_array.getchildren():
                    last_id = child.text.split(value)[1]
                value = "{value}{id}".format(value=value, id=int(last_id)+1)

            sub_element_item = ElementTree.SubElement(string_array, "item")
            sub_element_item.text = value

            strings_xml.write(path)
            return value

    if add_id:
        value = "{value}{id}".format(value=value, id=last_id+1)

    # write the entry as it does not exist
    new_string_array = ElementTree.SubElement(strings_xml.getroot(), "string-array", attrib={"name": array_name})
    sub_element_item = ElementTree.SubElement(new_string_array, "item")
    sub_element_item.text = value

    strings_xml.write(path)
    return value


def get_manifest_out_of_files(files):
    """
    Parses `files` for a file that ends with `androidmanifest.xml`.
    :param Set[str] files: list of paths to files as absolute paths
    :return: manifest string if in `files`, else None
    """
    for file_name in files:
        if file_name.lower().endswith("androidmanifest.xml"):
            return file_name
    return None
