# TODO
# - java bindings
#
# Conditional build:
%bcond_with	ruby		# build Ruby bindings
%bcond_without	python	# build Python2 bindings
%bcond_without	php		# build PHP bindings
%bcond_without	tests		# build without tests

Summary:	Library for working with Data Matrix 2D bar-codes
Name:		libdmtx
Version:	0.7.2
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libdmtx/%{name}-%{version}.tar.bz2
# Source0-md5:	0684cf3857591e777b57248d652444ae
URL:		http://www.libdmtx.org/
BuildRequires:	ImageMagick-devel
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL_image-devel
BuildRequires:	libpng-devel
%endif
%if %{with php}
BuildRequires:	%{php_name}-devel
%endif
%if %{with python}
BuildRequires:	python-devel
%endif
%if %{with ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
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

%package utils
Summary:	Utilities for %{name}
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description utils
The %{name}-utils package contains utilities that use %{name}.

%package -n %{php_name}-dmtx
Summary:	PHP bindings for %{name}
License:	GPL v2+
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}
Provides:	php(dmtx) = %{version}
Obsoletes:	php-libdmtx < 0.7.2-4

%description -n %{php_name}-dmtx
This package contains bindings for using %{name} from PHP.

%package -n python-libdmtx
Summary:	Python bindings for %{name}
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libdmtx
The python-%{name} package contains bindings for using %{name} from
Python.

%package -n ruby-libdmtx
Summary:	Ruby bindings for %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	ruby(%{name}) = %{version}

%description -n ruby-libdmtx
The ruby-%{name} package contains bindings for using %{name} from
Ruby.

%prep
%setup -q

# fix permissions
chmod a-x wrapper/{php,python}/README

%build
%configure \
	--disable-static

%{__make}

# temporary installation required by the language wrappers
install -d tmp
%{__make} install \
	DESTDIR=$(pwd)/tmp

# language wrappers must be built separately
cd wrapper

%if %{with php}
cd php
phpize
%configure \
	--disable-static \

%{__make} \
	EXTRA_CFLAGS="-I$(pwd)/../../tmp%{_includedir}" \
	DMTX_SHARED_LIBADD="-L$(pwd)/../../tmp%{_libdir} -ldmtx"
cd ..
%endif

%if %{with python}
cd python
# fix paths
sed -i.orig -e "s|%{_prefix}/local/include|$(pwd)/../../tmp%{_includedir}|" -e "s|%{_prefix}/local/lib|$(pwd)/../../tmp%{_libdir}|" setup.py
%{__python} setup.py build
chmod 0755 build/lib.*/*.so
cd ..
%endif

%if %{with ruby}
cd ruby
ruby extconf.rb
%{__make} \
	CPPFLAGS="-I$(pwd)/../../tmp%{_includedir}" \
	LIBPATH="-L$(pwd)/../../tmp%{_libdir} -ldmtx"
cd ..
%endif

#cd java
#make LIBDMTX_LA="/tmp%{_libdir}/libdmtx.so"
#cd ..
cd ..

%if %{with tests}
%{__make} check
cd test
for t in simple unit; do
	./${t}_test/${t}_test
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdmtx.la

cd wrapper
%if %{with php}
%{__make} -C php install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/dmtx.ini
; Enable dmtx extension module
extension=dmtx.so
EOF
%endif

%if %{with python}
cd python
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..
%py_postclean
%endif

%if %{with ruby}
%{__make} -C ruby install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.LESSER ChangeLog KNOWNBUG NEWS README README.linux TODO
%attr(755,root,root) %{_libdir}/libdmtx.so.*.*.*
%ghost %{_libdir}/libdmtx.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/dmtx.h
%{_pkgconfigdir}/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dmtxquery
%attr(755,root,root) %{_bindir}/dmtxread
%attr(755,root,root) %{_bindir}/dmtxwrite
%{_mandir}/man1/dmtxquery.1*
%{_mandir}/man1/dmtxread.1*
%{_mandir}/man1/dmtxwrite.1*

%if %{with php}
%files -n %{php_name}-dmtx
%defattr(644,root,root,755)
%doc COPYING wrapper/php/README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/dmtx.ini
%attr(755,root,root) %{php_extensiondir}/dmtx.so
%endif

%if %{with python}
%files -n python-libdmtx
%defattr(644,root,root,755)
%doc wrapper/python/README
%{py_sitedir}/pydmtx.py[co]
%attr(755,root,root) %{py_sitedir}/_pydmtx.so
%{py_sitedir}/pydmtx-*.egg-info
%endif

%if %{with ruby}
%files -n ruby-libdmtx
%defattr(644,root,root,755)
%doc wrapper/ruby/README
%attr(755,root,root) %{ruby_sitearchdir}/*.so
%endif
