__all__ = [
    'text_substr',
    'text_replace',
    'text_split',
    'text_count',
]

def text_substr(text, **kwargs):
    start = kwargs.pop('start')
    end = kwargs.pop('end')
    try:
        start = int(start)
    except ValueError:
        start = 0
    try:
        end = int(end)
        text = text[start:end]
    except ValueError:
        text = text[start:]
    return text

def text_replace(text, **kwargs):
    src = kwargs.pop('src')
    dest = kwargs.pop('dest')
    count = int(kwargs.pop('count'))
    text = text.replace(src, dest, count)
    return text

def text_split(text, **kwargs):
    pattern = kwargs.pop('pattern')
    count = int(kwargs.pop('count'))
    text = text.split(pattern, count)
    return text

def text_count(text, **kwargs):
    import pandas as pd
    pattern = kwargs.pop('pattern')
    if pattern == '':
        cnt = len(text)
    else:
        cnt = text.count(pattern)
    df = pd.DataFrame([cnt])
    df.columns = ['count']
    return df
