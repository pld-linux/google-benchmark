#
# Conditional build:
%bcond_with	python	# Python 3 module (requires Bazel to build, fails)
#
Summary:	Library to benchmark code snippets
Summary(pl.UTF-8):	Biblioteka do testowania wydajności fragmentów kodu
Name:		google-benchmark
Version:	1.7.1
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/benchmark/releases
Source0:	https://github.com/google/benchmark/archive/v%{version}/benchmark-%{version}.tar.gz
# Source0-md5:	0459a6c530df9851bee6504c3e37c2e7
URL:		https://github.com/google/benchmark
BuildRequires:	cmake >= 3.16.3
BuildRequires:	libstdc++-devel >= 6:4.8
%if %{with python}
BuildRequires:	bazel
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-pybind11
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library to benchmark code snippets, similar to unit tests.

%description -l pl.UTF-8
Biblioteka do testowania wydajności fragmentów kodu, podobnie do
testów jednostkowych.

%package devel
Summary:	Header files for Google Benchmark library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Google Benchmark
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Google Benchmark library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Google Benchmark.

%package -n python3-benchmark
Summary:	Python binding for Google Benchmark library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki Google Benchmark
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-benchmark
Python binding for Google Benchmark library.

%description -n python3-benchmark -l pl.UTF-8
Wiązanie Pythona do biblioteki Google Benchmark.

%prep
%setup -q -n benchmark-%{version}

%build
%cmake -B build \
	-DBENCHMARK_ENABLE_ASSEMBLY_TESTS=OFF \
	-DBENCHMARK_ENABLE_LTO=ON \
	-DBENCHMARK_ENABLE_TESTING=OFF

%{__make} -C build

%if %{with python}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS README.md docs/{AssemblyTests.md,tools.md}
%attr(755,root,root) %{_libdir}/libbenchmark.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbenchmark.so.1
%attr(755,root,root) %{_libdir}/libbenchmark_main.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbenchmark_main.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbenchmark.so
%attr(755,root,root) %{_libdir}/libbenchmark_main.so
%{_includedir}/benchmark
%{_pkgconfigdir}/benchmark.pc
%{_libdir}/cmake/benchmark

%if %{with python}
%files -n python3-benchmark
%defattr(644,root,root,755)
%dir %{py3_sitedir}/benchmark
%attr(755,root,root) %{py3_sitedir}/benchmark/_benchmark.cpython-*.so
%{py3_sitedir}/benchmark/__init__.py
%{py3_sitedir}/benchmark/__pycache__
%endif
