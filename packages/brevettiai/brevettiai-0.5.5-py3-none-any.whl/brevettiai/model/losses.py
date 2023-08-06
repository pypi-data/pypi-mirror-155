import numpy as np
import tensorflow as tf
from tensorflow.python.keras.losses import LossFunctionWrapper
from tensorflow.python.keras.utils import losses_utils
from pydantic import BaseModel
from typing import List, Union
from typing_extensions import Literal
from pydantic import Field


def weighted_loss(y_true, y_pred, baseloss, sample_weights, sample_weights_bias, output_weights, zero_channels_weighted=True, **kwargs):
    baseloss_fn = tf.keras.losses.get(baseloss)
    loss = baseloss_fn(y_true[..., None], y_pred[..., None], **kwargs)

    if sample_weights is not None:
        ww = tf.tensordot(y_true, tf.cast(sample_weights, y_true.dtype), axes=[-1, 0]) + tf.cast(sample_weights_bias,
                                                                                                y_true.dtype)
        ww = tf.clip_by_value(ww, 0, np.inf)
        loss = loss * ww

    if not tf.reduce_all(zero_channels_weighted):
        nonzero_channels = tf.reduce_any(y_true != 0, tf.range(1, tf.rank(y_true) - 1), keepdims=True)

        if not isinstance(zero_channels_weighted, bool):
            # make broadcastable
            reshaper = tf.cast(tf.pad(tf.ones(tf.rank(y_true)-1), [[0, 1]], constant_values=-1), tf.int32)
            zero_channels_weighted = tf.reshape(tf.constant(zero_channels_weighted), reshaper)

        weight = nonzero_channels | zero_channels_weighted
        loss = loss * tf.cast(weight, loss.dtype)

    if output_weights is not None:
        loss = tf.tensordot(loss, tf.cast(output_weights, loss.dtype), axes=1)

    return loss


class WeightedLoss(LossFunctionWrapper):
    def __init__(self, **kwargs):
        super().__init__(weighted_loss, **kwargs)

    @property
    def fn_kwargs(self):
        return self._fn_kwargs


class WeightedLossFactory(BaseModel):
    sample_weights: List[List[float]] = Field(default=None)
    sample_weights_bias: List[float] = Field(default=None)
    output_weights: List[float] = Field(default=None)
    zero_channels_weighted: Union[bool, List[bool]] = Field(default=True)
    label_smoothing: float = 0.0
    baseloss: str = "binary_crossentropy"

    def get_loss(self, from_logits: bool = False,
                 reduction: Literal['AUTO', 'NONE', 'SUM', 'SUM_OVER_BATCH_SIZE'] = "AUTO",
                 name: str = 'weighted_loss'):

        return WeightedLoss(
            name=name,
            reduction=getattr(losses_utils.ReductionV2, reduction),
            from_logits=from_logits,
            **self.dict())
