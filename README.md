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
