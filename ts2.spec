Summary:	VoIP server for gamers
Summary(pl):	Serwer VoIP dla graczy
Name:		ts2
Version:	rc2_201916
Release:	1
License:	redistributable for non-commercial use
Group:		Networking/Daemons
Source0:	ftp://ftp.teamspeak.org/releases/%{name}_server_%{version}.tar.bz2
# Source0-md5:	b0ac9a065c5a4cd8b7020d8e6d56b879
Source1:	%{name}.init
URL:		http://www.teamspeak.org/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TeamSpeak was primarily designed to work for people who are behind a
NAT router (share internet). Further more it was designed for gamers.
That mean to us it had to use as little bandwidth as possible, while
having a reasonable voice quality. The authors think they achieved
that with the 650 bytes/s maximum CELP codec.

%description -l pl
TeamSpeak zosta³ zaprojektowany g³ównie do pracy dla ludzi za
routerami z maskowaniem adresów (dziel±cymi Internet). Ponadto by³
pomy¶lany dla graczy. Oznacza to, ¿e ma zu¿ywaæ jak najmniej pasma,
zapewniaj±c rozs±dn± jako¶æ g³osu. Autorzy uwa¿aj±, ¿e osi±gnêli to
przy pomocy kodeka CELP z maksimum 650 bajtów/sekundê.

%prep
%setup -q -n tss2_rc2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/rc.d/init.d}

install server_linux $RPM_BUILD_ROOT%{_bindir}/tss
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/tss

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Readme.txt slicense.txt httpdocs
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/tss
