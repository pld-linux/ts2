Summary:	VoIP server for gamers
Summary(pl):	Serwer VoIP dla graczy
Name:		ts2
Version:	rc2_20201
Release:	3
Epoch:		1
License:	redistributable for non-commercial use
Group:		Networking/Daemons
Source0:	ftp://ftp.freenet.de/pub/4players/teamspeak.org/releases/ts2_server_%{version}.tar.bz2
# Source0-md5:	e1f0dace646affc80c1e0d83fa7f9161
Source1:	%{name}.init
URL:		http://www.goteamspeak.com/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	uid	139
%define	_localstatedir	/var/lib/tss

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
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_libdir}/tss/{,{mysql,sqlite}_sql,tcpquerydocs} \
	$RPM_BUILD_ROOT%{_datadir}/tss \
	$RPM_BUILD_ROOT%{_localstatedir}/tss \

install server_linux $RPM_BUILD_ROOT%{_libdir}/tss/tss
install *.so $RPM_BUILD_ROOT%{_libdir}/tss
install mysql_sql/* $RPM_BUILD_ROOT%{_libdir}/tss/mysql_sql
install sqlite_sql/* $RPM_BUILD_ROOT%{_libdir}/tss/sqlite_sql

cp -a httpdocs $RPM_BUILD_ROOT%{_datadir}/tss
cp -a tcpquerydocs $RPM_BUILD_ROOT%{_datadir}/tss

> $RPM_BUILD_ROOT%{_localstatedir}/bad_names.txt
> $RPM_BUILD_ROOT%{_localstatedir}/server.dbs
> $RPM_BUILD_ROOT%{_localstatedir}/server.ini
> $RPM_BUILD_ROOT%{_localstatedir}/server.log

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/tss

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/bin/id -u tss 2>/dev/null`" ]; then
	if [ "`/bin/id -u tss`" != "%{uid}" ]; then
		echo "Error: user tss doesn't have uid=%{uid}. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u %{uid} \
		-d /var/lib/tss -s /bin/sh -g daemon \
		-c "TeamSpeak Server" tss 1>&2
fi

%post
/sbin/chkconfig --add tss
if [ -f /var/lock/subsys/tss ]; then
	/etc/rc.d/init.d/tss restart >&2
else
	echo "Run \"/etc/rc.d/init.d/tss start\" to start TeamSpeak." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/tss ]; then
		/etc/rc.d/init.d/tss stop
	fi
	/sbin/chkconfig --del tss
fi

%postun
if [ "$1" = "0" ]; then
    %userremove tss
fi

%files
%defattr(644,root,root,755)
%doc README changelog.txt
%doc INSTALL INSTALL.mysql
%attr(754,root,root) /etc/rc.d/init.d/tss

%dir %attr(755,root,root) %{_libdir}/tss
%attr(755,root,root) %{_libdir}/tss/tss
%attr(755,root,root) %{_libdir}/tss/*.so

%dir %attr(755,root,root) %{_libdir}/tss/mysql_sql
%attr(644,root,root) %{_libdir}/tss/mysql_sql/*.sql
%dir %attr(755,root,root) %{_libdir}/tss/sqlite_sql
%attr(644,root,root) %{_libdir}/tss/sqlite_sql/*.sql

%{_datadir}/tss

%dir %attr(700,tss,root) %{_localstatedir}
%ghost %attr(700,tss,root) %{_localstatedir}/bad_names.txt
%ghost %attr(700,tss,root) %{_localstatedir}/server.dbs
%ghost %attr(700,tss,root) %{_localstatedir}/server.ini
%ghost %attr(700,tss,root) %{_localstatedir}/server.log
