import os
from xml.etree.ElementTree import parse
import argparse


def write_txt(write_name, data):
    with open(write_name, '+a') as f:
        f.write(data)


def read_xml(class_list, arg_type):
    i = 0
    for root, dirs, filenames in os.walk(xml_dir):
        for filename in filenames:
            xml_path = os.path.join(root, filename)
            tree = parse(xml_path)
            xml_root = tree.getroot()
            im_name = xml_root.find('filename').text
            im_height = xml_root.findtext('./size/height')
            im_width = xml_root.findtext('./size/width')
            im_path = os.path.join(image_dir, im_name)
            obj_list = [str(i), im_path, im_width, im_height]
            for obj in xml_root.findall('object'):
                classname = obj.findtext('./name')
                class_index = str(class_list.index(classname))
                xmin = obj.findtext('./bndbox/xmin')
                ymin = obj.findtext('./bndbox/ymin')
                xmax = obj.findtext('./bndbox/xmax')
                ymax = obj.findtext('./bndbox/ymax')
                obj_list.extend([class_index, xmin, ymin, xmax, ymax])
            obj_list.append('\n')
            dataline = ' '.join(obj_list)
            print(dataline)
            txt = arg_type + '.txt'
            write_txt(txt, dataline)
            i += 1
    write_txt(txt, ' \n')


if __name__ == '__main__':

    arg = argparse.ArgumentParser('更改数据')
    arg.add_argument('--image', '-i', type=str, help='图片文件夹名')
    arg.add_argument('--xml', '-x', type=str, help='xml文件夹名')
    arg.add_argument('--type', '-t', type=str, help='数据类型')
    args = arg.parse_args()

    work_path = os.getcwd()
    image_dir = os.path.join(work_path, args.image)
    xml_dir = os.path.join(work_path, args.xml)
    classname_path = os.path.join(work_path, 'data.names')
    with open(classname_path, 'r') as r:
        class_list = [cl_name.strip() for cl_name in r.readlines()]
    read_xml(class_list, args.type)
