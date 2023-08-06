Changelog
=========

2.3 (2022-06-20)
----------------

-   Add method to calculate sky map overlap with multi-ordered (MOC) sky maps.
    This works with any combination of MOC and standard flat sky maps.

-   Add queryable searches field for superevents. This will allow us to
    separate out undesired searches if needed such as CBC searches done with
    Burst pipelines.

-   Add odds ratio of real association vs random coincidence.
    This is meant to assist the RRT in assessing a joint candidate
    in GraceDB, similar to the coherence value provided by
    Bayestar.

-   Add automatically generated documentation using sphinx. This is hosted
    on readthedocs and triggered with every commit on master.

-   Remove unnecessary local creation of coincidence_far.json.

-   Update README.md with updated documentation and link.

2.2 (2022-02-02)
----------------

-   Change minimum python version to 3.8 to fix a pinned dependency.

-   Fix broken FAR study tests.

-   Catch errors when searches or pipelines are set to None.


2.1 (2022-01-18)
----------------

-   Move tests directory from ligo/tests to ligo/raven/tests.

-   Fix broken .gitlab-ci.yml build and tests.

-   Add option to calculate coinc far with MDC events.

-   Update dependencies by reducing non-required packages.


2.0 (2021-11-09)
----------------

-   Switch to using the gracedb_sdk API instead of gracedb REST. This should
    drastically decrease the latency when calling gracedb.

-   Add ability to find and process MDC events. This will keep the streams
    of normal and MDC searches separate by only allowing searches with MDCs
    to find other MDCs (i.e. superevent MDCs with external MDCs.)

-   Add bin scripts to run RAVEN functions using the command line.

-   Add option to use a given em_rate, intended for offline use.

-   Add option to pass event dictionaries to functions. This should reduce
    the number of gracedb queries and improve latency.

-   Fix some minor bugs when creating messages to gracedb.

-   Remove some old legacy code.

-   Update documentation, dependencies.


1.18 (2020-03-02)
-----------------

-   Return coinc FAR as well when uploading to GraceDb.

-   Calculate joint FAR for low significance GRBs in order to run RAVEN on
    events in the joint LVK-Fermi and LVK-Swift targeted searches.

-   In query, add filter for searches. This is so that can run separates
    searches/search windows for GRB vs SubGRB events.


1.17 (2019-09-08)
-----------------

-   Add FAR study that runs automatically when making/updating a merge request.

-   Remove monkeypatch calls from tests.

-   Use GW sky map from superevent.


1.16 (2019-08-27)
-----------------

-   Add unittests to automatically run when making/updating a merge request.
    Also these tests can be run locally with `python setup.py test`

-   Add additional tests based on
    https://git.ligo.org/brandon.piotrzkowski/ravenreview (tests agreed by
    the RAVEN review commitee that demonstrate the functions are working
    correctly) in order test the code and expedite future review/deployment.

-   Add lint to check style of code.

-   Remove check for time window when uploading coincidence FAR since this
    does not work for time windows for both superevents and external events.

-   Remove commented code and unused legacy functions.

-   Change terms in GCN rates to be floats.

-   Change format of time difference message to include three digits.

-   Check that skymaps don't normalize to negative values.

-   Allow external sky map filename to be passed as an argument, so can use
    other external sky maps not just Fermi.

-   Fix search messages to both be simpler and so that groups and pipelines
    no longer flip.


1.15 (2019-07-02)
-----------------

-   Change GRB subthreshold search to 'SubGRB' to follow gracedb convention.

-   Optimize the calculation of sky map overlapping integral.

-   Changed descriptions of functions. Now passing errors from coinc_far to
    calc_signif_gracedb to upload. Coincidence_far.json now includes preferred
    event.

-   Remove ability to add 'EM_COINC' label; that label will now be applied in
    gwcelery. Add check for time window when uploading coincidence FAR.

-   Submits error message to gracedb if skymap_overlap_integral creates zero
    division error.

-   Use ligo.skymap to fix bug in SE where sky maps are not read in correctly.

-   Change if/elif structure when sending gracedb logs to prevent double
    uploads of the coincidence far. 

-   Fix search bug where the time window was reversed in the log entries.


1.14 (2019-06-06)
-----------------

-   Add choice of GRB search to calculate coinc FAR. Update GCN rates.

-   Add function coinc_far that calculates coincidence far but doesn't upload
    to gracedb. Requested by the GBM team and is intended for testing and
    offline purposes.
 

1.13 (2019-05-29)
-----------------

-   Fix bug in query where nothing is returned.


1.12 (2019-05-14)
-----------------

-   Update results from search query all at once rather than looping.


1.11 (2019-04-22)
-----------------

-   Update calls for calculating coincidence FARs to use strings rather than
    RAVEN class objects.


1.10 (2019-02-15)
-----------------

-   Fix link in log message.


1.9 (2019-02-15)
----------------

-   Write and upload coincidence_far.json when computing temporal and
    spatiotemporal coincidence FARs. This will simplify matters when
    constructing the EM_COINC circulars.


1.8 (2018-10-03)
----------------

-   Fixed tagnames to tag_name when writing log comments in GraceDb.


1.7 (2018-09-26)
-------------------

-   Use ligo.skymap.io module instead of deprecated lalinference.io module.

-   Added spatio-temporal coincidence FAR calculating ability that utilizes
    skymaps from both the LVC and Fermi.


1.6 (2018-09-24)
----------------

-   Update ligo.raven.search query and search methods to allow pipeline
    specification. Then, while searching for external triggers, we can
    distinguish between SNEWS and Fermi/Swift triggers.


1.5 (2018-08-14)
----------------

-   Update ligo.raven.search.calc_signif_gracedb to compute the FAR for
    coincidences between superevents and external triggers as opposed to GW
    triggers and external triggers.


1.4 (2018-08-14)
----------------

-   Option to pass group specification to ligo.raven.search and
    ligo.raven.query that filters out superevent search results depending on
    the group of the preferred_event


1.3 (2018-08-02)
----------------

-   Added dependency on ligo-segments

-   Work around missing six dependency in healpy 1.12.0

-   Debugged broken links in comments uploaded to GraceDb. For superevents,
    the links need to be /superevents not /events.

-   Debugged ligo.raven.gracedb_events.SE so that it has a graceid attribute

-   Update VOEventLib package version so that the bug found by Tanner P. is fixed

-   Handle searches with superevents

-   Option to pass an instance of GraceDb to ligo.raven.search and
    ligo.raven.gracedb_events; needed for implementation with GWCelery
    where we might be be using the default GraceDb url

-   Update call to GraceDb superevent object so that it uses superevent method
    vs superevents


1.1.dev0 (2018-06-19)
------------------------

-   Renamed package to ligo-raven to avoid confusion and conflict with
    another package called raven on PyPI

-   Ported to Python 3 / Dropped Python 2 support entirely

-   Project handed off to Min-A Cho and Shaon Ghosh

 
1.0 (2016-11-03)
----------------

-   Last commit by Alex Urban
