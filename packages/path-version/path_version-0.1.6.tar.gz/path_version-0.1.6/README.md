# Path Version

Helper to get the git hash of the last change to a particular sub-directory
in a repository.

Needs to be a separate package so that we can install it in the same virtualenv
as poetry and poetry-dynamic-versioning at least until we have poetry 1.2 and
proper poetry plugin support.
