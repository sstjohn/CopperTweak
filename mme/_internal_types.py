from scapy.fields import FieldListField, ConditionalField, Field

def TypeConditionalField(t, f):
        cond = lambda p: p.mmtype == t
        return ConditionalField(f, cond)

def ArrayField(name, default, field, count):
	return FieldListField(name, [default] * count, field, count_from = lambda p: count)
