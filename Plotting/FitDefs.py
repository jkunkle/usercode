
defaults = {}

defaults['bw_cmsshape'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 160 }
defaults['Gauss_cmsshape'] = { 'mean' : 0, 'sigma' : 2.495, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3  }
defaults['Gauss_cmsshape_tandp'] = { 'mean' : 0, 'sigma' : 2.495, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3  }
defaults['Landau_cmsshape'] = { 'mean' : 90, 'sigma' : 10, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 180 }
defaults['Gauss_mc_tandp'] = { 'mean' : 0, 'sigma' : 2.495, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3  }
defaults['bw_cmsshape_tandp'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'cms_alpha' : 67.3, 'cms_beta' : 0.11, 'cms_gamma' : 0.05, 'cms_peak' : 91.2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 40, 'fit_max' : 160 }

#defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : -0.008, 'poly_quadratic' : -0.00002, 'poly_cubic' : 0.0000002,  'poly_quartic' : 0.001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
defaults['bw_poly'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'poly_linear' : 10, 'poly_quadratic' : -0.05, 'poly_cubic' : -0.00001,  'poly_quartic' : 0.0000001, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160 }
defaults['Gauss_poly'] = { 'mean' : 0, 'sigma' : 2.495, 'poly_linear' : 1, 'poly_quadratic' : 4, 'poly_cubic' : 3, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3  }

defaults['bw_exp'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
defaults['bw_exp_tandp'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
defaults['Gauss_exp'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : 0.05, 'exp_start' : 80, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

defaults['bw_cheby'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'a0' : -0.05, 'a1' : -0.05, 'a2' : 0.5, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
defaults['Gauss_cheby'] = { 'mean' : 0, 'sigma' : 2.495, 'a0' : 0.01, 'a1' : -0.1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }

defaults['bw_bernstein'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 7, 'b0' : 1, 'b1' : 1, 'b2' : 2, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160 }
defaults['Gauss_bernstein'] = { 'mean' : 0, 'sigma' : 2.495, 'b0' : 1, 'b1' : 1, 'b2' : 1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }

alts = {'bw_cmsshape' : {}, 'Gauss_cmsshape' : {}, 'Gauss_cmsshape_tandp' : {}, 'bw_poly' : {}, 'Gauss_poly' : {}, 'bw_exp' : {}, 'Gauss_exp' : {}, 'bw_cheby' : {} , 'Gauss_cheby' : { }, 'bw_bernstein' : {}, 'Gauss_bernstein' : {}, 'Landau_cmsshape' : {}, 'bw_exp_tandp' : {}, 'Gauss_mc_tandp': {}, 'bw_cmsshape_tandp' : {} }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_25-30']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_30-35']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_35-40']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_40-45']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_45-50']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_50-60']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_25-40']     = { 'Bias' : -1.0, 'Width' : 3.0 , 'Cut' : -8, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.3, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_25-40']     = { 'Bias' : 0.38, 'Width' : 3.4 , 'Cut' : -3.7, 'Power' : 30, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 30000, 'nbkg' : 2000, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                              'cms_beta' : 0.027, 'cms_gamma' : 0.029, 'cms_peak' : 91, 'nsig' : 6500, 'nbkg' : 1000, 
                                                               'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.19, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 100, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                             'cms_beta' : 0.027, 'cms_gamma' : 0.034, 'cms_peak' : 88, 'nsig' : 17000, 'nbkg' : 3700, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.1, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.034, 'cms_gamma' : 0.043, 'cms_peak' : 88, 'nsig' : 18000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_nom_eta_0.50-1.00_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.3, 'Power' : 30, 'cms_alpha' : 99, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 87, 'nsig' : 18000, 'nbkg' : 4400, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.1, 'Power' : 30, 'cms_alpha' : 113, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_40-70']     = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 110, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 89, 'nsig' : 30000, 'nbkg' : 1400, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_nom_eta_1.57-2.10_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 2.5 , 'Cut' : -1.6, 'Power' : 30, 'cms_alpha' : 98, 
                                                             'cms_beta' : 0.027, 'cms_gamma' : 0.022, 'cms_peak' : 88, 'nsig' : 13000, 'nbkg' : 2800, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 3.0 , 'Cut' : -3, 'Power' : 10, 'cms_alpha' : 99, 
                                                             'cms_beta' : 0.048, 'cms_gamma' : 0.031, 'cms_peak' : 88, 'nsig' : 7700, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_2.10-2.20_pt_40-70']     = { 'Bias' : 1.4, 'Width' : 3.0 , 'Cut' : -3, 'Power' : 10, 'cms_alpha' : 99, 
                                                             'cms_beta' : 0.048, 'cms_gamma' : 0.031, 'cms_peak' : 88, 'nsig' : 7700, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_nom_eta_2.10-2.20_pt_40-70']     = { 'Bias' : 1.5, 'Width' : 2.9 , 'Cut' : -3.6, 'Power' : 10, 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.022, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 2600, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_2.20-2.30_pt_40-70']     = { 'Bias' : 1.8, 'Width' : 2.7 , 'Cut' : -3.3, 'Power' : 30, 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.022, 'cms_gamma' : 0.09, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_2.30-2.40_pt_40-70']     = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.037, 'cms_gamma' : 0.015, 'cms_peak' : 88, 'nsig' : 11000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_nom_eta_2.30-2.40_pt_40-70']     = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.037, 'cms_gamma' : 0.015, 'cms_peak' : 88, 'nsig' : 11000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180 }
alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_40-70']     = { 'Bias' : 2, 'Width' : 2.8 , 'Cut' : -1.2, 'Power' : 30, 'cms_alpha' : 143, 
                                                             'cms_beta' : 0.0234, 'cms_gamma' : 0.044, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                             'fit_min': 40, 'fit_max' : 180 }
#alts['bw_cmsshape']['fit_nom_eta_2.40-2.50_pt_40-70']    = { 'Bias' : 2.0, 'Width' : 2.8 , 'Cut' : -1.06, 'Power' : 30, 'cms_alpha' : 100, 
#                                                             'cms_beta' : 0.024, 'cms_gamma' : 0.014, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 620, 
#                                                             'fit_min': 40, 'fit_max' : 180 }

alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.26, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 60, 'nbkg' : 130, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :50 , 'nbkg' : 10, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-1.44_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_70-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.7, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max']    = { 'Bias' : -0.05, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_70-max']    = { 'Bias' : 1.76, 'Width' : 1.7 , 'Cut' : -0.57, 'Power' : 8, 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.006, 'cms_gamma' : 0.0002, 'cms_peak' : 88.7, 'nsig' : 80, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_2.10-2.40_pt_70-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_70-100']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.26, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 60, 'nbkg' : 130, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-1.44_pt_70-100']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_70-100']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_0.50-1.00_pt_70-100']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-100']    = { 'Bias' : -0.03, 'Width' : 2.5 , 'Cut' : -0.3, 'Power' : 30, 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.02, 'cms_peak' : 87, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-100']    = { 'Bias' : -0.05, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_70-100']    = { 'Bias' : 1.76, 'Width' : 1.7 , 'Cut' : -0.57, 'Power' : 8, 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.006, 'cms_gamma' : 0.0002, 'cms_peak' : 88.7, 'nsig' : 80, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_2.10-2.40_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_2.40-2.50_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_2.40-2.50_pt_70-100']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_1.57-2.50_pt_70-100']    = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.2, 'Power' : 30, 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_0.00-0.10_pt_100-max']    = { 'Bias' : -0.6, 'Width' : 2.5 , 'Cut' : -0.28, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.008, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' :50 , 'nbkg' : 10, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_100-max']    = { 'Bias' : 2, 'Width' : 2.5 , 'Cut' : -0.8, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.013, 'cms_gamma' : 0.013, 'cms_peak' : 92, 'nsig' :50 , 'nbkg' : 10, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_100-max']    = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -3.0, 'Power' : 12, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 94, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_0.10-0.50_pt_100-max']    = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -3.0, 'Power' : 12, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 94, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_0.50-1.00_pt_100-max']    = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -3.0, 'Power' : 12, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 94, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_100-max']    = { 'Bias' : -0.6, 'Width' : 2.5 , 'Cut' : -0.3, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 94, 'nsig' :200 , 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-1.44_pt_100-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 172, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.054, 'cms_peak' : 91, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.50-1.00_pt_100-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.001, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_100-max']    = { 'Bias' : -0.8, 'Width' : 0.5 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.001, 'cms_gamma' : 0.01, 'cms_peak' : 88, 'nsig' :150 , 'nbkg' : 70, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.00-0.10_pt_100-max']    = { 'Bias' : -0.7, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_0.10-0.50_pt_100-max']    = { 'Bias' : -0.05, 'Width' : 2 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 40, 'nbkg' : 40, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.00-1.44_pt_100-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_1.57-2.10_pt_100-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -0.24, 'Power' : 30, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.04, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_100-max']    = { 'Bias' : 2, 'Width' : 2.5 , 'Cut' : -3.0, 'Power' : 8, 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.001, 'cms_peak' : 88.7, 'nsig' : 80, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_nom_eta_2.40-2.50_pt_100-max']    = { 'Bias' : 2, 'Width' : 2.5 , 'Cut' : -4.0, 'Power' : 5, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.032, 'cms_peak' : 90.0, 'nsig' : 80, 'nbkg' : 400, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape']['fit_inv_eta_2.10-2.40_pt_100-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -1.4, 'Power' : 10, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_nom_eta_2.10-2.40_pt_100-max']    = { 'Bias' : 1.5, 'Width' : 3 , 'Cut' : -1.4, 'Power' : 10, 'cms_alpha' : 180, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape']['fit_inv_eta_1.57-2.50_pt_100-max']    = { 'Bias' : 1.0, 'Width' : 2.5 , 'Cut' : -1.2, 'Power' : 30, 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }

alts['bw_cmsshape_tandp']['fit_nom_eta_0.00-0.10_pt_70-max']    = { 'Bias' : -0.9, 'Width' : 2.5 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.008, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape_tandp']['fit_nom_eta_0.50-1.00_pt_70-max']    = { 'Bias' : -0.9, 'Width' : 2.5 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.008, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape_tandp']['fit_nom_eta_1.57-2.10_pt_70-max']    = { 'Bias' : -0.9, 'Width' : 2.5 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.008, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_70-max']    = { 'Bias' : -0.9, 'Width' : 2.5 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.008, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }
alts['bw_cmsshape_tandp']['fit_nom_eta_2.40-2.50_pt_70-max']    = { 'Bias' : -0.9, 'Width' : 2.5 , 'Cut' : -0.2, 'Power' : 30, 'cms_alpha' : 114, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.008, 'cms_peak' : 91, 'nsig' :300 , 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 160 }


alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_15-20']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_20-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_15-20']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_20-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 46, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_15-20']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 46, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_20-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 46, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 46, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_15-20']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_20-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_25-30']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_15-20']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_20-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_25-30']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_15-20']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_20-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_25-30']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_15-25']  = { 'mean' : 1.3, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_15-20']  = { 'mean' : 1.3, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_20-25']  = { 'mean' : 1.3, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_25-30']  = { 'mean' : 1.3, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_15-25']  = { 'mean' : 1.6, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_15-20']  = { 'mean' : 1.6, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_20-25']  = { 'mean' : 1.6, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_25-30']  = { 'mean' : 1.6, 'sigma' : 0.5 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 95, 
                                                             'cms_beta' : 0.034, 'cms_gamma' : 0.05, 'cms_peak' : 89, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_35-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-1.44_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_25-40']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_30-35']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_35-40']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_40-45']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_45-50']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.50_pt_45-50']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.10-0.50_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 81, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.066, 'cms_peak' : 88, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.10-0.50_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 81, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.066, 'cms_peak' : 88, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 81, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.066, 'cms_peak' : 88, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.50-1.00_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 81, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.066, 'cms_peak' : 88, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_35-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_35-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.12, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 113, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 89, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_35-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.065, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.065, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_30-35']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.065, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_40-70']  = { 'mean' : 0.33, 'sigma' : 0.4 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_50-60']  = { 'mean' : 0.33, 'sigma' : 0.4 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_60-70']  = { 'mean' : 0.33, 'sigma' : 0.4 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 60, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.014, 'cms_gamma' : 0.036, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.016, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.019, 'cms_gamma' : 0.066, 'cms_peak' : 89, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 470, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_50-60']  = { 'mean' : 1.1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.014, 'cms_gamma' : 0.036, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 470, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_0.50-1.00_pt_50-60']  = { 'mean' : 1.1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.016, 'cms_gamma' : 0.055, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 470, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.023, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 23000, 'nbkg' : 470, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.014, 'cms_gamma' : 0.036, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.019, 'cms_gamma' : 0.066, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 1000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 120, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.016, 'cms_gamma' : 0.049, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.018, 'cms_gamma' : 0.053, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 190, 
                                                             'cms_beta' : 0.018, 'cms_gamma' : 0.053, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_50-60']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_60-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 300, 
                                                             'cms_beta' : 0.016, 'cms_gamma' : 0.047, 'cms_peak' : 88, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.30_pt_50-60']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.30_pt_60-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.30_pt_50-60']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.30_pt_60-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.40_pt_50-60']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.40_pt_60-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.016, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_50-60']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_60-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.30-2.40_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.30-2.40_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.30-2.40_pt_50-60']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.30-2.40_pt_60-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_25-30']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.066, 'cms_gamma' : 0.023, 'cms_peak' : 94, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_45-50']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.025, 'cms_gamma' : 0.12, 'cms_peak' : 91, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_50-60']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 200, 
                                                             'cms_beta' : 0.018, 'cms_gamma' : 0.053, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_40-70']  = { 'mean' : 2, 'sigma' : 1.9 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.02, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_50-60']  = { 'mean' : 2, 'sigma' : 1.9 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.02, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_60-70']  = { 'mean' : 2, 'sigma' : 1.9 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.02, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }


alts['Gauss_cmsshape']['fit_inv_eta_0.00-0.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_nom_eta_0.00-0.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_nom_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_inv_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_inv_eta_0.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_nom_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_inv_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_nom_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.2, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_inv_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_nom_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 0.5 }
alts['Gauss_cmsshape']['fit_inv_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.3, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_nom_eta_2.10-2.20_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.3, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_inv_eta_2.10-2.20_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_nom_eta_2.20-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.3, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_inv_eta_2.20-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }
alts['Gauss_cmsshape']['fit_nom_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.4, 'nSigma' : 0.6 }
alts['Gauss_cmsshape']['fit_inv_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 180, 'rho' : 0.5, 'nSigma' : 1 }

#******************************************************************************************************************
#******************************************************************************************************************

alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.00-0.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.5 , 'cms_alpha' : 75, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.08, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.10-0.50_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.50-1.00_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.6 , 'cms_alpha' : 50, 
                                                             'cms_beta' : 0.07, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.00-1.44_pt_15-25']  = { 'mean' : 1.4, 'sigma' : 0.5 , 'cms_alpha' : 61, 
                                                             'cms_beta' : 0.16, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.57-2.10_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.57-2.10_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 88, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.10-2.20_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.10-2.20_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 88, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.20-2.40_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 88, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.40-2.50_pt_15-25']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 40, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.40-2.50_pt_15-25']  = { 'mean' : 0.8, 'sigma' : 1.6 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.07, 'cms_peak' : 88, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }


alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.00-0.10_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.5 , 'cms_alpha' : 60, 
                                                             'cms_beta' : 0.1, 'cms_gamma' : 0.05, 'cms_peak' : 91, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_25-30']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 53, 
                                                             'cms_beta' : 0.2, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.40-2.50_pt_35-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 74, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.06, 'cms_peak' : 86, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.57-2.50_pt_25-40']  = { 'mean' : 1.2, 'sigma' : 1.7 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.10-0.50_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 82, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.1, 'cms_peak' : 86, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.6 , 'cms_alpha' : 91, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.12, 'cms_peak' : 86, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.00-1.44_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.09, 'cms_gamma' : 0.1, 'cms_peak' : 86, 'nsig' : 20000, 'nbkg' : 700, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.57-2.10_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 50000, 'nbkg' : 1000, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.10-2.20_pt_25-40']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.066, 'cms_peak' : 90, 'nsig' : 1500, 'nbkg' : 200, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.10-0.50_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 84, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.00-1.44_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 84, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.07, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.00-1.44_pt_40-45']  = { 'mean' : 1.5, 'sigma' : 0.3 , 'cms_alpha' : 84, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 92, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.05, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_45-50']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 71, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.02, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.00-0.10_pt_50-55']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 78, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.10-0.50_pt_50-55']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 78, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.57-2.10_pt_50-55']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 89, 
                                                             'cms_beta' : 0.05, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.00-0.10_pt_55-60']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 78, 
                                                             'cms_beta' : 0.06, 'cms_gamma' : 0.04, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.00-1.44_pt_55-60']  = { 'mean' : 1.5, 'sigma' : 0.8 , 'cms_alpha' : 68, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 81, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.03, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.00-1.44_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.10-2.20_pt_60-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.09, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }

alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.00-0.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 77.5, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.06, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.10-0.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 1.5 , 'cms_alpha' : 75, 
                                                             'cms_beta' : 0.045, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 75, 
                                                             'cms_beta' : 0.045, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.00-1.44_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 77.5, 
                                                             'cms_beta' : 0.08, 'cms_gamma' : 0.06, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.57-2.10_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.045, 'cms_gamma' : 0.028, 'cms_peak' : 88, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.10-2.20_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.30_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.8, 'sigma' : 1.0 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.090, 'cms_peak' : 88, 'nsig' : 10000, 'nbkg' : 500, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.30-2.40_pt_40-70']  = { 'mean' : 1.2, 'sigma' : 1.3 , 'cms_alpha' : 150, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.05, 'cms_peak' : 90, 'nsig' : 13000, 'nbkg' : 3000, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.40-2.50_pt_40-70']  = { 'mean' : 1, 'sigma' : 0.8 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 5000, 'nbkg' : 150, 
                                                             'fit_min': 50, 'fit_max' : 170, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.40-2.50_pt_40-70']  = { 'mean' : 2, 'sigma' : 1.9 , 'cms_alpha' : 90, 
                                                             'cms_beta' : 0.03, 'cms_gamma' : 0.02, 'cms_peak' : 88, 'nsig' : 12000, 'nbkg' : 670, 
                                                             'fit_min': 50, 'fit_max' : 150, 'rho' : 1, 'nSigma' : 3 }


alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.00-0.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.2, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.00-0.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 88, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.2, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.10-0.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 2.0 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.020, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 160, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.2, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_0.50-1.00_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.03, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.2, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.00-1.44_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 88, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_1.57-2.10_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.10-2.20_pt_70-max'] = { 'mean' : 2, 'sigma' : 2 , 'cms_alpha' : 100, 
                                                             'cms_beta' : 0.01, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.3, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.10-2.20_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 86, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.20-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.3, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.20-2.40_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_nom_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 80, 
                                                             'cms_beta' : 0.02, 'cms_gamma' : 0.003, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.4, 'nSigma' : 2 }
alts['Gauss_cmsshape_tandp']['fit_inv_eta_2.40-2.50_pt_70-max'] = { 'mean' : 1, 'sigma' : 0.5 , 'cms_alpha' : 70, 
                                                             'cms_beta' : 0.04, 'cms_gamma' : 0.01, 'cms_peak' : 90, 'nsig' : 100, 'nbkg' : 80, 
                                                             'fit_min': 40, 'fit_max' : 170, 'rho' : 0.5, 'nSigma' : 2 }


alts['Gauss_exp']['fit_inv_eta_0.10-0.50_pt_40-70'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : 0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_0.00-0.10_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_1.00-1.44_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 75, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_1.57-2.10_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 75, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.10-2.20_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.20-2.30_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.30-2.40_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.40-2.50_pt_25-40'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.08, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_0.00-0.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.01, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 70, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_0.00-0.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.01, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 80, 'fit_max' : 180, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_0.10-0.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 85, 'fit_max' : 160, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_1.00-1.44_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_1.00-1.44_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.05, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_1.57-2.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.0, 'exp_width' : -0.05, 'nsig' : 10000, 'nbkg' : 30000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_1.57-2.10_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_2.10-2.20_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.10-2.20_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_2.20-2.30_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.20-2.30_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_2.30-2.40_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.30-2.40_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_nom_eta_2.40-2.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }
alts['Gauss_exp']['fit_inv_eta_2.40-2.50_pt_15-25'] = { 'mean' : 0, 'sigma' : 2.495, 'exp_width' : -0.001, 'nsig' : 30000, 'nbkg' : 18000, 'fit_min': 60, 'fit_max' : 200, 'rho' : 1, 'nSigma' : 3 }

alts['bw_exp']['fit_inv_eta_0.00-0.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' : 140 }
alts['bw_exp']['fit_nom_eta_1.00-1.44_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :160 }
alts['bw_exp']['fit_inv_eta_1.00-1.44_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :200 }
alts['bw_exp']['fit_nom_eta_1.57-2.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :160 }
alts['bw_exp']['fit_inv_eta_1.57-2.10_pt_15-25'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.1, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :160 }

alts['bw_exp']['fit_nom_eta_0.00-0.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_0.00-0.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
alts['bw_exp']['fit_nom_eta_0.10-0.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_0.10-0.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
alts['bw_exp']['fit_nom_eta_0.50-1.00_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_0.50-1.00_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
alts['bw_exp']['fit_nom_eta_1.00-1.44_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_1.00-1.44_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :140 }
alts['bw_exp']['fit_nom_eta_1.57-2.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_1.57-2.10_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 70, 'fit_max' :180 }
alts['bw_exp']['fit_nom_eta_2.10-2.20_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_2.10-2.20_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
alts['bw_exp']['fit_nom_eta_2.20-2.30_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_2.20-2.30_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
alts['bw_exp']['fit_nom_eta_2.30-2.40_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_2.30-2.40_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
alts['bw_exp']['fit_nom_eta_2.40-2.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 80, 'fit_max' :180 }
alts['bw_exp']['fit_inv_eta_2.40-2.50_pt_25-40'] = { 'Bias' : 0.874, 'Width' : 1.968 , 'Cut' : -1.13, 'Power' : 30, 'exp_width' : -0.05, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }

alts['bw_exp']['fit_nom_eta_2.10-2.40_pt_70-max'] = { 'Bias' : -0.3, 'Width' : 0.5 , 'Cut' : -0.1, 'Power' : 30, 'exp_width' : 0.015, 'nsig' : 5000, 'nbkg' : 1800, 'fit_min': 60, 'fit_max' :180 }
