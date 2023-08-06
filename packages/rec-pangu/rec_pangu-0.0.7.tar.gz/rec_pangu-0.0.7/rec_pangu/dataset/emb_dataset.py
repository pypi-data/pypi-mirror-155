# -*- ecoding: utf-8 -*-
# @ModuleName: emb_dataset
# @Copyright: Deep_Wisdom 
# @Author: wk
# @Email: wangkai@fuzhi.ai
# @Time: 2022/1/18 2:12 下午
from .base_dataset import BaseDataset
import torch

class EmbDataset(BaseDataset):
    def __init__(self, config, df, emb_df, enc_dict=None):
        super(EmbDataset, self).__init__(config=config,df=df,enc_dict=enc_dict)

        #处理emb部分
        self.emb_df = emb_df

        self.df = self.df.merge(self.emb_df, on=self.config['item_col']).dropna().reset_index(drop=True)

        self.df = self.df.rename(columns={'vector':'content_emb'})

        self.df['content_emb'] = self.df['content_emb']

        self.feature_name.append('content_emb')

    def __getitem__(self, index):
        data = dict()
        for col in self.feature_name:
            if col in self.dense_cols:
                data[col] = torch.Tensor([self.enc_df[col].iloc[index]]).squeeze(-1)
            elif col in self.sparse_cols:
                data[col] = torch.Tensor([self.enc_df[col].iloc[index]]).long().squeeze(-1)
            elif col =='content_emb':
                data[col] = torch.Tensor([float(x) for x in self.df['content_emb'].iloc[index].split('|')]).squeeze(-1)
        data['label'] = torch.Tensor([self.enc_df['label'].iloc[index]]).squeeze(-1)
        return data

    def __len__(self):
        return len(self.df)


