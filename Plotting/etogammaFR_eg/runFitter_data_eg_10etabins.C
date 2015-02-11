void runFitter_data_eg_10etabins()
{
  gROOT->LoadMacro("CMSstyle.C");
  CMSstyle();
  // gROOT->LoadMacro("ZeeFitter_eeData_nvtx.cc");
  // loop_runfits();

  TString plotdir;
  TString resdir;

  /*
  plotdir = "plots_eg_dataABCD/";
  gSystem->MakeDirectory(plotdir); 
  gSystem->MakeDirectory(plotdir+"nvtx0/"); 
  gSystem->MakeDirectory(plotdir+"nvtx1/"); 
  gSystem->MakeDirectory(plotdir+"nvtx2/"); 
 // gSystem->MakeDirectory(plotdir+"nvtx3/"); 
 
  
  resdir = "fitRes_eg_dataABCD/";  
  gSystem->MakeDirectory(resdir); 
  TFile fres("fitRes_eg_dataABCD/fitresult.root","NEW") ;
  fres.Close();
  gROOT->LoadMacro("ZeeFitter_egData_nvtx.cc");
  loop_runfits();
  //  return;
  */
  //------------------------------------------
  plotdir = "plots_eg_dataABCD_10etabins/";
  gSystem->MakeDirectory(plotdir); 
  gSystem->MakeDirectory(plotdir+"nvtx0/"); 
  gSystem->MakeDirectory(plotdir+"nvtx1/"); 
  gSystem->MakeDirectory(plotdir+"nvtx2/"); 
  //gSystem->MakeDirectory(plotdir+"nvtx3/"); 
   
  resdir = "fitRes_eg_dataABCD_10etabins/";  
  gSystem->MakeDirectory(resdir); 
  TFile fres("fitRes_eg_dataABCD_10etabins/fitresult.root","NEW") ;
  fres.Close();
  gROOT->LoadMacro("ZeeFitter_egData_nvtx_eta10.cc");
  loop_runfits();
  return;
}
