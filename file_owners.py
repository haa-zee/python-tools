# -*- coding: utf-8 -*-
# Counting objects by owner and looking for unknown file and folder owners
# @bug: handling filenames encoded other than ASCII (these gets '*'
#       instead of the owner :(

import os,sys
import win32security


def count_owners(owner_dict, rootdir, object_list):
    for name in object_list:
        try:
            security_descriptor=win32security.GetFileSecurity(
                os.path.join(rootdir,name),
                win32security.OWNER_SECURITY_INFORMATION
                )
        
            owner=security_descriptor.GetSecurityDescriptorOwner()
        except Exception:
            # Mostly: no permission to access this object
            owner='*'
            
        try:
            owner_name=win32security.LookupAccountSid(None,owner)
        except Exception:
            # It is an unknown owner
            owner_name=str(owner)
            # Just for debug
            print rootdir, name, owner_name

        if owner_name in owner_dict:
            owner_dict[owner_name]+=1
        else:
            owner_dict[owner_name]=1



owners={}
root_dir=sys.argv[1] if len(sys.argv)>1 else 'C:\\'
print root_dir
for root, dirs, files in os.walk(root_dir):
    count_owners(owners, root, dirs)
    count_owners(owners, root, files)

print "\n\n"+"-"*80+"\n"
for owner, count in owners.iteritems():
    print owner, count
