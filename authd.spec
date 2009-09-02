%define lib_name_orig lib%{name} 
%define lib_major 0
%define lib_name %mklibname %name %{lib_major}
%define develname %mklibname -d %name

Summary:	Software for obtaining and verifying user credentials 
Name:		authd
Version:	0.2.3
Release:	%mkrel 3
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
%patch0 -p0 -b .patch
%patch1 -p0

chmod 644 ChangeLog COPYING

%build
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_REENTRANT"

%configure

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

