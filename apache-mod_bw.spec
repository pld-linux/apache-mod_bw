# TODO:
# - cron?
%define		mod_name	bw
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: bandwidth limits
Summary(pl.UTF-8):	Moduł do Apache: limity pasma
Name:		apache-mod_%{mod_name}
Version:	0.92
Release:	1
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	http://ivn.cl/files/source/mod_bw-%{version}.tgz
# Source0-md5:	90f5e632dad5de8d49dcdb61453dcf97
Source1:	%{name}.conf
URL:		http://www.ivn.cl/apache/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	apache(modules-api) = %apache_modules_api
Requires:	crondaemon
Requires:	procps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
"Mod_bandwidth" is a module for the Apache webserver that enable the
setting of server-wide or per connection bandwidth limits, based on
the directory, size of files and remote IP/domain.

%description -l pl.UTF-8
Moduł pozwalający na ograniczanie pasma serwera Apache bazując na
katalogu, wielkości plików lub zdalnym IP/domenie.

%prep
%setup -qc

%build
%{apxs} -c mod_bw.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf} \
	$RPM_BUILD_ROOT%{_var}/run/%{name}/{link,master} \
	$RPM_BUILD_ROOT{/etc/cron.d,%{_sbindir}}

install -p .libs/mod_bw.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/97_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc mod_bw.txt LICENSE ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
#%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/%{name}
#%attr(755,root,root) %{_sbindir}/*
%attr(750,http,root) %dir %{_var}/run/%{name}
%attr(750,http,root) %dir %{_var}/run/%{name}/link
%attr(750,http,root) %dir %{_var}/run/%{name}/master
