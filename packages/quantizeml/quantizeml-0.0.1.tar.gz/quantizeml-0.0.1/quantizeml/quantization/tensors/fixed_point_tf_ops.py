import tensorflow as tf

from .qtensor import QTensor, floor_through
from .fixed_point import FixedPoint
from .qfloat import QFloat


@tf.experimental.dispatch_for_binary_elementwise_apis(FixedPoint, tf.Tensor)
def fp_tensor_binary_elementwise_api_handler(api_func, x, y):
    return api_func(x.to_float(), y)


@tf.experimental.dispatch_for_binary_elementwise_apis(tf.Tensor, FixedPoint)
def tensor_fp_binary_elementwise_api_handler(api_func, x, y):
    return api_func(x, y.to_float())


@tf.experimental.dispatch_for_api(tf.add)
def fp_add(x: FixedPoint, y: FixedPoint):
    return x + y


@tf.experimental.dispatch_for_api(tf.clip_by_value)
def fp_clip_by_value(t: FixedPoint, clip_value_min, clip_value_max, name=None):
    """Clips tensor values to a specified min and max.

    Args:
        t (:obj:`FixedPoint`): the FixedPoint to be clipped.
        clip_value_min (:obj:`FixedPoint`, int): the minimum value.
        clip_value_max (:obj:`FixedPoint`, int): the maximum value.
        name (str): an optional name for the Tensorflow ops
    Returns:
        :obj:`FixedPoint`: the clipped FixedPoint.
    """
    if isinstance(clip_value_min, int):
        clip_value_min = FixedPoint(clip_value_min)
    if isinstance(clip_value_max, int):
        clip_value_max = FixedPoint(clip_value_max)
    if not isinstance(clip_value_min, FixedPoint) or not isinstance(clip_value_max, FixedPoint):
        raise TypeError("Min/max values must be integer or FixedPoint")
    # Adjust the clip min/max values fractional bits
    s_min_values = FixedPoint._lshift(
        clip_value_min.values, (t.frac_bits - clip_value_min.frac_bits))
    s_max_values = FixedPoint._lshift(
        clip_value_max.values, (t.frac_bits - clip_value_max.frac_bits))
    clip_values = tf.clip_by_value(t.values, s_min_values, s_max_values, name)
    return FixedPoint(clip_values, t.frac_bits, t.value_bits)


@tf.experimental.dispatch_for_api(tf.math.reduce_sum)
def fp_reduce_sum(input_tensor: FixedPoint, axis=None, keepdims=False, name=None):
    """Computes the sum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be summed.
        axis (list): the dimensions to reduce. If None (the default), reduces all
        dimensions.
        keepdims (bool): If true, retains reduced dimensions with length 1.
        name (str): an optional name for the Tensorflow ops
    Returns:
        :obj:`FixedPoint`: the summed FixedPoint.
    """
    # The sum fractional bits is the max of all terms
    s_frac_bits = tf.math.reduce_max(input_tensor.frac_bits)
    # Align all terms on the same fractional bits
    input_values = FixedPoint._lshift(
        input_tensor.values, s_frac_bits - input_tensor.frac_bits)
    # Reduce sum
    s_values = tf.math.reduce_sum(
        input_values, axis, keepdims=keepdims, name=name)
    # Return a new FixedPoint
    return FixedPoint(s_values, s_frac_bits, input_tensor.value_bits)


@tf.experimental.dispatch_for_api(tf.linalg.matmul)
def fp_matmul(a: FixedPoint,
              b: QTensor,
              transpose_a=False,
              transpose_b=False,
              adjoint_a=False,
              adjoint_b=False,
              a_is_sparse=False,
              b_is_sparse=False,
              output_type=None,
              name=None):
    """Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

    A `tf.Tensor` of the same type as `a` and `b` where each inner-most matrix
    is the product of the corresponding matrices in `a` and `b`, e.g. if all
    transpose or adjoint attributes are `False`:
    `output[..., i, j] = sum_k (a[..., i, k] * b[..., k, j])`,
    for all indices `i`, `j`.
    Note: This is matrix product, not element-wise product.


    Args:
        a (:obj:`FixedPoint`): a FixedPoint of rank > 1.
        b (:obj:`FixedPoint`): a FixedPoint with same rank as `a`.
        transpose_a (bool): If `True`, `a` is transposed before multiplication.
        transpose_b (bool): If `True`, `b` is transposed before multiplication.
        adjoint_a (bool): If `True`, `a` is conjugated and transposed before
        multiplication.
        adjoint_b (bool): If `True`, `b` is conjugated and transposed before
        multiplication.
        a_is_sparse (bool): must be False, argument kept for compatibility with
        original tf.matmul.
        b_is_sparse (bool): must be False, argument kept for compatibility with
        original tf.matmul.
        output_type (NoneType): must be None, argument kept for compatibility
        with original tf.matmul.
        name (str): Name for the operation (optional).
    Returns:
        :obj:`FixedPoint`: the multiplied FixedPoint.
    """
    if a_is_sparse:
        raise TypeError(
            f"unsupported argument: a_is_sparse, provided {a_is_sparse}")
    if b_is_sparse:
        raise TypeError(
            f"unsupported argument: b_is_sparse, provided {b_is_sparse}")
    if output_type is not None:
        raise TypeError(
            f"unsupported argument: output_type, provided {output_type}")

    # We don't support matmul between vectors
    tf.debugging.assert_rank_at_least(a.values, 2)
    tf.debugging.assert_rank_at_least(b.values, 2)

    # Evaluate the maximum number of fractional bits
    a_frac_bits = tf.reduce_max(a.frac_bits)

    if not transpose_a:
        # If a has multiple fractional bits, we must align the values along the
        # last dimension before the matmul collapses it
        a = tf.cond(tf.rank(a.frac_bits) > 0,
                    lambda : a << (a_frac_bits - a.frac_bits),
                    lambda : a)

    if isinstance(b, FixedPoint):
        if transpose_b:
            # Because of the transposition, the quantization dim of b will be
            # collapsed by matmul, so we might need to align values
            b_frac_bits = tf.reduce_max(b.frac_bits)
            b = tf.cond(tf.rank(b.frac_bits) > 0,
                        lambda : b << (b_frac_bits - b.frac_bits),
                        lambda : b)
        else:
            b_frac_bits = b.frac_bits
    else:
        b_frac_bits = b.scales.frac_bits
        if transpose_b:
            # We only support tranposed matmul if the QFloat is per-tensor
            tf.debugging.assert_rank(tf.rank(b.scales.values), 0)

    # Do matmul on values
    m_values = floor_through(
        tf.matmul(a.values, b.values, transpose_a, transpose_b, adjoint_a,
                  adjoint_b, name))
    if isinstance(b, QFloat):
        # Multiply by the scales
        m_values *= b.scales.values

    # The resulting fractional bits being the sum of a and b fractional bits, we
    # limit them to those of the first term by subtracting the other
    m_values = FixedPoint._rshift(m_values, b_frac_bits)
    # Return a new FixedPoint
    return FixedPoint(m_values, a_frac_bits, a.value_bits)


@tf.experimental.dispatch_for_api(tf.shape)
def fp_shape(input: FixedPoint, out_type=tf.dtypes.int32, name=None):
    return tf.shape(input.values, out_type, name)


@tf.experimental.dispatch_for_api(tf.reshape)
def fp_reshape(tensor: FixedPoint, shape, name=None):
    tf.assert_rank(tensor.frac_bits, tf.constant(0))
    output = tf.reshape(tensor.values, shape, name)
    return FixedPoint(output, tensor.frac_bits, tensor.value_bits)


@tf.experimental.dispatch_for_api(tf.transpose)
def fp_transpose(a: FixedPoint, perm=None, conjugate=False, name="transpose"):
    tf.assert_rank(a.frac_bits, tf.constant(0))
    output =  tf.transpose(a.values, perm, conjugate, name)
    return FixedPoint(output, a.frac_bits, a.value_bits)


@tf.experimental.dispatch_for_api(tf.math.reduce_max)
def fp_reduce_max(input_tensor: FixedPoint,
                  axis=None,
                  keepdims=False,
                  name=None):
    """Computes the maximum of elements across dimensions of a FixedPoint.

    Args:
        input_tensor (:obj:`FixedPoint`): the FixedPoint to be estimated.
        axis (list): the dimensions to reduce. If None (the default), reduces all
        dimensions.
        keepdims (bool): If true, retains reduced dimensions with length 1.
        name (str): an optional name for the Tensorflow ops
    Returns:
        :obj:`FixedPoint`: the maximum FixedPoint.
    """
    # The sum fractional bits is the max on each exis
    if len(input_tensor.frac_bits.shape) == 0:
        s_frac_bits = tf.math.reduce_max(input_tensor.frac_bits)
    else:
        s_frac_bits = tf.math.reduce_max(input_tensor.frac_bits,
                                         axis=axis,
                                         keepdims=keepdims)
    # Align all terms on the same fractional bits: in reality it will only
    # keep the bigger one
    input_values = FixedPoint._lshift(input_tensor.values,
                                      s_frac_bits - input_tensor.frac_bits)
    # Reduce max
    s_values = tf.math.reduce_max(input_values,
                                  axis,
                                  keepdims=keepdims,
                                  name=name)
    # Return a new FixedPoint
    return FixedPoint(s_values, s_frac_bits, input_tensor.value_bits)


@tf.experimental.dispatch_for_api(tf.math.maximum)
def fp_maximum(x: FixedPoint, y: FixedPoint, name=None):
    """Returns the max of x and y (i.e. x > y ? x : y) element-wise.

    Args:
        x (:obj:`FixedPoint`): a FixedPoint tensor.
        y (:obj:`FixedPoint`): a FixedPoint tensor.
        name (str): an optional name for the Tensorflow ops
    Returns:
        :obj:`FixedPoint`: s FixedPoint containing maximum values.
    """
    # Align all terms on the same fractional bits
    a_frac_bits, a_values, b_values = x._align_values(y)
    # Apply maximum
    max_values = tf.math.maximum(a_values, b_values, name=name)
    # Return a new FixedPoint
    return FixedPoint(max_values, a_frac_bits, x.value_bits)
