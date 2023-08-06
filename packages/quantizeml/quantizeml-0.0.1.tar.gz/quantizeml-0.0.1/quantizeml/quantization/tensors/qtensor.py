from copy import copy
import tensorflow as tf

def round_through(x):
    """Element-wise rounding to the closest integer with full gradient propagation.
    A trick from [Sergey Ioffe](http://stackoverflow.com/a/36480182).

    """
    rounded = tf.math.round(x)
    return x + tf.stop_gradient(rounded - x)


def floor_through(x):
    floored = tf.math.floor(x)
    return x + tf.stop_gradient(floored - x)


def ceil_through(x):
    ceiled = tf.math.ceil(x)
    return x + tf.stop_gradient(ceiled - x)


class QTensor(tf.experimental.ExtensionType):
    """Abstract class to exchange quantized tensors between layers

    The QTensor values are actually stored as integer, but it provides a
    conversion method to project these values into a float representation.

    The value_bits parameter sets the maximum integer values that can be stored:
        int_max = 2^bits - 1.

    When a QTensor is created, its values are clipped to [-int_max, int_max].
    """
    values: tf.Tensor = 1.0
    value_bits: int = 7
    shape: tf.TensorShape  # Required to convert to a KerasTensor

    def to_float(self):
        """Returns a float representation of the QTensor

        Returns:
            :obj:`tensorflow.Tensor`: the float representation.
        """
        raise NotImplementedError

    def clone(self):
        """Returns a copy of the QTensor

        Returns:
            :obj:`QTensor`: the copy.
        """
        return copy(self)

    def __str__(self):
        x_float = self.to_float()
        return f"QTensor: {x_float}"

    @staticmethod
    def int_max(value_bits):
        return 2 ** value_bits - 1

    @staticmethod
    def clamp(values, value_bits):
        int_max = QTensor.int_max(value_bits)
        return tf.clip_by_value(values, -int_max, int_max)
