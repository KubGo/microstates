# microstates
Respository for clustering micorstates.

It is repository used for my master's degree thesis work. It's refactored code that I wrote eariler, it is more structured now and it has modular structure, but it isn't perfect. For sure naming, functions and methods need some further refactoring.

## Base usage:

Use `Participant` class for single participant testing for microstates.

Use `GroupTests` class for bulk tests of group of participants.

### Example
```
from testing import GroupTests, Participant


gr_tests = GroupTests("./data/",
		methods=('kmeans','pca'))

gr_tests.run_group_tests("./all_test_results")

gr_tests.run_group_tests("./all_test_results_interpolated", interpolate_microstates=True)

participant = Participant("./data/P27")

participant.runTests("./P27AllResults")
```
## Reports

Example report is placed inside the `examples` directory for clustering of k-means for sportsman from paper [Neural Oscillation During Mental Imagery in Sport: An Olympic Sailor Case Study](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2021.669422/full). It is for `Fitness activity` with separate clustering of microstates for guided and self-produced imaginary. Whole `kmeans` folder needs to be downloaded in order for html report to work corectly.
