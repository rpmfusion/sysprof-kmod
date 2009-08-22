# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:           sysprof-kmod
Summary:        Kernel module for sysprof
Version:        1.0.12
Release:        2%{?dist}.15

Group:          System Environment/Kernel
License:        GPLv2+
URL:            http://www.daimi.au.dk/~sandmann/sysprof/
Source0:        http://www.daimi.au.dk/~sandmann/sysprof/sysprof-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         sysprof-avoid_depmod.patch

ExclusiveArch:  i686 x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
%{summary}.


%prep
%{?kmodtool_check}
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c
pushd sysprof-%{version}
%patch0 -p1 -b .patch0
# configure script breaks in mock builds (missing BRs), so we create here 
# a config.h with the needed symbol
echo '#define PACKAGE_VERSION "%{version}"' > config.h
popd

for kernel_version  in %{?kernel_versions} ; do
    cp -a sysprof-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kv in %{?kernel_versions} ; do
    d=$PWD/_kmod_build_${kv%%___*}
    pushd $d/module
    make KDIR="${kv##*___}"
    popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kv in %{?kernel_versions} ; do
    d=$RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kv%%___*}/%{kmodinstdir_postfix}
    install -dm 755 $d
    install -pm 755 _kmod_build_${kv%%___*}/module/sysprof-module.ko $d
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.15
- rebuild for new kernels

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.14
- rebuild for new kernels

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.13
- rebuild for new kernels

* Fri Jul 31 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.12
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.11
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.10
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.9
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0.12-2
- rebuild for new F11 features

* Wed Feb 11 2009 Gianluca Sforna <giallu gmail com> - 1.0.12-1
- version update to 1.0.12
- adapt to rpmfusion akmod

* Thu Jun 12 2008 Gianluca Sforna <giallu gmail com> - 1.0.10-1
- version update to 1.0.10

* Wed Apr  9 2008 Gianluca Sforna <giallu gmail com> - 1.0.9-1
- version update to 1.0.9

* Tue Jan 22 2008 Gianluca Sforna <giallu gmail com> - 1.0.8-2
- Fix upgrade path from F7

* Sat Nov  3 2007 Gianluca Sforna <giallu gmail com>
- Really avoid depmod 

* Tue Aug 21 2007 Gianluca Sforna <giallu gmail com>
- Update License field

* Thu Jul 26 2007 Gianluca Sforna <giallu gmail com>
- No more i586 builds
- disable kdump
  (see http://article.gmane.org/gmane.linux.redhat.fedora.devel/59829)

* Fri Jan  5 2007 Gianluca Sforna <giallu gmail com>
- rebuild for kernel 2.6.19-1.2904

* Thu Dec 23 2006 Gianluca Sforna <giallu gmail com>
- rebuild for kernel 2.6.19-1.2891

* Thu Dec 22 2006 Gianluca Sforna <giallu gmail com>
- rebuild for kernel 2.6.19-1.2890

* Thu Dec 21 2006 Gianluca Sforna <giallu gmail com> 1.0.8-1
- version update
- rebuild for kernel 2.6.19-1.2889
- disable xen variant (all archs) and kdump (on i686)

* Sun Nov 19 2006 Gianluca Sforna <giallu gmail com> 1.0.7-1.1
- version update
- use Release 1.1 to be sure EVR in devel is newer than FC6

* Wed Nov  1 2006 Gianluca Sforna <giallu gmail com> 1.0.5-1
- version update
- drop upstreamed patch

* Tue Oct 17 2006 Gianluca Sforna <giallu gmail com>
- rebuild for kernel 2.6.18-1.2798

* Sun Oct 8 2006 Gianluca Sforna <giallu gmail com> 1.0.3-5
- rebuild for kernel 2.6.18-1.2747
- add patch for linux/config.h include

* Thu Oct 5 2006 Gianluca Sforna <giallu gmail com> 1.0.3-3
- rebuild

* Thu Oct 5 2006 Gianluca Sforna <giallu gmail com> 1.0.3-2
- remove (not supported) ppc arch

* Thu Jun 22 2006 Gianluca Sforna <giallu gmail com> 1.0.3-1
- version update
- fixed rpmlint warning about summary 

* Sat May 13 2006 Gianluca Sforna <giallu gmail com> 1.0.2-2
- removed some unnecessary diffs from the template spec

* Sat May 13 2006 Gianluca Sforna <giallu gmail com> 1.0.2-1
- Initial Version
