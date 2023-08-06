from torch import nn
from typing import Any
from typing import Dict
from typing import List
from typing import Callable
from typing import Optional
from cftool.array import squeeze

from .core import Backbone
from ..protocol import EncoderBase
from ..protocol import Encoder1DBase
from .....types import tensor_dict_type
from .....protocol import TrainerState
from .....constants import INPUT_KEY
from .....constants import LATENT_KEY
from .....modules.blocks import Conv2d


class Preset:
    remove_layers: Dict[str, List[str]] = {}
    target_layers: Dict[str, Dict[str, str]] = {}
    increment_configs: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register_settings(cls) -> Callable:
        def _register(settings: Preset) -> None:
            cls.remove_layers.update(settings.remove_layers)
            cls.target_layers.update(settings.target_layers)
            cls.increment_configs.update(settings.increment_configs)

        return _register


@EncoderBase.register("backbone")
class BackboneEncoder(EncoderBase):
    def __init__(
        self,
        name: str,
        in_channels: int,
        latent_channels: Optional[int] = None,
        num_downsample: Optional[int] = None,
        *,
        finetune: bool = True,
        pretrained: bool = False,
        use_to_rgb: bool = False,
        to_rgb_bias: bool = False,
        backbone_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(in_channels, num_downsample, latent_channels)  # type: ignore
        if in_channels == 3 and not use_to_rgb:
            self.to_rgb = None
        else:
            self.to_rgb = Conv2d(in_channels, 3, kernel_size=1, bias=to_rgb_bias)
        self.net = Backbone(
            name,
            pretrained=pretrained,
            requires_grad=finetune,
            **(backbone_config or {}),
        )
        self.num_downsample = self.net.num_downsample
        self.latent_channels = self.net.latent_channels
        if num_downsample is not None and num_downsample != self.num_downsample:
            raise ValueError(
                f"provided `num_downsample` ({num_downsample}) is not "
                f"identical with `target_downsample` ({self.num_downsample}), "
                f"please consider set `num_downsample` to {self.num_downsample}"
            )
        if latent_channels is not None and latent_channels != self.latent_channels:
            raise ValueError(
                f"provided `latent_channels` ({latent_channels}) is not "
                f"identical with `preset_latent_channels` ({self.latent_channels}), "
                f"please consider set `latent_channels` to {self.latent_channels}"
            )

    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        net = batch[INPUT_KEY]
        if self.to_rgb is not None:
            net = self.to_rgb(net)
        return self.net(net)


@Encoder1DBase.register("backbone")
class BackboneEncoder1D(Encoder1DBase):
    def __init__(
        self,
        name: str,
        in_channels: int,
        latent_dim: Optional[int] = None,
        *,
        finetune: bool = True,
        pretrained: bool = False,
        backbone_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(in_channels, -1)
        self.encoder = BackboneEncoder(
            name,
            in_channels,
            latent_dim,
            finetune=finetune,
            pretrained=pretrained,
            backbone_config=backbone_config,
        )
        self.latent_dim = self.encoder.latent_channels
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        outputs = self.encoder(batch_idx, batch, state, **kwargs)
        latent = outputs[LATENT_KEY]
        if latent.shape[-2] != 1 or latent.shape[-1] != 1:
            latent = self.pool(latent)
        outputs[LATENT_KEY] = squeeze(latent)
        return outputs


__all__ = [
    "BackboneEncoder",
    "BackboneEncoder1D",
]
