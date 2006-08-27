prefix := @prefix@
etcdir := $(prefix)/etc
sysconfdir := $(prefix)/etc/sysconfig
sbindir := $(prefix)/sbin
initdir := $(prefix)/etc/init.d

all:
	@echo This package does not require building.

install:
	echo installing to $(prefix)
# aux files
	install -d etc/net $(etcdir)
	install -D etc/sysconfig/network $(sysconfdir)
	install -D etc/net/scripts/network.init $(initdir)/network

# Install the whole /etc/net tree at once.
	cp -rp etc/net $(etcdir)

# sbin links
	mkdir -p $(sbindir)
	ln -s ../etc/net/scripts/ifup $(sbindir)/ifup
	ln -s ../etc/net/scripts/ifdown $(sbindir)/ifdown
