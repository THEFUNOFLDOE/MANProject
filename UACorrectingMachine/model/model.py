import difflib as dl
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from functools import partial
from torch import device, cuda
from django.conf import settings
import os


model_name = "schhwmn/mbart-large-50-finetuned-ukr-gec"
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=os.path.join(settings.BASE_DIR, ".cache"))
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=os.path.join(settings.BASE_DIR, ".cache"))
device = device("cuda" if cuda.is_available() else "cpu")


def highlight_text(text, class_type):
    """Add html markup & css style before and after text"""

    string = f'''<mark class="{class_type}">{text}</mark>'''

    return string


# Tokenizer parameters
max_token_length = 50
tokenizer_dict = dict(return_tensors = 'pt',
                      padding = 'max_length',
                      truncation = True,
                      max_length = max_token_length)


def predict_sequences(text, num_return_sequences, model, tokenizer, tokenizer_kwargs_dict):
    
    # Tokenize input text
    inputs = tokenizer(text, **tokenizer_kwargs_dict)
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    
    # Generate model's prediction
    output_ids = model.generate(input_ids=input_ids, 
                                num_beams=10, 
                                num_return_sequences=num_return_sequences,
                                attention_mask=attention_mask
                               )
    
    # Decode model's output 
    output_strings = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    
    markup_errors = []
    markup_checks = []
    
    for output_str in output_strings:
        markup_error, markup_check = '', ''
        
        # Use difflib module to find differences in two strings
        seq_matcher = dl.SequenceMatcher(None, text, output_str)
    
        # Iterate through indexes of equal / changed chunks of text
        for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
            # Add equal elements without change
            if tag == 'equal':
              markup_error += text[i1:i2]
              markup_check += output_str[j1:j2]
            # Add changed chunks with html-markup
            else:
              markup_error += highlight_text(text[i1:i2], "errorSign")
              markup_check += highlight_text(output_str[j1:j2], "checkedSign")
        
        markup_errors.append(markup_error)
        markup_checks.append(markup_check)
        
            
    return (markup_errors, markup_checks)


predict_correction = partial(predict_sequences,
                             model=model,
                             tokenizer=tokenizer,
                             tokenizer_kwargs_dict=tokenizer_dict
                             )
