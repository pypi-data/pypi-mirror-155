from torch import nn

from .mmoe import MMoE
from .bottom import BSTBottom, TxT


class MultiTaskBST(nn.Module):
    """
    Args:
        deep_dims: size of the dictionary of embeddings.
        seq_dim: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int.
        seq_hidden_size: the dimension of the feedforward network model.
        expert_num: the number of expert layer.
        expert_hidden_sizes: the dimension of the feedforward network model.
        task_num: the number of task output.
        task_hidden_sizes: the dimension of the feedforward network model.
        task_last_activations: list of activations for each task.
        num_wide: the number of wide input features (default=0).
        num_shared: the number of embedding shared with sequence transformer (default=1).
    """
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations, num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None, 
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super(MultiTaskBST, self).__init__()
        self.shared_bottom = BSTBottom(
            deep_dims=deep_dims,
            seq_dim=seq_dim,
            seq_embed_dim=seq_embed_dim,
            deep_embed_dims=deep_embed_dims,
            seq_hidden_size=seq_hidden_size,
            num_wide=num_wide,
            num_shared=num_shared,
            item_embedding_weight=item_embedding_weight,
            shared_embeddings_weight=shared_embeddings_weight,
            context_head_kwargs=context_head_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        self.mmoe = MMoE(
            input_size=seq_embed_dim,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, deep_in, seq_in, vl_in, wide_in, shared_in):
        bottom_features = self.shared_bottom(deep_in=deep_in, seq_in=seq_in, vl_in=vl_in, wide_in=wide_in, shared_in=shared_in)
        outs = self.mmoe(bottom_features)
        return outs


class MultiTaskTxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.is_candidate_mode = is_candidate_mode
        self.shared_bottom = TxT(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = cross_size + self.shared_bottom.sequence_transformer.seq_embed_dim
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        bottom_features = self.shared_bottom(ctx_in, seq_in, vl_in, candidate_in, seq_history)
        outs = self.mmoe(bottom_features)
        return outs
