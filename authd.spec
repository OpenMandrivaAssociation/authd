%define name	authd
%define	version	0.2.2	
%define release %mkrel 4
%define lib_name_orig	lib%{name} 
%define lib_major 0
%define lib_name %mklibname %name %{lib_major}
%define develname %mklibname -d %name

Summary:	Software for obtaining and verifying user credentials 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.cs.berkeley.edu/~bnc/authd/
Source:		http://www.theether.org/authd/%{name}-%{version}.tar.gz
Source1:	authd.init
Patch0:		authd-Makefile.in.patch	
Requires:	openssh-clients, openssh-server
Requires(pre): 	rpm-helper	
Provides:	%{name}-%{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}
Buildrequires:  libe-cluster >= 0.2, openssl-devel

%package 	-n %{develname}
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

%description -n %{develname} 
authd is a software package for obtaining and verifying user credentials
which contain cryptographic signatures based on RSA public key cryptography.
Provide file auth.h and libauth.a .

%prep
rm -rf ${buildroot}
%setup -q
%patch0 -p0 -b .patch

%build
%configure --prefix=%{buildroot} \
		--bindir==%{buildroot}%{_bindir} \
		--libdir=%{buildroot}%{_libdir} \
		--sbindir=%{buildroot}%{_sbindir} \
		--sysconfdir=%{buildroot}%{_sysconfdir}
%make

%install
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}
%makeinstall INSTALL_USER=%(id -un) INSTALL_GROUP=%(id -gn)
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/authd

%clean
rm -fr %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root) 
%doc INSTALL ChangeLog
%config(noreplace) %{_initrddir}/authd
%{_sbindir}/authd

%files	-n %{develname}
%defattr(-,root,root)
%doc INSTALL ChangeLog
%{_includedir}/auth.h
%{_libdir}/libauth.a


