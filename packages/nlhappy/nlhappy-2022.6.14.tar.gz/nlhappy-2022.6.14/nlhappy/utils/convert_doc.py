from spacy.tokens import Doc
from datasets import Dataset 
from typing import List, Dict
from tqdm import tqdm 
import random




def convert_docs_to_dataset(docs: List[Doc], sentence_level: bool =False) -> Dataset:
    """
    Convert a document to a dataset.
    args:
        docs: a list of spacy.tokens.Doc
        sentence_level: whether to convert to sentence level dataset
    """

    if sentence_level:
        print('注意: 转换为句子级别数据集, 仅适用于token, span分类任务')
    if isinstance(docs, Doc):
        docs = [docs]
        

    d = {'text':[], 'labels':[],  'spans':[], 'tokens':[], 'triples':[]}
    for doc in tqdm(docs, desc='处理数据....'):
        if not sentence_level:
            d['text'].append(doc.text)
            d['labels'].append([label for label in doc._.labels])

            spans = []
            if ('all' in doc.spans) and len(doc.spans['all']) > 0:
                for span in doc.spans['all']:
                    spans.append({'offset': (span.start_char, span.end_char), 'label': span.label_, 'text': span.text})
            d['spans'].append(spans)

            tokens = []
            if len(doc.ents) > 0:
                for token in doc:
                    t = {'offset': (token.idx, token.idx+1), 'text': token.text}
                    bio = token.ent_iob_ + '-' + token.ent_type_ if token.ent_iob_ != 'O' else token.ent_iob_
                    t['label'] = bio
                    tokens.append(t)
            d['tokens'].append(tokens)

            triples = []
            for spo in doc._.spoes:
                sub = spo.subject
                pred = spo.predicate
                obj = spo.object
                triples.append({'subject': {'offset':(sub.start_char, sub.end_char), 'text':sub.text}, 'predicate': pred, 'object': {'offset':(obj.start_char, obj.end_char), 'text':obj.text}})
            d['triples'].append(triples)

        else:
            for sent in doc.sents:
                d['text'].append(sent.text)
                d['labels'].append([])
                sent_start = sent.start_char
                spans = []
                if ('all' in doc.spans) and len(doc.spans['all']) > 0:
                    for span in doc.spans['all']:
                        if span.sent == sent:
                            spans.append({'offset': (span.start_char - sent_start, span.end_char - sent_start), 'label': span.label_, 'text': span.text})
                d['spans'].append(spans)

                tokens = []
                if len(doc.ents) > 0:
                    for token in sent:
                        t = {'offset': (token.idx - sent_start, token.idx - sent_start+1), 'text': token.text}
                        bio = token.ent_iob_ + '-' + token.ent_type_ if token.ent_iob_ != 'O' else token.ent_iob_
                        t['label'] = bio
                        tokens.append(t)
                d['tokens'].append(tokens)

                triples = []
                d['triples'].append(triples)
    print("保存数据....")
    ds = Dataset.from_dict(d)
    return ds




def convert_ents_to_prompt_span_dataset(docs: list,
                                       synonym_dict: Dict[str, List]={}, 
                                       add_negtive_sample: bool = False,
                                       sentence_level: bool = False) -> Dataset:
    """将doc转换为prompt span数据集

    Args:
        docs (list): 待转换的文档列表
        synonym_dict (Dict[str, List], optional): 同义词字典. Defaults to {}.
        add_negtive_sample (bool, optional): 是否添加负样本. Defaults to False.
        sentence_level (bool, optional): 是否转换为句子级别. Defaults to False.

    Returns:
        Dataset: 转换的数据集
    """
    all_labels = set([ent.label_ for doc in docs for ent in doc.ents])
    text_ls = []
    prompt_ls = []
    spans_ls = []
    for doc in tqdm(docs):
        if not sentence_level:
            label_dict = {}
            for ent in doc.ents:
                if ent.label_ not in label_dict:
                    label_dict[ent.label_] = []
                label_dict[ent.label_].append({'text': ent.text, 'offset':[ent.start_char, ent.end_char]})
            if len(label_dict) == 0:
                continue
            else:
                for label in label_dict:
                    text_ls.append(doc.text)
                    if label in synonym_dict:
                        prompt_ls.append(random.choice(synonym_dict[label]+[label]))
                    else: 
                        prompt_ls.append(label)
                    spans_ls.append(label_dict[label])
                if add_negtive_sample:
                    other_labels = all_labels - set(label_dict.keys())
                    if len(other_labels)>0:
                        text_ls.append(doc.text)
                        label = random.choice(list(other_labels))
                        if label in synonym_dict:
                            prompt_ls.append(random.choice(synonym_dict[label]+[label]))
                        else:
                            prompt_ls.append(label)
                        spans_ls.append([])
        else:
            for sent in doc.sents:
                label_dict = {}
                for ent in sent.ents:
                    if ent.label_ not in label_dict:
                        label_dict[ent.label_] = []
                    label_dict[ent.label_].append({'text': ent.text, 'offset':[ent.start_char-sent.start_char, ent.end_char-sent.start_char]})
                if len(label_dict) == 0:
                    continue
                else:
                    for label in label_dict:
                        text_ls.append(sent.text)
                        if label in synonym_dict:
                            prompt_ls.append(random.choice(synonym_dict[label]+[label]))
                        else: 
                            prompt_ls.append(label)
                        spans_ls.append(label_dict[label])
                    if add_negtive_sample:
                        other_labels = all_labels - set(label_dict.keys())
                        if len(other_labels)>0:
                            text_ls.append(sent.text)
                            label = random.choice(list(other_labels))
                            if label in synonym_dict:
                                prompt_ls.append(random.choice(synonym_dict[label]+[label]))
                            else:
                                prompt_ls.append(label)
                            spans_ls.append([])   
    print("转换数据....") 
    ds = Dataset.from_dict({'text': text_ls, 'prompt': prompt_ls, 'spans': spans_ls})
    print("转换完成....")
    return ds



    
def convert_events_to_prompt_span_dataset(docs: List[Doc],
                                        synonym_dict: Dict[str, List[str]] = {},
                                        span_synonym_dict : Dict[str, List[str]] = {},
                                        add_negative_sample: bool =False,
                                        sentence_level: bool = False,
                                        add_span_prompt: bool = False) -> Dataset:

    """convert doc._.events to prompt span dataset({'text': '', 'prompt': '', 'spans': []})
    Args:
        docs (List[Doc]): doc list
        synonym_dict (Dict[str, List[str]], optional): synonym dict like {'姓名':[名称]}. Defaults to {}.
        span_synonym_dict (Dict[str, List[str]], optional): span synonym dict like {'姓名':[名称]}. Defaults to {}.
        add_negative_sample (bool, optional): add negative sample. Defaults to False.
        sentence_level (bool, optional): if cut into sentence-level text. the text contains all sentences the event belongs to. Defaults to False.
        add_span_prompt (bool, optional): if add span prompt to dataset. Defaults to False.

    Returns:
        Dataset: converted dataset
    """
    all_roles = set([role for doc in docs for event in doc._.events for role in event.roles])
    all_span_labels = set([span.label_ for doc in docs for event in doc._.events for role in event.roles for span in event.roles[role]])
    text_ls = []
    prompt_ls = []
    spans_ls = []
    for doc in tqdm(docs):
        for event in doc._.events:
            if not sentence_level:
                span_label_dict = {} # 用来保存每种类别的span
                for role in event.roles:
                    if role in synonym_dict:
                        role = random.choice(synonym_dict[role]+[role])
                    text_ls.append(doc.text)
                    prompt_ls.append(event.label + '的' + role)
                    spans_ls.append([{'text': span.text, 'offset':[span.start_char, span.end_char]} for span in event.roles[role]])
                    if add_span_prompt:
                        for span in event.roles[role]:
                            if span.label_ not in span_label_dict:
                                span_label_dict[span.label_] = []
                            span_label_dict[span.label_].append({'text': span.text, 'offset':[span.start_char, span.end_char]})
                # 添加span prompt数据
                if add_span_prompt:
                    for span_label in span_label_dict:
                        if span_label in span_synonym_dict:
                            span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                        text_ls.append(doc.text)
                        prompt_ls.append(span_label)
                        spans_ls.append(span_label_dict[span_label])
                    
                if add_negative_sample:
                    other_roles = all_roles - set(event.roles.keys())
                    if len(other_roles)>0:
                        role = random.choice(list(other_roles))
                        if role in synonym_dict:
                            role = random.choice(synonym_dict[role]+[role])
                        text_ls.append(doc.text)
                        prompt_ls.append(event.label + '的' + role)
                        spans_ls.append([])
                    if add_span_prompt:
                        other_span_labels = all_span_labels - set(span_label_dict.keys())
                        if len(other_span_labels)>0:
                            span_label = random.choice(list(other_span_labels))
                            if span_label in span_synonym_dict:
                                span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                            text_ls.append(doc.text)
                            prompt_ls.append(span_label)
                            spans_ls.append([])
            else:
                text = ''.join([sent.text for sent in event.sents])
                span_label_dict = {} # 用来保存每种类别的span
                for role in event.roles:
                    if role in synonym_dict:
                        role = random.choice(synonym_dict[role]+[role])
                    text_ls.append(text)
                    prompt_ls.append(event.label + '的' + role)
                    spans_ls.append([{'text': span.text, 'offset':[span.start_char-event.sents[0].start_char, span.end_char-event.sents[0].start_char]} for span in event.roles[role]])
                    if add_span_prompt:
                        for span in event.roles[role]:
                            if span.label_ not in span_label_dict:
                                span_label_dict[span.label_] = []
                            span_label_dict[span.label_].append({'text': span.text, 'offset':[span.start_char-event.sents[0].start_char, span.end_char-event.sents[0].start_char]})
                # 添加span prompt数据
                if add_span_prompt:
                    for span_label in span_label_dict:
                        if span_label in span_synonym_dict:
                            span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                        text_ls.append(text)
                        prompt_ls.append(span_label)
                        spans_ls.append(span_label_dict[span_label])
                # 添加负样本 
                if add_negative_sample:
                    other_roles = all_roles - set(event.roles.keys())
                    if len(other_roles)>0:
                        role = random.choice(list(other_roles))
                        if role in synonym_dict:
                            role = random.choice(synonym_dict[role]+[role])
                        text_ls.append(text)
                        prompt_ls.append(event.label + '的' + role)
                        spans_ls.append([])
                    if add_span_prompt:
                        other_span_labels = all_span_labels - set(span_label_dict.keys())
                        if len(other_span_labels)>0:
                            span_label = random.choice(list(other_span_labels))
                            if span_label in span_synonym_dict:
                                span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                            text_ls.append(text)
                            prompt_ls.append(span_label)
                            spans_ls.append([])
                        
    print("转换为数据集....")
    ds = Dataset.from_dict({'text': text_ls, 'prompt': prompt_ls, 'spans': spans_ls})
    print("转换完成")
    return ds



def convert_relations_to_prompt_span_dataset(docs: List[Doc],
                                             synonym_dict: Dict[str, List[str]]={},
                                             span_synonym_dict: Dict[str, List[str]]={},
                                             sentence_level: bool = False,
                                             add_negative_sample: bool = False,
                                             add_span_prompt: bool = False) -> Dataset:
    text_ls = []
    prompt_ls = []
    spans_ls = []
    if add_span_prompt:
        # get all span labels
        all_span_labels = set()
        for doc in docs:
            for rel in doc._.relations:
                all_span_labels.add(rel.sub.label_)
                for obj in rel.objs:
                    all_span_labels.add(obj.label_)
    all_relation_labels = set([rel.label for doc in docs for rel in doc._.relations])
    for doc in tqdm(docs):
        if not sentence_level:
            # 添加relation prompt数据
            for rel in doc._.relations:
                text_ls.append(doc.text)
                if rel.label in synonym_dict:
                    rel_label = random.choice(synonym_dict[rel.label]+[rel.label])
                else:
                    rel_label = rel.label
                prompt_ls.append(rel.sub.text + '的' + rel_label)
                spans = []
                for obj in rel.objs:
                    spans.append({'text': obj.text, 'offset':[obj.start_char, obj.end_char]})
                spans_ls.append(spans)
            if add_negative_sample:
                other_rel_labels = all_relation_labels - set([rel.label for rel in doc._.relations])
                if len(other_rel_labels)>0:
                    for rel in doc._.relations:
                        rel_label = random.choice(list(other_rel_labels))
                        if rel_label in synonym_dict:
                            rel_label = random.choice(synonym_dict[rel_label]+[rel_label])
                        text_ls.append(doc.text)
                        prompt_ls.append(rel.sub.text + '的' + rel_label)
                        spans_ls.append([])
            # 添加span prompt数据
            if add_span_prompt:
                span_label_dict = {}
                for rel in doc._.relations:
                    if rel.sub.label_ not in span_label_dict:
                        span_label_dict[rel.sub.label_] = []
                    span_label_dict[rel.sub.label_].append({'text': rel.sub.text, 'offset':[rel.sub.start_char, rel.sub.end_char]})
                    for obj in rel.objs:
                        if obj.label_ not in span_label_dict:
                            span_label_dict[obj.label_] = []
                        span_label_dict[obj.label_].append({'text': obj.text, 'offset':[obj.start_char, obj.end_char]})
                for span_label in span_label_dict:
                    text_ls.append(doc.text)
                    if span_label in span_synonym_dict:
                        span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                    prompt_ls.append(span_label)
                    spans_ls.append(span_label_dict[span_label])
                if add_negative_sample:
                    other_span_labels = all_span_labels - set(span_label_dict.keys())
                    if len(other_span_labels)>0:
                        span_label = random.choice(list(other_span_labels))
                        if span_label in span_synonym_dict:
                            span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                        text_ls.append(doc.text)
                        prompt_ls.append(span_label)
                        spans_ls.append([])
        else:
            rel_labels = set([rel.label for rel in doc._.relations])
            for rel in doc._.relations:
                text = ''.join([sent.text for sent in rel.sents])
                text_ls.append(text)
                rel_label = rel.label
                if rel_label in synonym_dict:
                    rel_label = random.choice(synonym_dict[rel_label]+[rel_label])
                prompt_ls.append(rel.sub.text + '的' + rel_label)
                spans = []
                for obj in rel.objs:
                    spans.append({'text': obj.text, 'offset':[obj.start_char-rel.sents[0].start_char, obj.end_char-rel.sents[0].start_char]})
                spans_ls.append(spans)
                if add_negative_sample:
                    other_rel_labels = all_relation_labels - rel_labels
                    if len(other_rel_labels)>0:
                        text_ls.append(text)
                        rel_label = random.choice(list(other_rel_labels))
                        if rel_label in synonym_dict:
                            rel_label = random.choice(synonym_dict[rel_label]+[rel_label])
                        prompt_ls.append(rel.sub.text + '的' + rel_label)
                        spans_ls.append([])
            if add_span_prompt:
                span_label_dict = {}
                for rel in doc._.relations:
                    if rel.sub.label_ not in span_label_dict:
                        span_label_dict[rel.sub.label_] = []
                    span_label_dict[rel.sub.label_].append({'text': rel.sub.text, 'offset':[rel.sub.start_char, rel.sub.end_char]})
                    for obj in rel.objs:
                        if obj.label_ not in span_label_dict:
                            span_label_dict[obj.label_] = []
                        span_label_dict[obj.label_].append({'text': obj.text, 'offset':[obj.start_char, obj.end_char]})
                for span_label in span_label_dict:
                    left_idx = min([span['offset'][0] for span in span_label_dict[span_label]])
                    right_idx = max([span['offset'][1] for span in span_label_dict[span_label]])
                    sents = list(doc[left_idx:right_idx].sents)
                    last = sents.pop()
                    sents.append(last.sent)
                    text = ''.join([sent.text for sent in sents])
                    text_ls.append(text)
                    spans = []
                    for span in span_label_dict[span_label]:
                        # for span in spans:
                        span_ = {'text': span['text'], 'offset':[span['offset'][0]-sents[0].start_char, span['offset'][1]-sents[0].start_char]}
                        spans.append(span_)
                    spans_ls.append(spans)
                    if span_label in span_synonym_dict:
                        synonym_label = random.choice(span_synonym_dict[span_label]+[span_label])
                        prompt_ls.append(synonym_label)
                    else:
                        prompt_ls.append(span_label)
                    if add_negative_sample:
                        other_span_labels = all_span_labels - set(span_label_dict.keys())
                        if len(other_span_labels)>0:
                            span_label = random.choice(list(other_span_labels))
                            if span_label in span_synonym_dict:
                                span_label = random.choice(span_synonym_dict[span_label]+[span_label])
                            text_ls.append(text)
                            prompt_ls.append(span_label)
                            spans_ls.append([])           
    print('转换数据中...')
    assert len(text_ls) == len(prompt_ls) == len(spans_ls)
    ds = Dataset.from_dict({'text': text_ls, 'prompt': prompt_ls, 'spans': spans_ls})
    print('转换数据完成')
    return ds
                                       