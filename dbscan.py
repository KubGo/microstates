from testing import Participant

participant = Participant("../../data/all_data/P28", methods=('dbscan',))

participant.runTests("./P27AllResults")