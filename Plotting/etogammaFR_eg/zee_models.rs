GamGamMass[0,300];
ZMCmass[60,160];
mgg_sig_m0[91.0, 80, 100];
mgg_sig_sigma[1.5, 0.5, 4.0];
mgg_sig_alpha[1.5, 1.0, 3]; 
mgg_sig_n[4.0, 0.5, 5]; 
mgg_sig_gsigma[2.5, 2.0, 10];
mgg_sig_frac[0.3, 0, 0.5];

MggGaussSig = Gaussian(GamGamMass, mgg_sig_m0, mgg_sig_gsigma);
MggCBSig    = CBShape(GamGamMass, mgg_sig_m0, mgg_sig_sigma, mgg_sig_alpha, mgg_sig_n);
MggSig      = AddPdf(MggGaussSig, MggCBSig, mgg_sig_frac);

mgg_sig_m0_cat0[110.0, 90, 150];
mgg_sig_sigma_cat0[1.0, 0.5, 1.5];
mgg_sig_alpha_cat0[1.0, 0.5, 5]; 
mgg_sig_n_cat0[2.0, 0.5, 10]; 
mgg_sig_gsigma_cat0[2.0, 1.3, 5];
mgg_sig_frac_cat0[0.5, 0, 1];

MggGaussSig_cat0 = Gaussian(GamGamMass, mgg_sig_m0_cat0, mgg_sig_gsigma_cat0);
MggCBSig_cat0    = CBShape(GamGamMass, mgg_sig_m0_cat0, mgg_sig_sigma_cat0, mgg_sig_alpha_cat0, mgg_sig_n_cat0);
MggSig_cat0      = AddPdf(MggGaussSig_cat0, MggCBSig_cat0, mgg_sig_frac_cat0);

mgg_sig_m0_cat1[110.0, 90, 150];
mgg_sig_sigma_cat1[1.0, 0.8, 2.5];
mgg_sig_alpha_cat1[2.0, 1.0, 3]; 
mgg_sig_n_cat1[2.0, 1.5, 10]; 
mgg_sig_gsigma_cat1[3.0, 2.5, 10];
mgg_sig_frac_cat1[0.3, 0, 0.5];

MggGaussSig_cat1 = Gaussian(GamGamMass, mgg_sig_m0_cat1, mgg_sig_gsigma_cat1);
MggCBSig_cat1    = CBShape(GamGamMass, mgg_sig_m0_cat1, mgg_sig_sigma_cat1, mgg_sig_alpha_cat1, mgg_sig_n_cat1);
MggSig_cat1      = AddPdf(MggGaussSig_cat1, MggCBSig_cat1, mgg_sig_frac_cat1);

mgg_sig_m0_cat2[110.0, 90, 150];
mgg_sig_sigma_cat2[1.0, 1.0, 3];
mgg_sig_alpha_cat2[1.0, 0.5, 5]; 
mgg_sig_n_cat2[2.0, 0.5, 10]; 
mgg_sig_gsigma_cat2[4.0, 3.0, 5.0];
mgg_sig_frac_cat2[0.2, 0, 0.5];

MggGaussSig_cat2 = Gaussian(GamGamMass, mgg_sig_m0_cat2, mgg_sig_gsigma_cat2);
MggCBSig_cat2    = CBShape(GamGamMass, mgg_sig_m0_cat2, mgg_sig_sigma_cat2, mgg_sig_alpha_cat2, mgg_sig_n_cat2);
MggSig_cat2      = AddPdf(MggGaussSig_cat2, MggCBSig_cat2, mgg_sig_frac_cat2);

mgg_sig_m0_cat3[110.0, 90, 150];
mgg_sig_sigma_cat3[2.5, 2.0, 5];
mgg_sig_alpha_cat3[1.0, 0.5, 5]; 
mgg_sig_n_cat3[2.0, 0.5, 10]; 
mgg_sig_gsigma_cat3[4.0, 3.0, 10.0];
mgg_sig_frac_cat3[0.5, 0, 1];

MggGaussSig_cat3 = Gaussian(GamGamMass, mgg_sig_m0_cat3, mgg_sig_gsigma_cat3);
MggCBSig_cat3    = CBShape(GamGamMass, mgg_sig_m0_cat3, mgg_sig_sigma_cat3, mgg_sig_alpha_cat3, mgg_sig_n_cat3);
MggSig_cat3      = AddPdf(MggGaussSig_cat3, MggCBSig_cat3, mgg_sig_frac_cat3);

mgg_bkg_slope[-0.04,-1, 1];
MggBkg = Exponential(GamGamMass, mgg_bkg_slope);

mgg_bkg_slope_cat0[-0.04,-1, 1];
MggBkg_cat0 = Exponential(GamGamMass, mgg_bkg_slope_cat0);

mgg_bkg_slope_cat1[-0.04,-1, 1];
MggBkg_cat1 = Exponential(GamGamMass, mgg_bkg_slope_cat1);


mgg_bkg_slope_cat2[-0.04,-1, 1];
MggBkg_cat2 = Exponential(GamGamMass, mgg_bkg_slope_cat2);

mgg_bkg_slope_cat3[-0.04,-1, 1];
MggBkg_cat3 = Exponential(GamGamMass, mgg_bkg_slope_cat3);

