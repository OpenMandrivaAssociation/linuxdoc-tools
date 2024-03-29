Summary:	A text formatting package based on SGML
Name:		linuxdoc-tools
Version:	0.9.82
Release:	1
License:	Freely distributable
Group:		Publishing
Url:		https://packages.debian.org/sid/linuxdoc-tools
Source0:	http://http.debian.net/debian/pool/main/l/linuxdoc-tools/linuxdoc-tools_%{version}.orig.tar.gz
Patch0:		linuxdoc-tools-0.9.82-fix-configure-checks.patch
Patch1:		https://src.fedoraproject.org/rpms/linuxdoc-tools/raw/master/f/linuxdoc-tools-0.9.20-lib64.patch

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
%autosetup -p1
autoreconf -i

%build
%configure \
	--with-installed-nsgmls \
	--with-installed-iso-entities \
	--disable-docs
# Packaging brain-damage
cd entity-map
autoconf
%configure --enable-docs pdf
cd ..

%make OPTIMIZE="%{optflags}"
perl -pi -e 's,\$main::prefix/share/sgml/iso-entities-8879.1986/iso-entities.cat,/usr/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           lib/LinuxDocTools.pm

%install
%make_install perl5libdir=%{perl_vendorlib}

perl -pi -e 's,/usr/share/sgml/iso-entities-8879.1986/iso-entities.cat,\$main::prefix/share/sgml/sgml-iso-entities-8879.1986/catalog,' \
           %{buildroot}%{_datadir}/%{name}/LinuxDocTools.pm

# Some files need moving around.
rm -f %{buildroot}%{_datadir}/%{name}/epsf.*
rm -f %{buildroot}%{_datadir}/%{name}/url.sty
install -d %{buildroot}%{_datadir}/texmf/tex/latex/misc
mv %{buildroot}%{_datadir}/%{name}/*.sty \
	%{buildroot}%{_datadir}/texmf/tex/latex/misc

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
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/entity-map
%{_datadir}/texmf/tex/latex/misc/*.sty
%{perl_vendorlib}/Text/*.pm
%{perl_vendorlib}/LinuxDocTools.pm
%{perl_vendorlib}/LinuxDocTools
%{_mandir}/*/*

