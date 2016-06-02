%define _binaries_in_noarch_packages_terminate_build   0

Name: Enarksh
Version: 0.9.0
Release: 1%{?dist}
Summary: An efficient MMP scheduler.
Group: Applications/Internet
BuildArch: noarch
License: Proprietary
Requires: dos2unix
Requires: php-cli
Requires: php-mysqlnd
Requires: php-soap
Requires: php-xml
# rpm -ivh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
# yum --enablerepo=remi install php-zmq
Requires: php-zmq
Requires: zeromq3
Vendor: Set Based IT Consultancy
Requires(pre): shadow-utils


%Description
OnzeRelaties a Relation Management System


%prep
rm -rf %{buildroot}


%install
mkdir -p %{buildroot}/opt/onzerelaties/
cp -a /opt/onzerelaties/build/* %{buildroot}/opt/onzerelaties/
rm -f %{buildroot}/opt/onzerelaties/www/index.php

%files
%dir "/opt/onzerelaties"
%defattr(-,mmm,mmm,0770)
/opt/onzerelaties/include
/opt/onzerelaties/lib
/opt/onzerelaties/vendor
%defattr(0664,mmm,mmm,0775)
/opt/onzerelaties/share
%defattr(0550,mmm,mmm,0770)
/opt/onzerelaties/bin
/opt/onzerelaties/libexec
%defattr(0660,mmm,mmm,0770)
/opt/onzerelaties/etc
%defattr(-,mmm,mmm,0770)
/opt/onzerelaties/var
%defattr(0444,mmm,mmm,0775)
/opt/onzerelaties/www/company
/opt/onzerelaties/www/css
/opt/onzerelaties/www/dhtml
/opt/onzerelaties/www/images
/opt/onzerelaties/www/js
%defattr(0444,mmm,mmm,0775)
/opt/onzerelaties/www/error.xhtml
/opt/onzerelaties/www/favicon.ico
%defattr(0440,mmm,mmm,-)
/opt/onzerelaties/www/*.php


%clean
rm -rf %{buildroot}


%pretrans
# Put the OnzeRelaties back offline
if [ -f /opt/onzerelaties/bin/offline -a ! -f /opt/onzerelaties/var/maintenance_time.txt ]; then
  /opt/onzerelaties/bin/mmm_offline +5
  touch /opt/onzerelaties/var/maintenance_rpm.txt
fi

%pre
getent group mmm >/dev/null || groupadd mmm
getent passwd mmm >/dev/null || useradd -g mmm -d /opt/onzerelaties -s /sbin/nologin -c "OnzeRelaties" mmm
exit 0

%post
# Replace user's password for MySQL with the actual password.
if [ -f /opt/onzerelaties/etc/password_user ]; then
  # Set the correct file permissions for the password file.
  chmod 0400 /opt/onzerelaties/etc/password_user
  chown mmm.mmm /opt/onzerelaties/etc/password_user

  umask 0277

  MMM_MYSQL_PASSWORD=`cat /opt/onzerelaties/etc/password_user`

  sed -e 's/const\ \+MMM_MYSQL_PASSWORD\ *=\ *'\''mmm_user'\''\;/const MMM_MYSQL_PASSWORD     = '\'$MMM_MYSQL_PASSWORD\''\;/' /opt/onzerelaties/etc/config.template.php > /opt/onzerelaties/etc/config.template.tmp
  mv /opt/onzerelaties/etc/config.template.tmp /opt/onzerelaties/etc/config.template.php

  sed -e 's/const\ \+MMM_MYSQL_PASSWORD\ *=\ *'\''mmm_user'\''\;/const MMM_MYSQL_PASSWORD     = '\'$MMM_MYSQL_PASSWORD\''\;/' /opt/onzerelaties/etc/config.php > /opt/onzerelaties/etc/config.tmp
  mv /opt/onzerelaties/etc/config.tmp /opt/onzerelaties/etc/config.php

  chmod 0440    /opt/onzerelaties/etc/config.template.php /opt/onzerelaties/etc/config.php
  chown mmm.mmm /opt/onzerelaties/etc/config.template.php /opt/onzerelaties/etc/config.php
fi

# Replace owner's password for MySQL with the actual password.
if [ -f /opt/onzerelaties/etc/password_owner ]; then
  # Set the correct file permissions for the password file.
  chmod 0400 /opt/onzerelaties/etc/password_owner
  chown mmm.mmm /opt/onzerelaties/etc/password_owner

  umask 0277

  MMM_MYSQL_PASSWORD=`cat /opt/onzerelaties/etc/password_owner`

  sed -e 's/password\ *=\ *mmm_owner/password      = '$MMM_MYSQL_PASSWORD'/' /opt/onzerelaties/etc/dlgen.cfg > /opt/onzerelaties/etc/dlgen.tmp
  mv /opt/onzerelaties/etc/dlgen.tmp /opt/onzerelaties/etc/dlgen.cfg

  chmod 0440    /opt/onzerelaties/etc/dlgen.cfg
  chown mmm.mmm /opt/onzerelaties/etc/dlgen.cfg
fi

%posttrans
# Load all (modified) stored procedures in to MySQL.
if [ -f /opt/onzerelaties/etc/password_owner ]; then
  chmod 0660 /opt/onzerelaties/etc/config.php
  su - mmm -s /bin/sh -c "(cd /opt/onzerelaties && ./bin/dlgen -c etc/dlgen.cfg)"
  chmod 0440 /opt/onzerelaties/etc/config.php
fi

# Put OnzeRelaties back online
if [ -f /opt/onzerelaties/var/maintenance_rpm.txt ]; then
  /opt/onzerelaties/bin/mmm_online
  rm /opt/onzerelaties/var/maintenance_rpm.txt
fi

