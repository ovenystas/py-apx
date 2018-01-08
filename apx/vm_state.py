import struct
from apx.vm_base import *

u8_struct = struct.Struct("B")
u16_struct = struct.Struct("<H")
u32_struct = struct.Struct("<I")
s8_struct = struct.Struct("<b")
s16_struct = struct.Struct("<h")
s32_struct = struct.Struct("<i")


class VmState:
    def __init__(self, value=None):
        self.value=value
        self.key=None #when self.value is dict
        self.array_index = None #used when we have array of records/dict
        self.stack = [] #used for complex data structures (records inside records etc.)


class VmPackState(VmState):
    """
    Stackable VM state
    """
    def __init__(self, value = None):
        super().__init__(value)

    def record_enter(self):
        if (self.key is None) and (self.array_index is None):
            if not isinstance(self.value, dict):
                raise ValueError('value must be of type dict')
        else:
            if self.array_index is not None:
                self.stack.append((self.value, self.key, self.array_index))
                self.value = self.value[self.array_index]
                self.key=None
                self.array_index=None
            else:
                self.stack.append((self.value, self.key, self.array_index))
                self.value = self.value[self.key]
                self.key=None
                self.array_index=None


    def record_select(self, name):
        if not isinstance(self.value, dict):
            raise RuntimeError('Expected dict, got {}'.format(type(self.value)))
        self.key = name

    def record_leave(self):
        if len(self.stack)>0:
            self.value, self.key, self.array_index = self.stack.pop()
            if self.array_index is not None:
                self.array_index+=1
        self.key = None

    def array_enter(self):
        if (self.key is None) and (self.array_index is None):
            if not isinstance(self.value, list):
                raise ValueError('value must be of type list')
            self.array_index = 0
        else:
            self.stack.append((self.value, self.key, self.array_index))
            if self.key is not None:
                self.value = self.value[self.key]
            elif self.array_index is not None:
                self.value = self.value[self.array_index]
            else:
                raise RuntimeError('array_enter called out of context')
            self.key=None
            self.array_index=0

    def array_leave(self):
        if len(self.stack)>0:
            self.value, self.key, self.array_index = self.stack.pop()
            if self.array_index is not None:
                self.array_index+=1
        else:
            self.array_index = None

    def pack_u8(self, data, data_offset, array_len = 0):
        return self.pack_struct(u8_struct, UINT8_LEN, data, data_offset, array_len)

    def pack_u16(self, data, data_offset, array_len = 0):
        return self.pack_struct(u16_struct, UINT16_LEN, data, data_offset, array_len)

    def pack_u32(self, data, data_offset, array_len = 0):
        return self.pack_struct(u32_struct, UINT32_LEN, data, data_offset, array_len)

    def pack_s8(self, data, data_offset, array_len = 0):
        return self.pack_struct(s8_struct, SINT8_LEN, data, data_offset, array_len)

    def pack_s16(self, data, data_offset, array_len = 0):
        return self.pack_struct(s16_struct, SINT16_LEN, data, data_offset, array_len)

    def pack_s32(self, data, data_offset, array_len = 0):
        return self.pack_struct(s32_struct, SINT32_LEN, data, data_offset, array_len)

    def pack_str(self, data, data_offset, str_len):
        if isinstance(self.value, dict):
            if self.key is None:
                raise RuntimeError('key must not be None')
            value = self.value[self.key].encode('utf-8')
        else:
            value = self.value.encode('utf-8')
        if str_len < len(data):
            truncated = data[0:str_len]
        struct.pack_into('{:d}s'.format(str_len), data, data_offset, value)
        data_offset+=str_len
        return data_offset

    def pack_struct(self, struct_obj: struct.Struct, elem_len: int, data: bytearray, data_offset: int, array_len: int):
        """
        Calls the pack_into method of the struct_obj object with some added intelligence
        """
        if isinstance(self.value, dict):
            if self.key is None:
                raise RuntimeError('key must not be None')
            value = self.value[self.key]
        else:
            value = self.value
        if array_len > 0:
            if not isinstance(value, list):
                raise ValueError('value must be a list, got {}'.format(str(value)))
            if len(self.value)<array_len:
                raise ValueError('Not enough elements in list value list {0}. Expected {1} items'.format(repr(self.value), array_len))
            for i in range(array_len):
                struct_obj.pack_into(data, data_offset, value[i])
                data_offset+=elem_len
        else:
            struct_obj.pack_into(data, data_offset, value)
            data_offset+=elem_len
        return data_offset

class VmUnpackState(VmState):
    def __init__(self):
        super().__init__()

    def record_enter(self):
        if (self.key is None) and (self.array_index is None):
            self.value = {}
        else:
            if self.array_index is not None:
                self.stack.append((self.value, self.key, self.array_index))
                self.value = {}
                self.key=None
                self.array_index=None
            else:
                raise NotImplementedError('nested records')


    def record_select(self, name):
        if not isinstance(self.value, dict):
            raise RuntimeError("record_select performed before record_enter")
        self.key=name

    def record_leave(self):
        if len(self.stack)>0:
            child_value = self.value
            self.value, self.key, self.array_index = self.stack.pop()
            if self.array_index is not None:
                self.value.append(child_value)
                self.array_index+=1
            elif self.key is not None:
                self.value[self.key] = child_value
        self.key = None

    def array_enter(self):
        if (self.key is None) and (self.array_index is None):
            self.value = []
            self.array_index=0
        else:
            self.stack.append((self.value, self.key, self.array_index))
            self.value = []
            self.key=None
            self.array_index=0

    def array_leave(self):
        if self.array_index is None:
            raise RuntimeError('array_leave called before array_enter')
        if len(self.stack)>0:
            child_value = self.value
            self.value, self.key, self.array_index = self.stack.pop()
            if self.array_index is not None:
                self.value.append(child_value)
                self.array_index+=1
            elif self.key is not None:
                self.value[self.key]=child_value
                self.key=None
        else:
            self.array_index = None


    def unpack_u8(self, data, data_offset, array_len=0):
        return self.unpack_struct(u8_struct, UINT8_LEN, data, data_offset, array_len)

    def unpack_u16(self, data, data_offset, array_len=0):
        return self.unpack_struct(u16_struct, UINT16_LEN, data, data_offset, array_len)

    def unpack_u32(self, data, data_offset, array_len=0):
        return self.unpack_struct(u32_struct, UINT32_LEN, data, data_offset, array_len)

    def unpack_s8(self, data, data_offset, array_len=0):
        return self.unpack_struct(s8_struct, SINT8_LEN, data, data_offset, array_len)

    def unpack_s16(self, data, data_offset, array_len=0):
        return self.unpack_struct(s16_struct, SINT16_LEN, data, data_offset, array_len)

    def unpack_s32(self, data, data_offset, array_len=0):
        return self.unpack_struct(s32_struct, SINT32_LEN, data, data_offset, array_len)
    
    def unpack_str(self, data, data_offset, str_len=0):
        data_len = len(data)-data_offset
        if data_len < str_len:
            raise ValueError('Not enough bytes available in data array. Need {:d}, bytes, got {:d}'.format(str_len, data_len))
        struct.unpack_from('{:d}s'.format(str_len), data, data_offset)
        #in case of trailing null terminators we want to get rid of those in the final string.
        str_end = data_offset+str_len
        data_begin=data_end=data_offset
        vale = None
        while(data_end < str_end):
            if data[data_end] == 0:                
                break
            data_end+=1
        value = data[data_offset:data_end].decode('utf-8')
        if isinstance(self.value, dict):
            if self.key is None:
                raise RuntimeError('key must not be None')
            self.value[self.key] = value
        else:
            self.value = value
        return data_offset+str_len


    def unpack_struct(self, struct_obj: struct.Struct, elem_len: int, data: bytearray, data_offset: int, array_len: int):
        if array_len > 0:
            value = []
            for i in range(array_len):
                tmp, = struct_obj.unpack_from(data, data_offset)
                value.append(tmp)
                data_offset+=elem_len
        else:
            value, = struct_obj.unpack_from(data, data_offset)
            data_offset+=elem_len
        if isinstance(self.value, dict):
            if self.key is None:
                raise RuntimeError('key must not be None')
            self.value[self.key] = value
        else:
            self.value = value
        return data_offset