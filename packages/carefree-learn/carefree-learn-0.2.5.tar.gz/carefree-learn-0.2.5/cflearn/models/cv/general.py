import torch.nn as nn

from torch import Tensor
from typing import Any
from typing import Dict
from typing import Optional
from cftool.misc import check_requires

from .encoder import EncoderBase
from .encoder import Encoder1DBase
from .decoder import DecoderBase
from .decoder import Decoder1DBase
from ...types import tensor_dict_type
from ...misc.toolkit import auto_num_layers


class EncoderDecoder(nn.Module):
    def __init__(
        self,
        is_1d: int,
        in_channels: int,
        out_channels: Optional[int] = None,
        target_downsample: Optional[int] = None,
        latent_padding_channels: Optional[int] = 16,
        num_classes: Optional[int] = None,
        *,
        latent: int = 128,
        decoder_latent: Optional[int] = None,
        img_size: Optional[int] = None,
        min_size: int = 2,
        num_downsample: Optional[int] = None,
        num_upsample: Optional[int] = None,
        latent_resolution: Optional[int] = None,
        encoder: str = "vanilla",
        decoder: str = "vanilla",
        encoder_config: Optional[Dict[str, Any]] = None,
        decoder_config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__()
        # up / down sample stuffs
        if num_downsample is None:
            if img_size is None:
                raise ValueError(
                    "either `img_size` or `num_downsample` should be provided "
                    "(when `num_downsample` is not provided, it will be inferred "
                    "automatically with `img_size` & `min_size`)"
                )
            args = img_size, min_size, target_downsample
            num_downsample = auto_num_layers(*args, use_stride=encoder == "vanilla")
        num_upsample = num_upsample or num_downsample
        if latent_resolution is None and img_size is None:
            raise ValueError(
                "either `img_size` or `latent_resolution` should be provided "
                "in `VanillaVAEBase` (when `latent_resolution` is not provided, "
                "it will be inferred automatically with `img_size`)"
            )
        # check num_downsample requirement
        self.encoder_base = (Encoder1DBase if is_1d else EncoderBase).get(encoder)  # type: ignore
        self.decoder_base = (Decoder1DBase if is_1d else DecoderBase).get(decoder)  # type: ignore
        requires_num_downsample = check_requires(self.encoder_base, "num_downsample")
        if not requires_num_downsample:
            num_downsample = None
        # properties
        self.is_1d = is_1d
        self.latent = latent
        self.decoder_latent = decoder_latent or latent
        self.latent_key = "latent_dim" if is_1d else "latent_channels"
        self.img_size = img_size
        self.latent_padding_channels = latent_padding_channels
        self.num_classes = num_classes
        self.num_downsample = num_downsample
        self.num_upsample = num_upsample
        # encoder
        if encoder_config is None:
            encoder_config = {}
        if check_requires(self.encoder_base, "img_size"):
            encoder_config["img_size"] = img_size
        if requires_num_downsample:
            encoder_config["num_downsample"] = num_downsample
        encoder_config["in_channels"] = in_channels
        encoder_config[self.latent_key] = latent
        self.encoder = self.encoder_base.make(encoder, config=encoder_config)
        if not is_1d and img_size is not None:
            latent_resolution = self.encoder.latent_resolution(img_size)
        # decoder
        if decoder_config is None:
            decoder_config = {}
        decoder_config[self.latent_key] = self.decoder_latent
        decoder_config["img_size"] = img_size
        decoder_config["num_classes"] = num_classes
        decoder_config["out_channels"] = out_channels or in_channels
        if num_upsample is not None and not decoder.startswith("style"):
            decoder_config["num_upsample"] = num_upsample
        if latent_resolution is not None:
            decoder_config["latent_resolution"] = latent_resolution
        self.decoder = self.decoder_base.make(decoder, config=decoder_config)
        self.latent_resolution = self.decoder.latent_resolution

    def resize(self, net: Tensor) -> Tensor:
        return self.decoder.resize(net)

    def encode(self, batch: tensor_dict_type, **kwargs: Any) -> Tensor:
        return self.encoder.encode(batch, **kwargs)

    def decode(self, batch: tensor_dict_type, **kwargs: Any) -> Tensor:
        net = self.decoder.decode(batch, **kwargs)
        return self.resize(net)


__all__ = ["EncoderDecoder"]
