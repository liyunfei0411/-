# import os
# import io

# import Pil.Image
import tensorflow as tf
from object_detection.utils import dataset_util

flags = tf.app.flags
flags.DEFINE_string('class_name', '', 'Path to the txt class_name')
flags.DEFINE_string('input', '', 'Path to the txt input')
flags.DEFINE_string('output', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


def create_tf_exmaple(data_dict):
    full_path = data_dict['file_path']
    with tf.gfile.GFile(full_path, 'rb') as fid:
        encoded_jpg = fid.read()
    # encoded_jpg_io = io.BytesIO(encoded_jpg)
    # image = Pil.Image.open(encoded_jpg_io)
    width, height = (int(data_dict['width']), int(data_dict['height']))
    filename = full_path.split('/')[-1].encode('utf8')
    image_format = b'jpg'
    xmins = [float(data_dict['xmin']) / width]
    xmaxs = [float(data_dict['xmax']) / width]
    ymins = [float(data_dict['ymin']) / height]
    ymaxs = [float(data_dict['ymax']) / height]
    classes_text = [data_dict['class_name'].encode('utf8')]
    classes = [int(data_dict['class_num'])]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def get_name(num):
    name_path = FLAGS.class_name
    with open(name_path, 'r') as f:
        name_list = f.readlines()
    name = name_list[int(num)].strip()
    return name


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output)
    data_path = FLAGS.input
    # data_path = 'train.txt'
    with open(data_path, 'r') as r:
        while True:
            content = r.readline().strip()
            data_list = content.split(' ')
            total = int((len(data_list)-4) / 5)
            for i in range(total):
                class_num = data_list[i*5+4]
                xmin = data_list[i*5+5]
                ymin = data_list[i*5+6]
                xmax = data_list[i*5+7]
                ymax = data_list[i*5+8]
                class_name = get_name(class_num)
                w_dict = {'file_path': data_list[1],
                          'width': data_list[2],
                          'height': data_list[3],
                          'class_name': class_name,
                          'class_num': class_num,
                          'xmin': xmin,
                          'xmax': xmax,
                          'ymin': ymin,
                          'ymax': ymax
                          }
                # print(w_dict)
                tf_exmaple = create_tf_exmaple(w_dict)
                writer.write(tf_exmaple.SerializeToString())
    writer.close()


if __name__ == '__main__':
    tf.app.run()
    # main()



