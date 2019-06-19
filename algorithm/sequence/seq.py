__all__ = [
    'seq_sequence',
]

def seq_sequence(seq1, seq2, **kwargs):
    from .sequence import SequenceClassification
    embedding_dim = int(kwargs.pop('embedding_dim'))
    hidden_dim = int(kwargs.pop('hidden_dim'))
    learning_rate = float(kwargs.pop('learning_rate'))
    max_seq_len = int(kwargs.pop('max_seq_len'))
    batch_size = int(kwargs.pop('batch_size'))
    epochs = int(kwargs.pop('epochs'))

    model = SequenceClassification(embedding_dim=embedding_dim, hidden_dim=hidden_dim)
    model.fit(seq1, seq2, max_seq_len=max_seq_len, learning_rate=learning_rate, batch_size=batch_size,
              epochs=epochs, verbose=True)
    # TODO
    pass

def seq_predict(seq_model, seq, **kwargs):
    import pandas as pd
    type_ = kwargs.pop('type_')
    predict_label = kwargs.pop('predict_label')
    if type_ == 'proba':
        predict = model.predict_proba(seq)
    else:
        predict = model.predict(seq)
    df = pd.DataFrame(predict)
    df.columns = [predict_label]
    return df

