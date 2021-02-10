import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from cogs.chatbot.utils import load_data, load_tokenizers
from cogs.chatbot.layers import CustomSchedule, Transformer, create_masks
import os
import time
import random

class Chatbot(object):

  def __init__(self):

    self.num_layers = 4
    self.d_model = 128
    self.dff = 512
    self.num_heads = 8
    self.dropout_rate = 0.1
    self.max_length = 40
    self.batch_size = 64
    self.target_vocab_size = 16000
    self.max_checkpoint = 10

    self.data_path = "./cogs/chatbot/data"
    self.checkpoint_path = "./cogs/chatbot/checkpoints/train"
    self.tokenizer_path = "./cogs/chatbot/tokenizers"
    self.inputs_savepath = f"{self.tokenizer_path}/inputs_token"
    self.outputs_savepath = f"{self.tokenizer_path}/outputs_token"

    self.inputs, self.outputs = load_data(f"{self.data_path}/training_data.txt")
    self.inputs_tokenizer, self.outputs_tokenizer = load_tokenizers(inputs_outputs_savepaths=[self.inputs_savepath, self.outputs_savepath])

    self.input_vocab_size = self.inputs_tokenizer.vocab_size + 2
    self.target_vocab_size = self.outputs_tokenizer.vocab_size + 2

    self.learning_rate = CustomSchedule(self.d_model)
    self.optimizer = tf.keras.optimizers.Adam(self.learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)
    self.transformer = Transformer(
      self.num_layers, self.d_model,
      self.num_heads, self.dff,
      self.input_vocab_size,
      self.target_vocab_size,
      pe_input=self.input_vocab_size,
      pe_target=self.target_vocab_size,
      rate=self.dropout_rate)

    self.ckpt = tf.train.Checkpoint(transformer=self.transformer,
                               optimizer=self.optimizer)
    self.ckpt_manager = tf.train.CheckpointManager(self.ckpt, self.checkpoint_path, max_to_keep=self.max_checkpoint)

    self.ckpt.restore(self.ckpt_manager.latest_checkpoint)
    print (f"Latest checkpoint restored: {self.ckpt_manager.latest_checkpoint}")
      
  def evaluate(self, inp_sentence):
    start_token = [self.inputs_tokenizer.vocab_size]
    end_token = [self.inputs_tokenizer.vocab_size + 1]
    
    inp_sentence = start_token + self.inputs_tokenizer.encode(inp_sentence) + end_token
    encoder_input = tf.expand_dims(inp_sentence, 0)
    
    decoder_input = [self.outputs_tokenizer.vocab_size]
    output = tf.expand_dims(decoder_input, 0)
      
    for i in range(self.max_length):
      enc_padding_mask, combined_mask, dec_padding_mask = create_masks(
          encoder_input, output)
    
      predictions, attention_weights = self.transformer(encoder_input, 
                                                        output,
                                                        False,
                                                        enc_padding_mask,
                                                        combined_mask,
                                                        dec_padding_mask)
      
      predictions = predictions[: ,-1:, :]

      predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
      
      if predicted_id == self.outputs_tokenizer.vocab_size+1:
        return tf.squeeze(output, axis=0), attention_weights
      
      output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0), attention_weights

  def reply(self, sentence):
    result, attention_weights = self.evaluate(sentence)
    
    predicted_sentence = self.outputs_tokenizer.decode([i for i in result 
                                              if i < self.outputs_tokenizer.vocab_size])

    return predicted_sentence, attention_weights, sentence, result