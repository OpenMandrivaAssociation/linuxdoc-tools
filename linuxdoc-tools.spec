Summary: A text formatting package based on SGML
Name: linuxdoc-tools
Obsoletes: linuxdoc-sgml
Version: 0.9.21
Release: %mkrel 14
License: Freely distributable
Group: Publishing
Source: http://people.debian.org/~sano/linuxdoc-tools/archives/%{name}_%{version}.tar.bz2
Patch0: linuxdoc-tools-0.9.21-letter.patch
Patch1: linuxdoc-tools-0.9.20-strip.patch
Patch2: linuxdoc-tools-ifpdf.patch
Requires: jade
Requires: docbook-utils
#gw needed by sgml2info
Requires: texinfo
Url: http://people.debian.org/~sano/linuxdoc-tools/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires:	flex
BuildRequires:	openjade
BuildRequires:	sgml-common
BuildRequires:	groff-for-man
Requires: tetex-latex gawk groff
Provides: sgml-tools
Provides: linuxdoc-sgml

%description
Linuxdoc-tools is a text formatting suite based on SGML (Standard
Generalized Markup Language), using the LinuxDoc document type.
Linuxdoc-tools allows you to produce LaTeX, HTML, GNU info, LyX, RTF,
plain text (via groff), and other format outputs from a single SGML
source.  Linuxdoc-tools is intended for writing technical software
documentation.

%prep
%setup -q
%patch0 -p1 -b .letter
%patch1 -p1 -b .strip
%patch2 -p1 -b .ifpdf

%build
%configure2_5x --with-installed-nsgmls --with-installed-iso-entities
# Packaging brain-damage
( cd entity-map
  autoconf
  %configure2_5x
)
%make OPTIMIZE="%{optflags}"
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           lib/LinuxDocTools.pm

%install
rm -rf %{buildroot}
%makeinstall
mv %{buildroot}%{_docdir}/%{name} %{buildroot}%{_docdir}/%{name}-%{version}
perl -pi -e 's,/usr/share/sgml/iso-entities-8879.1986/iso-entities.cat,\$main::prefix/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           %{buildroot}%{_datadir}/%{name}/LinuxDocTools.pm

# Some files need moving around.
rm -f %{buildroot}%{_datadir}/%{name}/epsf.*
rm -f %{buildroot}%{_datadir}/%{name}/url.sty
install -d %{buildroot}%{_datadir}/texmf/tex/latex/misc
mv %{buildroot}%{_datadir}/%{name}/*.sty \
	%{buildroot}%{_datadir}/texmf/tex/latex/misc

# Move perl modules to perl_vendorlib
mkdir -p %{buildroot}%{perl_vendorlib}/Text
mv %{buildroot}%{_libdir}/perl5/Text/EntityMap.pm \
	%{buildroot}%{perl_vendorlib}/Text/

cat > doc/COPYRIGHT <<EOF
(C) International Organization for Standardization 1986
Permission to copy in any form is granted for use with
conforming SGML systems and applications as defined in
ISO 8879, provided this notice is included in all copies.
EOF

%clean
rm -rf %{buildroot}

%post
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%postun
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%files
%defattr (-,root,root)
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%{perl_vendorlib}/Text/*.pm
%{_mandir}/*/*

