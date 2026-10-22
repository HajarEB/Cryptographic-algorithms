import ecdsa
from bignum import *

def verify_ecdsa(message_hash, r, s, public_key, B):
    q = ecdsa.convertParams(ecdsa.q, B)
    p = ecdsa.convertParams(ecdsa.p, B)
    a = ecdsa.convertParams(ecdsa.a, B)
    b = ecdsa.convertParams(ecdsa.b, B)

    G = [
        ecdsa.convertParams(ecdsa.Gx, B),
        ecdsa.convertParams(ecdsa.Gy, B)
    ]
    c = [p, a, b]

    r = ecdsa.hextoB(r, B)
    s = ecdsa.hextoB(s, B)
    h = ecdsa.hextoB(message_hash, B)

    if not ([0] != r and compare(r, q) < 0 and
            [0] != s and compare(s, q) < 0):
        return False

    w = modinv(s, q, B)

    u1 = reduce(multiply(h, w, B), q, B)
    u2 = reduce(multiply(r, w, B), q, B)

    P1 = double_addECbig(G, u1, c, B)
    P2 = double_addECbig(public_key, u2, c, B)

    P = addECbig(P1, P2, c, B)

    if P == [[0], [0]]:
        return False

    v = reduce(P[0], q, B)

    return compare(v, r) == 0


def test_ecdsa():
    snum = "215463721"
    message_hash = "1234567890abcdef"
    base = 32

    privkey = ecdsa.get_privkey(snum)

    G = [ecdsa.convertParams(ecdsa.Gx, base), ecdsa.convertParams(ecdsa.Gy, base)]

    c = [ecdsa.convertParams(ecdsa.p, base), ecdsa.convertParams(ecdsa.a, base), ecdsa.convertParams(ecdsa.b, base)]

    public_key = double_addECbig(G, ecdsa.hextoB(privkey, base), c, base)

    r1, s1 = ecdsa.ECDSA(snum, message_hash, base)
    r2, s2 = ecdsa.ECDSA(snum, message_hash, base)

    print("Signature 1:", r1, s1)
    print("Signature 2:", r2, s2)

    assert all(isinstance(x, str) for x in (r1, s1, r2, s2))
    assert all(int(x, 16) > 0 for x in (r1, s1, r2, s2))

    print("Basic signature checks passed.")

    assert verify_ecdsa(message_hash, r1, s1, public_key, base)
    assert verify_ecdsa(message_hash, r2, s2, public_key, base)

    print("Both ECDSA signatures verified successfully.")


if __name__ == "__main__":
    test_ecdsa()
