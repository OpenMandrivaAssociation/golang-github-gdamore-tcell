%global debug_package %{nil}  # Don't actually install any built things.
%global goipath         github.com/gdamore/tcell
Version:                1.1.0

%gometa

%global common_description %{expand:
Package tcell provides a cell based view for text terminals, like xterm. It was
inspired by termbox, but differs from termbox in some important ways. It also
adds substantial functionality beyond termbox.}

Name:           %{goname}
Release:        1%{?dist}
Summary:        An alternate terminal package
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

%description
%{common_description}


%package devel
Summary:       %{summary}
BuildArch:     noarch

BuildRequires: golang(github.com/gdamore/encoding)
BuildRequires: golang(github.com/lucasb-eyer/go-colorful)
BuildRequires: golang(github.com/mattn/go-runewidth)
BuildRequires: golang(github.com/smartystreets/goconvey/convey)
BuildRequires: golang(golang.org/x/text/encoding)
BuildRequires: golang(golang.org/x/text/encoding/charmap)
BuildRequires: golang(golang.org/x/text/encoding/japanese)
BuildRequires: golang(golang.org/x/text/encoding/korean)
BuildRequires: golang(golang.org/x/text/encoding/simplifiedchinese)
BuildRequires: golang(golang.org/x/text/encoding/traditionalchinese)
BuildRequires: golang(golang.org/x/text/transform)

# These are all needed for rebuilding the terminfo database.
BuildRequires: ncurses-base
BuildRequires: ncurses-term
BuildRequires: rxvt-unicode

%description devel
%{common_description}

This package contains library source intended for building other packages
which use import path with %{goipath} prefix.


%prep
%gosetup -q

rm -rf terminfo/database terminfo/term_*.go
mkdir terminfo/database


%build
%gobuildroot

# Rebuild database from source.
%gobuild -o _bin/mkinfo terminfo/mkinfo.go
pushd terminfo
../_bin/mkinfo -all
popd

# Demo executables; not used for anything.
for f in boxes mouse unicode; do
    %gobuild -o _bin/${f} _demos/${f}.go
done


%install
%goinstall


%check
%gochecks


%files devel -f devel.file-list
%doc README.md AUTHORS
%license LICENSE


%changelog
* Wed Oct 10 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.0-1
- Update to latest version
- Rebuild terminfo from Fedora information

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.0.0-2
- Re-template against More Go Packaging guidelines

* Fri Mar 16 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.0.0-1
- Update to first released version
- Check build of demos

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.2.20170807gitd55f61c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0-0.1.20170807gitd55f61c
- Add commit date to revision

* Fri Aug 18 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0-0.1.gitd55f61c
- Initial package for Fedora
