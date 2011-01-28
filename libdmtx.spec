%bcond_with	ruby
%bcond_without	test
Summary:	Library for working with Data Matrix 2D bar-codes
Name:		libdmtx
Version:	0.7.2
Release:	1
License:	LGPL v2+
Group:		Libraries
URL:		http://www.libdmtx.org/
Source0:	http://downloads.sourceforge.net/libdmtx/%{name}-%{version}.tar.bz2
# Source0-md5:	0684cf3857591e777b57248d652444ae
BuildRequires:	ImageMagick-devel
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
# required for tests
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL_image-devel
BuildRequires:	libpng-devel
# language bindings
#BuildRequires:  java-1.6.0-devel
BuildRequires:	php-devel
BuildRequires:	python-devel
%if %{with ruby}
BuildRequires:	ruby
BuildRequires:	ruby-devel
%endif

%description
libdmtx is open source software for reading and writing Data Matrix 2D
bar-codes on Linux, Unix, OS X, Windows, and mobile devices. At its
core libdmtx is a shared library, allowing C/C++ programs to use its
capabilities without restrictions or overhead.

The included utility programs, dmtxread and dmtxwrite, provide the
official interface to libdmtx from the command line, and also serve as
a good reference for programmers who wish to write their own programs
that interact with libdmtx. All of the software in the libdmtx package
is distributed under the LGPLv2 and can be used freely under these
terms.

%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        utils
Summary:	Utilities for %{name}
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utilities that use %{name}.

# language bindings
%package -n     php-libdmtx
Summary:	PHP bindings for %{name}
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php-common

%description -n php-libdmtx
The php-%{name} package contains bindings for using %{name} from PHP.

%package -n     python-libdmtx
Summary:	Python bindings for %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-libdmtx
The python-%{name} package contains bindings for using %{name} from
Python.

%package -n     ruby-libdmtx
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
	--disable-static \

%{__make} %{?_smp_mflags}

# temporary installation required by the language wrappers
install -d tmp
%{__make} install \
	DESTDIR=$(pwd)/tmp

# language wrappers must be built separately
cd wrapper/php
phpize
%configure \
	--disable-static \

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{__make} \
	EXTRA_CFLAGS="-I$(pwd)/../../tmp%{_includedir}" \
	DMTX_SHARED_LIBADD="-L$(pwd)/../../tmp%{_libdir} -ldmtx"
cd ..

cd python
# fix paths
sed -i.orig -e "s|%{_prefix}/local/include|$(pwd)/../../tmp%{_includedir}|" -e "s|%{_prefix}/local/lib|$(pwd)/../../tmp%{_libdir}|" setup.py
python setup.py build
chmod 0755 build/lib.*/*.so
cd ..

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

%if %{with test}
%{__make} check
cd test
for t in simple unit
do
	./${t}_test/${t}_test
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

cd wrapper
%{__make} -C php install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cd python
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cd ..

%if %{with ruby}
%{__make} -C ruby install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

#pushd java
#popd
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING.LESSER ChangeLog KNOWNBUG NEWS README README.linux TODO
%attr(755,root,root) %{_libdir}/%{name}.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(755,root,root) %{_libdir}/%{name}.so
%{_pkgconfigdir}/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dmtx*
%{_mandir}/man1/dmtx*.1*

%files -n php-libdmtx
%defattr(644,root,root,755)
%doc COPYING wrapper/php/README
%attr(755,root,root) %{_libdir}/php/*.so

%files -n python-libdmtx
%defattr(644,root,root,755)
%doc wrapper/python/README
%{py_sitedir}/*

%if %{with ruby}
%files -n ruby-libdmtx
%defattr(644,root,root,755)
%doc wrapper/ruby/README
%attr(755,root,root) %{ruby_sitearchdir}/*.so
%endif
