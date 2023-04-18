#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: toa
# GNU Radio version: 3.10.5.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio import zeromq




class pager_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.rtl_samp_rate = rtl_samp_rate = 1058400
        self.decimation = decimation = 48
        self.samp_rate = samp_rate = rtl_samp_rate // decimation
        self.lpf = lpf = firdes.low_pass(1.0, rtl_samp_rate, rtl_samp_rate / (2*decimation),5000, window.WIN_HAMMING, 6.76)
        self.hw_freq = hw_freq = 157.55e6

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_short, 1, 'ipc:///tmp/pager_ch2.socket', 500, False, (-1), '', False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_short, 1, 'ipc:///tmp/pager_ch1.socket', 500, False, (-1), '', False)
        self.soapy_plutosdr_source_0 = None
        dev = 'driver=plutosdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_plutosdr_source_0 = soapy.source(dev, "fc32", 1, 'driver=plutosdr',
                                  stream_args, tune_args, settings)
        self.soapy_plutosdr_source_0.set_sample_rate(0, rtl_samp_rate)
        self.soapy_plutosdr_source_0.set_bandwidth(0, 1000000)
        self.soapy_plutosdr_source_0.set_gain_mode(0, True)
        self.soapy_plutosdr_source_0.set_frequency(0, hw_freq)
        self.soapy_plutosdr_source_0.set_gain(0, min(max(20, 0.0), 73.0))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(decimation, lpf, (157.925e6 - hw_freq), rtl_samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation, lpf, (157.95e6 - hw_freq), rtl_samp_rate)
        self.blocks_float_to_short_0_0 = blocks.float_to_short(1, 8192)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 8192)
        self.analog_nbfm_rx_0_0_0_0 = analog.nbfm_rx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=(50e-6),
        	max_dev=5e3,
          )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=(50e-6),
        	max_dev=5e3,
          )
        self.analog_agc_xx_0_0 = analog.agc_ff((1e-4), 0.2, 0.2)
        self.analog_agc_xx_0_0.set_max_gain(65536)
        self.analog_agc_xx_0 = analog.agc_ff((1e-4), 0.2, 0.2)
        self.analog_agc_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.analog_agc_xx_0_0, 0), (self.blocks_float_to_short_0_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_nbfm_rx_0_0_0_0, 0), (self.analog_agc_xx_0_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_float_to_short_0_0, 0), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_nbfm_rx_0_0_0_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))


    def get_rtl_samp_rate(self):
        return self.rtl_samp_rate

    def set_rtl_samp_rate(self, rtl_samp_rate):
        self.rtl_samp_rate = rtl_samp_rate
        self.set_lpf(firdes.low_pass(1.0, self.rtl_samp_rate, self.rtl_samp_rate / (2*self.decimation), 5000, window.WIN_HAMMING, 6.76))
        self.set_samp_rate(self.rtl_samp_rate // self.decimation)
        self.soapy_plutosdr_source_0.set_sample_rate(0, self.rtl_samp_rate)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_lpf(firdes.low_pass(1.0, self.rtl_samp_rate, self.rtl_samp_rate / (2*self.decimation), 5000, window.WIN_HAMMING, 6.76))
        self.set_samp_rate(self.rtl_samp_rate // self.decimation)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_lpf(self):
        return self.lpf

    def set_lpf(self, lpf):
        self.lpf = lpf
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lpf)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(self.lpf)

    def get_hw_freq(self):
        return self.hw_freq

    def set_hw_freq(self, hw_freq):
        self.hw_freq = hw_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((157.95e6 - self.hw_freq))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((157.925e6 - self.hw_freq))
        self.soapy_plutosdr_source_0.set_frequency(0, self.hw_freq)




def main(top_block_cls=pager_nogui, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
