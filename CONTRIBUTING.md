# Contributing

CogC is evaluation-first.

Before adding a compression mechanism:

1. show the existing baseline;
2. identify prior art and reuse opportunities;
3. keep the mechanism optional;
4. add tests for critical information preservation;
5. add an eval case that can demonstrate downstream benefit;
6. do not substitute token reduction for task success.

Pull requests that add learned behavior should include the dataset provenance, target-model profile, baseline comparison and failure cases.
