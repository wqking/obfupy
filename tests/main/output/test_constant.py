import codecs
(Il1lll1lII1l, lI1IIIIIIl1I, l1l1l1I1l1Il, IIl1lI11ll11, llIl1I1lIII1, I1l11l1lll1l, IllIl11Il1l1, lI1lIIIlIll1, IIIl11I11IlI, llllIII1lIll, I111lI1Il1ll, llII11Il1II1, II11lIII111l, II1llllII1lI, IlIl1II111I1, IIlIll11I1l1, IlI1l1l1l11l, ll1Il1IIIllI, l11II1l111ll) = (int, 'cba'[::-1], codecs.decode('nop', 'rot13'), codecs.decode(b'616263', 'hex').decode('utf-8'), ~-377603424 ^ 498544604 + -120941186, 'fed'[::-1], ''.join([chr(I11lIIII11lI ^ 12740) for I11lIIII11lI in [4588]]), ~-980641681 ^ 477252386 - -503389295, isinstance, 279463732 ^ 609338321 ^ 74711527 + 814056191, isinstance, 620157264 ^ 597836414 ^ (128024589 ^ 16063280), (931409003 ^ 415474445) - (459494232 + 333724683), str, codecs.decode(b'e280a8', 'hex').decode('utf-8'), len, 1.0, codecs.decode(b'3139', 'hex').decode('utf-8'), str)

def I1lI11II1lII(II1l11lIl1II, lII11lllI1Il):
    try:
        return II1l11lIl1II != lII11lllI1Il
    except:
        return not II1l11lIl1II == lII11lllI1Il

def Ill1I1ll11II():
    assert not I1lI11II1lII(l11II1l111ll(llII11Il1II1), ll1Il1IIIllI)

def test_int():
    return Ill1I1ll11II()

def I1IIlIIlI11l():
    lI1l1Il1lIll_a_78733 = IlI1l1l1l11l
    l1l1llllI11I_b_97081 = llllIII1lIll
    l1l1llllI11I_b_97081 = l1l1llllI11I_b_97081 + lI1lIIIlIll1
    assert I111lI1Il1ll(l1l1llllI11I_b_97081, Il1lll1lII1l)

def test_intAndFloat():
    return I1IIlIIlI11l()

def Illl1111lIII():
    lllIl1lllIll_a_83884 = lI1IIIIIIl1I
    assert IIIl11I11IlI(lllIl1lllIll_a_83884, II1llllII1lI)

def test_builtinFunction():
    return Illl1111lIII()

def l1I1llllIlI1():
    Il11ll11I1II_str_40974 = IIl1lI11ll11
    assert not I1lI11II1lII(Il11ll11I1II_str_40974, l1l1l1I1l1Il)
    assert not I1lI11II1lII(IIlIll11I1l1(Il11ll11I1II_str_40974), llllIII1lIll)

def test_builtinFunctionAsVariable():
    return l1I1llllIlI1()

def IllI11IlI1l1(I111I1IIl1lI_str_74164):
    return IIlIll11I1l1(I111I1IIl1lI_str_74164)

def funcBuiltinFunctionAsArgument(str):
    return IllI11IlI1l1(str)

def II11lIIl11I1():
    IllllIlI1l1I_str_67305 = I1l11l1lll1l
    assert not I1lI11II1lII(funcBuiltinFunctionAsArgument(IllllIlI1l1I_str_67305), II11lIII111l)

def test_funcBuiltinFunctionAsArgument():
    return II11lIIl11I1()

def IllII1lllIll():
    IIlII1I1llI1_a_49327 = IlIl1II111I1
    assert not I1lI11II1lII(IIlIll11I1l1(IIlII1I1llI1_a_49327), lI1lIIIlIll1)
    assert not I1lI11II1lII(IIlII1I1llI1_a_49327, IllIl11Il1l1)

def test_unicodeString():
    return IllII1lllIll()

def lI1I1lI1l11l():

    def open():
        return open.value
    open.value = llIl1I1lIII1
    assert not I1lI11II1lII(open.value, llIl1I1lIII1)
    assert not I1lI11II1lII(open(), llIl1I1lIII1)

def test_builtinFunctionAsNestedFunc():
    return lI1I1lI1l11l()