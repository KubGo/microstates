from .Results import Results

class ComparisonResults:
    
    def __init__(self, results: list[Results]):
        self.names = self.get_names_list(results)
        self.probabilities = self.get_probabilities(results)
        self.entropies = self.get_entropies(results)
        self.transition_matrices = self.get_transition_matrices(results)
        self.microstates_maps = self.get_microstates_maps(results)
        self.signal_part = self.get_signal_part(results)
        self.test_p_values = self.get_test_p_values(results)
        self.microstates_chain = self.get_microstates_chains(results)
       
    def get_names_list(self, results: list[Results]):
        return [result.get_name() for result in results]
    def get_probabilities(self, results: list[Results]):
        return {
            result.get_name(): result.empirical_p
            for result in results
        }

    def get_entropies(self, results: list[Results]):
        return {
            result.get_name(): {
                "h_max": result.h_max,
                "h": result.h,
                "h_mc": result.h_mc,
            }
            for result in results
        }
    
    def get_transition_matrices(self, results: list[Results]):
        return {
            result.get_name(): result.transition_matrix
            for result in results
        }
    
    def get_microstates_maps(self, results: list[Results]):
        return {
            result.get_name(): result.cluster_centers
            for result in results
        }
    
    def get_signal_part(self, results: list[Results]):
        return {
            result.get_name(): result.alpha_wave
            for result in results
        }

    def get_microstates_chains(self, results: list[Results]):
        return {
            result.get_name(): result.clusters_chain
            for result in results
        }

    def get_test_p_values(self, results: list[Results]):
        return {
            result.get_name(): {
                "markov0": result.p_markov_test_0,
                "markov1": result.p_markov_test_1,
                "markov2": result.p_markov_test_2,
                "homogenity": result.p_conditional_homogenity,
                "symmetry": result.p_symmetry_test,
            }
            for result in results
        }
