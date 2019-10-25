This repository contains sources for RPMs that are used
to build Software Collections for CentOS by SCLo SIG.

This branch is for sclo-php70, sclo-php71 and sclo-php72 packages
(for rh-php70, rh-php71 SCL and rh-php72 SCL)


PHP 7.0 / EL-6

    build -bs *spec --define "scl rh-php70" --define "dist .el6"
    cbs add-pkg    sclo6-sclo-php70-sclo-candidate --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs add-pkg    sclo6-sclo-php70-sclo-testing   --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs add-pkg    sclo6-sclo-php70-sclo-release   --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs build      sclo6-sclo-php70-sclo-el6       <above>.src.rpm
    cbs tag-build  sclo6-sclo-php70-sclo-testing   <previous>

PHP 7.0 / EL 7

    build -bs *spec --define "scl rh-php70" --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php70-sclo-candidate --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php70-sclo-testing   --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php70-sclo-release   --owner=sclo  sclo-php70-php-pecl-apcu-bc
    cbs build      sclo7-sclo-php70-sclo-el7       <above>.src.rpm
    cbs tag-build  sclo7-sclo-php70-sclo-testing   <previous>

PHP 7.1 / EL 7

    build -bs *spec --define "scl rh-php71" --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php71-sclo-candidate --owner=sclo  sclo-php71-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php71-sclo-testing   --owner=sclo  sclo-php71-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php71-sclo-release   --owner=sclo  sclo-php71-php-pecl-apcu-bc
    cbs build      sclo7-sclo-php71-sclo-el7       <above>.src.rpm
    cbs tag-build  sclo7-sclo-php71-sclo-testing   <previous>

PHP 7.2 / EL 7

    build -bs *spec --define "scl rh-php72" --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php72-sclo-candidate --owner=sclo  sclo-php72-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php72-sclo-testing   --owner=sclo  sclo-php72-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php72-sclo-release   --owner=sclo  sclo-php72-php-pecl-apcu-bc
    cbs build      sclo7-sclo-php72-sclo-el7       <above>.src.rpm
    cbs tag-build  sclo7-sclo-php72-sclo-testing   <previous>


PHP 7.3 / EL 7

    build -bs *spec --define "scl rh-php73" --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php73-sclo-candidate --owner=sclo  sclo-php73-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php73-sclo-testing   --owner=sclo  sclo-php73-php-pecl-apcu-bc
    cbs add-pkg    sclo7-sclo-php73-sclo-release   --owner=sclo  sclo-php73-php-pecl-apcu-bc
    cbs build      sclo7-sclo-php73-sclo-el7       <above>.src.rpm
    cbs tag-build  sclo7-sclo-php73-sclo-testing   <previous>

