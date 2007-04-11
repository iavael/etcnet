Name:		etcnet
Version:	0.8.4
Release:	2%{?dist}
Summary:	This is /etc/net network configuration system
License:	GPL
Group:		System Environment/Base
URL:		http://etcnet.org/
Source:		%{name}-%{version}.tar.gz
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires:	grep, iproute, wireless-tools >= 28-0.pre10.4, chkconfig, initscripts
BuildArch:	noarch
Conflicts:	net-scripts
Conflicts:	initscripts <= 8.35-1
# This is yet to be checked individually.
#Conflicts:	ethtool < 3-alt4, pcmcia-cs < 3.2.8-alt2, ifplugd < 0.28-alt2
Provides:	network-config-subsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
# We must lock on certain homebrew initscripts version, because Fedora package
# is completely unpredictable. This can't be resolved ATM.
Requires:	initscripts = 8.39-1.etcnet.0


%description
/etc/net represents a new approach to Linux network configuration tasks.
Inspired by the limitations of traditional network configuration subsystems,
/etc/net provides builtin support for configuration profiles, interface name
management, removable devices, full iproute2 command set, interface
dependencies resolution, QoS and firewall configuration frameworks.
/etc/net provides support for the following interface types: Ethernet, WiFi
(WEP), IPv4/IPv6 tunnels, PSK IPSec tunnels, VLAN, PLIP, Ethernet bonding and
bridging, traffic equalizer, Pent@NET, Pent@VALUE, SkyStar-2, UML TUN/TAP,
OpenVPN TUN/TAP, usbnet and PPP. Due to its modular structure, support for new
interface types can be added without overall design changes.

# This is yet to be researched on Fedora.
#%package full
#Summary:	/etc/net plus everything it can work with
#Group:		System/Configuration/Networking
#Requires:	%name = %version-%release, wireless-tools
#Requires:	dhcpcd >= 1.3.22pl4-alt3, iptables, iptables-ipv6, ebtables
#Requires:	ethtool >= 3-alt4, ifplugd >= 0.28-alt2, ipsecadm >= 0.9-alt8
#Requires:	hotplug, ncpfs, pcmcia-cs >= 3.2.8-alt2, ppp, vlan-utils24, bridge-utils
#Requires:	pptp-client, wpa_supplicant, zcip, rp-pppoe-base >= 3.6-alt2, openvpn, tunctl
#
#%description full
#This virtual package requires /etc/net and all packages that may appear useful
#for /etc/net. Accurate requirements should result in correct package versions
#in ALTLinux system.


%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make -f contrib/Makefile prefix=%{buildroot} install
install -m 644 contrib/50-Fedora-6 %buildroot/etc/net/options.d/

%post
if [ $1 -eq 1 ]; then
# This is a fresh install.
	/sbin/chkconfig --add network
fi

%preun
if [ $1 -eq 0 ]; then
# This is an erase.
	/sbin/chkconfig --del network
fi


%files
%defattr(-,root,root,-)
%doc docs/README* docs/ChangeLog docs/TODO
%doc examples/
%doc contrib/
/sbin/ifup
/sbin/ifdown
%{_initrddir}/network
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/net/scripts
%dir %{_sysconfdir}/net/ifaces
%dir %{_sysconfdir}/net/ifaces/default
%dir %{_sysconfdir}/net/ifaces/lo
%dir %{_sysconfdir}/net/ifaces/unknown
%dir %{_sysconfdir}/net/options.d
%{_sysconfdir}/net/scripts/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/default/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/unknown/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/lo/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/sysctl.conf
%config(noreplace) %{_sysconfdir}/net/options.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/network
%{_mandir}/man5/*
%{_mandir}/man8/*


#%files full

%clean
rm -rf %{buildroot}

%changelog
* Sat Sep 16 2006 Denis Ovsienko <linux@pilot.org.ua> - 0.8.4-1
- 0.8.4 release for Fedora

* Thu Jun 15 2006 Denis Ovsienko <linux@pilot.org.ua> - 0.8.3-fc5.0.test4
- initial Fedora build
