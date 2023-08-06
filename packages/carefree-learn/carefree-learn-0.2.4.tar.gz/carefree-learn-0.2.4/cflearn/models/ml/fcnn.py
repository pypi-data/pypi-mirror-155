import torch.nn as nn

from typing import Any
from typing import List
from typing import Optional

from .protocol import MERGED_KEY
from .protocol import MLCoreProtocol
from ...types import tensor_dict_type
from ...protocol import TrainerState
from ...constants import PREDICTIONS_KEY
from ...modules.blocks import mapping_dict


@MLCoreProtocol.register("fcnn")
class FCNN(MLCoreProtocol):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        num_history: int,
        hidden_units: Optional[List[int]] = None,
        *,
        mapping_type: str = "basic",
        bias: bool = True,
        activation: str = "ReLU",
        batch_norm: bool = False,
        dropout: float = 0.0,
    ):
        super().__init__(in_dim, out_dim, num_history)
        in_dim *= num_history
        if hidden_units is None:
            dim = max(32, min(1024, 2 * in_dim))
            hidden_units = 2 * [dim]
        mapping_base = mapping_dict[mapping_type]
        blocks: List[nn.Module] = []
        for hidden_unit in hidden_units:
            mapping = mapping_base(
                in_dim,
                hidden_unit,
                bias=bias,
                activation=activation,
                batch_norm=batch_norm,
                dropout=dropout,
            )
            blocks.append(mapping)
            in_dim = hidden_unit
        blocks.append(nn.Linear(in_dim, out_dim, bias))
        self.hidden_units = hidden_units
        self.net = nn.Sequential(*blocks)

    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        net = batch[MERGED_KEY]
        if len(net.shape) > 2:
            net = net.contiguous().view(len(net), -1)
        return {PREDICTIONS_KEY: self.net(net)}


__all__ = ["FCNN"]
