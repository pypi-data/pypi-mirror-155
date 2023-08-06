import tensorflow as tf
import numpy as np
from typing import Union
from .qtensor import floor_through
from .fixed_point import FixedPoint
from .lookup import RegisterCustomHashTable

QTENSOR_T = Union[FixedPoint, tf.Tensor]

# frac bits and value bits for coefficients
COEF_FRAC_BITS = 5
COEF_VALUE_BITS = COEF_FRAC_BITS + 1
# coefficients are constants, so they can be quantized once
K_1_125 = FixedPoint.quantize(
    1.125, COEF_FRAC_BITS, COEF_VALUE_BITS)
K_0_3125 = FixedPoint.quantize(
    -0.3125, COEF_FRAC_BITS, COEF_VALUE_BITS)
K_1_59375 = FixedPoint.quantize(
    1.59375, COEF_FRAC_BITS, COEF_VALUE_BITS)
K_0_625 = FixedPoint.quantize(
    -0.625, COEF_FRAC_BITS, COEF_VALUE_BITS)


def _reciprocal_x_ge_1_5_values(x):
    # y' = 1.125 - 0.3125 * x
    x = x * K_0_3125
    x_reciprocal = x + K_1_125
    return x_reciprocal.values


def _reciprocal_x_lt_1_5_values(x):
    # y' = 1.59375 - 0.625 * x
    x = x * K_0_625
    x_reciprocal = x + K_1_59375
    return x_reciprocal.values


def _reciprocal_pwl(x, out_value_bits):
    x_values = x.values
    x_frac_bits = x.frac_bits
    # Determine required frac bits to keep only one int bit. Note that
    # this can be done in hardware by counting the number of leading zeros
    # in x_values.
    req_frac_bits = floor_through(tf.experimental.numpy.log2(x_values))

    # The PWL function works in the range [1, 2). To project x into that range,
    # we can consider that:
    #
    # x = x_values * 2^-x_frac_bits
    # x = x_values * 2^-x_frac_bits * 2^req_frac_bits * 2^-req_frac_bits
    #
    # We can then define y as follows:
    #
    # y = x_values * 2^-req_frac_bits
    #
    # So x can be re-written as:
    #
    # x = y * 2^req_frac_bits * 2^-x_frac_bits
    #
    # To get there:
    #
    # y = x * 2^x_frac_bits * 2^-req_frac_bits
    # y = (x_values * 2^-x_frac_bits) * 2^x_frac_bits * 2^-req_frac_bits
    # y = x_values * 2^-req_frac_bits
    #
    # This will guarantee that y is in the range [1, 2). We can further expand
    # this definition:
    #
    # y = x_values * 2^-req_frac_bits * 2^out_frac_bits * 2^-out_frac_bits
    # y = (x_values * 2^-req_frac_bits * 2^out_frac_bits) * 2^-out_frac_bits
    #
    # So if we define
    #
    # y_values = x_values * 2^-req_frac_bits * 2^out_frac_bits
    #
    # y = y_values * 2^-out_frac_bits
    #
    # And we obtain y as a FixedPoint in the desired range.

    # Promote x to use the same value bits as output
    x = x.promote(out_value_bits)
    # output int bits will only require 1 int bit, the rest is for
    # frac_bits
    out_frac_bits = out_value_bits - 1
    # To obtain y_values, we multiply x by 2^(-req_frac_bits + out_frac_bits)
    # and get the values
    y_values = x.mul_pow_2(-req_frac_bits + out_frac_bits).values
    # y_values will only require 1 int bit, the rest is for_frac_bits
    # It is now trivial to define y
    y = FixedPoint(y_values, out_frac_bits, out_value_bits)

    # The limit is to choose the PWL function is 1.5 (= 3 * 2^-1)
    limit_1_5 = FixedPoint.quantize(1.5, out_frac_bits, out_value_bits)
    cond_tensor = y >= limit_1_5
    # Estimate output values using one of the PWL functions
    reciprocal_y_values = tf.where(cond_tensor,
                                   _reciprocal_x_ge_1_5_values(y),
                                   _reciprocal_x_lt_1_5_values(y))
    reciprocal_y = FixedPoint(reciprocal_y_values, out_frac_bits,
                              out_value_bits)

    # Since we defined previously
    #
    # y = x * 2^x_frac_bits * 2^-req_frac_bits
    #
    # And
    #
    # x = y * 2^-x_frac_bits * 2^+req_frac_bits
    #
    # The reciprocal is:
    #
    # 1/x = 1/y * 2^-req_frac_bits * 2^+x_frac_bits
    # 1/x = 1/y * 2^(x_frac_bits - req_frac_bits)
    #
    # We use the mul_pow_2 method to keep the same frac_bits as 1/y.
    reciprocal_x = reciprocal_y.mul_pow_2(x_frac_bits - req_frac_bits)
    return reciprocal_x


def reciprocal(x: QTENSOR_T, out_value_bits: int = 32, name: str = None):
    """Piece-wise approximation of y = 1/x.

    The approximation works on values in the range [1, 2).
    To go into that range, we shift the input to put the leftmost bit (MSB) to
    1 and change the frac_bits so that there is only one int bit.
    Once that is done the approximation is as follows:

    y' = 1.59375 - 0.625 * x if x < 1.5
    y' = 1.125 - 0.3125 * x  if x >= 1.5

    Note that this can be performed in hardware this way:

    y' = 51 * 2^-5 - x * (2^-1 + 2^-3) if x < 1.5
    y' = 36 * 2^-5 - x * (2^-2 + 2^-4) if x >= 1.5

    Implementation inspired by:

    Cardarilli, G.C., Di Nunzio, L., Fazzolari, R. et al.
    A pseudo-softmax function for hardware-based high speed image classification.
    Sci Rep 11, 15307 (2021). https://doi.org/10.1038/s41598-021-94691-7

    Args:
        x (:obj:`FixedPoint` or :obj:`tf.Tensor`): The value to compute its reciprocal.
        out_value_bits (int, optional): The number of bits of the output. Defaults to 32.
        name (str, optional): The name of the operation. Defaults to None.

    Returns:
        :obj:`FixedPoint` or :obj:`tf.Tensor`: The reciprocal of x.
    """
    # Input is not FixedPoint: use unquantized float version
    if not isinstance(x, FixedPoint):
        return tf.math.reciprocal(x)
    if out_value_bits < COEF_VALUE_BITS:
        raise ValueError(f"out_value_bits must be >= {COEF_VALUE_BITS}")
    # Estimate reciprocal just with values
    return _reciprocal_pwl(x, out_value_bits)


def _get_static_hash_table(range_bitwidth: int, frac_bits: int):
    """Given an input range bitwitdh, register a static hash table which contains the reciprocal
    values between (-2**range_bitwidth) and (2**range_bitwidth - 1).

    Args:
        range_bitwidth (int): The bitwidth of the range of the table.
        frac_bits (int): The resolution of fractional bits.

    Returns:
        :obj:`tf.lookup.StaticHashTable`: The static hash table.
    """
    def _serialize_hash_table():
        # Given that StaticHashTable does not support Tensor, all the values are computed in
        # numpy directly.
        keys_tensor = np.array(range(1, 2**range_bitwidth), dtype=np.int32)
        vals_tensor = np.floor(1/keys_tensor * 2.0 ** frac_bits).astype(np.float32)
        return keys_tensor, vals_tensor, 0

    # Register the table if it does not exist as a global variable
    table_name = f'reciprocal_lut_{frac_bits}_{range_bitwidth}bits'
    with RegisterCustomHashTable(table_name, _serialize_hash_table) as register:
        table = register.get_table()
    return table


def reciprocal_lut(
        x: QTENSOR_T, frac_bits: int = None, out_value_bits: int = 32, name: str = None):
    """Compute the reciprocal of a FixedPoint value, using a lookup table.

    Args:
        x (:obj:`FixedPoint` or :obj:`tf.Tensor`): The value to compute its reciprocal.
        frac_bits (int, optional): The resolution of fractional bits. Defaults to None.
        out_value_bits (int, optional): The number of bits of the output. Defaults to 32.
        name (str, optional): The name of the operation. Defaults to None.

    Returns:
        :obj:`FixedPoint` or :obj:`tf.Tensor`: The reciprocal of x.
    """
    # Retrieves the reciprocal lookup table only if x is a FixedPoint
    if not isinstance(x, FixedPoint):
        return tf.math.reciprocal(x)

    # Retrieves the hash static table of x.value_bits
    frac_bits = frac_bits or x.frac_bits
    hash_table = _get_static_hash_table(x.value_bits, frac_bits)

    # Given that the input is a FixedPoint, it is guarantee the equivalence below:
    # float(1/x) = 1 / float(x) =  1/x.values * 2^x.frac_bits
    # Then, we can approximate the reciprocal of x to:
    # float(1/x) ~= reciprocal_lut(x.values) * 2^x.frac_bits
    # in two steps:
    # 1. Compute the reciprocal of x.values of absolute value
    x_inv = FixedPoint(hash_table(x.abs().values), frac_bits, out_value_bits)
    # 2. Scale by 2**x.frac_bits
    return x_inv * FixedPoint(FixedPoint._pow2(x.frac_bits)) * x.sign


@tf.experimental.dispatch_for_api(tf.math.reciprocal)
def fp_reciprocal(x: FixedPoint, name=None):
    """Returns the reciprocal of x element-wise, i.e. 1/x.

    The reciprocal is calculated with a piece_wise function and same value_bits
    as x.

    Args:
        x (:obj:`FixedPoint`): The value to compute its reciprocal.

    Returns:
        :obj:`FixedPoint`: the reciprocal of the input.
    """
    return reciprocal(x, x.value_bits, name)
