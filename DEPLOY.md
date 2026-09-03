# Deploying prep.pythoncharmers.com

The notes are markdown in `docs/`, built into a static site by
[MkDocs](https://www.mkdocs.org/) with the
[Material](https://squidfunk.github.io/mkdocs-material/) theme, and served from
an S3 bucket behind CloudFront — the same pattern as the brand sites in
`charmers_website_project/deploy/STATIC_SITES.md`. The bucket blocks all public
access; only the distribution can read it, via Origin Access Control.

**This replaces the hosted GitBook space** that served `prep.pythoncharmers.com`
until now. See "Cutting over from GitBook" at the end before switching DNS.

## Working on the notes locally

```bash
make serve     # http://localhost:8000, live-reloads as you edit
make build     # one-off build into build/site
make check     # link, example and formatting checks
```

`make build` runs MkDocs with `--strict`, which fails on a broken internal
link or a page missing from the nav. `make check` covers what that cannot see:
`check_links.py` verifies every cross-reference anchor resolves,
`check_examples.py` extracts the backup programs from `problem_solving.md` and
actually runs them, and `fix_nbsp.py` strips invisible non-breaking spaces.
`check_urls.py` checks external links but is slow and noisy, so it is not in
`make check` — run it by hand every few months.

## Deploying

Merges to `master` deploy automatically via
`.github/workflows/deploy.yml`. To deploy by hand:

```bash
make deploy DISTRIBUTION=<distribution-id>
```

That builds, runs the checks, syncs to S3 and invalidates CloudFront. **Always
invalidate** — CloudFront caches aggressively, and a sync without an
invalidation leaves visitors on the old pages until they expire.

## Standing up the infrastructure

This has not been created yet. The steps mirror
`charmers_website_project/deploy/STATIC_SITES.md`, and its scripts do most of
the work — run them from that repo.

```bash
# 1. Bucket, with public access blocked
aws s3api create-bucket --bucket prep.pythoncharmers.com-static \
    --region ap-southeast-2 \
    --create-bucket-configuration LocationConstraint=ap-southeast-2 \
    --profile pythoncharmers
aws s3api put-public-access-block --bucket prep.pythoncharmers.com-static \
    --profile pythoncharmers \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# 2. Certificate, in us-east-1 -- CloudFront will not accept one from elsewhere.
#    A single name here: prep is a subdomain, so there is no apex/www pair.
aws acm request-certificate --region us-east-1 \
    --domain-name prep.pythoncharmers.com \
    --validation-method DNS --profile pythoncharmers
uv run python scripts/validate_acm_certificate.py <arn> --wait

# 3. Distribution, OAC and bucket policy
uv run python scripts/create_static_site_distribution.py \
    --bucket prep.pythoncharmers.com-static \
    --alias prep.pythoncharmers.com \
    --certificate-arn <arn>

# 4. Route 53 A-record alias for prep.pythoncharmers.com to the distribution's
#    d....cloudfront.net domain, hosted zone Z2FDTNDATAQYW2 (CloudFront's fixed
#    zone id, the same for every distribution).
```

Then put the distribution id into the `CLOUDFRONT_DISTRIBUTION_ID` repository
variable so the workflow can invalidate it.

### Two things that are not obvious

Both are inherited from the shared pattern and handled by
`create_static_site_distribution.py`:

**Directory URLs need a CloudFront Function.** MkDocs writes
`basics/index.html`, but a visitor asks for `/basics/`, and `DefaultRootObject`
only covers `/`. The shared `charmers-static-index-rewrite` function appends
`index.html`. Without it every page below the root 404s.

**S3 returns 403, not 404, for a missing object** when reached through Origin
Access Control. Both codes are mapped to the 404 page with a 404 status;
mapping only 404 shows CloudFront's XML "Access Denied", which reads as a
permissions fault rather than a typo.

## CI

`.github/workflows/deploy.yml` builds and checks on every pull request, and
additionally deploys on a push to `master`. It authenticates to AWS with
OIDC — a role assumed from GitHub, so there are no long-lived keys in repo
secrets. Create the role with a trust policy for
`token.actions.githubusercontent.com`, restricted to this repository, granting
only `s3:PutObject`/`DeleteObject`/`ListBucket` on the bucket and
`cloudfront:CreateInvalidation` on the distribution.

Required repository settings:

| Setting | Kind | Value |
|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | secret | ARN of the deploy role |
| `AWS_REGION` | variable | `ap-southeast-2` |
| `S3_BUCKET` | variable | `prep.pythoncharmers.com-static` |
| `CLOUDFRONT_DISTRIBUTION_ID` | variable | the distribution id |

Until these exist the deploy step is skipped rather than failing, so the build
and checks still run on pull requests.

## Cutting over from GitBook

`prep.pythoncharmers.com` currently resolves to GitBook's hosted service. The
live site and this repository have been able to drift apart, so **before
switching DNS, check whether the GitBook space contains edits that were never
committed here** — anything written in GitBook's web editor would be lost.

Once the distribution is up, verify it over its `d....cloudfront.net` name
first, then repoint the Route 53 record. Keep the GitBook space in place,
unpublished, until the new site has been serving for a few weeks.

The old GitBook files — `book.json`, `SUMMARY.md`, `INSTALL.md` and the
`gitbook serve` Makefile — have been removed. `mkdocs.yml` is the live
configuration and the nav lives there; the originals are in git history if you
need to refer back to them.
