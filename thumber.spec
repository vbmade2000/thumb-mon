%define _unpackaged_files_terminate_build 0


Name: thumber
Version: 1
Release: 0
Summary: Thumb drive detector

License: GPL
URL: https://github.com/vbmade2000/thumber
BuildArch:      noarch
Source0: thumber-1.0.tar.gz
# BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-XXXXX)


%description
Daemon to detect thumb drive insertion and notify on various channels

%prep
%setup -n thumber

%build

%install
# rm -rf $RPM_BUILD_ROOT

# site-packages
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber
cp -rp . ${RPM_BUILD_ROOT}/usr/lib64/python2.7/site-packages/thumber


#install -m 0755 __init__.py $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber/__init__.py
#install -m 0755 logger.py $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber/logger.py
#install -m 0755 notifier.py $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber/notifier.py
#install -m 0755 thumbermain.py $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber/thumbermain.py

mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -a thumberd $RPM_BUILD_ROOT/usr/bin/thumberd

# /etc
install -m 0755 -d $RPM_BUILD_ROOT/etc/thumber
install -m 0755 thumber.conf $RPM_BUILD_ROOT/etc/thumber/thumber.conf

# service file
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system
install -m 0755 thumber.service $RPM_BUILD_ROOT/etc/systemd/system/thumber.service

# Plugins
# cp -Rf plugins $RPM_BUILD_ROOT/usr/lib64/python2.7/site-packages/thumber 


%files
%dir /usr/lib64/python2.7/site-packages/thumber
/usr/lib64/python2.7/site-packages/thumber/plugins
/usr/lib64/python2.7/site-packages/thumber/__init__.py
/usr/lib64/python2.7/site-packages/thumber/logger.py
/usr/lib64/python2.7/site-packages/thumber/notifier.py
/usr/lib64/python2.7/site-packages/thumber/thumbermain.py
#/usr/bin
/usr/bin/thumberd
/etc/thumber
/etc/thumber/thumber.conf
#/etc/systemd/system
/etc/systemd/system/thumber.service
# Exclude pyc and pyos
# %exclude /path_to_files/*.pyc



%changelog
* Fri Aug 16 2019 Malhar Vora <mlvora.2010@gmail.com> - 1.0
Initial spec

