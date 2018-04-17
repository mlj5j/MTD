# /usr/bin/python

#Author: Ben Tannenwald
#Date: April 16, 2018
#Purpose: Class for handling testbeam bar data

import os,sys, argparse
from ROOT import gROOT, TH1D, TFile, TTree, TChain, TCanvas, TH2D, TLegend, gStyle

class barClass:
    def __init__(self, tree, runType, topDir):
        self.tree = tree
        self.topDir = topDir
        self.signalThreshold = 0
        self.xBoundaries = []
        self.xBoundaries_split = []
        self.yBoundaries = []

        self.setVarsByRunType(runType)

        self.h_b1 = TH2D("h_b1", "h_b1", 40, -5, 35, 35, 0, 35)
        self.h_b2 = TH2D("h_b2", "h_b2", 40, -5, 35, 35, 0, 35)
        self.h_b3 = TH2D("h_b3", "h_b3", 40, -5, 35, 35, 0, 35)
        self.h_b4 = TH2D("h_b4", "h_b4", 40, -5, 35, 35, 0, 35)
        self.h_b5 = TH2D("h_b5", "h_b5", 40, -5, 35, 35, 0, 35)
        self.h_b1_t = TH2D("h_b1_t", "h_b1_t", 40, -5, 35, 35, 0, 35)
        self.h_b2_t = TH2D("h_b2_t", "h_b2_t", 40, -5, 35, 35, 0, 35)
        self.h_b3_t = TH2D("h_b3_t", "h_b3_t", 40, -5, 35, 35, 0, 35)
        self.h_b4_t = TH2D("h_b4_t", "h_b4_t", 40, -5, 35, 35, 0, 35)
        self.h_b5_t = TH2D("h_b5_t", "h_b5_t", 40, -5, 35, 35, 0, 35)
        
        self.h_mcp0_ch1 = TH1D("h_mcp0_bar1", "h_mcp0_ch1", 25, 0, 500);
        self.h_mcp0_ch3 = TH1D("h_mcp0_bar3", "h_mcp0_ch3", 25, 0, 500);
        self.h_mcp0_ch5 = TH1D("h_mcp0_bar5", "h_mcp0_ch5", 25, 0, 500);
        self.h_mcp1_ch10 = TH1D("h_mcp1_ch10", "h_mcp1_ch10", 25, 0, 500);
        self.h_mcp1_ch12 = TH1D("h_mcp1_ch12", "h_mcp1_ch12", 25, 0, 500);
        
        self.h_ch1_vs_ch2 = TH2D("h_ch1_vs_ch2", "h_ch1_vs_ch2", 22, 0, 1100, 22, 0, 1100)
        self.h_ch3_vs_ch4 = TH2D("h_ch3_vs_ch4", "h_ch3_vs_ch4", 22, 0, 1100, 22, 0, 1100)
        self.h_ch5_vs_ch6 = TH2D("h_ch5_vs_ch6", "h_ch5_vs_ch6", 22, 0, 1100, 22, 0, 1100)
        self.h_ch10_vs_ch11 = TH2D("h_ch10_vs_ch11", "h_ch10_vs_ch11", 22, 0, 1100, 22, 0, 1100)
        self.h_ch12_vs_ch13 = TH2D("h_ch12_vs_ch13", "h_ch12_vs_ch13", 22, 0, 1100, 22, 0, 1100)
        
        self.h_ch1_ch2_ratio_xq1 = TH1D("h_ch1_ch2_ratio_xq1", "h_ch1_ch2_ratio_xq1", 100, 0.0, 2.0)
        self.h_ch1_ch2_ratio_xq2 = TH1D("h_ch1_ch2_ratio_xq2", "h_ch1_ch2_ratio_xq2", 100, 0.0, 2.0)
        self.h_ch1_ch2_ratio_xq3 = TH1D("h_ch1_ch2_ratio_xq3", "h_ch1_ch2_ratio_xq3", 100, 0.0, 2.0)
        self.h_ch1_ch2_ratio_xq4 = TH1D("h_ch1_ch2_ratio_xq4", "h_ch1_ch2_ratio_xq4", 100, 0.0, 2.0)
        self.h_ch3_ch4_ratio_xq1 = TH1D("h_ch3_ch4_ratio_xq1", "h_ch3_ch4_ratio_xq1", 100, 0.0, 2.0)
        self.h_ch3_ch4_ratio_xq2 = TH1D("h_ch3_ch4_ratio_xq2", "h_ch3_ch4_ratio_xq2", 100, 0.0, 2.0)
        self.h_ch3_ch4_ratio_xq3 = TH1D("h_ch3_ch4_ratio_xq3", "h_ch3_ch4_ratio_xq3", 100, 0.0, 2.0)
        self.h_ch3_ch4_ratio_xq4 = TH1D("h_ch3_ch4_ratio_xq4", "h_ch3_ch4_ratio_xq4", 100, 0.0, 2.0)
        self.h_ch5_ch6_ratio_xq1 = TH1D("h_ch5_ch6_ratio_xq1", "h_ch5_ch6_ratio_xq1", 100, 0.0, 2.0)
        self.h_ch5_ch6_ratio_xq2 = TH1D("h_ch5_ch6_ratio_xq2", "h_ch5_ch6_ratio_xq2", 100, 0.0, 2.0)
        self.h_ch5_ch6_ratio_xq3 = TH1D("h_ch5_ch6_ratio_xq3", "h_ch5_ch6_ratio_xq3", 100, 0.0, 2.0)
        self.h_ch5_ch6_ratio_xq4 = TH1D("h_ch5_ch6_ratio_xq4", "h_ch5_ch6_ratio_xq4", 100, 0.0, 2.0)
        self.h_ch10_ch11_ratio_xq1 = TH1D("h_ch10_ch11_ratio_xq1", "h_ch10_ch11_ratio_xq1", 100, 0.0, 2.0)
        self.h_ch10_ch11_ratio_xq2 = TH1D("h_ch10_ch11_ratio_xq2", "h_ch10_ch11_ratio_xq2", 100, 0.0, 2.0)
        self.h_ch10_ch11_ratio_xq3 = TH1D("h_ch10_ch11_ratio_xq3", "h_ch10_ch11_ratio_xq3", 100, 0.0, 2.0)
        self.h_ch10_ch11_ratio_xq4 = TH1D("h_ch10_ch11_ratio_xq4", "h_ch10_ch11_ratio_xq4", 100, 0.0, 2.0)
        self.h_ch12_ch13_ratio_xq1 = TH1D("h_ch12_ch13_ratio_xq1", "h_ch12_ch13_ratio_xq1", 100, 0.0, 2.0)
        self.h_ch12_ch13_ratio_xq2 = TH1D("h_ch12_ch13_ratio_xq2", "h_ch12_ch13_ratio_xq2", 100, 0.0, 2.0)
        self.h_ch12_ch13_ratio_xq3 = TH1D("h_ch12_ch13_ratio_xq3", "h_ch12_ch13_ratio_xq3", 100, 0.0, 2.0)
        self.h_ch12_ch13_ratio_xq4 = TH1D("h_ch12_ch13_ratio_xq4", "h_ch12_ch13_ratio_xq4", 100, 0.0, 2.0)

        self.c1 = TCanvas("c1", "c1", 800, 800)
        self.c2 = TCanvas("c2", "c2", 800, 800)
        self.c3 = TCanvas("c3", "c3", 800, 800)
        self.c4 = TCanvas("c4", "c4", 800, 800)

        gStyle.SetOptStat(0000)

        # make some directories if not already existent
        if not os.path.isdir(self.topDir):
            os.system( 'mkdir {0}'.format(self.topDir) )
        self.topDir = '{0}/{1}'.format(topDir, runType)
        if not os.path.isdir( '{0}/{1}'.format(topDir, runType) ):
            os.system( 'mkdir {0}'.format(self.topDir) )

        # run analysis
        self.loopEvents()

    # =============================

    def setVarsByRunType(self, runType):
        """ set various constants as function of runType"""

        if runType == "all5exposure":
            self.signalThreshold = 100
            self.xBoundaries_split = [-2, 6, 15, 24, 33]
            self.xBoundaries = [-2, 33]
            self.yBoundaries = [8.5, 12.5, 16.5, 20.5, 24.5]

    # =============================

    def fillChannelPlots(self, event, barNum, h_b, h_mcp, h_lr_ratio, h_lr_ratio_x1, h_lr_ratio_x2, h_lr_ratio_x3, h_lr_ratio_x4, h_b_test):
        """ function to fill bar-specific plots"""
        
        # calculate channel numbers given bar number --> there is probably a smarter way to automate this with fewer lines
        leftSiPMchannel = rightSiPMchannel = vetoSiPMchannel = mcpChannel = -1
        if barNum == 1 or barNum == 2 or barNum == 3:
            rightSiPMchannel = 2*barNum - 1
            leftSiPMchannel  = 2*barNum
            mcpChannel = 0
            vetoSiPMchannel  = 2*barNum + 1
            if barNum == 3:
                vetoSiPMchannel  = 2*barNum + 4
                
        elif barNum == 4 or barNum == 5:
            rightSiPMchannel = 2*barNum + 2
            leftSiPMchannel  = 2*barNum + 3
            mcpChannel = 1
            if barNum == 4:
                vetoSiPMchannel  = 2*barNum -3
            if barNum == 5:
                vetoSiPMchannel  = 2*barNum 

            
        if (event.amp[rightSiPMchannel] > self.signalThreshold and event.amp[vetoSiPMchannel] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004):
            h_b.Fill(event.x_dut[2], event.y_dut[2])
            h_mcp.Fill( event.amp[mcpChannel] )
            h_lr_ratio.Fill( event.amp[rightSiPMchannel], event.amp[leftSiPMchannel] )
            
            if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                h_lr_ratio_x1.Fill( event.amp[rightSiPMchannel] / event.amp[leftSiPMchannel] )
            if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                h_lr_ratio_x2.Fill( event.amp[rightSiPMchannel] / event.amp[leftSiPMchannel] )
            if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                h_lr_ratio_x3.Fill( event.amp[rightSiPMchannel] / event.amp[leftSiPMchannel] )
            if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                h_lr_ratio_x4.Fill( event.amp[rightSiPMchannel] / event.amp[leftSiPMchannel] )

            if (abs(event.y_dut[2] - self.yBoundaries[barNum - 1]) < 2.5 and event.x_dut[2]>=self.xBoundaries[0] and event.x_dut[2]<=self.xBoundaries[1]):
                h_b_test.Fill(event.x_dut[2], event.y_dut[2])
                    
        return h_b, h_mcp, h_lr_ratio, h_lr_ratio_x1,  h_lr_ratio_x2,  h_lr_ratio_x3,  h_lr_ratio_x4, h_b_test

    # =============================
    
    def loopEvents(self):
        """ function looping over all events in file"""

        print self.tree.GetEntries()
        nTotal=0

        for event in self.tree:        
            if (nTotal > 10000):
                break
            nTotal += 1
            if (nTotal % 10000 == 0):
                print nTotal, "processed"

                
            self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t = self.fillChannelPlots(event, 1, self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t)

            self.h_b2, self.h_mcp0_ch3, self.h_ch3_vs_ch4, self.h_ch3_ch4_ratio_xq1, self.h_ch3_ch4_ratio_xq2, self.h_ch3_ch4_ratio_xq3, self.h_ch3_ch4_ratio_xq4, self.h_b2_t = self.fillChannelPlots(event, 2, self.h_b2, self.h_mcp0_ch3, self.h_ch3_vs_ch4, self.h_ch3_ch4_ratio_xq1, self.h_ch3_ch4_ratio_xq2, self.h_ch3_ch4_ratio_xq3, self.h_ch3_ch4_ratio_xq4, self.h_b2_t)

            self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t = self.fillChannelPlots(event, 1, self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t)

            self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t = self.fillChannelPlots(event, 1, self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t)

            self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t = self.fillChannelPlots(event, 1, self.h_b1, self.h_mcp0_ch1, self.h_ch1_vs_ch2, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, self.h_b1_t)

            
            """if (event.amp[1] > self.signalThreshold and event.amp[3] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004):
                self.h_b1.Fill(event.x_dut[2], event.y_dut[2])
                self.h_mcp0_ch1.Fill( event.amp[0] )
                self.h_ch1_vs_ch2.Fill( event.amp[1], event.amp[2] )

                if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                    self.h_ch1_ch2_ratio_xq1.Fill( event.amp[1] / event.amp[2] )
                if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                    self.h_ch1_ch2_ratio_xq2.Fill( event.amp[1] / event.amp[2] )
                if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                    self.h_ch1_ch2_ratio_xq3.Fill( event.amp[1] / event.amp[2] )
                if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                    self.h_ch1_ch2_ratio_xq4.Fill( event.amp[1] / event.amp[2] )"""

            if (event.amp[3] > self.signalThreshold and event.amp[5] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 ):
                self.h_b2.Fill(event.x_dut[2], event.y_dut[2])
                self.h_mcp0_ch3.Fill( event.amp[0] )
                self.h_ch3_vs_ch4.Fill( event.amp[3], event.amp[4] )
        
                if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                    self.h_ch3_ch4_ratio_xq1.Fill( event.amp[3] / event.amp[4] )
                if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                    self.h_ch3_ch4_ratio_xq2.Fill( event.amp[3] / event.amp[4] )
                if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                    self.h_ch3_ch4_ratio_xq3.Fill( event.amp[3] / event.amp[4] )
                if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                    self.h_ch3_ch4_ratio_xq4.Fill( event.amp[3] / event.amp[4] )

            if (event.amp[5] > self.signalThreshold and event.amp[10] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 ):
                self.h_b3.Fill(event.x_dut[2], event.y_dut[2])
                self.h_mcp0_ch5.Fill( event.amp[0] )
                self.h_ch5_vs_ch6.Fill( event.amp[5], event.amp[6] )
                
                if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                    self.h_ch5_ch6_ratio_xq1.Fill( event.amp[5] / event.amp[6] )
                if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                    self.h_ch5_ch6_ratio_xq2.Fill( event.amp[5] / event.amp[6] )
                if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                    self.h_ch5_ch6_ratio_xq3.Fill( event.amp[5] / event.amp[6] )
                if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                    self.h_ch5_ch6_ratio_xq4.Fill( event.amp[5] / event.amp[6] )
        
            if (event.amp[10] > self.signalThreshold and event.amp[5] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 ):
                self.h_b4.Fill(event.x_dut[2], event.y_dut[2])
                self.h_mcp1_ch10.Fill( event.amp[9] )
                self.h_ch10_vs_ch11.Fill( event.amp[10], event.amp[11] )

                if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                    self.h_ch10_ch11_ratio_xq1.Fill( event.amp[10] / event.amp[11] )
                if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                    self.h_ch10_ch11_ratio_xq2.Fill( event.amp[10] / event.amp[11] )
                if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                    self.h_ch10_ch11_ratio_xq3.Fill( event.amp[10] / event.amp[11] )
                if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                    self.h_ch10_ch11_ratio_xq4.Fill( event.amp[10] / event.amp[11] )
        
            if (event.amp[12] > self.signalThreshold and event.amp[10] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 ):
                self.h_b5.Fill(event.x_dut[2], event.y_dut[2])
                self.h_mcp1_ch12.Fill( event.amp[9] )
                self.h_ch12_vs_ch13.Fill( event.amp[12], event.amp[13] )

                if( event.x_dut[2]>=-2 and event.x_dut[2] < 6):
                    self.h_ch12_ch13_ratio_xq1.Fill( event.amp[12] / event.amp[13] )
                if( event.x_dut[2]>= 6 and event.x_dut[2] < 15):
                    self.h_ch12_ch13_ratio_xq2.Fill( event.amp[12] / event.amp[13] )
                if( event.x_dut[2]>=14 and event.x_dut[2] < 24):
                    self.h_ch12_ch13_ratio_xq3.Fill( event.amp[12] / event.amp[13] )
                if( event.x_dut[2]>=22 and event.x_dut[2] < 33):
                    self.h_ch12_ch13_ratio_xq4.Fill( event.amp[12] / event.amp[13] )
        
            #if (event.amp[1] > self.signalThreshold and event.amp[3] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 and abs(event.y_dut[2] -8.5) < 2.5 and event.x_dut[2]>=-2 and event.x_dut[2]<=33):
            #    self.h_b1_t.Fill(event.x_dut[2], event.y_dut[2])
            if (event.amp[3] > self.signalThreshold and event.amp[5] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 and abs(event.y_dut[2] -12.5) < 2.5 and event.x_dut[2]>=-2 and event.x_dut[2]<=33):
                self.h_b2_t.Fill(event.x_dut[2], event.y_dut[2])
            if (event.amp[5] > self.signalThreshold and event.amp[10] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 and abs(event.y_dut[2] -16.5) < 2.5 and event.x_dut[2]>=-2 and event.x_dut[2]<=33):
                self.h_b3_t.Fill(event.x_dut[2], event.y_dut[2])
            if (event.amp[10] > self.signalThreshold and event.amp[5] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 and abs(event.y_dut[2] -20.5) < 2.5 and event.x_dut[2]>=-2 and event.x_dut[2]<=33):
                self.h_b4_t.Fill(event.x_dut[2], event.y_dut[2])
            if (event.amp[12] > self.signalThreshold and event.amp[10] < self.signalThreshold and abs(event.xSlope) < 0.0004 and abs(event.ySlope) < 0.0004 and abs(event.y_dut[2] -24.5) < 2.5 and event.x_dut[2]>=-2 and event.x_dut[2]<=33):
                self.h_b5_t.Fill(event.x_dut[2], event.y_dut[2])


        print "AHHHH, bar 1 has {0} entries".format(self.h_b1.GetEntries())
        self.draw2Dbar(self.c1, self.h_b1, 1)
        self.draw2Dbar(self.c1, self.h_b2, 2)
        self.draw2Dbar(self.c1, self.h_b3, 3)
        self.draw2Dbar(self.c1, self.h_b4, 4)
        self.draw2Dbar(self.c1, self.h_b5, 5)
        self.draw2Dbar(self.c1, self.h_b1_t, 1, "test")
        self.draw2Dbar(self.c1, self.h_b2_t, 2, "test")
        self.draw2Dbar(self.c1, self.h_b3_t, 3, "test")
        self.draw2Dbar(self.c1, self.h_b4_t, 4, "test")
        self.draw2Dbar(self.c1, self.h_b5_t, 5, "test")
        
        self.c2.cd()
        self.c2.SetLeftMargin(0.15);
        self.c2.SetRightMargin(0.05);
        self.c2.SetBottomMargin(0.10);
        self.c2.SetTopMargin(0.05);
        # kBlack == 1, kRed == 632, kBlue == 600, kGreen == 416, kMagenta == 616
        self.h_mcp0_ch1.SetLineColor(1) # kBlack
        self.h_mcp0_ch3.SetLineColor(600) # kBlue
        self.h_mcp0_ch5.SetLineColor(632) # kRed
        self.h_mcp1_ch10.SetLineColor(416+2) # kGreen+2
        self.h_mcp1_ch12.SetLineColor(616-3) # kMagenta-3
        
        self.h_mcp0_ch1.SetLineWidth(3) 
        self.h_mcp0_ch3.SetLineWidth(3) 
        self.h_mcp0_ch5.SetLineWidth(3) 
        self.h_mcp1_ch10.SetLineWidth(3) 
        self.h_mcp1_ch12.SetLineWidth(3) 
        
        self.h_mcp1_ch12.SetYTitle("Noramlized Entries / 20 mV")
        self.h_mcp1_ch12.SetXTitle("MCP Amplitude [mV]")
        self.h_mcp1_ch12.SetTitle("")
        self.h_mcp1_ch12.DrawNormalized()
        self.h_mcp1_ch12.GetYaxis().SetRangeUser(0,1.6)
        
        self.h_mcp0_ch3.DrawNormalized("same")
        self.h_mcp0_ch5.DrawNormalized("same")
        self.h_mcp1_ch10.DrawNormalized("same")
        self.h_mcp0_ch1.DrawNormalized("same")
        
        leg = TLegend(0.5, 0.4, .85, .7);
        leg.AddEntry(self.h_mcp0_ch1, "MCP Amplitude: Bar 1 Signal", "l");
        leg.AddEntry(self.h_mcp0_ch3, "MCP Amplitude: Bar 2 Signal", "l");
        leg.AddEntry(self.h_mcp0_ch5, "MCP Amplitude: Bar 3 Signal", "l");
        leg.AddEntry(self.h_mcp1_ch10, "MCP Amplitude: Bar 4 Signal", "l");
        leg.AddEntry(self.h_mcp1_ch12, "MCP Amplitude: Bar 5 Signal", "l");
        leg.Draw("same");
        
        self.c2.Print("{0}/mcp_amplitudes.png".format(self.topDir) )

        
        self.drawLvsRinBar(self.c3, self.h_ch1_vs_ch2, 1)
        self.drawLvsRinBar(self.c3, self.h_ch3_vs_ch4, 2)
        self.drawLvsRinBar(self.c3, self.h_ch5_vs_ch6, 3)
        self.drawLvsRinBar(self.c3, self.h_ch10_vs_ch11, 4)
        self.drawLvsRinBar(self.c3, self.h_ch12_vs_ch13, 5)
        
        
        self.drawXquadrants(self.c4, self.h_ch1_ch2_ratio_xq1, self.h_ch1_ch2_ratio_xq2, self.h_ch1_ch2_ratio_xq3, self.h_ch1_ch2_ratio_xq4, 1)
        self.drawXquadrants(self.c4, self.h_ch3_ch4_ratio_xq1, self.h_ch3_ch4_ratio_xq2, self.h_ch3_ch4_ratio_xq3, self.h_ch3_ch4_ratio_xq4, 2)
        self.drawXquadrants(self.c4, self.h_ch5_ch6_ratio_xq1, self.h_ch5_ch6_ratio_xq2, self.h_ch5_ch6_ratio_xq3, self.h_ch5_ch6_ratio_xq4, 3)
        self.drawXquadrants(self.c4, self.h_ch10_ch11_ratio_xq1, self.h_ch10_ch11_ratio_xq2, self.h_ch10_ch11_ratio_xq3, self.h_ch10_ch11_ratio_xq4, 4)
        self.drawXquadrants(self.c4, self.h_ch12_ch13_ratio_xq1, self.h_ch12_ch13_ratio_xq2, self.h_ch12_ch13_ratio_xq3, self.h_ch12_ch13_ratio_xq4, 5)
        
        
    # =============================

    def draw2Dbar(self, c0, h0, barNum, test=""):
        """ function to recieve canvas (c0), histogram (h0), and name for 2D bar plot"""
        c0.cd()
        h0.SetTitle( "Bar {0}".format(barNum) )
        h0.SetXTitle("X [mm]")
        h0.SetYTitle("Y [mm]")
        h0.Draw("colz")
        
        #h0.Integral(x1, x2, y1, y2)
        #7-10, 12-14, 16
        ymin = 4*barNum + 3
        ymax = 4*barNum + 7
        window = h0.Integral(4, 38, ymin, ymax)
        
        if h0.GetEntries() > 0:
            print "In bar {0}: {1}\t Total: {2}\t % in Bar: {3}".format(barNum, window, h0.GetEntries(), window/h0.GetEntries())
        else:
            print "no entries"

        c0.Print( "{0}/bar{1}_python{2}.png".format(self.topDir, barNum, test) )

    # =============================

    def drawLvsRinBar(self, c0, h0, barNum):
        """ function to recieve canvas (c0), histogram (h0), and name for 2D bar plot"""
        c0.cd()
        c0.SetLeftMargin(0.15);
        h0.SetTitle( "Bar {0}: R vs L Amplitudes".format(barNum) )
        h0.SetXTitle("Right SiPM [mV]")
        h0.SetYTitle("Left SiPM [mV]")
        h0.Draw("colz")
        
        c0.Print( "{0}/bar{1}_rightVleft.png".format(self.topDir, barNum) )

    # =============================

    def drawXquadrants(self, c0, h_x1, h_x2, h_x3, h_x4, barNum):
        """ function to recieve canvas (c0), histograms (h_xN [N=1,2,3,4], and bar number"""
        c0.cd()
        c0.SetLeftMargin(0.15);
        c0.SetRightMargin(0.05);
        c0.SetBottomMargin(0.10);
        c0.SetTopMargin(0.10);
        # kBlack == 1, kRed == 632, kBlue == 600, kGreen == 416, kMagenta == 616
        h_x1.SetLineColor(1) # kBlack
        h_x2.SetLineColor(600) # kBlue
        h_x3.SetLineColor(632) # kRed
        h_x4.SetLineColor(416+2) # kGreen+2
        
        h_x1.SetLineWidth(3)
        h_x2.SetLineWidth(3)
        h_x3.SetLineWidth(3)
        h_x4.SetLineWidth(3)
        
        h_x4.SetYTitle("Noramlized Entries / Bin")
        h_x4.SetXTitle("Right SiPM Amplitude / Left SiPM Amplitude")
        h_x4.SetTitle("Bar {0}".format(barNum))
        h_x4.DrawNormalized()
        h_x4.GetYaxis().SetRangeUser(0,1.6)
        
        h_x3.DrawNormalized("same")
        h_x2.DrawNormalized("same")
        h_x1.DrawNormalized("same")
        
        leg = TLegend(0.6, 0.5, .85, .7);
        leg.AddEntry(h_x1, "Right/Left Amplitude: Q1", "l");
        leg.AddEntry(h_x2, "Right/Left Amplitude: Q2", "l");
        leg.AddEntry(h_x3, "Right/Left Amplitude: Q3", "l");
        leg.AddEntry(h_x4, "Right/Left Amplitude: Q4", "l");
        leg.Draw("same");
        
        c0.Print("{0}/bar{1}_RL_ratio_xq.png".format(self.topDir, barNum))

    # =============================
