Summary:	A text formatting package based on SGML
Name:		linuxdoc-tools
Version:	0.9.21
Release:	22
License:	Freely distributable
Group:		Publishing
Url:		http://people.debian.org/~sano/linuxdoc-tools/
Source0:	http://people.debian.org/~sano/linuxdoc-tools/archives/%{name}_%{version}.tar.bz2
Patch0:		linuxdoc-tools-0.9.21-letter.patch
Patch1:		linuxdoc-tools-0.9.20-strip.patch
Patch2:		linuxdoc-tools-ifpdf.patch
Patch3:		linuxdoc-tools_0.9.68-yyleng.patch

BuildRequires:	flex-devel
BuildRequires:	openjade
BuildRequires:	sgml-common
BuildRequires:	groff-for-man
Requires:	docbook-utils
Requires:	gawk
Requires:	groff
Requires:	openjade
#gw needed by sgml2info
Requires:	tetex-latex
Requires:	texinfo

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
%patch3 -p1 -b .yyleng

%build
%configure2_5x \
	--with-installed-nsgmls \
	--with-installed-iso-entities
# Packaging brain-damage
( cd entity-map
  autoconf
  %configure2_5x
)
%make OPTIMIZE="%{optflags}"
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           lib/LinuxDocTools.pm

%install
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
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/Text
mv $RPM_BUILD_ROOT%{_libdir}/perl5/Text/EntityMap.pm \
	$RPM_BUILD_ROOT%{perl_vendorlib}/Text/

cat > doc/COPYRIGHT <<EOF
(C) International Organization for Standardization 1986
Permission to copy in any form is granted for use with
conforming SGML systems and applications as defined in
ISO 8879, provided this notice is included in all copies.
EOF

%post
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%postun
[ -x %{_bindir}/texhash ] && /usr/bin/env - %{_bindir}/texhash > /dev/null 2>&1
exit 0

%files
%doc %{_docdir}/%{name}-%{version}
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%{perl_vendorlib}/Text/*.pm
%{_mandir}/*/*

