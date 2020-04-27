pfile = PwFile(fname, fpass, encrypt)

aclist = pfile.getacs()
aclist.newac() # make this static?
# add other methods for aclist?

ac = aclist.findac(service)
# is this assuming one account per service?

ac.change_pass(newpass)
ac.getpass()
ac.delete_ac()
ac.change_field(name, val)
ac.add_field(name,field_val)
