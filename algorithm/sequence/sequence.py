import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional
import numpy as np
import json


def read_from_json(file_name):
    l = json.load(open(file_name, 'r'))
    return l


def save_to_json(file_name, l):
    json.dump(l, open(file_name, 'w'))


class SeqDataset(Dataset):
    def __init__(self, X, y=None, max_seq_len=100):
        self.X = X
        self.y = y
        self.max_seq_len = max_seq_len

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        seq = self.X[idx]
        if not self.y is None:
            label = self.y[idx]
        input = np.zeros((self.max_seq_len, len(seq[0])))
        length = min(len(seq), self.max_seq_len)
        input[:length] = seq[:length]
        if not self.y is None:
            return {"input": input, "length": length, "label": label}
        else:
            return {"input": input, "length": length}


class Model(torch.nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim=1, num_layers=4):
        super(Model, self).__init__()
        self.num_layers = num_layers
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.batch_size = None
        self.embed = torch.nn.Linear(input_dim, embedding_dim)
        self.rnn = torch.nn.GRU(embedding_dim, hidden_size=hidden_dim, num_layers=num_layers)
        self.out = torch.nn.Linear(hidden_dim, output_dim)

    def init_hidden(self, batch_size):
        self.batch_size = batch_size
        self.hidden = torch.zeros(self.num_layers, batch_size, self.hidden_dim)

    def forward(self, input, seq_len):
        embedding = self.embed(input)
        embedding = torch.nn.utils.rnn.pack_padded_sequence(embedding, seq_len, batch_first=True)
        h, self.hidden = self.rnn(embedding)
        h, _ = torch.nn.utils.rnn.pad_packed_sequence(h, batch_first=True)
        h = h[:, -1]
        out = self.out(h)
        return out


class SequenceClassification():
    def __init__(self, embedding_dim=16, hidden_dim=16):
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.model = None

    def _check_num_category(self, l):
        l = np.array(l).reshape(-1, )
        l = np.unique(l)
        return len(l)

    def fit(self, X, y, max_seq_len=100, batch_size=128, epochs=200, learning_rate=0.01, verbose=False):
        dataset = SeqDataset(X, y, max_seq_len=max_seq_len)
        sample_strategy = torch.utils.data.WeightedRandomSampler([1.0 / len(dataset) for _ in range(len(dataset))],
                                                                 len(dataset), False)
        dataset_loader = DataLoader(dataset, batch_size=batch_size, num_workers=0, sampler=sample_strategy)
        input_dim = len(X[0][0])
        output_dim = self._check_num_category(y)
        self.model = Model(input_dim, self.embedding_dim, self.hidden_dim, output_dim)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.model.train()
        for epoch in range(epochs):
            for i, batch in enumerate(dataset_loader):
                input = batch['input']
                seq_len = batch['length']
                labels = batch['label']
                self.model.zero_grad()
                input = torch.tensor(input).float()
                seq_len = torch.tensor(seq_len)
                labels = torch.LongTensor(labels)
                seq_len, sorted_index = torch.sort(seq_len, 0, descending=True)
                input = torch.index_select(input, 0, sorted_index).float()
                labels = torch.index_select(labels, 0, sorted_index)
                self.model.init_hidden(batch_size)
                out = self.model(input, seq_len)
                loss = torch.nn.functional.cross_entropy(out, labels)
                loss.backward()
                optimizer.step()
            if verbose:
                print(f"{epoch+1}/{epochs} loss {loss:.9f}")

    def predict(self, X, max_seq_len=100, batch_size=128):
        proba = self.predict_porba(X, max_seq_len, batch_size)
        labels = np.argmax(proba, axis=1)
        return labels

    def predict_porba(self, X, max_seq_len=100, batch_size=128):
        dataset = SeqDataset(X, max_seq_len=max_seq_len)
        dataset_loader = DataLoader(dataset, batch_size=batch_size, num_workers=0, shuffle=False, sampler=None)

        self.model.eval()
        proba = None
        for i, batch in enumerate(dataset_loader):
            input = batch['input']
            seq_len = batch['length']
            input = torch.tensor(input).float()
            seq_len = torch.tensor(seq_len)
            seq_len, sorted_index = torch.sort(seq_len, 0, descending=True)
            input = torch.index_select(input, 0, sorted_index).float()
            self.model.init_hidden(batch_size)
            out = self.model(input, seq_len)
            out = torch.nn.functional.softmax(out)
            out = out.detach().numpy()
            if proba is None:
                proba = out
            else:
                proba = np.vstack((proba, out))
        return proba


if __name__ == "__main__":
    # 参数
    batch_size = 3
    epochs = 100
    max_seq_len = 3
    embedding_dim = 8
    hidden_dim = 8
    learning_rate = 0.01

    # 从json读取数据为嵌套列表
    # 样例数据
    # data = [[[[1, 2, 3.0], [1, 1, 5.0]], 0],
    #         [[[1, 2, 3.0], [1, 2, 5.0], [9.0, 7.9, 8]], 1],
    #         [[[1, 3, 2.0]], 0]]
    # save_to_json('seq_data.json', data)
    data = read_from_json('seq_data.json')
    x_train = [x[0] for x in data]
    y_train = [x[1] for x in data]

    # 模型建立
    model = SequenceClassification(embedding_dim=embedding_dim, hidden_dim=hidden_dim)

    # 模型训练
    model.fit(x_train, y_train, max_seq_len=max_seq_len, learning_rate=learning_rate, batch_size=batch_size,
              epochs=epochs, verbose=True)

    # 模型预测（分别预测概率和标签）
    predict = model.predict_porba(x_train)
    print(predict)
    labels = model.predict(x_train)
    print(labels)
    pass
