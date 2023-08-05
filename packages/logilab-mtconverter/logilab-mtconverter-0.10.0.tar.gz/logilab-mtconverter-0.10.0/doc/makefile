all: apydoc

apydoc:
	epydoc -o apidoc --html -v --graph all --no-private --exclude="__pkginfo__" --exclude="setup" -n "Logilab's mtconverter library" ../logilab/mtconverter

clean:
	rm -rf apidoc
