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
    
    # Overwrite some assemble function
    # _read_shapes function in PSassembler is not available for both uncompressed and compressed shape. 
    def _read_shapes(self, f):
        """
        Read SHAPES (rastered shapes) section in PulSeq file f to object dict memory.
        Shapes are formatted with two header lines, followed by lines of single data points in compressed pulseq shape format

        Args:
            f (_io.TextIOWrapper): File pointer to read from

        Returns:
            str: Raw next line in file after section ends
        """
        rline = ''
        line = ''
        self._logger.info('Shapes: Reading...')
        while True:
            line = f.readline()
            rline = self._simplify(line)
            if line == '' or rline in self._pulseq_keys: break
            if len(rline.split()) == 2 and rline.split()[0].lower() == 'shape_id':
                shape_id = int(rline.split()[1])
                n = int(self._simplify(f.readline()).split()[1])
                self._warning_if(shape_id in self._shapes, f'Repeat shape ID {shape_id}, overwriting')
                self._shapes[shape_id] = np.zeros(n)

                x_temp=[]
                while True:
                    new_line=self._simplify(f.readline())
                    if new_line == '':
                        break
                    else:
                        x_temp.append(float(new_line))
                if(len(x_temp)==n):
                    self._shapes[shape_id] = np.array(x_temp)
                elif(len(x_temp)<n):
                    i = 0
                    prev = -2
                    x = 0
                    line_idx=0
                    while i < n:
                        dx = x_temp[line_idx]
                        line_idx = line_idx + 1
                        x += dx
                        self._warning_if(x > 1 or x < 0, f'Shape {shape_id} entry {i} is {x}, outside of [0, 1], rounding')
                        if x > 1:
                            x = 1
                        elif x < 0:
                            x = 0
                        self._shapes[shape_id][i] = x
                        if dx == prev:
                            r = int(x_temp[line_idx])
                            line_idx=line_idx+1
                            for _ in range(0, r):
                                i += 1
                                x += dx
                                self._warning_if(x > 1 or x < 0, f'Shape {shape_id} entry {i} is {x}, outside of [0, 1], rounding')
                                if x > 1:
                                    x = 1
                                elif x < 0:
                                    x = 0
                                self._shapes[shape_id][i] = x
                        i += 1
                        prev = dx

        self._logger.info('Shapes: Complete')

        return rline
    
tse_2_seq = pulseq_interpreter()
tse_2_seq.assemble("./test_files/demo_tse_2.seq")