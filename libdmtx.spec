#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Library for working with Data Matrix 2D bar-codes
Name:		libdmtx
Version:	0.7.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libdmtx/%{name}-%{version}.tar.bz2
# Source0-md5:	d3a4c0becd92895eb606dbdb78b023e2
URL:		http://www.libdmtx.org/
BuildRequires:	ImageMagick-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL_image-devel
BuildRequires:	libpng-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdmtx is open source software for reading and writing Data Matrix 2D
bar-codes on Linux, Unix, OS X, Windows, and mobile devices. At its
core libdmtx is a shared library, allowing C/C++ programs to use its
capabilities without restrictions or overhead.

The included utility programs, dmtxread and dmtxwrite, provide the
official interface to libdmtx from the command line, and also serve as
a good reference for programmers who wish to write their own programs
that interact with libdmtx.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
	--disable-static

%{__make}

%if %{with tests}
%{__make} check
./test/simple_test/simple_test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdmtx.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog KNOWNBUG NEWS README README.linux TODO
%attr(755,root,root) %{_libdir}/libdmtx.so.*.*.*
%ghost %{_libdir}/libdmtx.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/dmtx.h
%{_pkgconfigdir}/%{name}.pc
%{_mandir}/man3/%{name}.3*
