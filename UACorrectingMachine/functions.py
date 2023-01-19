import re
from ua_gec import Corpus


CORPUS = Corpus(partition="test")


def highlight_text(text, color='yellow', padding='0.45em', margin='0.1em'):
    string = f'''<mark 
                    style="background: {color};
                    padding: {padding};
                    line-height: 2.5;
                    text_align: center;
                    border-radius: 0.35em;
                    margin: {margin};">{text}
                  </mark>'''

    return string


def show_corrections(text):
    error_pattern = r'\{(([^\{]*\(*\)*)=>([^\{]*\(*\)*):::error_type=([^\{]*))\}'
    markup_mistake, markup_correction = '', ''
    offset = 0

    matches = re.finditer(error_pattern, text)

    for match in matches:
        start, end = match.span(0)

        start_mistake, end_mistake = match.span(2)
        start_correction, end_correction = match.span(3)
        start_error_type, end_error_type = match.span(4)

        highlight_correction = text[start_correction:end_correction]
        highlighted_correction = highlight_text(highlight_correction, '#9df9ef')

        highlight_mistake = text[start_mistake:end_mistake]
        highlighted_mistake = highlight_text(highlight_mistake, '#ffa8B6')

        highlight_error_type = text[start_error_type:end_error_type]
        highlighted_error_type = highlight_text(highlight_error_type, '#feca74')

        fragment = text[offset:start]

        markup_correction += f"{fragment}{highlighted_correction}{highlighted_error_type}"
        markup_mistake += f"{fragment} {highlighted_mistake}"

        offset = end

    markup_correction += text[offset:]
    markup_mistake += text[offset:]

    html = f'''
          <div style="display:flex; flex-direction: row; text-align: justify;">
            <div style="margin: 0 1em;"><h3>Джерело</h3><p>{markup_mistake}</p></div>
            <div style="margin: 0 1em;"><h3>Виправлено</h3><p>{markup_correction}</p></div>
          </div>
          '''
    return html
