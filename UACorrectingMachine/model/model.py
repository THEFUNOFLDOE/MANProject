import difflib as dl
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from functools import partial
from torch import device, cuda
from MANProject.settings import BASE_DIR


model_name = "schhwmn/mbart-large-50-finetuned-ukr-gec"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=BASE_DIR)
device = device("cuda" if cuda.is_available() else "cpu")


def highlight_text(text, color='yellow', padding='0.45em', margin='0.1em'):
    """Add html markup & css style before and after text"""

    string = f'''<mark style="background: {color};
                  padding: {padding};
                  line-height: 2.5;
                  text_align: center;
                  border-radius: 0.35em;
                  margin: {margin};">{text}</mark>'''

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
    
    # === HTML-markup ===
    
    # Add html-headers
    s1_header = 'Джерело'
    s2_header = 'Виправлено'
    
    # Div container for two rows
    html = '''
    <div style="display:flex; 
    flex-direction: row; 
    text-align: justify;
    border-radius: 7px;
    border: 2px dashed #8e9aaf;
    padding: 28px;">
    '''
    
    # Contents of the first, second columns respectively
    col1_html = f'''<div style="margin: 0 1em; width: 50%;"><h3>{s1_header}</h3>'''
    col2_html = f'''<div style="margin: 0 1em; width: 50%;"><h3>{s2_header}</h3>'''
    
    for output_str in output_strings:
        markup_s1, markup_s2 = '', ''
        
        # Use difflib module to find differences in two strings
        seq_matcher = dl.SequenceMatcher(None, text, output_str)
    
        # Iterate through indexes of equal / changed chunks of text
        for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
            # Add equal elements without change
            if tag == 'equal':
              markup_s1 += text[i1:i2]
              markup_s2 += output_str[j1:j2]
            # Add changed chunks with html-markup
            else:
              markup_s1 += highlight_text(text[i1:i2], '#ffa8B6', padding='0.2em', margin='0')
              markup_s2 += highlight_text(output_str[j1:j2], '#9df9ef', padding='0.2em', margin='0')
                
        col1_html += f'''<p>{markup_s1}</p>'''
        col2_html += f'''<p>{markup_s2}</p>'''
        
    col1_html += '</div>'
    col2_html += '</div>'
    
    html += col1_html + col2_html + '</div>'
            
    return html


predict_correction = partial(predict_sequences,
                             model=model,
                             tokenizer=tokenizer,
                             tokenizer_kwargs_dict=tokenizer_dict
                             )
