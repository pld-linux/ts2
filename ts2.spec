Name:		ts2
Version:	rc2_201916
Release:	1
License:	redistributable for non-commercial use
Group:		Networking/Daemons
Url:		http://www.teamspeak.org/
Source0:	ftp://ftp.teamspeak.org/releases/%{name}_server_%{version}.tar.bz2
Source1:	%{name}.init
Summary:	VOIP server for gamers
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TeamSpeak was primarily designed to work for people who are behind a
NAT router (share internet). Further more it was designed for gamers.
That mean to us it had to use as little bandwidth as possible, while
having a reasonable voice quality. We think we achieved that with the
650 bytes/s maximum CELP codec.

%prep
%setup -q -n tss2_rc2

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_sysconfdir}/rc.d/init.d}
install -m 755 server_linux $RPM_BUILD_ROOT/%{_bindir}/tss
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/tss

%files
%defattr(644,root,root,755)
%doc Readme.txt slicense.txt httpdocs/
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/tss
