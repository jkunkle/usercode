#include  "occi.h"
#include  "oci.h"

#include <boost/foreach.hpp>

#include <vector>
#include <algorithm>
#include <iostream>

int main( void ) { 

    oracle::occi::Environment *env = oracle::occi::Environment::createEnvironment();

    std::string connection_string = "(DESCRIPTION=";
    connection_string            += "(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))";
    connection_string            += "(CONNECT_DATA=(SERVICE_NAME=cms_omds_lb.cern.ch)";
    connection_string            += "))";

    std::string user_name = "CMS_HCL_APPUSER_R";
    std::string password = "HCAL_Reader_55";

    std::cout << connection_string << std::endl;

    oracle::occi::Connection *conn = env->createConnection( user_name, password, connection_string );

    //oracle::occi::Statement *stmt = conn->createStatement("SELECT * FROM CMS_HCL_HCAL_COND.HCAL_TRIGGER_KEYS");
    oracle::occi::Statement *stmt = conn->createStatement("select table_name, column_name from all_tab_cols where owner='CMS_HCL_HCAL_COND' and column_name='RECORD_ID'");
    oracle::occi::ResultSet *rs = stmt->executeQuery();

    std::vector<std::string> matched_tables;
    while( rs->next() ) {
        std::string name = rs->getString(1);
        matched_tables.push_back(name);
    }

    std::vector<std::string> empty_tables;
    empty_tables.push_back("HCAL_CCM_TEST_RESULTS");
    empty_tables.push_back("HCAL_CHANNEL_ON_OFF_STATES");
    empty_tables.push_back("HCAL_DCS_ENV_VALUES_V2");
    empty_tables.push_back("HCAL_DCS_MONITORING_TYPE01");
    empty_tables.push_back("HCAL_DCS_MONITORING_TYPE02");
    empty_tables.push_back("HCAL_HARDWARE_LOGICAL_MAPS_V2");
    empty_tables.push_back("HCAL_LASER_CONDS");
    empty_tables.push_back("HCAL_RADDAM_HF");
    empty_tables.push_back("HCAL_RBX_CONFIGURATIONS");
    empty_tables.push_back("HCAL_RBX_CONFIGURATION_MAPS");
    empty_tables.push_back("HF_PMT_SX5_TEST_CALIB_COEFF");
    empty_tables.push_back("HO_CERN904_QIE_CHAN_CORR");
    empty_tables.push_back("HO_CERN904_SPMPK_COMBS");
    empty_tables.push_back("HO_CERN904_TEST_MAP");
    empty_tables.push_back("HO_CERNSX5_PELTIER_IVSLOPE");
    empty_tables.push_back("HO_CERNSX5_PLTV_PLTCUR");
    empty_tables.push_back("HO_CERNSX5_PLTV_TEMPDEGC");
    empty_tables.push_back("HO_CERNSX5_SPMPK_COMBS");
    empty_tables.push_back("HO_CERNSX5_STBLV_TEMPDEGC");
    empty_tables.push_back("HO_CERNSX5_TEST_MAP");
    empty_tables.push_back("HO_CERNUX5_PLTSCAN_CHRG");
    empty_tables.push_back("HO_CERNUX5_PLTSCAN_CONDS");
    empty_tables.push_back("HO_CERNUX5_PLTSCAN_PEDESTALS");
    empty_tables.push_back("HO_CERNUX5_PLTSCAN_PEDGAINSLP");
    empty_tables.push_back("HO_CERNUX5_PLTV_PLTCUR");
    empty_tables.push_back("HO_CERNUX5_PLTV_TEMPDEGC");
    empty_tables.push_back("HO_CERNUX5_SELF_TRIGGER");
    empty_tables.push_back("HO_CERNUX5_SPMPK_COMBS");
    empty_tables.push_back("HO_CERNUX5_TEST_MAP");
    empty_tables.push_back("V_HCAL_DCS_ENV_TOLERANCES_V1");
    empty_tables.push_back("V_HCAL_DCS_MONITORING_TYPE02");
    empty_tables.push_back("V_HCAL_HWR_LOGICAL_MAPS_V2");
    empty_tables.push_back("V_HCAL_RBX_CONFIGURATIONS");
    empty_tables.push_back("V_HCAL_RBX_DEL_PED_CONFIGS");
    empty_tables.push_back("V_QIECARD_ADC_NORMMODE_CHAN");
  
    BOOST_FOREACH(const std::string & table, matched_tables ) {

        if( std::find(empty_tables.begin(), empty_tables.end(), table ) != empty_tables.end() ) {
            continue;
        }

        std::string statement = "SELECT * FROM CMS_HCL_HCAL_COND." + table + " where CONDITION_DATA_SET_ID=125361080";
        //std::string statement = "SELECT * FROM CMS_HCL_HCAL_COND." + table + " WHERE ROWNUM<10";

        std::cout <<statement << std::endl;
        oracle::occi::Statement *tblstmt = conn->createStatement(statement);
        
        oracle::occi::ResultSet *tblrs = tblstmt->executeQuery();

        std::vector<oracle::occi::MetaData> md = tblrs->getColumnListMetaData();

        std::cout << "Got " << md.size() << " metadatas " << std::endl;

        int count=0;
        while( tblrs->next() ) {
            count++;
            std::cout << tblrs->getString(1) << std::endl;
        }

        if( count==0 ) {
            empty_tables.push_back( table);
        }

    }

    std::cout << "empty tables" << std::endl;
    BOOST_FOREACH( const std::string & et, empty_tables ) {
        std::cout <<  et << std::endl;
    }


}

