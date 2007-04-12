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
	@install -d $(etcnetdir)/ifaces/default/fw/ip6tables/filter
	@install -d $(etcnetdir)/ifaces/default/fw/ip6tables/mangle
	@install -d $(etcnetdir)/ifaces/default/fw/ebtables/filter
	@install -d $(etcnetdir)/ifaces/default/fw/ebtables/broute
	@install -d $(etcnetdir)/ifaces/default/fw/ebtables/nat
	@install -d $(etcnetdir)/ifaces/lo
	@install -d $(etcnetdir)/ifaces/unknown
	@install -d $(etcnetdir)/options.d
	@install -d $(etcnetdir)/scripts/contrib
	@install -m 644 etc/net/ifaces/default/{options,sysctl.conf}* $(etcnetdir)/ifaces/default
	@install -m 644 etc/net/ifaces/default/fw/options $(etcnetdir)/ifaces/default/fw
	@install -m 644 etc/net/ifaces/default/fw/iptables/{loadorder,modules,syntax} $(etcnetdir)/ifaces/default/fw/iptables
	@install -m 644 etc/net/ifaces/default/fw/ip6tables/{loadorder,modules,syntax} $(etcnetdir)/ifaces/default/fw/ip6tables
	@install -m 644 etc/net/ifaces/default/fw/ebtables/{loadorder,modules} $(etcnetdir)/ifaces/default/fw/ebtables
	@install -m 644 etc/net/ifaces/default/fw/iptables/filter/* $(etcnetdir)/ifaces/default/fw/iptables/filter
	@install -m 644 etc/net/ifaces/default/fw/iptables/mangle/* $(etcnetdir)/ifaces/default/fw/iptables/mangle
	@install -m 644 etc/net/ifaces/default/fw/iptables/nat/* $(etcnetdir)/ifaces/default/fw/iptables/nat
	@install -m 644 etc/net/ifaces/default/fw/ip6tables/filter/* $(etcnetdir)/ifaces/default/fw/ip6tables/filter
	@install -m 644 etc/net/ifaces/default/fw/ip6tables/mangle/* $(etcnetdir)/ifaces/default/fw/ip6tables/mangle
	@install -m 644 etc/net/ifaces/default/fw/ebtables/filter/* $(etcnetdir)/ifaces/default/fw/ebtables/filter
	@install -m 644 etc/net/ifaces/default/fw/ebtables/broute/* $(etcnetdir)/ifaces/default/fw/ebtables/broute
	@install -m 644 etc/net/ifaces/default/fw/ebtables/nat/* $(etcnetdir)/ifaces/default/fw/ebtables/nat
	@# Finally done with default iface.
	@install -m 644 etc/net/ifaces/unknown/{options,README} $(etcnetdir)/ifaces/unknown
	@install -m 644 etc/net/ifaces/lo/{options,ipv4address} $(etcnetdir)/ifaces/lo
	@install -m 644 etc/net/options.d/* $(etcnetdir)/options.d
	@install -m 755 etc/net/scripts/contrib/* $(etcnetdir)/scripts/contrib
	@install -m 644 etc/net/scripts/functions* $(etcnetdir)/scripts
	@install -m 755 etc/net/scripts/{config-,create-,destroy-,ifdown,ifup,setup-,shutdown-}* $(etcnetdir)/scripts
	@install -m 755 etc/net/scripts/{ifplugd.action,network.init} $(etcnetdir)/scripts
	@install -m 644 etc/net/sysctl.conf $(etcnetdir)
	@install -d $(mandir)/man{5,8}
	@install -m 644 docs/*.8 $(mandir)/man8
	@install -m 644 docs/*.5 $(mandir)/man5

# 2. Install aux files.
	@install -D -m 644 etc/sysconfig/network $(sysconfdir)/network
	@install -D -m 755 etc/net/scripts/network.init $(initdir)/network

# 3. Create /sbin links.
	@install -d $(sbindir)
	@ln -s ../etc/net/scripts/ifup $(sbindir)/ifup
	@ln -s ../etc/net/scripts/ifdown $(sbindir)/ifdown
	@echo Done!
