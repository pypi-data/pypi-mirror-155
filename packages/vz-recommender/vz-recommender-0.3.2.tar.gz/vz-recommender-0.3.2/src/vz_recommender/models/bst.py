from typing import *

import torch
from torch import nn

from .bottom import BSTBottom
from transformers import AutoModel, AutoTokenizer, AutoConfig, DistilBertTokenizer, DistilBertModel


class BST(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in, search_in=search_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class BSTBERT(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, nlp_encoder_path, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        # self.nlp_device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)
        # self.nlp_encoder.to(self.nlp_device)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        search_in = self.nlp_encoder(**search_in).last_hidden_state[:,0,:].to(dtype=torch.float32)
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in, search_in=search_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class BSTBERT2(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, tokenizer_path=None, nlp_encoder_path=None, 
                 num_wide=0, num_shared=0, nlp_dim=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                         num_wide, num_shared, nlp_dim, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)
        self.nlp_head = NLPHead(tokenizer_path=tokenizer_path, nlp_encoder_path=nlp_encoder_path)
        
    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).

        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        search_out = self.nlp_head(search_in=search_in)
        outs = torch.cat([seq_out, ctx_out, search_out], dim=1)
        outs = self.dense1(outs)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)


class NLPHead(nn.Module):
    """
    Args:
        tokenizer_path: path of hg tokenizer.
        nlp_encoder_path: path of hg pre trained model.
    """
    def __init__(self, tokenizer_path, nlp_encoder_path):
        super().__init__()
        self.nlp_encoder = AutoModel.from_pretrained(nlp_encoder_path)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=False)
        self.nlp_device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.nlp_encoder.to(self.nlp_device)
        
    def forward(self, search_in):
        """
        Args:
            search_in: tensor, Tensor of shape [batch_size, 1] (default=None).
        
        Return: 
            search_out: Tensor, shape [batch_size, len(deep_dims)*deep_embed_dims+(num_shared*seq_embed_dim)+num_wide+nlp_dim]
        """
        search_in = self.tokenizer(list(search_in), return_tensors='pt', truncation=True, padding=True, max_length=512).to(self.nlp_device)
        search_out = self.nlp_encoder(**search_in).last_hidden_state[:,0,:].to(dtype=torch.float32)

        return search_out
