%define real_version 3.4.6
%define base_prefix /opt/kaltura/mencoder
%define debug_package %{nil}
Summary: Utilities and libraries for MPlayer movie encoder
Name: kaltura-mencoder
Version: %{real_version}
Release: 9 
License: GPL
Group: Applications/Multimedia
URL: http://www.mplayerhq.hu 

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

Source: svn://svn.mplayerhq.hu/mplayer/trunk/%{name}-%{real_version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: prelink
Requires:kaltura-a52dec,kaltura-libfaac,kaltura-libass,kaltura-x264
Provides: libmp3lame.so.0
Provides: libtwolame.so.0
Provides: libfaac.so.0
Provides: libschroedinger-1.0.so.0
Provides: libmad.so.0


%description
Utilities and libraries for MPlayer movie encoder

%prep
%setup -qn %{name}-%{real_version} 
rm -rf %{_builddir}/%{name}-%{real_version}/.svn
rm %{_builddir}/%{name}-%{real_version}/mencoder-dir/libjpeg*

%build

%install
mkdir -p  $RPM_BUILD_ROOT%{base_prefix}/bin
ls -al %{_builddir}/%{name}-%{real_version}
mv %{_builddir}/%{name}-%{real_version}/mencoder-dir/mencoder $RPM_BUILD_ROOT/%{base_prefix}/bin
mv %{_builddir}/%{name}-%{real_version}/mencoder-dir/* $RPM_BUILD_ROOT/%{base_prefix}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_mencoder.sh << EOF
PATH=\$PATH:%{base_prefix}/bin
export PATH
EOF
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/kaltura_mencoder.conf << EOF
/opt/kaltura/mencoder/ffmpeg32bit/lib
/opt/kaltura/mencoder
EOF

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{base_prefix}/lib/.so.*.*.* &>/dev/null || :
ln -fs %{base_prefix}/bin/mencoder /opt/kaltura/bin/

%postun 
/sbin/ldconfig
if [ "$1" = 0 ] ; then
	rm -f /opt/kaltura/bin/mencoder
fi


%files
%defattr(-, root, root, 0755)
%config %{_sysconfdir}/profile.d/kaltura_mencoder.sh
%config %{_sysconfdir}/ld.so.conf.d/kaltura_mencoder.conf
%{base_prefix}

%changelog
* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.4.6-1
- initial build.

* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.4.6-2
 Needs libjpeg-turbo.i386 for runtime and also, debugpackage %%{nil} cause of prelink issues... 
