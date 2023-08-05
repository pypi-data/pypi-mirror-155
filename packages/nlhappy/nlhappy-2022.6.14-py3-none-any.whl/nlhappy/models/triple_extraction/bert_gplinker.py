import pytorch_lightning as pl
from transformers import BertModel, BertTokenizer
from ...layers import EfficientGlobalPointer
from ...layers.loss import MultiLabelCategoricalCrossEntropy, SparseMultiLabelCrossEntropy
from ...metrics.triple import TripleF1
import torch
from torch import Tensor
from typing import List, Set
from ...utils.data import Triple
from ...utils.preprocessing import fine_grade_tokenize
import os





class BertGPLinker(pl.LightningModule):
    """基于globalpointer的关系抽取模型
    参考:
    - https://kexue.fm/archives/8888
    - https://github.com/bojone/bert4keras/blob/master/examples/task_relation_extraction_gplinker.py
    """
    def __init__(
        self,
        hidden_size: int,
        lr: float,
        dropout: float,
        weight_decay: float,
        threshold: float,
        **data_params
    ):
        super(BertGPLinker, self).__init__()
        self.save_hyperparameters()
        
        self.tokenizer = self._init_tokenizer()
        
        self.bert = BertModel(data_params['bert_config'])
        self.dropout = torch.nn.Dropout(dropout)
        
        # span 分类器 
        # self.span_classifier = EfficientGlobalPointer(self.bert.config.hidden_size, hidden_size, len(data_params['s_label2id'])) 
        # 主语 宾语分类器
        self.so_classifier = EfficientGlobalPointer(self.bert.config.hidden_size, hidden_size, 2)
        # 主语 宾语 头对齐
        self.head_classifier = EfficientGlobalPointer(self.bert.config.hidden_size, hidden_size, len(data_params['p_label2id']), RoPE=False, tril_mask=False)
        # 主语 宾语 尾对齐
        self.tail_classifier = EfficientGlobalPointer(self.bert.config.hidden_size, hidden_size, len(data_params['p_label2id']), RoPE=False, tril_mask=False)

        # self.span_criterion = MultiLabelCategoricalCrossEntropy()
        self.so_criterion = MultiLabelCategoricalCrossEntropy()
        self.head_criterion = MultiLabelCategoricalCrossEntropy()
        self.tail_criterion = MultiLabelCategoricalCrossEntropy()

        self.train_metric = TripleF1()
        self.val_metric = TripleF1()
        self.test_metric = TripleF1()

    

    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        hidden_state = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask).last_hidden_state
        hidden_state = self.dropout(hidden_state)
        so_logits = self.so_classifier(hidden_state, mask=attention_mask)
        head_logits = self.head_classifier(hidden_state, mask=attention_mask)
        tail_logits = self.tail_classifier(hidden_state, mask=attention_mask)
        return so_logits, head_logits, tail_logits


    def shared_step(self, batch):
        #inputs为bert常规输入, span_ids: [batch_size, 2, seq_len, seq_len],
        #head_ids: [batch_size, len(label2id), seq_len, seq_len], tail_ids: [batch_size, len(label2id), seq_len, seq_len]
        input_ids, token_type_ids, attention_mask = batch['input_ids'], batch['token_type_ids'], batch['attention_mask']
        so_ture, head_true, tail_true = batch['so_ids'],  batch['head_ids'], batch['tail_ids']
        so_logits, head_logits, tail_logits = self(input_ids, token_type_ids, attention_mask)


        so_logits_ = so_logits.reshape(so_logits.shape[0] * so_logits.shape[1], -1)
        so_true_ = so_ture.reshape(so_ture.shape[0] * so_ture.shape[1], -1)
        so_loss = self.so_criterion(so_logits_, so_true_)
        
        head_logits_ = head_logits.reshape(head_logits.shape[0] * head_logits.shape[1], -1)
        head_true_ = head_true.reshape(head_true.shape[0] * head_true.shape[1], -1)
        head_loss = self.head_criterion(head_logits_, head_true_)
        
        tail_logits_ = tail_logits.reshape(tail_logits.shape[0] * tail_logits.shape[1], -1)
        tail_true_ = tail_true.reshape(tail_true.shape[0] * tail_true.shape[1], -1)
        tail_loss = self.tail_criterion(tail_logits_, tail_true_)
        
        loss = so_loss + head_loss + tail_loss
        return loss, so_logits, head_logits, tail_logits

    def on_train_start(self) -> None:
        state_dict = torch.load(self.hparams.pretrained_dir + self.hparams.plm + '/pytorch_model.bin')
        self.bert.load_state_dict(state_dict)

        
    def training_step(self, batch, batch_idx) -> dict:
        # 训练阶段不进行解码, 会比较慢
        loss, so_logits, head_logits, tail_logits = self.shared_step(batch)
        return {'loss': loss}


    def validation_step(self, batch, batch_idx) -> dict:
        so_true, head_true, tail_true = batch['so_ids'], batch['head_ids'], batch['tail_ids']
        loss, so_logits, head_logits, tail_logits = self.shared_step(batch)
        batch_triples = self.extract_triple(so_logits, head_logits, tail_logits, threshold=self.hparams.threshold)
        batch_true_triples = self.extract_triple(so_true, head_true, tail_true, threshold=self.hparams.threshold)
        self.val_metric(batch_triples, batch_true_triples)
        self.log('val/f1', self.val_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'val_loss': loss}


    def test_step(self, batch, batch_idx) -> dict:
        so_true, head_true, tail_true = batch['so_ids'], batch['head_ids'], batch['tail_ids']
        loss, so_logits, head_logits, tail_logits = self.shared_step(batch)
        batch_triples = self.extract_triple(so_logits, head_logits, tail_logits, threshold=self.hparams.threshold)
        batch_true_triples = self.extract_triple(so_true, head_true, tail_true, threshold=self.hparams.threshold)
        self.test_metric(batch_triples, batch_true_triples)
        self.log('test/f1', self.test_metric, on_step=False, on_epoch=True, prog_bar=True)
        return {'test_loss': loss}


    def configure_optimizers(self)  :
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        grouped_parameters = [
            {'params': [p for n, p in self.bert.named_parameters() if not any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.bert.named_parameters() if any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr, 'weight_decay': 0.0},
            {'params': [p for n, p in self.so_classifier.named_parameters() if not any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.so_classifier.named_parameters() if any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': 0.0},
            {'params': [p for n, p in self.head_classifier.named_parameters() if not any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.head_classifier.named_parameters() if any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': 0.0},
            {'params': [p for n, p in self.tail_classifier.named_parameters() if not any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': self.hparams.weight_decay},
            {'params': [p for n, p in self.tail_classifier.named_parameters() if any(nd in n for nd in no_decay)],
            'lr': self.hparams.lr* 10, 'weight_decay': 0.0}
        ]
        self.optimizer = torch.optim.AdamW(grouped_parameters)
        self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lambda epoch: 1.0 / (epoch + 1.0))
        return [self.optimizer], [self.scheduler]


    def extract_triple(
        self, 
        so_logits: Tensor,
        head_logits: Tensor, 
        tail_logtis: Tensor, 
        threshold: float
        ) -> List[Set[Triple]]:
        """
        将三个globalpointer预测的结果进行合并，得到三元组的预测结果
        参数:
        - so_logits: [batch_size, 2, seq_len, seq_len]
        - head_logits: [batch_size, predicate_type, seq_len, seq_len]
        - tail_logtis: [batch_size, predicate_type, seq_len, seq_len]
        返回:
        - batch_size大小的列表，每个元素是一个集合，集合中的元素是三元组
        """

        so_logits = so_logits.chunk(so_logits.shape[0])
        head_logits = head_logits.chunk(head_logits.shape[0])
        tail_logtis = tail_logtis.chunk(tail_logtis.shape[0])
        assert len(head_logits) == len(tail_logtis) == len(so_logits)
        batch_triples = []
        for i in range(len(so_logits)):
            subjects, objects = set(), set()
            for l, h, t in zip(*torch.where(so_logits[i].squeeze(0) > threshold)):
                if  l == 0:
                    subjects.add((h, t))
                else:
                    objects.add((h, t))
            
            triples = set()
            for sh, st in subjects:
                for oh, ot in objects:
                    p1s = torch.where(head_logits[i].squeeze(0)[:, sh, oh] > threshold)[0].tolist()
                    p2s = torch.where(tail_logtis[i].squeeze(0)[:, st, ot] > threshold)[0].tolist()
                    ps = set(p1s) & set(p2s)
                    if len(ps) > 0:
                        for p in ps:
                            triples.add(Triple(triple=(sh.item(), st.item(), self.hparams['p_id2label'][p], oh.item(), ot.item())))
            batch_triples.append(triples)
        return batch_triples

    
    def _init_tokenizer(self):
        with open('./vocab.txt', 'w') as f:
            for k in self.hparams.token2id.keys():
                f.writelines(k + '\n')
        self.hparams.bert_config.to_json_file('./config.json')
        tokenizer = BertTokenizer.from_pretrained('./')
        os.remove('./vocab.txt')
        os.remove('./config.json')
        return tokenizer


    def predict(self, text: str, device:str, threshold = None) -> Set[Triple]:
        """模型预测
        参数:
        - text: 要预测的单条文本
        - device: 设备
        - threshold: 三元组抽取阈值, 如果为None, 则为模型训练时的阈值
        返回
        - 预测的三元组
        """
        tokens = fine_grade_tokenize(text, self.tokenizer)
        inputs = self.tokenizer.encode_plus(
            tokens,
            add_special_tokens=True,
            max_length=self.hparams.max_length,
            truncation=True,
            return_tensors='pt'
        )
        inputs.to(torch.device(device))
        so_logits, head_logits, tail_logits = self(**inputs)
        if threshold == None:
            batch_triples = self.extract_triple(so_logits, head_logits, tail_logits, threshold=self.hparams.threshold)
        else:
            batch_triples = self.extract_triple(so_logits, head_logits, tail_logits, threshold=threshold)
        return [(triple[0]-1, triple[1], triple[2], triple[3]-1, triple[4])  for triple in batch_triples[0]]


        


    


        

    


