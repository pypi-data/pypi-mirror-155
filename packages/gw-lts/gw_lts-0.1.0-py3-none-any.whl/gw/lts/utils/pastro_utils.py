#!/usr/bin/env python3

import numpy

mc_centers = numpy.logspace(0, 2, 100)
L_centers = numpy.logspace(0, 2.5, 102)

# options: mean and sigma chirp-mass for each signal type 
#          ranking stat threshold

def noise_dist(mc_centers = mc_centers, L_centers = L_centers):
	# make up a noise distribution which is independent of mchirp, p_noise = exp(-L)
	p_x_c0 = numpy.zeros((len(mc_centers), len(L_centers)))
	for i in range(len(mc_centers)): p_x_c0[i,:] = numpy.exp(-L_centers)
	p_x_c0 /= p_x_c0.sum()
	return p_x_c0

# signal distribution is a gaussian in chirp mass defined by some mean and sigma values; 
# ranking stat is used for scaling 

def signal_dist(mean, sigma, mc_centers=mc_centers, L_centers=L_centers):
	p_x_ci = numpy.zeros((len(mc_centers), len(L_centers)))
	for i in range(len(mc_centers)):
		p_x_ci[i,:] = numpy.exp(-(mc_centers[i] - mean)**2./(2.*sigma**2.)) * L_centers**-4.
	p_x_ci /= p_x_ci.sum()
	return p_x_ci


def p_x_c(bns=(1.2, .2), nsbh=(3.0, .4), bbh=(50., 10.)):
	mean_bns, sigma_bns = bns
	mean_nsbh, sigma_nsbh = nsbh
	mean_bbh, sigma_bbh = bbh
	return  {"Terrestrial": noise_dist(),
		"BNS": signal_dist(mean_bns, sigma_bns),
		"NSBH": signal_dist(mean_nsbh, sigma_nsbh),
		"BBH": signal_dist(mean_bbh, sigma_bbh)}

def p_c(p_x_c, ranking_stat_thresh= 4, N_events={"Terrestrial": 1e6, "BNS": 10, "NSBH": 10, "BBH": 1000}):
	N_above_thresh = {"Terrestrial": N_events["Terrestrial"],
			"BNS": N_events["BNS"],
			"NSBH": N_events["NSBH"],
			"BBH": N_events["BBH"]}
	p_c = {k: N_above_thresh[k]/sum(N_above_thresh.values()) / (p_x_c[k][:,ranking_stat_thresh:]).sum() for k in p_x_c}
	return p_c

def p_astro(mc, L, p_x_c, p_c, mc_centers = mc_centers, L_centers = L_centers):
	mc_ix = numpy.searchsorted(mc_centers, mc)
	L_ix = numpy.searchsorted(L_centers, L)
	out = {k: p_x_c[k][mc_ix, L_ix] * p_c[k] for k in p_x_c}
	norm = sum(out.values())
	return {k: out[k]/norm for k in out}

