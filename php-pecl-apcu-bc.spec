# centos/sclo spec file for php-pecl-apcu-bc, from:
#
# remirepo spec file for php-pecl-apcu-bc
#
# Copyright (c) 2015-2019 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix %{scl_prefix}
%if "%{scl}" == "rh-php70"
%global sub_prefix sclo-php70-
%endif
%if "%{scl}" == "rh-php71"
%global sub_prefix sclo-php71-
%endif
%if "%{scl}" == "rh-php72"
%global sub_prefix sclo-php72-
%endif
%if "%{scl}" == "rh-php73"
%global sub_prefix sclo-php73-
%endif
%scl_package       php-pecl-apcu-bc
%endif

%global proj_name  apcu_bc
%global pecl_name  apcu-bc
%global ext_name   apc
%global apcver     %(%{_bindir}/php -r 'echo (phpversion("apcu")?:0);' 2>/dev/null || echo 65536)
%global with_zts   0%{!?_without_zts:%{?__ztsphp:1}}
# After 40-apcu.ini
%global ini_name   50-%{ext_name}.ini

Name:           %{?sub_prefix}php-pecl-%{pecl_name}
Summary:        APCu Backwards Compatibility Module
Version:        1.0.5
Release:        2%{?dist}
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

License:        PHP
URL:            http://pecl.php.net/package/APCu

BuildRequires:  %{?scl_prefix}php-devel > 7
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-pecl-apcu-devel >= 5.1.2

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-pecl-apcu%{?_isa} >= 5.1.2

Obsoletes:      %{?scl_prefix}php-pecl-apc              < 4
Provides:       %{?scl_prefix}php-apc                   = %{apcver}
Provides:       %{?scl_prefix}php-apc%{?_isa}           = %{apcver}
Provides:       %{?scl_prefix}php-pecl-apc              = %{apcver}-%{release}
Provides:       %{?scl_prefix}php-pecl-apc%{?_isa}      = %{apcver}-%{release}
Provides:       %{?scl_prefix}php-pecl(APC)             = %{apcver}
Provides:       %{?scl_prefix}php-pecl(APC)%{?_isa}     = %{apcver}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
# For "more" SCL
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This module provides a backwards compatible API for APC.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -qc
mv %{proj_name}-%{version} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_APCU_BC_VERSION/{s/.* "//;s/".*$//;p}' php_apc.h)
if test "x${extver}" != "x%{version}%{?prever}%{?gh_date:dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever}%{?gh_date:dev}.
   exit 1
fi
cd ..

cat << 'EOF' | tee %{ini_name}
; Enable %{summary}
extension=%{ext_name}.so
EOF

: Build apcu_bc %{version} with apcu %{apcver}


%build
cd NTS
%{_bindir}/phpize
%configure \
   --enable-apcu-bc \
   --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the package XML file
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{proj_name}/$i
done


%check
cd NTS
# Check than both extensions are reported (BC mode)
%{_bindir}/php -n \
   -d extension=apcu.so \
   -d extension=%{buildroot}%{php_extdir}/apc.so \
   -m | grep 'apc$'

# Upstream test suite for NTS extension
TEST_PHP_EXECUTABLE=%{_bindir}/php \
TEST_PHP_ARGS="-n -d extension=apcu.so -d extension=%{buildroot}%{php_extdir}/apc.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{_bindir}/php -n run-tests.php --show-diff


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{proj_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/apc.so


%changelog
* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 1.0.5-2
- build for sclo-php72

* Tue Mar 12 2019 Remi Collet <remi@remirepo.net> - 1.0.5-1
- update to 1.0.5

* Wed Nov 14 2018 Remi Collet <remi@remirepo.net> - 1.0.3-3
- minor change for sclo-php72

* Wed Aug  9 2017 Remi Collet <remi@remirepo.net> - 1.0.3-2
- minor change for sclo-php71

* Tue Nov  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- cleanup for SCLo build

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-5
- rebuild for PHP 7.1 new API version

* Mon Jul 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-4
- re-enable ZTS build with PHP 7.1

* Sat Jul 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- disable ZTS build with PHP 7.1

* Mon Mar  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-2
- fix apcver macro definition

* Thu Feb 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3 (beta)

* Fri Jan 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (beta)

* Wed Jan  6 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (beta)

* Mon Jan  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-0
- test build for upcoming 1.0.1

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- missing dependency on APCu

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0 (beta)

* Mon Dec  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2
- test build of upcomming 1.0.0

* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 5.1.2-0.1.20151204git52b97a7
- test build of upcomming 5.1.2
- initial package
