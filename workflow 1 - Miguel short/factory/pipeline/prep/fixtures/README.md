# pipeline/prep/fixtures

Frozen copies of the run artifacts the regression suite reads (2026-09-20). Run folders are disposable
and get retired, so a test may never point at `shorts_run<N>/`. Small files (markers, manifests,
transcripts, reader records, selections) are tracked; matte layers (`*.webm`) are local-only and the
tests that hash them print SKIP when they are absent. Paths inside these JSON files are historical
values, not dependencies.
