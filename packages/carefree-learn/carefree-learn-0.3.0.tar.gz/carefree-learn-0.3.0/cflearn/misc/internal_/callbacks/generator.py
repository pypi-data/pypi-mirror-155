import os
import torch

import numpy as np

from .general import ImageCallback
from ...toolkit import to_numpy
from ...toolkit import to_torch
from ...toolkit import to_device
from ...toolkit import save_images
from ...toolkit import eval_context
from ....trainer import Trainer
from ....trainer import TrainerCallback
from ....constants import INPUT_KEY
from ....constants import LABEL_KEY
from ....constants import PREDICTIONS_KEY
from ....models.cv.protocol import GeneratorMixin
from ....models.cv.stylizer.constants import STYLE_KEY
from ....models.cv.segmentor.constants import LV1_ALPHA_KEY

try:
    from cfcv.misc.toolkit import min_max_normalize
except:
    min_max_normalize = None


@TrainerCallback.register("gan")
@TrainerCallback.register("vae")
@TrainerCallback.register("vae2d")
@TrainerCallback.register("style_vae")
@TrainerCallback.register("generator")
class GeneratorCallback(ImageCallback):
    def __init__(self, num_keep: int = 25, num_interpolations: int = 16):
        super().__init__(num_keep)
        self.num_interpolations = num_interpolations

    def log_artifacts(self, trainer: Trainer) -> None:
        if not self.is_rank_0:
            return None
        batch = next(iter(trainer.validation_loader))
        batch = to_device(batch, trainer.device)
        original = batch[INPUT_KEY]
        model = trainer.model
        if not isinstance(model, GeneratorMixin):
            msg = "`GeneratorCallback` is only compatible with `GeneratorMixin`"
            raise ValueError(msg)
        is_conditional = model.is_conditional
        labels = None if not is_conditional else batch[LABEL_KEY]
        image_folder = self._prepare_folder(trainer)
        # original
        save_images(original, os.path.join(image_folder, "original.png"))
        # reconstruct
        if model.can_reconstruct:
            with eval_context(model):
                reconstructed = model.reconstruct(original, labels=labels)
            save_images(reconstructed, os.path.join(image_folder, "reconstructed.png"))
        # sample
        with eval_context(model):
            sampled = model.sample(len(original))
        save_images(sampled, os.path.join(image_folder, "sampled.png"))
        # interpolation
        with eval_context(model):
            interpolations = model.interpolate(self.num_interpolations)
        save_images(interpolations, os.path.join(image_folder, "interpolations.png"))
        # conditional sampling
        if model.num_classes is None:
            return None
        cond_folder = os.path.join(image_folder, "conditional")
        os.makedirs(cond_folder, exist_ok=True)
        with eval_context(model):
            for i in range(model.num_classes):
                sampled = model.sample(len(original), class_idx=i)
                interpolations = model.interpolate(len(original), class_idx=i)
                save_images(sampled, os.path.join(cond_folder, f"sampled_{i}.png"))
                path = os.path.join(cond_folder, f"interpolations_{i}.png")
                save_images(interpolations, path)


@TrainerCallback.register("siren_gan")
@TrainerCallback.register("siren_vae")
@TrainerCallback.register("sized_generator")
class SizedGeneratorCallback(GeneratorCallback):
    def log_artifacts(self, trainer: Trainer) -> None:
        if not self.is_rank_0:
            return None
        super().log_artifacts(trainer)
        model = trainer.model
        image_folder = self._prepare_folder(trainer, check_num_keep=False)
        sample_method = getattr(model, "sample", None)
        if sample_method is None:
            raise ValueError(
                "`sample` should be implemented when `SizedGeneratorCallback` is used "
                "(and the `sample` method should support accepting `size` kwarg)"
            )
        resolution = getattr(model, "img_size", 32)
        with eval_context(model):
            for i in range(1, 4):
                size = resolution * 2**i
                batch_size = 1 if size > 256 else 4
                sampled = sample_method(batch_size, size=size).cpu()
                path = os.path.join(image_folder, f"sampled_{size}x{size}.png")
                save_images(sampled, path)


@ImageCallback.register("unet")
@ImageCallback.register("u2net")
@ImageCallback.register("cascade_u2net")
class AlphaSegmentationCallback(ImageCallback):
    def log_artifacts(self, trainer: Trainer) -> None:
        if not self.is_rank_0:
            return None
        batch = next(iter(trainer.validation_loader))
        batch = to_device(batch, trainer.device)
        with eval_context(trainer.model):
            results = trainer.model(0, batch)
        original = batch[INPUT_KEY]
        label = batch[LABEL_KEY].float()
        logits = results[PREDICTIONS_KEY]
        if isinstance(logits, list):
            logits = logits[0]
        if logits.shape[1] != 1:
            logits = logits[:, [-1]]
        seg_map = torch.sigmoid(logits)
        if min_max_normalize is not None:
            seg_map = min_max_normalize(seg_map)
        sharp_map = (seg_map > 0.5).to(torch.float32)
        image_folder = self._prepare_folder(trainer)
        save_images(original, os.path.join(image_folder, "original.png"))
        save_images(label, os.path.join(image_folder, "label.png"))
        save_images(seg_map, os.path.join(image_folder, "mask.png"))
        save_images(sharp_map, os.path.join(image_folder, "mask_sharp.png"))
        lv1_alpha = results.get(LV1_ALPHA_KEY)
        if lv1_alpha is not None:
            save_images(lv1_alpha, os.path.join(image_folder, "lv1_mask.png"))
        np_original = to_numpy(original)
        if min_max_normalize is not None:
            np_original = min_max_normalize(np_original)
        np_label, np_mask, np_sharp = map(to_numpy, [label, seg_map, sharp_map])
        rgba = np.concatenate([np_original, np_label], axis=1)
        rgba_pred = np.concatenate([np_original, np_mask], axis=1)
        rgba_sharp = np.concatenate([np_original, np_sharp], axis=1)
        save_images(to_torch(rgba), os.path.join(image_folder, "rgba.png"))
        save_images(to_torch(rgba_pred), os.path.join(image_folder, "rgba_pred.png"))
        save_images(to_torch(rgba_sharp), os.path.join(image_folder, "rgba_sharp.png"))


@TrainerCallback.register("adain")
@TrainerCallback.register("style_transfer")
class StyleTransferCallback(ImageCallback):
    def log_artifacts(self, trainer: Trainer) -> None:
        if not self.is_rank_0:
            return None
        batch = next(iter(trainer.validation_loader))
        batch = to_device(batch, trainer.device)
        content = batch[INPUT_KEY]
        style = batch[STYLE_KEY]
        model = trainer.model
        image_folder = self._prepare_folder(trainer)
        # inputs
        save_images(content, os.path.join(image_folder, "original.png"))
        save_images(style, os.path.join(image_folder, "styles.png"))
        # stylize
        with eval_context(model):
            stylized = model.stylize(content, style)
        save_images(stylized, os.path.join(image_folder, "stylized.png"))


__all__ = [
    "GeneratorCallback",
    "SizedGeneratorCallback",
    "AlphaSegmentationCallback",
    "StyleTransferCallback",
]
