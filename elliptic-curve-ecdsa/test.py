from ecdsa import*

def test_ecdsa():
    privkey = "153071423"
    message_hash = "1234567890abcdef"
    base = 32

    r1, s1 = ECDSA(privkey, message_hash, base)
    r2, s2 = ECDSA(privkey, message_hash, base)

    print("Signature 1:", r1, s1)
    print("Signature 2:", r2, s2)

    assert all(isinstance(x, str) for x in (r1, s1, r2, s2))
    assert all(int(x, 16) > 0 for x in (r1, s1, r2, s2))

    print("Basic signature checks passed.")


if __name__ == "__main__":
    test_ecdsa()
