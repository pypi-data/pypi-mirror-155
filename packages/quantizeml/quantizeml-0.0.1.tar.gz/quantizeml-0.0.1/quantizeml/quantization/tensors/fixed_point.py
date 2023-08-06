import tensorflow as tf

from .qtensor import QTensor, floor_through


class FixedPoint(QTensor):
    """A Tensor of integer values representing fixed-point numbers

    Args:
        values (:obj:`tensorflow.Tensor`): a tensor of integer values
        frac_bits (:obj:`tensorflow.Tensor`): an integer tensor of fractional bits
        value_bits (int): the number of value bits
    """
    frac_bits: tf.Tensor = 0.

    def __init__(self, values, frac_bits=0, value_bits=32):
        # We store fractional bits in a float tensor to speed up calculations
        if isinstance(frac_bits, tf.Tensor):
            self.frac_bits = tf.cast(frac_bits, tf.float32)
        else:
            self.frac_bits = tf.convert_to_tensor(frac_bits, tf.float32)
        self.value_bits = value_bits
        # We store integer values in a float tensor to speed up calculations
        if isinstance(values, tf.Tensor):
            values = tf.cast(values, tf.float32)
        else:
            values = tf.convert_to_tensor(values, dtype=tf.float32)
        # Clamp to fixed-point boundaries
        self.values = QTensor.clamp(values, value_bits)
        self.shape = self.values.shape

    @staticmethod
    def quantize(x, frac_bits, value_bits):
        """Converts a float Tensor to a FixedPoint

        It converts the original float values into integer values so that:

        x_int = round(x * 2 ^ frac_bits)

        It then evaluates the maximum integer values that can be stored for
        the specified value bits: int_max = 2^bits - 1.

        The resulting integer values are clipped to [-int_max, int_max].

        Args:
            x (:obj:`tensorflow.Tensor`): a tensor of float values.
            frac_bits (:obj:`tensorflow.Tensor`): an integer tensor of fractional bits
            value_bits (int): the number of value bits
        Returns:
            a :obj:`FixedPoint`
        """
        # Project float into integer fixed-point space
        values = floor_through(x * FixedPoint._pow2(frac_bits))
        return FixedPoint(values, frac_bits, value_bits)

    @property
    def sign(self):
        """Returns the sign of the FixedPoint

        Returns:
            :obj:`FixedPoint`: the sign as a FixedPoint.
        """
        return FixedPoint(tf.math.sign(self.values), 0, self.value_bits)

    @staticmethod
    def _pow2(n):
        return tf.math.pow(2., tf.cast(n, tf.float32))

    def to_float(self):
        return self.values / FixedPoint._pow2(self.frac_bits)

    def promote(self, bits):
        """Increase the number of value bits

        Args:
            bits(int): the new number of value bits

        Returns:
            :obj:`FixedPoint`: a FixedPoint with increased value bits
        """
        if not isinstance(bits, int):
            raise TypeError("Bitwidth must be an integer")
        if bits < 0:
            raise ValueError("Invalid bitwidth")
        if bits < self.value_bits:
            raise ValueError(
                "Reducing the number of value bits is lossy: use a quantizer instead")
        return FixedPoint(self.values, self.frac_bits, bits)

    @staticmethod
    def _rshift(values, shift):
        return floor_through(values / FixedPoint._pow2(shift))

    @staticmethod
    def _lshift(values, shift):
        return values * FixedPoint._pow2(shift)

    def mul_pow_2(self, shift):
        """Multiply the FixedPoint by 2^shift.

        Note: shift should be a positive or negative integer.

        Args:
            shift (int): the power of 2 to multiply by

        Returns:
            :obj:`FixedPoint`: the result as a FixedPoint
        """
        values = floor_through(self._lshift(self.values, shift))
        return FixedPoint(values, self.frac_bits, self.value_bits)

    def __rshift__(self, shift):
        # Convert to a float32 tensor to be able to subtract shift from frac_bits
        shift = tf.convert_to_tensor(shift, tf.float32)
        # Decrease the fractional bits by shift
        s_frac_bits = tf.math.maximum(0.0, self.frac_bits - shift)
        # Divide by 2^shift to decrease precision
        s_values = FixedPoint._rshift(self.values, shift)
        # Return a new FixedPoint with updated fractional bits
        return FixedPoint(s_values, s_frac_bits, self.value_bits)

    def __lshift__(self, shift):
        # Convert to a float32 tensor to be able to add shift to frac_bits
        shift = tf.convert_to_tensor(shift, tf.float32)
        # Increase the fractional bits by shift
        s_frac_bits = self.frac_bits + shift
        # Multiply by 2^shift to increase precision
        s_values = FixedPoint._lshift(self.values, shift)
        # Return a new FixedPoint with updated fractional bits
        return FixedPoint(s_values, s_frac_bits, self.value_bits)

    def _align_values(self, other):
        # The sub fractional bits are the max of both terms
        frac_bits = tf.math.maximum(self.frac_bits, other.frac_bits)
        self_values = FixedPoint._lshift(
            self.values, (frac_bits - self.frac_bits))
        other_values = FixedPoint._lshift(
            other.values, (frac_bits - other.frac_bits))
        return frac_bits, self_values, other_values

    def __add__(self, other):
        if isinstance(other, int):
            # Convert integer into a 32-bit fixed-point with no fractional bits
            return self + FixedPoint(other)
        elif isinstance(other, FixedPoint):
            s_frac_bits, s_int, o_values = self._align_values(other)
            s_int += o_values
            # Return a new FixedPoint
            return FixedPoint(s_int, s_frac_bits, self.value_bits)
        raise TypeError(
            f"unsupported operand type(s) for +: 'FixedPoint' and '{type(other)}'")

    def __sub__(self, other):
        if isinstance(other, int):
            # Convert integer into a 32-bit fixed-point with no fractional bits
            return self - FixedPoint(other)
        elif isinstance(other, FixedPoint):
            s_frac_bits, s_int, o_values = self._align_values(other)
            s_int -= o_values
            # Return a new FixedPoint
            return FixedPoint(s_int, s_frac_bits, self.value_bits)
        raise TypeError(
            f"unsupported operand type(s) for -: 'FixedPoint' and '{type(other)}'")

    def __mul__(self, other):
        if isinstance(other, int):
            return self * FixedPoint(other)
        elif isinstance(other, FixedPoint):
            # The product between fixed-point is straight-forward
            p_values = self.values * other.values
            # The resulting fractional bits being the sum of both terms, we
            # limit them to those of the first term by subtracting the others
            p_values = FixedPoint._rshift(p_values, other.frac_bits)
            # Return a new FixedPoint
            return FixedPoint(p_values, self.frac_bits, self.value_bits)
        raise TypeError(
            f"unsupported operand type(s) for *: 'FixedPoint' and '{type(other)}'")

    def __pow__(self, power):
        if isinstance(power, int):
            if power == 0:
                return FixedPoint(tf.ones_like(self.values), 0, self.value_bits)
            elif power == 1:
                return FixedPoint(self.values, self.frac_bits, self.value_bits)
            elif power > 1:
                return self * self ** (power - 1)
            else:
                raise NotImplementedError(
                    "Negative powers are not implemented yet")
        raise TypeError(
            f"unsupported operand type(s) for **: 'FixedPoint' and '{type(power)}'")

    def __gt__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for >: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values > o_values

    def __ge__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for >=: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values >= o_values

    def __eq__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for ==: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values == o_values

    def __ne__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for !=: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values != o_values

    def __lt__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for <: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values <= o_values

    def __le__(self, other):
        if not isinstance(other, FixedPoint):
            raise TypeError(
                f"unsupported operand type(s) for <=: 'FixedPoint' and '{type(other)}'")
        _, s_values, o_values = self._align_values(other)
        return s_values <= o_values

    def abs(self):
        """Returns the absolute value of the QTensor

        Returns:
            :obj:`QTensor`: the absolute value.
        """
        return FixedPoint(tf.math.abs(self.values), self.frac_bits, self.value_bits)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self // FixedPoint(other)
        elif isinstance(other, FixedPoint):
            # Align the dividend fractional bits on the max of both terms
            max_frac_bits = tf.math.maximum(self.frac_bits, other.frac_bits)
            s_values = self._lshift(
                self.values, (max_frac_bits - self.frac_bits))
            # Divide
            d_values = floor_through(s_values / other.values)
            # The result fractional bits are reduced by the divisor
            d_frac_bits = max_frac_bits - other.frac_bits
            # Return a new FixedPoint
            return FixedPoint(d_values, d_frac_bits, self.value_bits)
        raise TypeError(
            f"unsupported operand type(s) for //: 'FixedPoint' and '{type(other)}'")
