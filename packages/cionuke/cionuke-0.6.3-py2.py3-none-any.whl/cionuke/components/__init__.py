# NOTE: The order is important!
# assets comes first because dependency scraping might be expensive.
# We need the results of dependency scraping in order to form the
# windows path mapping args, which are used by the frames component,
# where tasks are generated.
COMPONENT_RESOLVE_ORDER = (
    'assets',
    'project',
    'title',
    'instance_type',
    'software',
    'environment',
    'metadata',
    'frames',
    'advanced',
) 