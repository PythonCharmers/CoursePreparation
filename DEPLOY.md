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

This is built and live (account `863275378519`, profile `pythoncharmers`).
Cut over from GitBook on 2026-09-03.

| Piece | Value |
|---|---|
| Bucket | `prep.pythoncharmers.com-static`, ap-southeast-2, all public access blocked |
| Distribution | `E860X92Z46FIJ` — `davhmfb96k65s.cloudfront.net` |
| Certificate | `arn:aws:acm:us-east-1:863275378519:certificate/af21a93a-7899-4b4d-9867-6c3510846918` |
| Origin access control | `E26W5NP176KK7A` |
| Viewer-request function | `charmers-static-index-rewrite` (shared with the brand sites) |
| Deploy role | `arn:aws:iam::863275378519:role/prep-pythoncharmers-deploy` |
| OIDC provider | `token.actions.githubusercontent.com` |
| DNS | `prep.pythoncharmers.com` A-record alias to the distribution |

### If you ever rebuild this

The commands mirror `charmers_website_project/deploy/STATIC_SITES.md`, whose
scripts do most of the work — run them from that repo:

```bash
aws s3api create-bucket --bucket prep.pythoncharmers.com-static \
    --region ap-southeast-2 \
    --create-bucket-configuration LocationConstraint=ap-southeast-2 \
    --profile pythoncharmers
aws s3api put-public-access-block --bucket prep.pythoncharmers.com-static \
    --profile pythoncharmers \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

aws acm request-certificate --region us-east-1 \
    --domain-name prep.pythoncharmers.com \
    --validation-method DNS --profile pythoncharmers
uv run python scripts/validate_acm_certificate.py <arn> --wait

uv run python scripts/create_static_site_distribution.py \
    --bucket prep.pythoncharmers.com-static \
    --alias prep.pythoncharmers.com \
    --certificate-arn <arn>

# Then a Route 53 A-record alias to the distribution's d....cloudfront.net
# domain, hosted zone Z2FDTNDATAQYW2 (CloudFront's fixed zone id).
```

**The one trap, if the name is ever pointed at a third-party host again:** ACM
checks CAA records on the name it is issuing for, and CAA is inherited from a
CNAME's *target*, not from our zone. While `prep` was a CNAME to
`hosting.gitbook.com` it inherited GitBook's CAA, which authorises DigiCert,
Google and Let's Encrypt but not Amazon, so ACM failed with `CAA_ERROR`. Adding
our own CAA at `prep` was not possible either, because DNS forbids a CNAME
coexisting with any other record at the same name. The CNAME had to go first.

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

All four repository settings are in place:

| Setting | Kind | Value |
|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | secret | `arn:aws:iam::863275378519:role/prep-pythoncharmers-deploy` |
| `AWS_REGION` | variable | `ap-southeast-2` |
| `S3_BUCKET` | variable | `prep.pythoncharmers.com-static` |
| `CLOUDFRONT_DISTRIBUTION_ID` | variable | `E860X92Z46FIJ` |

The role trusts only `repo:PythonCharmers/CoursePreparation:ref:refs/heads/master`,
so a pull request from a fork cannot assume it, and its policy grants nothing
beyond writing to that one bucket and invalidating that one distribution.

## The GitBook cutover

Done on 2026-09-03. `prep.pythoncharmers.com` previously CNAME'd to GitBook's
hosted service; it is now an A-record alias to the CloudFront distribution.

Before switching, the live GitBook site was compared against this repository —
it served the same 19 pages, with nothing written in GitBook's web editor that
was not already in git.

**The GitBook space itself has not been touched.** Leave it in place until the
new site has been serving for a few weeks, then delete it there. Nothing points
at it now.

The old GitBook files — `book.json`, `SUMMARY.md`, `INSTALL.md` and the
`gitbook serve` Makefile — have been removed. `mkdocs.yml` is the live
configuration and the nav lives there; the originals are in git history if you
need to refer back to them.
