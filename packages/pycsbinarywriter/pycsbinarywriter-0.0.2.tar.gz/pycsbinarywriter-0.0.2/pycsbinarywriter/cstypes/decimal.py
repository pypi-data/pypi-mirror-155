from .cstype import BaseCSType
import pycsbinarywriter.cstypes.simple as simpletypes
from typing import BinaryIO

from decimal import Decimal


__all__ = ['decimal']

'''
I was about to try and re-implement enough of System.Decimal to spit out a string and shit it into Python's decimal.Decimal, but then I actually read the code.

https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/Decimal.cs#L95
        // The lo, mid, hi, and flags fields contain the representation of the
        // Decimal value. The lo, mid, and hi fields contain the 96-bit integer
        // part of the Decimal. Bits 0-15 (the lower word) of the flags field are
        // unused and must be zero; bits 16-23 contain must contain a value between
        // 0 and 28, indicating the power of 10 to divide the 96-bit integer part
        // by to produce the Decimal value; bits 24-30 are unused and must be zero;
        // and finally bit 31 indicates the sign of the Decimal value, 0 meaning
        // positive and 1 meaning negative.

Then I wanted to die inside.

This code is here in case I fucked something up.

# https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/Decimal.cs for how decimal works in .NET
# We don't implement the whole thing, just provide conversion to binary and back.

# Also https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/IO/BinaryWriter.cs

# private const uint TenToPowerNine = 1000000000;
TEN_TO_POWER_NINE = np.uint32(1000000000)

# https://github.com/dotnet/runtime/blob/bba6c0b618f40adbfdcd9014dbd435351496d180/src/libraries/System.Private.CoreLib/src/System/Number.Formatting.cs#L1333
def _UInt32ToDecChars(buffer: bytes, pos: int, value: np.uint32, digits: int) -> Tuple[bytes, int]:
    #while (--digits >= 0 || value != 0)
    #{
    #    uint remainder;
    #    (value, remainder) = Math.DivRem(value, 10);
    #    *(--bufferEnd) = (byte)(remainder + '0');
    #}
    #return bufferEnd;

    # Python is a bit weirder to work with, in this regard.
    # Convert numpy.uint32 to int()
    value = int(value)
    digits -= 1
    while digits >= 0 or value != 0:
        value, remainder = divmod(value, 10)
        buffer[pos] = remainder + 48 # ord('0') == 48
        pos -= 1
        digits -= 1
    return buffer, pos

def _DecimalToNumber(d: _DotNetDecimal) -> str:
    buffer = b'\x00'*31

    # https://github.com/dotnet/runtime/blob/bba6c0b618f40adbfdcd9014dbd435351496d180/src/libraries/System.Private.CoreLib/src/System/Number.Formatting.cs#L352
    #byte* p = buffer + DecimalPrecision;
    pos = 29
    #while ((d.Mid | d.High) != 0)
    #{
    #    p = UInt32ToDecChars(p, decimal.DecDivMod1E9(ref d), 9);
    #}
    while (d.Mid | d.High) != 0:
        buffer, pos = _UInt32ToDecChars(buffer, pos, d._devDecMod1E9(), 9)
    #p = UInt32ToDecChars(p, d.Low, 0);
    buffer, pos = _UInt32ToDecChars(buffer, pos, d.Low, 0)

    #int i = (int)((buffer + DecimalPrecision) - p);
    digits = pos-29
    scale = d.Scale

    number.DigitsCount = i;
    number.Scale = i - d.Scale;

    byte* dst = number.GetDigitsPointer();
    while (--i >= 0)
    {
        *dst++ = *p++;
    }
    *dst = (byte)('\0');

class _DotNetDecCalc:
    #https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/Decimal.DecCalc.cs#L37
    # Jesus Christ.
    def __init__(self) -> None:
        self.uflags: np.uint32 = np.uint32(0)
        self.ulo: np.uint32 = np.uint32(0)
        self.umid: np.uint32 = np.uint32(0)
        self.uhi: np.uint32 = np.uint32(0)
        self.ulomid: np.uint32 = np.uint32(0)

    def _devDecMod1E9(self) -> np.uint32:
        #https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/Decimal.DecCalc.cs#L2506
        #ulong high64 = ((ulong)value.uhi << 32) + value.umid;
        high64: np.uint64 = (np.uint64(self.uhi) << 32) + np.uint64(self.umid)
        #ulong div64 = high64 / TenToPowerNine;
        div64: np.uint64 = high64 / TEN_TO_POWER_NINE
        #value.uhi = (uint)(div64 >> 32);
        self.uhi = np.uint32(div64 >> 32)
        #value.umid = (uint)div64;
        self.umid = np.uint32(div64)

        #ulong num = ((high64 - (uint)div64 * TenToPowerNine) << 32) + value.ulo;
        num: np.uint64 = ((high64 - np.uint32(div64) * TEN_TO_POWER_NINE) << 32) + self.ulo
        #uint div = (uint)(num / TenToPowerNine);
        div: np.uint32 = np.uint32(num / TEN_TO_POWER_NINE)
        #value.ulo = div;
        self.ulo = div
        #return (uint)num - div * TenToPowerNine;
        return np.uint32(num) - div * TEN_TO_POWER_NINE


class _DotNetDecimal:
    def __init__(self, hi: int=0, mid: int=0, lo: int=0, flags: int=0) -> None:
        self._lo64: np.uint64 = np.uint32(lo) + np.uint64(np.uint32(mid) << 32)
        self._hi32: np.uint32 = np.uint32(hi)
        self._flags: int = flags

    @property
    def High(self) -> np.uint32:
        return self._hi32

    @property
    def Mid(self) -> np.uint32:
        return np.uint32(self._lo64 >> 32)

    @property
    def Low(self) -> np.uint32:
        return np.uint32(self._lo64)

    @property
    def IsNegative(self) -> bool:
        return self._flags < 0

    @property
    def Scale(self) -> int:
        #internal int Scale => (byte)(_flags >> ScaleShift);
        # private const int ScaleShift = 16;
        #private const int ScaleMask = 0x00FF0000;
        return (self._flags & 0x00FF0000) >> 16
'''


class DecimalType(BaseCSType[Decimal]):
    def __init__(self) -> None:
        super().__init__('decimal', Decimal)

    def calcsize(self) -> int:
        return 16

    def unpack(self, data: bytes) -> Decimal:
        # https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/IO/BinaryWriter.cs
        # https://github.com/dotnet/runtime/blob/e420a0578c4964f8efbd9a14f9901c30ec686d6e/src/libraries/System.Private.CoreLib/src/System/Decimal.cs#L590
        #lo: int = simpletypes.int32.unpack(data[0:4])
        #mid: int = simpletypes.int32.unpack(data[4:8])
        #hi: int = simpletypes.int32.unpack(data[8:12])
        n = 0
        for b in data[0:12]:
            n = (n << 8) | b

        flags: int = simpletypes.int32.unpack(data[12:16])
        scale = (flags & 0x00FF0000) >> 16

        d = Decimal(n) / Decimal(scale)
        if flags < 0:
            d = -d
        return d

    def pack(self, value: Decimal) -> bytes:
        raise NotImplementedError()

    def unpackFrom(self, f: BinaryIO) -> Decimal:
        data: bytes = f.read(16)
        if len(data) < 16:
            return None
        return self.unpack(data)


decimal: DecimalType = DecimalType()
