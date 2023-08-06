import os
import sys
import json
import math
import torch
import argparse
import torchvision
import urllib.request

import numpy as np
import torch.nn as nn
import torch.nn.functional as F

from PIL import Image
from PIL import ImageDraw
from torch import Tensor
from typing import Any
from typing import Set
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Optional
from typing import NamedTuple
from typing import ContextManager
from zipfile import ZipFile
from collections import defaultdict
from collections import OrderedDict
from torch.optim import Optimizer
from cftool.misc import prod
from cftool.misc import check_requires
from cftool.misc import shallow_copy_dict
from cftool.misc import context_error_handler
from cftool.misc import DownloadProgressBar
from cftool.array import arr_type
from cftool.array import to_standard

from ..types import data_type
from ..types import param_type
from ..types import np_dict_type
from ..types import tensor_dict_type
from ..types import sample_weights_type
from ..constants import CACHE_DIR
from ..constants import INPUT_KEY
from ..constants import INFO_PREFIX
from ..constants import WARNING_PREFIX

try:
    import matplotlib.pyplot as plt
except:
    plt = None
try:
    from onnxruntime import InferenceSession
except:
    InferenceSession = None
try:
    from cfml.misc.toolkit import show_or_save
except:
    show_or_save = None


# general


def filter_kw(
    fn: Callable,
    kwargs: Dict[str, Any],
    strict: bool = True,
) -> Dict[str, Any]:
    kw = {}
    for k, v in kwargs.items():
        if check_requires(fn, k, strict):
            kw[k] = v
    return kw


def check_is_ci() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ci", type=int, default=0)
    args = parser.parse_args()
    return bool(args.ci)


def check_available(tag: str, repo: str, name: str) -> bool:
    with open(os.path.join(os.path.dirname(__file__), "available.json"), "r") as f:
        available = json.load(f)
    if repo != "pretrained-models":
        return True
    return name in available[tag]


def download(
    tag: str,
    repo: str,
    name: str,
    root: str,
    extension: str,
    force_download: bool,
    remove_zip: Optional[bool],
    extract_zip: bool,
) -> str:
    if not check_available(tag, repo, name):
        raise ValueError(f"'{name}' is currently not available at '{tag}'")
    prefix = f"https://github.com/carefree0910/{repo}/releases/download/{tag}/"
    os.makedirs(root, exist_ok=True)
    file = f"{name}.{extension}"
    path = os.path.join(root, file)
    is_zip = extension == "zip"
    zip_folder_path = os.path.join(root, name)
    exists = os.path.isdir(zip_folder_path) if is_zip else os.path.isfile(path)
    if exists and not force_download:
        return zip_folder_path if is_zip else path
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=name) as t:
        urllib.request.urlretrieve(
            f"{prefix}{file}",
            filename=path,
            reporthook=t.update_to,
        )
    if not is_zip:
        return path
    if extract_zip:
        with ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(zip_folder_path)
    if remove_zip is None:
        remove_zip = extract_zip
    if remove_zip:
        if extract_zip:
            os.remove(path)
        else:
            print(
                f"{WARNING_PREFIX}zip file is not extracted, "
                f"so we will not remove it!"
            )
    return zip_folder_path


def download_data_info(
    name: str,
    *,
    root: str = os.path.join(CACHE_DIR, "data_info"),
    force_download: bool = False,
) -> str:
    return download(
        "data_info",
        "pretrained-models",
        name,
        root,
        "json",
        force_download,
        None,
        False,
    )


def download_tokenizer(
    name: str,
    *,
    root: str = os.path.join(CACHE_DIR, "tokenizers"),
    force_download: bool = False,
) -> str:
    return download(
        "tokenizers",
        "pretrained-models",
        name,
        root,
        "pkl",
        force_download,
        None,
        False,
    )


def download_model(
    name: str,
    *,
    root: str = os.path.join(CACHE_DIR, "models"),
    force_download: bool = False,
) -> str:
    return download(
        "checkpoints",
        "pretrained-models",
        name,
        root,
        "pt",
        force_download,
        None,
        False,
    )


def download_reference(
    name: str,
    *,
    root: str = os.path.join(CACHE_DIR, "reference"),
    force_download: bool = False,
) -> str:
    return download(
        "reference",
        "pretrained-models",
        name,
        root,
        "pt",
        force_download,
        None,
        False,
    )


def download_dataset(
    name: str,
    *,
    root: str = os.getcwd(),
    force_download: bool = False,
    remove_zip: Optional[bool] = None,
    extract_zip: bool = True,
) -> str:
    return download(
        "latest",
        "datasets",
        name,
        root,
        "zip",
        force_download,
        remove_zip,
        extract_zip,
    )


def get_compatible_name(
    tag: str,
    repo: str,
    name: str,
    versions: List[Tuple[int, int]],
    *,
    bc: bool = False,
) -> str:
    version_info = sys.version_info
    version = None
    if bc:
        tgt_versions = list(
            filter(
                lambda ver: version_info.major < ver[0] or version_info.minor < ver[1],
                versions,
            )
        )
        if tgt_versions is not None:
            version = max(tgt_versions)
    if not bc:
        tgt_versions = list(
            filter(
                lambda ver: version_info.major > ver[0] or version_info.minor >= ver[1],
                versions,
            )
        )
        if tgt_versions is not None:
            version = max(tgt_versions)
    if version is not None:
        compatible_name = f"{name}_{version[0]}.{version[1]}"
        if check_available(tag, repo, compatible_name):
            name = compatible_name
        else:
            print(
                f"{WARNING_PREFIX}compatible name '{compatible_name}' is not available "
                f"on the server, will use the original name ({name}) instead"
            )
    return name


class WeightsStrategy:
    def __init__(self, strategy: Optional[str]):
        self.strategy = strategy

    def __call__(self, num_train: int, num_valid: int) -> sample_weights_type:
        if self.strategy is None:
            return None
        return getattr(self, self.strategy)(num_train, num_valid)

    def linear_decay(self, num_train: int, num_valid: int) -> sample_weights_type:
        return np.linspace(0, 1, num_train + 1)[1:]

    def radius_decay(self, num_train: int, num_valid: int) -> sample_weights_type:
        return np.sin(np.arccos(1.0 - np.linspace(0, 1, num_train + 1)[1:]))

    def log_decay(self, num_train: int, num_valid: int) -> sample_weights_type:
        return np.log(np.arange(num_train) + np.e)

    def sigmoid_decay(self, num_train: int, num_valid: int) -> sample_weights_type:
        x = np.linspace(-5.0, 5.0, num_train)
        return 1.0 / (1.0 + np.exp(-x))

    def visualize(self, export_path: str = "weights_strategy.png") -> None:
        if plt is None:
            raise ValueError(f"{WARNING_PREFIX}`matplotlib` is needed for `visualize`")
        if show_or_save is None:
            raise ValueError(f"{WARNING_PREFIX}`carefree-ml` is needed for `visualize`")
        n = 1000
        x = np.linspace(0, 1, n)
        y = self(n, 0)
        if isinstance(y, tuple):
            y = y[0]
        plt.figure()
        plt.plot(x, y)
        show_or_save(export_path)


# dl


def get_label_predictions(logits: np.ndarray, threshold: float) -> np.ndarray:
    # binary classification
    if logits.shape[-1] == 1:
        logit_threshold = math.log(threshold / (1.0 - threshold))
        return (logits > logit_threshold).astype(int)
    return logits.argmax(1)[..., None]


def get_full_logits(logits: np.ndarray) -> np.ndarray:
    # binary classification
    if logits.shape[-1] == 1:
        logits = np.concatenate([-logits, logits], axis=-1)
    return logits


def inject_debug(config: Dict[str, Any]) -> None:
    config["fixed_steps"] = 1
    config["valid_portion"] = 1.0e-4


def fix_denormal_states(
    states: tensor_dict_type,
    *,
    eps: float = 1.0e-32,
    verbose: bool = False,
) -> tensor_dict_type:
    new_states = shallow_copy_dict(states)
    num_total = num_denormal_total = 0
    for k, v in states.items():
        if not v.is_floating_point():
            continue
        num_total += v.numel()
        denormal = (v != 0) & (v.abs() < eps)
        num_denormal = denormal.sum().item()
        num_denormal_total += num_denormal
        if num_denormal > 0:
            new_states[k][denormal] = v.new_zeros(num_denormal)
    if verbose:
        print(f"{INFO_PREFIX}denormal ratio : {num_denormal_total / num_total:8.6f}")
    return new_states


def toggle_optimizer(m: nn.Module, optimizer: Optimizer) -> None:
    for param in m.parameters():
        param.requires_grad = False
    for group in optimizer.param_groups:
        for param in group["params"]:
            param.requires_grad = True


def to_torch(arr: np.ndarray) -> Tensor:
    return torch.from_numpy(to_standard(arr))


def to_numpy(tensor: Tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()


def to_device(
    batch: tensor_dict_type,
    device: torch.device,
    **kwargs: Any,
) -> tensor_dict_type:
    return {
        k: v.to(device, **kwargs)
        if isinstance(v, Tensor)
        else [vv.to(device, **kwargs) if isinstance(vv, Tensor) else vv for vv in v]
        if isinstance(v, list)
        else v
        for k, v in batch.items()
    }


def has_batch_norms(m: nn.Module) -> bool:
    bn_types = (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d, nn.SyncBatchNorm)
    for name, module in m.named_modules():
        if isinstance(module, bn_types):
            return True
    return False


def inject_parameters(
    src: nn.Module,
    tgt: nn.Module,
    *,
    strict: Optional[bool] = None,
    src_filter_fn: Optional[Callable[[str], bool]] = None,
    tgt_filter_fn: Optional[Callable[[str], bool]] = None,
    custom_mappings: Optional[Dict[str, str]] = None,
    states_callback: Optional[Callable[[tensor_dict_type], tensor_dict_type]] = None,
) -> None:
    if strict is None:
        strict = tgt_filter_fn is None
    src_states = src.state_dict()
    tgt_states = tgt.state_dict()
    if src_filter_fn is not None:
        pop_keys = [key for key in src_states if not src_filter_fn(key)]
        for key in pop_keys:
            src_states.pop(key)
    if tgt_filter_fn is not None:
        pop_keys = [key for key in tgt_states if not tgt_filter_fn(key)]
        for key in pop_keys:
            tgt_states.pop(key)
    if states_callback is not None:
        src_states = states_callback(shallow_copy_dict(src_states))
    if len(src_states) != len(tgt_states):
        raise ValueError(f"lengths of states are not identical between {src} and {tgt}")
    new_states = OrderedDict()
    if custom_mappings is not None:
        for src_k, tgt_k in custom_mappings.items():
            new_states[tgt_k] = src_states.pop(src_k)
            tgt_states.pop(tgt_k)
    for (src_k, src_v), (tgt_k, tgt_v) in zip(src_states.items(), tgt_states.items()):
        if src_v.shape != tgt_v.shape:
            raise ValueError(
                f"shape of {src_k} ({list(src_v.shape)}) is not identical with "
                f"shape of {tgt_k} ({list(tgt_v.shape)})"
            )
        new_states[tgt_k] = src_v
    tgt.load_state_dict(new_states, strict=strict)


class Diffs(NamedTuple):
    names1: List[str]
    names2: List[str]
    diffs: List[Tensor]


def sorted_param_diffs(m1: nn.Module, m2: nn.Module) -> Diffs:
    names1, params1 = list(zip(*m1.named_parameters()))
    names2, params2 = list(zip(*m2.named_parameters()))
    if len(params1) != len(params2):
        raise ValueError(f"lengths of params are not identical between {m1} and {m2}")
    diffs = []
    for p1, p2 in zip(params1, params2):
        (p1, _), (p2, _) = map(torch.sort, [p1.view(-1), p2.view(-1)])
        diffs.append(torch.abs(p1.data - p2.data))
    return Diffs(names1, names2, diffs)


def get_gradient(
    y: Tensor,
    x: Tensor,
    retain_graph: bool = False,
    create_graph: bool = False,
) -> Union[Tensor, Tuple[Tensor, ...]]:
    grads = torch.autograd.grad(y, x, torch.ones_like(y), retain_graph, create_graph)
    if len(grads) == 1:
        return grads[0]
    return grads


def set_requires_grad(module: nn.Module, requires_grad: bool = False) -> None:
    for param in module.parameters():
        param.requires_grad = requires_grad


def scheduler_requires_metric(scheduler: Any) -> bool:
    return check_requires(scheduler.step, "metrics")


# This is a modified version of https://github.com/sksq96/pytorch-summary
#  So it can summary `carefree-learn` model structures better
def summary(
    model: nn.Module,
    sample_batch: tensor_dict_type,
    *,
    return_only: bool = False,
) -> str:
    def _get_param_counts(module_: nn.Module) -> Tuple[int, int]:
        num_params = 0
        num_trainable_params = 0
        for param in module_.parameters():
            local_num_params = int(round(prod(param.data.shape)))
            num_params += local_num_params
            if param.requires_grad:
                num_trainable_params += local_num_params
        return num_params, num_trainable_params

    def register_hook(module: nn.Module) -> None:
        def hook(module_: nn.Module, inp: Any, output: Any) -> None:
            m_name = module_names.get(module_)
            if m_name is None:
                return

            inp = inp[0]
            if not isinstance(inp, Tensor):
                return
            if isinstance(output, (list, tuple)):
                for element in output:
                    if not isinstance(element, Tensor):
                        return
            elif not isinstance(output, Tensor):
                return

            m_dict: OrderedDict[str, Any] = OrderedDict()
            m_dict["input_shape"] = list(inp.size())
            if len(m_dict["input_shape"]) > 0:
                m_dict["input_shape"][0] = -1
            if isinstance(output, (list, tuple)):
                m_dict["output_shape"] = [[-1] + list(o.size())[1:] for o in output]
                m_dict["is_multiple_output"] = True
            else:
                m_dict["output_shape"] = list(output.size())
                if len(m_dict["output_shape"]) > 0:
                    m_dict["output_shape"][0] = -1
                m_dict["is_multiple_output"] = False

            num_params_, num_trainable_params_ = _get_param_counts(module_)
            m_dict["num_params"] = num_params_
            m_dict["num_trainable_params"] = num_trainable_params_
            raw_summary_dict[m_name] = m_dict

        if not isinstance(module, torch.jit.ScriptModule):
            hooks.append(module.register_forward_hook(hook))

    # get names
    def _inject_names(m: nn.Module, previous_names: List[str]) -> None:
        info_list = []
        for child in m.children():
            current_names = previous_names + [type(child).__name__]
            current_name = ".".join(current_names)
            module_names[child] = current_name
            info_list.append((child, current_name, current_names))
        counts: Dict[str, int] = defaultdict(int)
        idx_mapping: Dict[nn.Module, int] = {}
        for child, current_name, _ in info_list:
            idx_mapping[child] = counts[current_name]
            counts[current_name] += 1
        for child, current_name, current_names in info_list:
            if counts[current_name] == 1:
                continue
            current_name = f"{current_name}-{idx_mapping[child]}"
            module_names[child] = current_name
            current_names[-1] = current_name.split(".")[-1]
        for child, _, current_names in info_list:
            _inject_names(child, current_names)

    module_names: OrderedDict[nn.Module, str] = OrderedDict()
    existing_names: Set[str] = set()

    def _get_name(original: str) -> str:
        count = 0
        final_name = original
        while final_name in existing_names:
            count += 1
            final_name = f"{original}_{count}"
        existing_names.add(final_name)
        return final_name

    model_name = _get_name(type(model).__name__)
    module_names[model] = model_name
    _inject_names(model, [model_name])

    # create properties
    raw_summary_dict: OrderedDict[str, Any] = OrderedDict()
    hooks: List[Any] = []

    # register hook
    model.apply(register_hook)

    # make a forward pass
    with eval_context(model, use_grad=None):
        if not hasattr(model, "summary_forward"):
            model(0, sample_batch)
        else:
            model.summary_forward(0, sample_batch)  # type: ignore
        for param in model.parameters():
            param.grad = None

    # remove these hooks
    for h in hooks:
        h.remove()

    # get hierarchy
    hierarchy: OrderedDict[str, Any] = OrderedDict()
    for key in raw_summary_dict:
        split = key.split(".")
        d = hierarchy
        for elem in split[:-1]:
            d = d.setdefault(elem, OrderedDict())
        d.setdefault(split[-1], None)

    # reconstruct summary_dict
    def _inject_summary(current_hierarchy: Any, previous_keys: List[str]) -> None:
        if previous_keys and not previous_keys[-1]:
            previous_keys.pop()
        current_layer = len(previous_keys)
        current_count = hierarchy_counts.get(current_layer, 0)
        prefix = "  " * current_layer
        for k, v in current_hierarchy.items():
            current_keys = previous_keys + [k]
            concat_k = ".".join(current_keys)
            current_summary = raw_summary_dict.get(concat_k)
            summary_dict[f"{prefix}{k}-{current_count}"] = current_summary
            hierarchy_counts[current_layer] = current_count + 1
            if v is not None:
                _inject_summary(v, current_keys)

    hierarchy_counts: Dict[int, int] = {}
    summary_dict: OrderedDict[str, Any] = OrderedDict()
    _inject_summary(hierarchy, [])

    line_length = 120
    messages = ["=" * line_length]
    line_format = "{:30}  {:>20} {:>40} {:>20}"
    headers = "Layer (type)", "Input Shape", "Output Shape", "Trainable Param #"
    line_new = line_format.format(*headers)
    messages.append(line_new)
    messages.append("-" * line_length)
    total_output = 0
    for layer, layer_summary in summary_dict.items():
        layer_name = "-".join(layer.split("-")[:-1])
        if layer_summary is None:
            line_new = line_format.format(layer_name, "", "", "")
        else:
            line_new = line_format.format(
                layer_name,
                str(layer_summary["input_shape"]),
                str(layer_summary["output_shape"]),
                "{0:,}".format(layer_summary["num_trainable_params"]),
            )
            output_shape = layer_summary["output_shape"]
            is_multiple_output = layer_summary["is_multiple_output"]
            if not is_multiple_output:
                output_shape = [output_shape]
            for shape in output_shape:
                total_output += prod(shape)
        messages.append(line_new)

    total_params, trainable_params = _get_param_counts(model)
    # assume 4 bytes/number (float on cuda).
    x_batch = sample_batch[INPUT_KEY]
    get_size = lambda t: abs(prod(t.shape[1:]) * 4.0 / (1024**2.0))
    if not isinstance(x_batch, list):
        x_batch = [x_batch]
    total_input_size = sum(map(get_size, x_batch))
    # x2 for gradients
    total_output_size = abs(2.0 * total_output * 4.0 / (1024**2.0))
    total_params_size = abs(total_params * 4.0 / (1024**2.0))
    total_size = total_params_size + total_output_size + total_input_size

    non_trainable_params = total_params - trainable_params
    messages.append("=" * line_length)
    messages.append("Total params: {0:,}".format(total_params))
    messages.append("Trainable params: {0:,}".format(trainable_params))
    messages.append("Non-trainable params: {0:,}".format(non_trainable_params))
    messages.append("-" * line_length)
    messages.append("Input size (MB): %0.2f" % total_input_size)
    messages.append("Forward/backward pass size (MB): %0.2f" % total_output_size)
    messages.append("Params size (MB): %0.2f" % total_params_size)
    messages.append("Estimated Total Size (MB): %0.2f" % total_size)
    messages.append("-" * line_length)
    msg = "\n".join(messages)
    if not return_only:
        print(msg)
    return msg


class DDPInfo(NamedTuple):
    rank: int
    world_size: int
    local_rank: int


def get_ddp_info() -> Optional[DDPInfo]:
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        local_rank = int(os.environ["LOCAL_RANK"])
        return DDPInfo(rank, world_size, local_rank)
    return None


def get_world_size() -> int:
    ddp_info = get_ddp_info()
    return 1 if ddp_info is None else ddp_info.world_size


class mode_context(context_error_handler):
    """
    Help entering specific mode and recovering previous mode

    This is a context controller for entering specific mode at the beginning
    and back to previous mode at the end.

    Parameters
    ----------
    module : nn.Module, arbitrary PyTorch module.

    Examples
    --------
    >>> module = nn.Module()
    >>> with mode_context(module):
    >>>     pass  # do something

    """

    def __init__(
        self,
        module: nn.Module,
        *,
        to_train: Optional[bool],
        use_grad: Optional[bool],
        use_inference: Optional[bool] = None,
    ):
        self._to_train = to_train
        self._module, self._training = module, module.training
        self._cache = {p: p.requires_grad for p in module.parameters()}
        if use_grad is not None:
            for p in module.parameters():
                p.requires_grad_(use_grad)
        if use_grad is None:
            self._grad_context: Optional[ContextManager] = None
        else:
            self._grad_context = torch.enable_grad() if use_grad else torch.no_grad()
        if use_inference is None:
            self._inference_context: Optional[ContextManager] = None
        else:
            self._inference_context = torch.inference_mode(use_inference)

    def __enter__(self) -> None:
        if self._to_train is not None:
            self._module.train(mode=self._to_train)
        if self._grad_context is not None:
            self._grad_context.__enter__()
        if self._inference_context is not None:
            self._inference_context.__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._to_train is not None:
            self._module.train(mode=self._training)
        if self._inference_context is not None:
            self._inference_context.__exit__(exc_type, exc_val, exc_tb)
        if self._grad_context is not None:
            self._grad_context.__exit__(exc_type, exc_val, exc_tb)
        for p, v in self._cache.items():
            p.requires_grad_(v)


class train_context(mode_context):
    """
    Useful when we need to get gradients with our PyTorch model during evaluating.
    """

    def __init__(self, module: nn.Module, *, use_grad: bool = True):
        super().__init__(module, to_train=True, use_grad=use_grad, use_inference=False)


class eval_context(mode_context):
    """
    Useful when we need to predict something with our PyTorch model during training.
    """

    def __init__(
        self,
        module: nn.Module,
        *,
        use_grad: Optional[bool] = False,
        use_inference: Optional[bool] = None,
    ):
        if use_inference is None and use_grad is not None:
            use_inference = not use_grad
        super().__init__(
            module,
            to_train=False,
            use_grad=use_grad,
            use_inference=use_inference,
        )


class Initializer:
    """
    Initializer for neural network weights

    Examples
    --------
    >>> initializer = Initializer()
    >>> linear = nn.Linear(10, 10)
    >>> initializer.xavier_uniform(linear.weight)

    """

    defined_initialization = {
        "xavier_uniform",
        "xavier_normal",
        "normal",
        "truncated_normal",
    }
    custom_initializer: Dict[str, Callable] = {}

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._verbose_level = self.config.setdefault("verbose_level", 2)

    def initialize(self, param: param_type, method: str) -> Any:
        custom_initializer = self.custom_initializer.get(method)
        if custom_initializer is None:
            return getattr(self, method)(param)
        return custom_initializer(self, param)

    @classmethod
    def add_initializer(cls, f: Callable, name: str) -> None:
        if name in cls.defined_initialization:
            print(f"{WARNING_PREFIX}'{name}' initializer is already defined")
            return
        cls.defined_initialization.add(name)
        cls.custom_initializer[name] = f

    def xavier_uniform(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.xavier_uniform_(param.data, gain)

    def xavier_normal(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.xavier_normal_(param.data, gain)

    def normal(self, param: param_type) -> None:
        mean = self.config.setdefault("mean", 0.0)
        std = self.config.setdefault("std", 1.0)
        with torch.no_grad():
            param.data.normal_(mean, std)

    def truncated_normal(self, param: param_type) -> None:
        span = self.config.setdefault("span", 2.0)
        mean = self.config.setdefault("mean", 0.0)
        std = self.config.setdefault("std", 1.0)
        tol = self.config.setdefault("tol", 0.0)
        epoch = self.config.setdefault("epoch", 20)
        num_elem = param.numel()
        weight_base = param.new_empty(num_elem).normal_()
        get_invalid = lambda w: (w > span) | (w < -span)
        invalid = get_invalid(weight_base)
        success = False
        for _ in range(epoch):
            num_invalid = invalid.sum().item()
            if num_invalid / num_elem <= tol:
                success = True
                break
            with torch.no_grad():
                weight_base[invalid] = param.new_empty(num_invalid).normal_()
                invalid = get_invalid(weight_base)
        if not success:
            print(
                f"{WARNING_PREFIX}invalid ratio for truncated normal : "
                f"{invalid.to(torch.float32).mean():8.6f}, it might cause by "
                f"too little epoch ({epoch}) or too small tolerance ({tol})",
            )
        with torch.no_grad():
            param.data.copy_(weight_base.reshape(param.shape))
            param.data.mul_(std).add_(mean)

    def orthogonal(self, param: param_type) -> None:
        gain = self.config.setdefault("gain", 1.0)
        nn.init.orthogonal_(param.data, gain)


class DropNoGradStatesMixin:
    def state_dict(
        self,
        *,
        destination: Any = None,
        prefix: str = "",
        keep_vars: bool = False,
    ) -> tensor_dict_type:
        states = super().state_dict(destination=destination, prefix=prefix, keep_vars=keep_vars)  # type: ignore
        for key, _ in self.named_buffers():  # type: ignore
            states.pop(key)
        for key, value in self.named_parameters():  # type: ignore
            if not value.requires_grad:
                states.pop(key)
        return states

    def load_state_dict(
        self,
        state_dict: tensor_dict_type,
        strict: bool = True,
    ) -> None:
        with torch.no_grad():
            for key, value in self.named_parameters():  # type: ignore
                if value.requires_grad:
                    loaded_value = state_dict.get(key)
                    if strict and loaded_value is None:
                        raise ValueError(f"value for '{key}' is missing")
                    value.data.copy_(loaded_value)


class ONNX:
    def __init__(self, onnx_path: str):
        if InferenceSession is None:
            msg = "`ONNX` is not available when `onnxruntime` is not installed"
            raise ValueError(msg)
        self.ort_session = InferenceSession(onnx_path)
        self.output_names = [node.name for node in self.ort_session.get_outputs()]

    def predict(self, new_inputs: np_dict_type) -> np_dict_type:
        if self.ort_session is None:
            raise ValueError("`onnx_path` is not provided")
        ort_inputs = {
            node.name: to_standard(new_inputs[node.name])
            for node in self.ort_session.get_inputs()
        }
        return dict(zip(self.output_names, self.ort_session.run(None, ort_inputs)))


# ml


def to_2d(arr: data_type) -> data_type:
    if arr is None or isinstance(arr, str):
        return None
    if isinstance(arr, np.ndarray):
        return arr.reshape([len(arr), -1])
    if isinstance(arr[0], list):
        return arr
    return [[elem] for elem in arr]  # type: ignore


# cv


def auto_num_layers(
    img_size: int,
    min_size: int = 4,
    target_layers: Optional[int] = 4,
    *,
    use_stride: bool = False,
) -> int:
    fn = math.ceil if use_stride else math.floor
    max_layers = fn(math.log2(img_size / min_size))
    if target_layers is None:
        return max_layers
    return max(2, min(target_layers, max_layers))


def slerp(
    x1: torch.Tensor,
    x2: torch.Tensor,
    r1: Union[float, torch.Tensor],
    r2: Optional[Union[float, torch.Tensor]] = None,
) -> torch.Tensor:
    low_norm = x1 / torch.norm(x1, dim=1, keepdim=True)
    high_norm = x2 / torch.norm(x2, dim=1, keepdim=True)
    omega = torch.acos((low_norm * high_norm).sum(1))
    so = torch.sin(omega)
    if r2 is None:
        r2 = 1.0 - r1
    x1_part = (torch.sin(r1 * omega) / so).unsqueeze(1) * x1
    x2_part = (torch.sin(r2 * omega) / so).unsqueeze(1) * x2
    return x1_part + x2_part


def interpolate(
    src: Tensor,
    *,
    mode: str = "nearest",
    factor: Optional[Union[float, Tuple[float, float]]] = None,
    size: Optional[Union[int, Tuple[int, int]]] = None,
    anchor: Optional[Tensor] = None,
    determinate: bool = False,
    **kwargs: Any,
) -> Tensor:
    if "linear" in mode or mode == "bicubic":
        kwargs.setdefault("align_corners", False)
    c, h, w = src.shape[1:]
    if determinate:
        c, h, w = map(int, [c, h, w])
    if factor is not None:
        template = "`{}` will take no affect because `factor` is provided"
        if size is not None:
            print(f"{WARNING_PREFIX}{template.format('size')}")
        if anchor is not None:
            print(f"{WARNING_PREFIX}{template.format('anchor')}")
        if factor == 1.0 or factor == (1.0, 1.0):
            return src
        if not determinate:
            return F.interpolate(
                src,
                mode=mode,
                scale_factor=factor,
                recompute_scale_factor=True,
                **kwargs,
            )
        if not isinstance(factor, tuple):
            factor = factor, factor
        size = tuple(map(int, map(round, [h * factor[0], w * factor[1]])))  # type: ignore
    if size is None:
        if anchor is None:
            raise ValueError("either `size` or `anchor` should be provided")
        size = anchor.shape[2:]
        if determinate:
            size = tuple(map(int, size))  # type: ignore
    if not isinstance(size, tuple):
        size = size, size
    if h == size[0] and w == size[1]:
        return src
    net = F.interpolate(src, size=size, mode=mode, **kwargs)
    if not determinate:
        return net
    return net.view(-1, c, *size)


def mean_std(
    latent_map: Tensor,
    eps: float = 1.0e-5,
    *,
    determinate: bool = False,
) -> Tuple[Tensor, Tensor]:
    c, h, w = latent_map.shape[1:]
    if determinate:
        c, h, w = map(int, [c, h, w])
    spatial_dim = h * w
    latent_var = latent_map.view(-1, c, spatial_dim).var(dim=2) + eps
    latent_std = latent_var.sqrt().view(-1, c, 1, 1)
    latent_mean = latent_map.view(-1, c, spatial_dim).mean(dim=2).view(-1, c, 1, 1)
    return latent_mean, latent_std


def adain_with_params(
    src: Tensor,
    mean: Tensor,
    std: Tensor,
    *,
    determinate: bool = False,
) -> Tensor:
    src_mean, src_std = mean_std(src, determinate=determinate)
    src_normalized = (src - src_mean) / src_std
    return src_normalized * std + mean


def adain_with_tensor(src: Tensor, tgt: Tensor, *, determinate: bool = False) -> Tensor:
    tgt_mean, tgt_std = mean_std(tgt, determinate=determinate)
    return adain_with_params(src, tgt_mean, tgt_std, determinate=determinate)


def make_grid(arr: arr_type, n_row: Optional[int] = None) -> Tensor:
    if isinstance(arr, np.ndarray):
        arr = to_torch(arr)
    if n_row is None:
        n_row = math.ceil(math.sqrt(len(arr)))
    return torchvision.utils.make_grid(arr, n_row)


def save_images(arr: arr_type, path: str, n_row: Optional[int] = None) -> None:
    if isinstance(arr, np.ndarray):
        arr = to_torch(arr)
    if n_row is None:
        n_row = math.ceil(math.sqrt(len(arr)))
    torchvision.utils.save_image(arr, path, normalize=True, nrow=n_row)


def make_indices_visualization_map(indices: Tensor) -> Tensor:
    images = []
    for idx in indices.view(-1).tolist():
        img = Image.new("RGB", (28, 28), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        draw.text((12, 9), str(idx), (0, 0, 0))
        images.append(to_torch(np.array(img).transpose([2, 0, 1])))
    return torch.stack(images).float()
