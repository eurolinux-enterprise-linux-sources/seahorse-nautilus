Name:           seahorse-nautilus
Version:        3.8.0
%global         release_version %(echo %{version} | awk -F. '{print $1"."$2}')
Release:        5%{?dist}
Summary:        PGP encryption and signing for nautilus
License:        GPLv2+
URL:            https://live.gnome.org/Seahorse
Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/%{release_version}/%{name}-%{version}.tar.xz

# improve man page
Patch0: seahorse-tool-man.patch
# rhbz#1093123
Patch1: Add-correct-flag-for-reaping-the-progress-child.patch

BuildRequires:  gtk3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcr-devel
BuildRequires:  gnupg2
BuildRequires:  gpgme-devel >= 1.0
BuildRequires:  nautilus-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libcryptui-devel
BuildRequires:  libnotify-devel
BuildRequires:  intltool

Obsoletes: seahorse-plugins < 3.0

%description
Seahorse nautilus is an extension for nautilus which allows encryption
and decryption of OpenPGP files using GnuPG.


%prep
%setup -q
%patch0 -p1 -b .man
%patch1 -p1 -b .sigchld


%build
%configure --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/seahorse-pgp-encrypted.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/seahorse-pgp-keys.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/seahorse-pgp-signature.desktop

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%find_lang %{name} --with-gnome


%postun
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README THANKS
%{_bindir}/seahorse-tool
%{_libdir}/nautilus/extensions-3.0/libnautilus-seahorse.so
%{_datadir}/applications/*.desktop
%{_datadir}/GConf/gsettings/org.gnome.seahorse.nautilus.convert
%{_datadir}/glib-2.0/schemas/org.gnome.seahorse.nautilus.*gschema.xml
%{_datadir}/seahorse-nautilus/
%{_mandir}/man1/seahorse-tool.1*


%changelog
* Fri May  2 2014 Rui Matos <rmatos@redhat.com> - 3.8.0-5
- Fix for "seahorse-nautilus broken by glib2 regression related to
  SIGCHLD warnings"
- Resolves: #1093123

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.0-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.0-3
- Mass rebuild 2013-12-27

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.0-2
- Improve the man page
- Resolves: #948925

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92
- Install the gsettings schema files

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Rui Matos <rmatos@redhat.com> - 3.4.0-2
- Use rpm macros to define the version number
- Do verbose builds
- Fix %%files entries to comply with ownership rules

* Tue Mar 27 2012 Rui Matos <rmatos@redhat.com> - 3.4.0-1
- initial packaging for Fedora
