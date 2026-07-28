


import tensorflow as tf
import tensorflow.lite as lite


#-> lite.TFLiteConverter.from_keras_model_file
#-> lite.TFLiteConverter.from_saved_model()
#-> lite.TFLiteConverter.from_frozen_graph()
#-> lite.TFLiteConverter.from_session()

class TFLite:
    """
    INFO:
    ----------------------------------------------------------
    input:
    ----------------------------------------------------------
    ouput:
    
    """
    def __init__(self):
        self.tfmodel = ''
        self.output_data = 0
    def __help__():
    	pass
    def __version__():
    	pass        
    def Convert(self, model_dir, saveFile):
        #from tensorflow.contrib import lite

        # signature_keys , tags
        self.converter = lite.TFLiteConverter.from_saved_model(model_dir)
        self.tfmodel = self.converter.convert()
        open (saveFile , "wb") .write(self.tfmodel)
        print("model save in {}".format(self.tfmodel))
        
    def Evalute_size_model(self, tfmodel):
        # Show model size in KBs.
        float_model_size = len(tfmodel) / 1024 * 0.001
        print('Float model size = %dMBs.' % float_model_size)
        
    def Optimize(saveFile):
        # Re-convert the model to TF Lite using quantization.
        self.converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_quantized_model = converter.convert()

        # Show model size in KBs. 
        quantized_model_size = (len(tflite_quantized_model) / 1024) * 0.001
        print('Quantized model size = %dKBs,' % quantized_model_size)
        print('which is about %d%% of the float model size.'\
              % (quantized_model_size * 100 / float_model_size))
              
        open (saveFile , "wb") .write(tflite_quantized_model)
        
    def Load_Decoder(tflite_model, image):
        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path = tflite_model)
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Test model on random input data.
        input_shape = input_details[0]['shape']
        #input_data = np.array(image, dtype=np.float32) #np.uint32
        interpreter.set_tensor(input_details[0]['index'], [image])

        interpreter.invoke()

  
        self.output_data = interpreter.get_tensor(output_details[0]['index'])
    
    def Load_Encoder():
        pass
    # Convert the model
    # 'from_concrete_function' takes in a list of concrete functions, however.
    # currently only supports converting one fucntion at a time. Converting multiple
    # functions is under development.
    def Directly_model_to_tflite( model, 
                                 name_file, 
                                 froms =("from_frozen_graph","keras_model_file", "keras_model_file", "saved_model", "session", "fucntion")):
        if froms == "from_frozen_graph":
            convert = tf.lite.TFLiteConverter.from_frozen_graph(model)
        if froms == "keras_model_file":
            convert = tf.lite.TFLiteConverter.from_keras_model_file(model)
        if froms == "saved_model":
            convert = tf.lite.TFLiteConverter.from_saved_model(model)
        if froms == "session":
            convert = tf.lite.TFLiteConverter.from_session(model)
        if froms == "fucntion":
            # It just works in TF2.x .
            converter = tf.lite.TFLiteConverter.from_concrete_functions([model])
        
            tflite_model = converter.convert()
            open(name_file + ".tflite", "wb").write(tflite_model)
            print("Model is save in {}".format(name_file))  