# -*- coding: utf-8 -*-
# Counting objects by owner and looking for unknown file and folder owners
# @bug: handling filenames encoded other than ASCII (these gets '*'
#       instead of the owner :(

import os,sys
import win32security #@UnresolvedImport - http://stackoverflow.com/questions/16140948/is-there-a-way-to-suppress-unresolved-imports-in-eclipse-in-a-pydev-project


def count_owners(owner_dict, rootdir, object_list):
    for name in object_list:
        try:
            security_descriptor=win32security.GetFileSecurity(
                os.path.join(rootdir,name),
                win32security.OWNER_SECURITY_INFORMATION
                )
        
            owner=security_descriptor.GetSecurityDescriptorOwner()
        except Exception as exc:
            # Mostly: no permission to access this object
            owner='*'
            print exc
            
        try:
            owner_name=win32security.LookupAccountSid(None,owner)
        except Exception as exc:
            # It is an unknown owner
            owner_name=str(owner)
            # Just for debug
            print os.path.join(rootdir, name), owner_name

        if owner_name in owner_dict:
            owner_dict[owner_name]+=1
        else:
            owner_dict[owner_name]=1



owners={}


# To convert names returned by os.walk, os.listdir etc. to utf-8, you must give utf-8 encoded arguments to them.
# see: http://stackoverflow.com/questions/6425824/filename-formatting-in-python-under-windows

root_dir=u""+sys.argv[1] if len(sys.argv)>1 else u'C:\\'


print root_dir
for root, dirs, files in os.walk(root_dir):
    count_owners(owners, root, dirs)
    count_owners(owners, root, files)

print "\n\n"+"-"*80+"\n"
for owner, count in owners.iteritems():
    print owner, count
