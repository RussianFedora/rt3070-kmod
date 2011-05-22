# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

Name:		rt3070-kmod
Version:	2.3.0.4
Release:	1%{?dist}.1.R
Summary:	Kernel module for wireless devices with Ralink's rt307x chipsets

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/support.php?s=2
# No more direct link. The file is downloaded from the above page.
Source0:	DPO_RT3070_LinuxSTA_V2.3.0.4_20100604.tar.bz2
Source11:	rt3070-kmodtool-excludekernel-filterfile
Patch0:		rt3070-2.6.34.patch
Patch1:		rt3070-no2.4-in-kernelversion.patch
Patch2:		rt3070-Makefile.x-fixes.patch
Patch3:		rt3070-additional-devices.patch
Patch4:		rt3070-strip-tftpboot-copy.patch
Patch6:		rt3070-suppress-flood.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the documentation and configuration files for the Ralink
Driver for WiFi, a linux device driver for USB 802.11a/b/g universal NIC cards
that use Ralink rt307x chipsets.

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
pushd *RT3070*Linux*STA*
%patch0 -p1 -b .2.6.34
%patch1 -p1 -b .no24
%patch2 -p1 -b .rpmbuild
%patch3 -p1 -b .adddev
%patch4 -p1 -b .tftpboot
%patch6 -p1 -b .messageflood

# Fix permissions
for ext in c h; do
 find  . -name "*.$ext" -exec chmod -x '{}' \;
done

# To avoid possible conflict with rt2870 driver:
for sta in common/rtmp_init.c include/rt_ate.h include/os/rt_linux.h README_STA* RT2870STACard.dat ; do
 sed 's|RT2870STA|RT3070STA|g' $sta > tmp.sta
 touch -r $sta tmp.sta
 mv tmp.sta $sta
done
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a *RT3070*Linux*STA* _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" INST_DIR=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Aug 31 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.4-1
- Update to 2.3.0.4

* Sun Jun 27 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.2-1
- Update to 2.3.0.2

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.7
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.6
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-3.1
- rebuild for new kernels

* Sat Aug 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-3
- Suppress a flood of system log messages

* Mon Aug 03 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com>- 2.1.1.0-2
- Fix for kernels >= 2.6.31

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.3
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.2
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.1
- rebuild for new kernels

* Sat May 23 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- update to 2.1.1.0

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1.0-3
- rebuild for new F11 features

* Sun Feb 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.0.1.0-2
- Fix the 2.6.29 patch

* Thu Jan 15 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.0.1.0-1
- Initial build
