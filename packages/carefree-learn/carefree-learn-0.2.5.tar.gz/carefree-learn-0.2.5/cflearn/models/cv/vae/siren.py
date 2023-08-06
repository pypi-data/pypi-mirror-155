import torch

from torch import Tensor
from typing import Any
from typing import Dict
from typing import Optional
from cftool.misc import check_requires

from .vanilla import reparameterize
from ..protocol import GaussianGeneratorMixin
from ....types import tensor_dict_type
from ....protocol import TrainerState
from ....protocol import ModelProtocol
from ....constants import LABEL_KEY
from ....constants import PREDICTIONS_KEY
from ..encoder.protocol import Encoder1DBase
from ...implicit.siren import ImgSiren
from ....misc.toolkit import auto_num_layers
from ....losses.vae import MU_KEY
from ....losses.vae import LOG_VAR_KEY
from ....modules.blocks import Linear


@ModelProtocol.register("siren_vae")
class SirenVAE(ModelProtocol, GaussianGeneratorMixin):
    def __init__(
        self,
        img_size: int,
        in_channels: int,
        out_channels: Optional[int] = None,
        *,
        min_size: int = 2,
        latent_dim: int = 256,
        target_downsample: Optional[int] = None,
        num_classes: Optional[int] = None,
        conditional_dim: int = 16,
        num_layers: int = 4,
        w_sin: float = 1.0,
        w_sin_initial: float = 30.0,
        bias: bool = True,
        final_activation: Optional[str] = None,
        encoder1d: str = "vanilla",
        encoder1d_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        self.img_size = img_size
        self.latent_dim = latent_dim
        self.num_classes = num_classes
        self.out_channels = out_channels or in_channels
        args = img_size, min_size, target_downsample
        num_downsample = auto_num_layers(*args, use_stride=encoder1d == "vanilla")
        # encoder
        encoder1d_base = Encoder1DBase.get(encoder1d)
        if encoder1d_config is None:
            encoder1d_config = {}
        if check_requires(encoder1d_base, "img_size"):
            encoder1d_config["img_size"] = img_size
        encoder1d_config["in_channels"] = in_channels
        encoder1d_config["latent_dim"] = latent_dim
        if encoder1d == "vanilla":
            encoder1d_config["num_downsample"] = num_downsample
        self.encoder = encoder1d_base(**encoder1d_config)
        self.to_statistics = Linear(latent_dim, 2 * latent_dim, bias=False)
        # siren
        self.siren = ImgSiren(
            img_size,
            self.out_channels,
            latent_dim,
            num_classes,
            conditional_dim,
            num_layers=num_layers,
            w_sin=w_sin,
            w_sin_initial=w_sin_initial,
            bias=bias,
            final_activation=final_activation,
        )

    @property
    def can_reconstruct(self) -> bool:
        return True

    def decode(
        self,
        z: Tensor,
        *,
        labels: Optional[Tensor],
        size: Optional[int] = None,
        **kwargs: Any,
    ) -> Tensor:
        net = self.siren.decode(z, labels=labels, size=size)
        net = torch.tanh(net)
        return net

    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        net = self.encoder.encode(batch, **kwargs)
        net = self.to_statistics(net)
        mu, log_var = net.chunk(2, dim=1)
        net = reparameterize(mu, log_var)
        net = self.siren.decode(net, labels=batch.get(LABEL_KEY))
        return {PREDICTIONS_KEY: net, MU_KEY: mu, LOG_VAR_KEY: log_var}


__all__ = [
    "SirenVAE",
]
