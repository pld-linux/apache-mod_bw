# TODO:
# - cron?
%define		mod_name	bw
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: bandwidth limits
Summary(pl):	Modu� do Apache: limity pasma
Name:		apache-mod_%{mod_name}
Version:	0.6
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.ivn.cl/apache/bw_mod-%{version}.tgz
# Source0-md5:	0c92fa6344f487321291a592dbb49856
Source1:	%{name}.conf
Patch0:		%{name}-apr_1.0.patch
URL:		http://www.ivn.cl/apache/
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	%{apxs}
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache >= 2.0.0
Requires:	crondaemon
Requires:	procps
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
"Mod_bandwidth" is a module for the Apache webserver that enable the
setting of server-wide or per connection bandwidth limits, based on
the directory, size of files and remote IP/domain.

%description -l pl
Modu� pozwalaj�cy na ograniczanie pasma poprzez serwer Apache bazuj�c
na katalogu, wielko�ci plik�w oraz zdalnym IP/domenie.

%prep
%setup -q -n bw_mod-%{version}
%patch0 -p1

%build
perl -pi -e 's@include "apr@include "apr/apr@g' bw_mod-%{version}.c
perl -pi -e 's@^.*apr_buckets.h.*$@@'  bw_mod-%{version}.c
%{apxs} -c bw_mod-%{version}.c
mv .libs/bw_mod-%{version}.so mod_bw.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_var}/run/%{name}/{link,master} \
	$RPM_BUILD_ROOT{/etc/cron.d,%{_sbindir},%{_sysconfdir}/httpd.conf}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/97_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc bw_mod-%{version}.txt LICENSE
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/*mod_*.conf
#%config(noreplace) %verify(not size mtime md5) %attr(640,root,root) /etc/cron.d/%{name}
#%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_pkglibdir}/*
%attr(750,http,root) %dir %{_var}/run/%{name}
%attr(750,http,root) %dir %{_var}/run/%{name}/link
%attr(750,http,root) %dir %{_var}/run/%{name}/master
