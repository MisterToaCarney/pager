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
from gnuradio import zeromq
import osmosdr
import time




class pager_nogui(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.rtl_samp_rate = rtl_samp_rate = 242550
        self.decimation = decimation = 11
        self.samp_rate = samp_rate = rtl_samp_rate // decimation
        self.lpf = lpf = firdes.low_pass(1.0, rtl_samp_rate, rtl_samp_rate / (2*decimation),5000, window.WIN_HAMMING, 6.76)
        self.hw_freq = hw_freq = 157.95e6

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_short, 1, 'ipc:///tmp/pager_ch2.socket', 500, False, (-1), '', False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_short, 1, 'ipc:///tmp/pager_ch1.socket', 500, False, (-1), '', False)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(rtl_samp_rate)
        self.rtlsdr_source_0.set_center_freq(hw_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(18, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(decimation, lpf, (157.925e6 - hw_freq), rtl_samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation, lpf, (157.95e6 - hw_freq), rtl_samp_rate)
        self.blocks_float_to_short_0_0 = blocks.float_to_short(1, 8192)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 8192)
        self.analog_nbfm_rx_0_0_0_0 = analog.nbfm_rx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=(75e-6),
        	max_dev=5e3,
          )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=(75e-6),
        	max_dev=5e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.analog_nbfm_rx_0_0_0_0, 0), (self.blocks_float_to_short_0_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_float_to_short_0_0, 0), (self.zeromq_pub_sink_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_nbfm_rx_0_0_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))


    def get_rtl_samp_rate(self):
        return self.rtl_samp_rate

    def set_rtl_samp_rate(self, rtl_samp_rate):
        self.rtl_samp_rate = rtl_samp_rate
        self.set_lpf(firdes.low_pass(1.0, self.rtl_samp_rate, self.rtl_samp_rate / (2*self.decimation), 5000, window.WIN_HAMMING, 6.76))
        self.set_samp_rate(self.rtl_samp_rate // self.decimation)
        self.rtlsdr_source_0.set_sample_rate(self.rtl_samp_rate)

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
        self.rtlsdr_source_0.set_center_freq(self.hw_freq, 0)




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
