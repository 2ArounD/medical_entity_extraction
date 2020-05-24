import os
import tensorflow as tf
import pdb

# def test_on_image(sess, mc, model):
#     imdb = kitti('val', './data/KITTI', mc)
#     images, scales = imdb.read_image_batch(shuffle=False)
#     det_boxes, det_probs, det_class = sess.run(
#           [model.det_boxes, model.det_probs, model.det_class],
#           feed_dict={model.image_input:images})
#     return det_boxes


weights_path = '/home/arnoud/Documents/Sollicitaties/Ciphix/case/medical_entity_extraction/out/2around-projects-meder-11-output/model.ckpt-198'
export_dir = os.path.join('/home/arnoud/Documents/Sollicitaties/Ciphix/case/medical_entity_extraction/data/SavedModels')
print(export_dir)


graph = tf.Graph()
with tf.compat.v1.Session(graph=graph, config=tf.ConfigProto(allow_soft_placement=True)) as sess:
    mc = kitti_squeezeDetPlus_config()
    mc.IS_TRAINING = False
    mc.BATCH_SIZE = 1
    mc.PRETRAINED_MODEL_PATH = weights_path
    model = SqueezeDetPlusBNEval(mc)

    uninitialized_vars = []
    for var in tf.all_variables():
        try:
            sess.run(var)
        except tf.errors.FailedPreconditionError:
            uninitialized_vars.append(var)

    init_new_vars_op = tf.initialize_variables(uninitialized_vars)
    sess.run(init_new_vars_op)

    # print(test_on_image(sess, mc, model))
    # pdb.set_trace()

    # saver = tf.train.Saver(model.model_params)

    # input_tensor = graph.get_tensor_by_name('image_input:0')
    # output_tensor_bbox = graph.get_tensor_by_name('bbox/trimming/bbox:0')
    # output_tensor_class = graph.get_tensor_by_name('probability/class_idx:0')
    # output_tensor_conf = graph.get_tensor_by_name('probability/score:0')

    # pdb.set_trace()

    # converter = tflite.TFLiteConverter.from_session(sess, input_tensor,
    #                                                 [output_tensor_bbox,
    #                                                  output_tensor_conf])

    # pdb.set_trace()

    input_tensor_info = tf.saved_model.build_tensor_info(graph.get_tensor_by_name('image_input:0'))
    output_tensor_bbox_info = tf.saved_model.build_tensor_info(graph.get_tensor_by_name('bbox/trimming/bbox:0'))
    output_tensor_class_info = tf.saved_model.build_tensor_info(graph.get_tensor_by_name('probability/class_idx:0'))
    output_tensor_conf_info = tf.saved_model.build_tensor_info(graph.get_tensor_by_name('probability/score:0'))

    prediction_signature = tf.saved_model.signature_def_utils.build_signature_def(
                            inputs={'image': input_tensor_info},
                            outputs={'bbox': output_tensor_bbox_info,
                                     'class': output_tensor_class_info,
                                     'conf': output_tensor_conf_info},
                            method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME)

    # Export checkpoint to SavedModel
    builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
    builder.add_meta_graph_and_variables(sess,
                                         [tf.saved_model.tag_constants.SERVING],
                                         signature_def_map={
                                         'predict_images': prediction_signature},
                                         clear_devices=True,
                                         strip_default_attrs=True)
    builder.save()
    builder.save(as_text=True)
