import torch
import random

from abc import abstractmethod
from abc import ABC
from abc import ABCMeta
from torch import Tensor
from typing import Any
from typing import Optional

from ...types import tensor_dict_type
from ...protocol import TrainerState
from ...constants import INPUT_KEY
from ...constants import LABEL_KEY
from ...constants import PREDICTIONS_KEY
from ...misc.toolkit import slerp


class GeneratorMixin(ABC):
    latent_dim: int
    num_classes: Optional[int]

    # inherit

    @property
    @abstractmethod
    def device(self) -> torch.device:
        pass

    @property
    @abstractmethod
    def can_reconstruct(self) -> bool:
        pass

    @abstractmethod
    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        pass

    @abstractmethod
    def sample(
        self,
        num_samples: int,
        *,
        class_idx: Optional[int] = None,
        **kwargs: Any,
    ) -> Tensor:
        pass

    @abstractmethod
    def interpolate(
        self,
        num_samples: int,
        *,
        class_idx: Optional[int] = None,
        use_slerp: bool = False,
        **kwargs: Any,
    ) -> Tensor:
        pass

    # utilities

    @property
    def is_conditional(self) -> bool:
        return self.num_classes is not None

    def reconstruct(self, net: Tensor, **kwargs: Any) -> Tensor:
        name = self.__class__.__name__
        if not self.can_reconstruct:
            raise ValueError(f"`{name}` does not support `reconstruct`")
        labels = kwargs.pop(LABEL_KEY, None)
        batch = {INPUT_KEY: net, LABEL_KEY: labels}
        if self.is_conditional and labels is None:
            raise ValueError(
                f"`{LABEL_KEY}` should be provided in `reconstruct` "
                f"for conditional `{name}`"
            )
        return self.forward(0, batch, **kwargs)[PREDICTIONS_KEY]

    def get_sample_labels(
        self,
        num_samples: int,
        class_idx: Optional[int] = None,
    ) -> Optional[Tensor]:
        if self.num_classes is None:
            return None
        if class_idx is not None:
            return torch.full([num_samples], class_idx, device=self.device)
        return torch.randint(self.num_classes, [num_samples], device=self.device)


class GaussianGeneratorMixin(GeneratorMixin, metaclass=ABCMeta):
    @abstractmethod
    def decode(self, z: Tensor, *, labels: Optional[Tensor], **kwargs: Any) -> Tensor:
        pass

    def sample(
        self,
        num_samples: int,
        *,
        class_idx: Optional[int] = None,
        labels: Optional[Tensor] = None,
        **kwargs: Any,
    ) -> Tensor:
        z = torch.randn(num_samples, self.latent_dim, device=self.device)
        if labels is None:
            labels = self.get_sample_labels(num_samples, class_idx)
        elif class_idx is not None:
            msg = "`class_idx` should not be provided when `labels` is provided"
            raise ValueError(msg)
        return self.decode(z, labels=labels, **kwargs)

    def interpolate(
        self,
        num_samples: int,
        *,
        class_idx: Optional[int] = None,
        use_slerp: bool = False,
        **kwargs: Any,
    ) -> Tensor:
        z1 = torch.randn(1, self.latent_dim, device=self.device)
        z2 = torch.randn(1, self.latent_dim, device=self.device)
        ratio = torch.linspace(0.0, 1.0, num_samples, device=self.device)[:, None]
        z = slerp(z1, z2, ratio) if use_slerp else ratio * z1 + (1.0 - ratio) * z2
        if class_idx is None and self.num_classes is not None:
            class_idx = random.randint(0, self.num_classes - 1)
        labels = self.get_sample_labels(num_samples, class_idx)
        return self.decode(z, labels=labels, **kwargs)


class ImageTranslatorMixin(ABC):
    @abstractmethod
    def forward(
        self,
        batch_idx: int,
        batch: tensor_dict_type,
        state: Optional[TrainerState] = None,
        **kwargs: Any,
    ) -> tensor_dict_type:
        pass

    def onnx_forward(self, batch: tensor_dict_type) -> Any:
        return self.generate_from(batch[INPUT_KEY], determinate=True)

    def generate_from(self, net: Tensor, **kwargs: Any) -> Tensor:
        rs = self.forward(0, {INPUT_KEY: net}, **kwargs)[PREDICTIONS_KEY]
        if isinstance(rs, list):
            rs = rs[0]
        return rs
