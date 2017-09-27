# File: ldap.py
# Audiophiler CSHLDAP calls
# @author: Stephen Greene (sgreene570)


from audiophiler import ldap


def ldap_is_eboard(uid):
    eboard_group = ldap.get_group("eboard")
    return eboard_group.check_member(ldap.get_member(uid, uid=True))


def ldap_is_rtp(uid):
    rtp_group = ldap.get_group("rtp")
    return rtp_group.check_member(ldap.get_member(uid, uid=True))
