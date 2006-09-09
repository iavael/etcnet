prefix := @prefix@
etcnetdir := $(prefix)/etc/net
sysconfdir := $(prefix)/etc/sysconfig
sbindir := $(prefix)/sbin
initdir := $(prefix)/etc/rc.d/init.d
mandir := $(prefix)/usr/share/man

all:
	@echo This package does not require building.

install:
	@echo Installing /etc/net to $(prefix)

# 1. Install main /etc/net tree.
	@# Yes, default interface is quite messed up with files and directories.
	@install -d $(etcnetdir)/ifaces/default/fw/iptables/filter
	@install -d $(etcnetdir)/ifaces/default/fw/iptables/mangle
	@install -d $(etcnetdir)/ifaces/default/fw/iptables/nat
	@install -d $(etcnetdir)/ifaces/lo
	@install -d $(etcnetdir)/ifaces/unknown
	@install -d $(etcnetdir)/options.d
	@install -d $(etcnetdir)/scripts/contrib
	@install etc/net/ifaces/default/{options,sysctl.conf}* $(etcnetdir)/ifaces/default
	@install etc/net/ifaces/default/fw/options $(etcnetdir)/ifaces/default/fw
	@install etc/net/ifaces/default/fw/iptables/{loadorder,modules,syntax} $(etcnetdir)/ifaces/default/fw/iptables
	@install etc/net/ifaces/default/fw/iptables/filter/* $(etcnetdir)/ifaces/default/fw/iptables/filter
	@install etc/net/ifaces/default/fw/iptables/mangle/* $(etcnetdir)/ifaces/default/fw/iptables/mangle
	@install etc/net/ifaces/default/fw/iptables/nat/* $(etcnetdir)/ifaces/default/fw/iptables/nat
	@# Finally done with default iface.
	@install etc/net/ifaces/unknown/{options,README} $(etcnetdir)/ifaces/unknown
	@install etc/net/ifaces/lo/{options,ipv4address} $(etcnetdir)/ifaces/lo
	@install etc/net/options.d/* $(etcnetdir)/options.d
	@install etc/net/scripts/contrib/* $(etcnetdir)/scripts/contrib
	@install etc/net/scripts/{config-,create-,destroy-,functions,ifdown,ifup,setup-,shutdown-}* $(etcnetdir)/scripts
	@install etc/net/scripts/{ifplugd.action,network.init} $(etcnetdir)/scripts
	@install etc/net/sysctl.conf $(etcnetdir)
	@install -d $(mandir)/man{5,8}
	@install docs/*.8 $(mandir)/man8
	@install docs/*.5 $(mandir)/man5

# 2. Install aux files.
	@install -D etc/sysconfig/network $(sysconfdir)/network
	@install -D etc/net/scripts/network.init $(initdir)/network

# 3. Create /sbin links.
	@install -d $(sbindir)
	@ln -s ../etc/net/scripts/ifup $(sbindir)/ifup
	@ln -s ../etc/net/scripts/ifdown $(sbindir)/ifdown
	@echo Done!
