BUCKET      ?= prep.pythoncharmers.com-static
DISTRIBUTION ?=
PROFILE     ?= pythoncharmers
SITE        := build/site

.PHONY: help serve build check deploy invalidate clean

help:
	@echo "make serve      - preview at http://localhost:8000 with live reload"
	@echo "make build      - build the site into $(SITE)"
	@echo "make check      - run the link, example and formatting checks"
	@echo "make deploy     - build, check, sync to S3 and invalidate CloudFront"
	@echo "make clean      - remove the build directory"

serve:
	uv run --with mkdocs-material mkdocs serve

build:
	uv run --with mkdocs-material mkdocs build --strict

# --strict already fails the build on a broken internal link, so these cover
# what it cannot see: the code examples actually running, and the external URLs.
check:
	uv run check_links.py
	uv run check_examples.py
	uv run sync_programs.py
	uv run fix_nbsp.py

deploy: build check
	@test -n "$(DISTRIBUTION)" || { echo "Set DISTRIBUTION=<id> (see DEPLOY.md)"; exit 1; }
	aws s3 sync $(SITE)/ s3://$(BUCKET)/ --delete --profile $(PROFILE)
	$(MAKE) invalidate

# CloudFront caches aggressively; a sync without this leaves visitors on the
# old pages until they expire.
invalidate:
	aws cloudfront create-invalidation --distribution-id $(DISTRIBUTION) \
	    --paths '/*' --profile $(PROFILE)

clean:
	rm -rf build/
