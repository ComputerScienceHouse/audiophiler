# File: ldap.py
# Audiophiler CSHLDAP calls

from audiophiler import ldap

def ldap_is_eboard(uid):
    #find member object using uid
    member = ldap.get_member(uid, uid=True)
    #get groups that the member is part of
    group_list = member.get("memberOf")
    #compare every group the member is in to see
    #if it matches eboard
    for group_dn in group_list:
        if group_dn.split(",")[0][3:] == "eboard":
            return True
    return False

def ldap_is_rtp(uid):
    rtp_group = ldap.get_group("rtp")
    return rtp_group.check_member(ldap.get_member(uid, uid=True))
