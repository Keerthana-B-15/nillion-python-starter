from nada_dsl import *

def nada_main():

    # 1. Parties initialization
    judge0 = Party(name="Judge0")
    judge1 = Party(name="Judge1")
    judge2 = Party(name="Judge2")
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    ## Scores from judge 0
    j0_c0 = SecretUnsignedInteger(Input(name="j0_c0", party=judge0))
    j0_c1 = SecretUnsignedInteger(Input(name="j0_c1", party=judge0))
    ## Scores from judge 1
    j1_c0 = SecretUnsignedInteger(Input(name="j1_c0", party=judge1))
    j1_c1 = SecretUnsignedInteger(Input(name="j1_c1", party=judge1))
    ## Scores from judge 2
    j2_c0 = SecretUnsignedInteger(Input(name="j2_c0", party=judge2))
    j2_c1 = SecretUnsignedInteger(Input(name="j2_c1", party=judge2))

    # 3. Computation
    ## Add scores for contestant 0
    total_score_c0 = j0_c0 + j1_c0 + j2_c0
    ## Add scores for contestant 1
    total_score_c1 = j0_c1 + j1_c1 + j2_c1

    # 4. Output
    result_c0 = Output(total_score_c0, "final_score_c0", outparty)
    result_c1 = Output(total_score_c1, "final_score_c1", outparty)

    return [result_c0, result_c1]