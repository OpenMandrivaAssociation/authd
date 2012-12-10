%define lib_name_orig lib%{name} 
%define lib_major 0
%define lib_name %mklibname %name %{lib_major}
%define develname %mklibname -d %name

Summary:	Software for obtaining and verifying user credentials 
Name:		authd
Version:	0.2.3
Release:	%mkrel 5
License:	BSD-Like
Group:		System/Servers
URL:		http://www.cs.berkeley.edu/~bnc/authd/
Source:		http://www.theether.org/authd/%{name}-%{version}.tar.gz
Source1:	authd.init
Patch0:		authd-Makefile.in.patch
Patch1:		authd-linkage_fix.diff
Requires:	openssh-clients
Requires:	openssh-server
Requires(post): rpm-helper
Requires(preun): rpm-helper
Buildrequires:	libe-cluster >= 0.2
Buildrequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package -n	%{develname}
Summary:	Devel Package for authd 
Group:          Development/Other
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{lib_name}-devel
Obsoletes:	lib%{name}%{lib_major}-devel

%description
authd is a software package for obtaining and verifying user credentials 
which contain cryptographic signatures based on RSA public key cryptography. 
It includes a server (authd) for authenticating local users through UNIX 
domain sockets and processing credentials, and a client library (libauth.a) 
for requesting new credentials and verifying credentials signed by the server.

%description -n	%{develname} 
authd is a software package for obtaining and verifying user credentials
which contain cryptographic signatures based on RSA public key cryptography.
Provide file auth.h and libauth.a .

%prep

%setup -q
%patch0 -p1 -b .patch
%patch1 -p0

chmod 644 ChangeLog COPYING

%build
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_REENTRANT"

%configure2_5x

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}

%makeinstall INSTALL_USER=%(id -un) INSTALL_GROUP=%(id -gn)
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/authd

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root) 
%doc ChangeLog COPYING
%{_initrddir}/authd
%{_sbindir}/authd

%files	-n %{develname}
%defattr(-,root,root)
%{_includedir}/auth.h
%{_libdir}/libauth.a



%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.3-5mdv2011.0
+ Revision: 610006
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 0.2.3-4mdv2010.1
+ Revision: 537555
- rebuild

* Tue Feb 09 2010 Antoine Ginies <aginies@mandriva.com> 0.2.3-3mdv2010.1
+ Revision: 502816
- fix patch0 pb (initscript)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

* Thu Aug 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.3-1mdv2009.0
+ Revision: 271983
- 0.2.3
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Feb 12 2008 Antoine Ginies <aginies@mandriva.com> 0.2.2-4mdv2008.1
+ Revision: 165746
- fix executable-marked-as-config-file

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Jul 17 2007 Funda Wang <fwang@mandriva.org> 0.2.2-4mdv2008.0
+ Revision: 52830
- fix prereq
- New devel package policy


* Thu Mar 01 2007 Antoine Ginies <aginies@mandriva.com> 0.2.2-3mdv2007.0
+ Revision: 130581
- Import authd

* Thu Apr 20 2006 Erwan Velu <erwan@seanodes.com> 0.2.2-3mdk
- Fixing buildrequires

* Sat Apr 15 2006 Erwan Velu <erwan@seanodes.com> 0.2.2-2mdk
- Rebuild

* Fri Oct 29 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.2-1mdk
- Remove patch1 merged upstream

* Wed Aug 04 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.1-17mdk
- Fixing Provides

* Fri Jun 11 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.1-16mdk
- Fixing RSA_sign & RSA_verify with NID_md5

* Thu Apr 22 2004 Erwan Velu <erwan@mandrakesoft.com> 0.2.1-15mdk
- Rebuild

