Name:		etcnet
Version:	0.8.4
Release:	fc5.0.2
Summary:	/etc/net network configuration system
License:	GPL
Group:		System/Base
URL:		http://etcnet.org/
Source:		%name-%version.tar.gz
Source1:	README.Fedora
Source2:	50-RedHat
Requires:	grep, iproute, wireless-tools >= 28-0.pre10.4, chkconfig, initscripts
BuildArch:	noarch
Conflicts:	net-scripts
Conflicts:	initscripts <= 8.35-1
# This is yet to be checked individually.
#Conflicts:	ethtool < 3-alt4, pcmcia-cs < 3.2.8-alt2, ifplugd < 0.28-alt2
Provides:	network-config-subsystem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%define		_initdir /etc/rc.d/init.d
%define		_man5dir /usr/share/man/man5
%define		_man8dir /usr/share/man/man8

%description
/etc/net represents a new approach to Linux network configuration tasks.
Inspired by the limitations of traditional network configuration subsystems,
/etc/net provides builtin support for configuration profiles, interface name
management, removable devices, full iproute2 command set, interface
dependencies resolution and a QoS configuration framework.
/etc/net provides support for the following interface types: Ethernet, WiFi
(WEP), IPv4/IPv6 tunnels, PSK IPSec tunnels, VLAN, PLIP, Ethernet bonding and
bridging, traffic equalizer, Pent@NET, Pent@VALUE, SkyStar-2, usbnet
and PPP. Due to its modular structure, support for new interface types can be
added without overall design changes.

# This is yet to be researched on Fedora.
#%package full
#Summary:	/etc/net plus everything it can work with
#Group:		System/Configuration/Networking
#Requires:	%name = %version-%release, wireless-tools
#Requires:	dhcpcd >= 1.3.22pl4-alt3, iptables
#Requires:	ethtool >= 3-alt4, ifplugd >= 0.28-alt2, ipsecadm >= 0.9-alt8
#Requires:	hotplug, ncpfs, pcmcia-cs >= 3.2.8-alt2, ppp, vlan-utils24
#Requires:	pptp-client, wpa_supplicant, zcip, rp-pppoe-base >= 3.6-alt2
#
#%description full
#This virtual package requires /etc/net and all packages that may appear useful
#for /etc/net. Accurate requirements should result in correct package versions
#in ALTLinux system.


%prep
%setup -q
install %{SOURCE1} .

%build

%install
rm -rf %{buildroot}
mkdir -p %buildroot%_initdir
cp -a etc %buildroot

ln -s ../../../etc/net/scripts/network.init %buildroot%_initdir/network
mkdir -p %buildroot/sbin/
for n in ifup ifdown; do
	ln -s ../etc/net/scripts/$n %buildroot/sbin
done

mkdir -p %buildroot%_man8dir %buildroot%_man5dir
install -m 644 docs/etcnet*.8 %buildroot%_man8dir
install -m 644 docs/etcnet*.5 %buildroot%_man5dir
install -m 644 %SOURCE2 %buildroot/etc/net/options.d

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
%dir %_sysconfdir/net
%dir %_sysconfdir/net/scripts
%dir %_sysconfdir/net/ifaces
%dir %_sysconfdir/net/ifaces/default
%dir %_sysconfdir/net/ifaces/lo
%dir %_sysconfdir/net/ifaces/unknown
%dir %_sysconfdir/net/options.d
%_sysconfdir/net/scripts/*
%config(noreplace) %verify(not md5 mtime size) %_sysconfdir/net/ifaces/default/*
%config(noreplace) %verify(not md5 mtime size) %_sysconfdir/net/ifaces/unknown/*
%config(noreplace) %verify(not md5 mtime size) %_sysconfdir/net/ifaces/lo/*
%config(noreplace) %verify(not md5 mtime size) %_sysconfdir/net/sysctl.conf
%config %_initdir/network
%config %_sysconfdir/net/options.d/*
%config %verify(not md5 mtime size) %_sysconfdir/sysconfig/network
%doc docs/README* docs/ChangeLog docs/TODO
%doc examples/
%doc contrib/
%doc README.Fedora
%_man5dir/*
%_man8dir/*
/sbin/ifup
/sbin/ifdown

#%files full

%clean
rm -rf %{buildroot}

%changelog
* Thu Jun 15 2006 Denis Ovsienko <linux@pilot.org.ua> - 0.8.3-fc5.0.test4
- initial Fedora build
