__all__ = [
    'text_lda',
]

def text_lda(seq, **kwargs):
    from .lda import Lda
    import pandas as pd
    topic = int(kwargs.pop('topic'))
    model = Lda()
    model.train(seq, topic)
    ret = model.get_topics()
    ret = pd.DataFrame(ret)
    return ret
