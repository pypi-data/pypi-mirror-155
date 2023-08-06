from blindecdh import ECDHProtocol


def test_ecdh_match_both_sides() -> None:
    p1 = ECDHProtocol()
    p2 = ECDHProtocol()
    c1 = p1.run(p2.public_key)
    c2 = p2.run(p1.public_key)
    assert c1.derived_key == c2.derived_key
