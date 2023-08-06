# -*- ecoding: utf-8 -*-
# @ModuleName: process_data
# @Copyright: Deep_Wisdom 
# @Author: wk
# @Email: wangkai@fuzhi.ai
# @Time: 2022/1/20 8:21 下午

from .base_dataset import BaseDataset
from .multi_task_dataset import MultiTaskDataset
from .emb_dataset import EmbDataset
import torch.utils.data as D

def get_base_dataloader(train_df, valid_df, test_df, schema, batch_size = 512*3):

    train_dataset = BaseDataset(schema,train_df)
    enc_dict = train_dataset.get_enc_dict()
    valid_dataset = BaseDataset(schema, valid_df,enc_dict=enc_dict)
    test_dataset = BaseDataset(schema, test_df,enc_dict=enc_dict)

    train_loader = D.DataLoader(train_dataset,batch_size=batch_size,shuffle=True,num_workers=4)
    valid_loader = D.DataLoader(valid_dataset,batch_size=batch_size,shuffle=False,num_workers=0)
    test_loader = D.DataLoader(test_dataset,batch_size=batch_size,shuffle=False,num_workers=0)

    return train_loader,valid_loader,test_loader, enc_dict

def get_multi_task_dataloader(train_df, valid_df, test_df, schema, batch_size = 512*3):

    train_dataset = MultiTaskDataset(schema,train_df)
    enc_dict = train_dataset.get_enc_dict()
    valid_dataset = MultiTaskDataset(schema, valid_df,enc_dict=enc_dict)
    test_dataset = MultiTaskDataset(schema, test_df,enc_dict=enc_dict)

    train_loader = D.DataLoader(train_dataset,batch_size=batch_size,shuffle=True,num_workers=4)
    valid_loader = D.DataLoader(valid_dataset,batch_size=batch_size,shuffle=False,num_workers=0)
    test_loader = D.DataLoader(test_dataset,batch_size=batch_size,shuffle=False,num_workers=0)

    return train_loader,valid_loader,test_loader, enc_dict

def get_emb_dataloader(train_df, valid_df, test_df, emb_df, schema, batch_size = 512*3):

    train_dataset = EmbDataset(schema, train_df, emb_df)
    enc_dict = train_dataset.get_enc_dict()
    valid_dataset = EmbDataset(schema, valid_df, emb_df, enc_dict=enc_dict)
    test_dataset = EmbDataset(schema, test_df, emb_df, enc_dict=enc_dict)

    train_loader = D.DataLoader(train_dataset, batch_size=batch_size, shuffle=True,num_workers=4)
    valid_loader = D.DataLoader(valid_dataset, batch_size=batch_size, shuffle=False,num_workers=0)
    test_loader = D.DataLoader(test_dataset, batch_size=batch_size, shuffle=False,num_workers=0)

    return train_loader, valid_loader, test_loader, enc_dict

def get_dataloader(train_df, valid_df, test_df, schema, emb_df = None):
    if schema.get('use_content_emb',False):
        return get_emb_dataloader(train_df, valid_df, test_df, emb_df, schema)
    elif isinstance(schema['label_col'], list):
        return get_multi_task_dataloader(train_df, valid_df, test_df, schema)
    else:
        return get_base_dataloader(train_df, valid_df, test_df, schema)