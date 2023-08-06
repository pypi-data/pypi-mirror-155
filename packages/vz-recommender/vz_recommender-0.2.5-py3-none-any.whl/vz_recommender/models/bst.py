import math
from typing import *

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from transformers import DistilBertModel, DistilBertTokenizerFast

from .bottom import BSTBottom
from .txt import MeanMaxPooling, PositionalEncoding


class BST(BSTBottom):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, tokenizer, nlp_encoder,
                 num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None,
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super().__init__(deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, tokenizer, nlp_encoder,
                         num_wide, num_shared, context_head_kwargs, sequence_transformer_kwargs,
                         item_embedding_weight, shared_embeddings_weight)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, 1].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, 1] (default=None).
            shared_in: list, a list of Tensor of shape [batch_size, 1] (default=None).

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
