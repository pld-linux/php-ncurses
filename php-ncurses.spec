%define		modname	ncurses
Summary:	ncurses module for PHP
Summary(pl.UTF-8):	Moduł ncurses dla PHP
Name:		php-%{modname}
Version:	5.2.13.1
Release:	1
Epoch:		4
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://www.php.net/distributions/php-5.2.13.tar.bz2
# Source0-md5:	eb4d0766dc4fb9667f05a68b6041e7d1
Patch0:		php53.patch
BuildRequires:	ncurses-ext-devel
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Provides:	php(ncurses)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This PHP module adds support for ncurses functions (only for cli and
cgi SAPIs).

%description -l pl.UTF-8
Moduł PHP dodający obsługę funkcji ncurses (tylko do SAPI cli i cgi).

%prep
%setup -qc
mv php-*/ext/ncurses/* .
%patch0 -p1

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS example1.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
