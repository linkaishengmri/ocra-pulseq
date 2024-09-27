import pdb # Debugging
import numpy as np
import logging # For errors
import struct
from pulseq_assembler import PSAssembler

class pulseq_interpreter(PSAssembler):
    def __init__(self, rf_center=3e+6, rf_amp_max=5e+3, grad_max=1e+7,
                 clk_t=7e-3, tx_t=1.001, grad_t=10.003,
                 pulseq_t_match=False, ps_tx_t=1, ps_grad_t=10,
                 rf_delay_preload=False, addresses_per_grad_sample=1,
                 tx_warmup=0, grad_pad=0, adc_pad=0,
                 rf_pad_type='ext', grad_pad_type='ext'):
        super().__init__(rf_center, rf_amp_max, grad_max,
                 clk_t, tx_t, grad_t,
                 pulseq_t_match, ps_tx_t, ps_grad_t,
                 rf_delay_preload, addresses_per_grad_sample,
                 tx_warmup, grad_pad, adc_pad,
                 rf_pad_type, grad_pad_type)
    def log(str):
        print(str)
    
    # Overwrite assemble function
    def assemble(self, pulseq_file, byte_format=True):
        """
        Assemble Marcos machine code from PulSeq .seq file (PulSeq version 1.4.2)

        Args:
            pulseq_file (str): PulSeq file to assemble from
            byte_format (bool): Default True -- Return transmit and gradient data in bytes, rather than numpy.ndarray
        
        Returns:
            tuple: Transmit data (bytes or numpy.ndarray); list of gradient data (list) (bytes or numpy.ndarray);
                 command bytes (bytes); dictionary of final outputs (dict)
        """
        self._logger.info(f'Assembling ' + pulseq_file)
        if self.is_assembled:
            self._logger.info('Overwriting old sequence...')
        
        self._read_pulseq(pulseq_file)
        self._compile_tx_data()
        # self._compile_grad_data()
        # self._compile_instructions()
        # self.is_assembled = True
        # output_dict = {'readout_number' : self.readout_number, 'tx_t' : self._tx_t, 'rx_t' : self._rx_t}
        # for key, value in self._definitions.items():
        #     output_dict[key] = value
        # if byte_format:
        #     return (self.tx_bytes, self.grad_bytes, self.command_bytes, output_dict)
        # else:
        #     return (self.tx_arr, self.grad_arr, self.command_bytes, output_dict)
        
 
tse_2_seq = pulseq_interpreter()
tse_2_seq.assemble("./test_files/test_loopback.seq")