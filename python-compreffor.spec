#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-compreffor.spec)

Summary:	CFF table subroutinizer for FontTools
Summary(pl.UTF-8):	Generator podprocedur tablic CFF dla FontTools
Name:		python-compreffor
# keep 0.4.x here for python2 support
Version:	0.4.6.post1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/compreffor/
Source0:	https://files.pythonhosted.org/packages/source/c/compreffor/compreffor-%{version}.zip
# Source0-md5:	202273efacb23031fc87352527ace317
URL:		https://pypi.org/project/compreffor/
BuildRequires:	libstdc++-devel >= 6:4.3
%if %{with python2}
BuildRequires:	python-Cython >= 0.28.4
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-fonttools >= 3.1
BuildRequires:	python-pytest >= 2.8
%endif
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.28.4
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-fonttools >= 3.1
BuildRequires:	python3-pytest >= 2.8
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	python-modules >= 1:2.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CFF table subroutinizer for FontTools.

%description -l pl.UTF-8
Generator podprocedur tablic CFF dla FontTools.

%package -n python3-compreffor
Summary:	CFF table subroutinizer for FontTools
Summary(pl.UTF-8):	Generator podprocedur tablic CFF dla FontTools
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-compreffor
CFF table subroutinizer for FontTools.

%description -n python3-compreffor -l pl.UTF-8
Generator podprocedur tablic CFF dla FontTools.

%prep
%setup -q -n compreffor-%{version}

# move out of compreffor dir, so that:
# - `import compreffor` can search built-* dirs with binary modules instead of src
# - we don't package tests
%{__mv} src/python/compreffor/test tests
%{__sed} -i -e 's/compreffor\.test\.dummy/.dummy/' tests/pyCompressor_test.py

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/compreffor{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/compreffor-2
%dir %{py_sitedir}/compreffor
%attr(755,root,root) %{py_sitedir}/compreffor/_compreffor.so
%{py_sitedir}/compreffor/*.py[co]
%{py_sitedir}/compreffor-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-compreffor
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/compreffor
%dir %{py3_sitedir}/compreffor
%attr(755,root,root) %{py3_sitedir}/compreffor/_compreffor.cpython-*.so
%{py3_sitedir}/compreffor/*.py
%{py3_sitedir}/compreffor/__pycache__
%{py3_sitedir}/compreffor-%{version}-py*.egg-info
%endif
