#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Library for working with Data Matrix 2D bar-codes
Summary(pl.UTF-8):	Biblioteka do pracy z kodami paskowymi Data Matrix 2D
Name:		libdmtx
Version:	0.7.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/dmtx/libdmtx/releases
Source0:	https://github.com/dmtx/libdmtx/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	82edcd68e9f4fa779f5f7573baf2a9f5
URL:		https://github.com/dmtx/libdmtx
BuildRequires:	ImageMagick-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
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

%description -l pl.UTF-8
libdmtx to mające otwarte źródła oprogramowanie do odczytu i zapisu
kodów paskowych Data Matrix 3D pod Linuksem, Uniksem, OS X, Windows i
na platformach mobilnych. Główną częścią jest biblioteka
współdzielona, pozwalająca programom w C/C++ korzystać ze swoich
możliwości bez ograniczeń czy narzutów.

Załączone programy użytkowe - dmtxread i dmtxwrite - udostępniają
oficjalny interfejs libdmtx z poziomu linii poleceń, a także służą
jako dobre przykłady dla programistów chcących pisać własne programy
współpracujące z libdmtx.

%package devel
Summary:	Development files for libdmtx library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libdmtx
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use libdmtx.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libdmtx.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static

%{__make}

%if %{with tests}
%{__make} check \
	AM_CPPFLAGS+=-std=c99
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
%doc AUTHORS ChangeLog KNOWNBUG LICENSE NEWS README README.linux TODO
%attr(755,root,root) %{_libdir}/libdmtx.so.*.*.*
%ghost %{_libdir}/libdmtx.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdmtx.so
%{_includedir}/dmtx.h
%{_pkgconfigdir}/libdmtx.pc
%{_mandir}/man3/libdmtx.3*
