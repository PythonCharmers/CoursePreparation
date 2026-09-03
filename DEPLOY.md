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

**Already done** (account `863275378519`, profile `pythoncharmers`):

| Piece | Value |
|---|---|
| Bucket | `prep.pythoncharmers.com-static`, ap-southeast-2, all public access blocked |
| Deploy role | `arn:aws:iam::863275378519:role/prep-pythoncharmers-deploy` |
| OIDC provider | `token.actions.githubusercontent.com` |
| Repo settings | `AWS_DEPLOY_ROLE_ARN`, `AWS_REGION`, `S3_BUCKET` |

The built site has been synced to the bucket, so it is ready to serve as soon
as there is a distribution in front of it.

### Still to do: the certificate and distribution

**This is blocked until the DNS record moves**, for a reason worth
understanding before you try it.

ACM validates a certificate by checking CAA records on the name it is issuing
for. `prep.pythoncharmers.com` is currently a CNAME to `hosting.gitbook.com`,
and CAA is inherited from the CNAME's *target*, not from our zone. GitBook
publishes:

```
0 issue "digicert.com"
0 issue "pki.goog"
0 issue "letsencrypt.org"
```

Amazon is not on that list, so ACM fails with `CAA_ERROR`. Nor can we override
it by adding our own CAA at `prep`: DNS forbids any other record coexisting
with a CNAME at the same name, and Route 53 rejects the attempt.

So the order has to be:

```bash
# 1. Point prep at something we control. Either delete the GitBook CNAME
#    outright, or park it on a placeholder, then:
aws acm request-certificate --region us-east-1 \
    --domain-name prep.pythoncharmers.com \
    --validation-method DNS --profile pythoncharmers

# 2. Validate (run from charmers_website_project)
uv run python scripts/validate_acm_certificate.py <arn> --wait

# 3. Distribution, OAC and bucket policy (also from charmers_website_project)
uv run python scripts/create_static_site_distribution.py \
    --bucket prep.pythoncharmers.com-static \
    --alias prep.pythoncharmers.com \
    --certificate-arn <arn>

# 4. Route 53 A-record alias for prep.pythoncharmers.com to the distribution's
#    d....cloudfront.net domain, hosted zone Z2FDTNDATAQYW2 (CloudFront's fixed
#    zone id, the same for every distribution).
```

This means a short window where `prep.pythoncharmers.com` resolves to neither
the old site nor the new one — roughly the time ACM takes to issue plus the
distribution deploying, so plan it outside a course intake.

Finally, add the distribution id as the `CLOUDFRONT_DISTRIBUTION_ID` repository
variable, and tighten the deploy role's `cloudfront:CreateInvalidation`
statement from `"Resource": "*"` to that distribution's ARN.

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

| Setting | Kind | Value | Set? |
|---|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | secret | ARN of the deploy role | yes |
| `AWS_REGION` | variable | `ap-southeast-2` | yes |
| `S3_BUCKET` | variable | `prep.pythoncharmers.com-static` | yes |
| `CLOUDFRONT_DISTRIBUTION_ID` | variable | the distribution id | not yet |

Until all four exist the deploy step is skipped rather than failing, so the
build and checks still run on pull requests.

The role trusts only `repo:PythonCharmers/CoursePreparation:ref:refs/heads/master`,
so a pull request from a fork cannot assume it.

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
