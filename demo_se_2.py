from pulseq_assembler import PSAssembler


if __name__ == "__main__":
    tse_2_seq = PSAssembler()
    tse_2_seq.assemble("./test_files/test_loopback.seq")
