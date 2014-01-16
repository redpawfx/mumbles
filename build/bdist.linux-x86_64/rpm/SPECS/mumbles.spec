%define name mumbles
%define version 0.4
%define unmangled_version 0.4
%define release 15.fc15

Summary: Mumbles is notification system for the Gnome desktop.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: dot_j <dot_j@mumbles-project.org>
Url: http://www.mumbles-project.org/

%description
Mumbles is a plugin-driven, DBus based notification system written for the Gnome desktop. Similar to libnotify notifications and Growl for OSX (http://growl.info), Mumbles aims to provide a modern notification system for the GNU/Linux Desktop.

%prep
%setup -n %{name}-%{unmangled_version}

%build
/usr/bin/python setup.py build

%install
/usr/bin/python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
#rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
