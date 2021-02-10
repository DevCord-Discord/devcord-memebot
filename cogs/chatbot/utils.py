import os
import numpy as np
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import html
import tensorflow as tf

def load_data(filepath, shuffle=True):
  with open(filepath, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

  inputs, outputs = list(), list()
  for i, l in enumerate(lines):
    if i % 2 == 0:
      inputs.append(str.encode(html.unescape(l).lower(), "utf-8"))
    else:
      outputs.append(str.encode(html.unescape(l).lower(), "utf-8"))

  popped = 0
  for i, (ins, outs) in enumerate(zip(inputs, outputs)):
    if not ins or not outs:
      inputs.pop(i)
      outputs.pop(i)
      popped += 1

  print(f"Pairs popped: {popped}")
  if shuffle:
    print("\nShuffling...")
    inputs, outputs = shuffle_inputs_outputs(inputs, outputs)

  return inputs, outputs

def shuffle_inputs_outputs(inputs, outputs):
  inputs_outputs = list(zip(inputs, outputs))
  random.shuffle(inputs_outputs)
  inputs, outputs = zip(*inputs_outputs)
  return inputs, outputs

def load_tokenizers(inputs_outputs_savepaths):
  print("Loading tokenizers...")
  inputs_savepath, outputs_savepath = inputs_outputs_savepaths
  inputs_tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(inputs_savepath)
  outputs_tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(outputs_savepath)

  return inputs_tokenizer, outputs_tokenizer

def encode(inputs_outputs, inputs_outputs_tokenizer):
  inputs, outputs = inputs_outputs
  inputs_tokenizer, outputs_tokenizer = inputs_outputs_tokenizer

  inputs = [inputs_tokenizer.vocab_size] + inputs_tokenizer.encode(
      inputs) + [inputs_tokenizer.vocab_size+1]

  outputs = [outputs_tokenizer.vocab_size] + outputs_tokenizer.encode(
      outputs) + [outputs_tokenizer.vocab_size+1]
  
  return inputs, outputs

def tf_encode(inputs_outputs, inputs_outputs_tokenizer):
  result_in, result_out = tf.py_function(encode, [inputs_outputs, inputs_outputs_tokenizer], [tf.int64, tf.int64])
  result_in.set_shape([None])
  result_out.set_shape([None])

  return result_in, result_out

