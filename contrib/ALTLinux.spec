Name:		etcnet
Version:	0.8.0
Release:	alt0.10
Summary:	/etc/net network configuration system
Summary(ru_RU.KOI8-R): ������� ������������ ���� /etc/net
License:	GPL-2
Group:		System/Base
Packager:	Denis Ovsienko <pilot@altlinux.ru>
URL:		http://etcnet.org/
Source:		%name-%version.tar.gz
Source1:	50-ALTLinux-desktop
Source2:	50-ALTLinux-server
PreReq:		setup >= 0:2.1.9-ipl18mdk, service, startup >= 0:0.9.3-alt1
Requires:	grep, sed, iproute2, ifrename >= 28-alt5.pre10, chkconfig
BuildArch:	noarch
Conflicts:	net-scripts
Conflicts:	ethtool < 3-alt4, pcmcia-cs < 3.2.8-alt2, ifplugd < 0.28-alt2
Provides:	network-config-subsystem

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

%description -l ru_RU.KOI8-R
/etc/net ������������ ����� ������ � ������� ������������ ���� ��� Linux.
�������������� ������������� ������������ ��������� ������������ ����, /etc/net
������������� ���������� ��������� �������� ������������, ���������� �������
�����������, ������� ���������, ������� ������ ������ iproute2, ����������
������������ ������������ � ��������� ������������ QoS.
/etc/net ������������ ��������� ���� �����������: Ethernet, WiFi (WEP), �������
IPv4/IPv6, ������� PSK IPSec, VLAN, PLIP, Ethernet bonding � bridging, traffic
equalizer, Pent@NET, Pent@VALUE, SkyStar-2, usbnet � PPP. ��������� ���������
��������� ��������� ����� ����� ����������� ����� ���� ��������� ��� ���������
������ �������.

%package full
Summary:	/etc/net plus everything it can work with
Summary(ru_RU.KOI8-R): /etc/net � �ӣ, � ��� �� ����� ��������
Group:		System/Configuration/Networking
Requires:	%name = %version-%release, wireless-tools
Requires:	dhcpcd >= 1.3.22pl4-alt3, iptables
Requires:	ethtool >= 3-alt4, ifplugd >= 0.28-alt2, ipsecadm >= 0.9-alt8
Requires:	hotplug, ncpfs, pcmcia-cs >= 3.2.8-alt2, ppp, vlan-utils24
Requires:	pptp-client, wpa_supplicant, zcip, rp-pppoe-base >= 3.6-alt2

%description full
This virtual package requires /etc/net and all packages that may appear useful
for /etc/net. Accurate requirements should result in correct package versions
in ALTLinux system.

%description -l ru_RU.KOI8-R full
���� ����������� ����� ������� /etc/net � ��� ������, ������� ����� ���������
��������� ��� /etc/net. ������ ����������� ������ ������������ ���������� ������
������� � ������� ALTLinux.


%package defaults-desktop
Summary:	/etc/net defaults for a Linux desktop
Group:		System/Configuration/Networking
Provides:	%name-defaults
Conflicts:	%name-defaults-server
Requires:	%name

%description defaults-desktop
This package contains default options for a Linux desktop.


%package defaults-server
Summary:	/etc/net defaults for a Linux server
Group:		System/Configuration/Networking
Provides:	%name-defaults
Conflicts:	%name-defaults-desktop
Requires:	%name

%description defaults-server
This package contains default options for a Linux server.


%prep
%setup -q

%build

%install
%__mkdir_p %buildroot%_initdir
%__cp -a etc %buildroot
%__install -m 644 %SOURCE1 %buildroot/etc/net/options.d
%__install -m 644 %SOURCE2 %buildroot/etc/net/options.d

%__ln_s ../../..%_sysconfdir/net/scripts/network.init %buildroot%_initdir/network
%__mkdir_p %buildroot/sbin/
for n in ifup ifdown; do
	%__ln_s ..%_sysconfdir/net/scripts/$n %buildroot/sbin
done

%__install -D -m 644 docs/etcnet.8 %buildroot%_man8dir/etcnet.8
%__install -D -m 644 docs/etcnet-options.5 %buildroot%_man5dir/etcnet-options.5

%post
if [ $1 -lt 2 ]; then
# This is a fresh install.
	/sbin/chkconfig --add network
fi

%preun
if [ $1 -eq 0 ]; then
# This is an erase.
	/sbin/chkconfig --del network
fi

# since 0.5.0 we have 'network' chkconfig entry instead of 'etcnet' one
%triggerun -- %name < 0.5.1
if [ $2 -gt 0 ]; then
# This is etcnet upgrade.
	/sbin/chkconfig --del etcnet
	/sbin/chkconfig --add network
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
%exclude %_sysconfdir/net/options.d/50-*
%config %_sysconfdir/net/options.d/*
%config(noreplace) %verify(not md5 mtime size) %_sysconfdir/sysconfig/network
%doc docs/README* docs/ChangeLog docs/TODO
%doc examples/
%_man5dir/*
%_man8dir/*
/sbin/ifup
/sbin/ifdown

%files defaults-desktop
%config %_sysconfdir/net/options.d/50-ALTLinux-desktop

%files defaults-server
%config %_sysconfdir/net/options.d/50-ALTLinux-server

%files full

%changelog
* Wed Oct 26 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.15-alt1
- new version (#8118, #8332)
- updated required version for ifrename (iwlib bugfix)
- replaced rp-pppoe-client dependency with rp-pppoe-base (#7405)

* Fri Sep 30 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.14-alt1
- This release features:
 + bugfixes for bonding and interface dependencies code
 + a new NEVER_RMMOD option to workaround 2.6 kernels problems
 + a new command 'switchfrom'

* Sun Sep 18 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.13-alt1
- new version resolves #7970 and #7896

* Mon Aug 22 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.12-alt1
- new version with updated docs and minor bugfixes

* Fri Aug 12 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.11-alt2
- 00-default was lost in alt1

* Thu Aug 11 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.11-alt1
- new version fixes #7613 (Not correct handling of ifaces/unknown in 'service network reload')
- two new defaults-* packages

* Mon Aug 08 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.10-alt1
- new version: bugfixes and code cleanup
- spec cleanup

* Wed Jul 20 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.9-alt1
- new version features iptables support
- spec update

* Mon Jul 18 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.8-alt2
- added zcip to full requirements

* Fri Jul 15 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.8-alt1
- new version fixes several minor bugs introduced by 0.7.7 release

* Thu Jul 14 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.7-alt2
- adjusted version requirements

* Tue Jul 12 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.7-alt1
- new version:
 + finally fixed bug with interface group size
 + initial "unknown" interfaces support
 + vlantab code cleanup
 + added PPPoE config example by Alexey I. Froloff, 
 + more iftab info in README
 + logger enhancements by Andrew Kornilov
 + multiple network modules support
 + PPtP config example
 + added wireless interface config example by Nigel Kukard

* Fri Jul 08 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.6-alt4
- this build should fix #7269 and #7316

* Mon Jul 04 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.6-alt3
- adjusted ifplugd version conflict (#7092)

* Mon Jul 04 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.6-alt2
- new build fixes #7269

* Fri Jun 24 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.6-alt1
- new version:
 + VLAN: fixed comments, added new example
 + bridge fixes from Nigel Kukard
 + network.init patch from Mitch
 + new feature: options.d
 + enhanced style according to Dmitry Levin's notes
 + new feature: resolver postinstall command
 + new feature: DHCP_HOSTNAME
 + changed default ifplugstatus location
- ALTLinux-specific options

* Thu Jun 16 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.5-alt1
- new version
 + custom resolv.conf+DHCP bugfix
 + dhcpcd IFF_UP workaround
- spec cleanup

* Sat May 14 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.4-alt1
- new version
 + treat sysctl.conf at reload too (#6826)
 + initial auto-linkdetect whitelist (#6693)
 + wpa_supplicant improvements (#6582)

* Tue Apr 26 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.3-alt1
- new version
 + service network bugfix
 + ifplugd start bugfix
 + enabled WPA back

* Thu Apr 21 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.2-alt1
- new version
 + cleaner ppp/progress output
 + DONT_FLUSH variable semantics fix
 + new DHCP_ARGS option
 + fixed multihost support for stop operation
 + new reload operation

* Fri Mar 25 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.1-alt1
- new version:
 + network.init bugfix
 + ppp address bugfix
 + iplink processing bugfix
 + updated childfinder

* Mon Mar 21 2005 Denis Ovsienko <pilot@altlinux.ru> 0.7.0-alt1
- new version:
 + bugfixes
 + better performance
 + some incompatibility with previous releases (see ChangeLog)
 + initial configuration examples
 + initial multihost configuration support

* Sat Mar 05 2005 Denis Ovsienko <pilot@altlinux.ru> 0.6.4-alt1
- new version:
 + 8021q is no more unconditionally loaded, other VLAN code enhancements
 + another print_message()/print_progress() bugfix
 + initial config migration script

* Thu Mar 03 2005 Denis Ovsienko <pilot@altlinux.ru> 0.6.3-alt1
- new version (wireless bugfix)

* Wed Mar 02 2005 Denis Ovsienko <pilot@altlinux.ru> 0.6.2-alt1
- new version (minor bugfixes)

* Sat Feb 26 2005 Denis Ovsienko <pilot@altlinux.ru> 0.6.1-alt1
- new version (bugfix release):
 + print_progress()/ipv4route bugfix
 + by default wireless extensions are now configured for 'eth' interfaces only
 + fixed error message about missing iwconfig
 + removed garbage files

* Fri Feb 18 2005 Denis Ovsienko <pilot@altlinux.ru> 0.6.0-alt1
- new version:
 + PPP support
 + smart sysctl.conf
 + configuration checker
 + improved pre/post script invocation
 + progress messages can be disabled at all
 + ipneigh file support
 + Pent@NET and DHCP bugfixes

* Fri Feb 04 2005 Denis Ovsienko <pilot@altlinux.ru> 0.5.3-alt1
- new version (minor enhancements and bugfixes)
- trigger fix

* Mon Jan 03 2005 Denis Ovsienko <pilot@altlinux.ru> 0.5.2-alt1
- new version and network-config-subsystem resync

* Thu Dec 23 2004 Denis Ovsienko <pilot@altlinux.ru> 0.5.1-alt1
- new version
- fixes #5711
- better ALTLinux integration

* Sun Dec 05 2004 Denis Ovsienko <pilot@altlinux.ru> 0.4.2-alt1
- new version
- fixed docdir

* Sun Nov 07 2004 Denis Ovsienko <pilot@altlinux.ru> 0.4.1-alt1
- new version and first Sisypus build

* Tue Aug 31 2004 Denis Ovsienko <pilot@altlinux.ru> 0.2.2-alt2
- fixed default interfaces rpm attributes

* Sun Aug 29 2004 Denis Ovsienko <pilot@altlinux.ru> 0.2.2-alt1
- experimental wireless support
- some bugfixes

* Wed Aug 25 2004 Denis Ovsienko <pilot@altlinux.ru> 0.2.1-alt1
- new snapshot 0.2.1 (working PCMCIA)

* Sat Aug 21 2004 Denis Ovsienko <pilot@altlinux.ru> 0.2.0-alt1
- new snapshot 0.2.0

* Wed Aug 18 2004 Denis Ovsienko <pilot@altlinux.ru> 0.1.1-alt1
- First build for ALTLinux
