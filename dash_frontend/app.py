from dash import Dash,html,dcc,Output,Input,State
import dash
import dash_bootstrap_components as dbc


app = Dash( __name__,use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP])


def build_header():
    def return_dropdown_items(sector_name, hyperlinkref):
        return dbc.DropdownMenuItem(sector_name, href=f'{hyperlinkref}/{sector_name}')
    
    sectors = ['Food', 'BeverageAndTobaccoProducts', 'TextileMillsAndTextileProductMills', 'WoodProducts',
               'Paper', 'PrintingAndRelatedSupportActivities', 'PetroleumAndCoalProducts', 'AllOtherChemicals',
               'PlasticsAndRubberProducts', 'NonmetallicMineralProducts', 'Foundrie',
               'FabricatedMetalProducts', 'Machinery', 'AllOtherElectronicProducts',
               'ElectricalEquipmentAppliancesAndComponents', 'FurnitureAndRelatedProducts',
               'MiscellaneousManufacturing', 'IronSteelAndFerroalloys', 'ComputerAndPeripheralEquipment',
               'BasicChemicalsResinsAndSynthetics', 'MotorVehiclesAndParts', 'NonferrousMetals',
               'CommunicationsEquipment', 'PharmaceuticalsAndMedicines', 'AerospaceProductsAndParts',
               'WholesaleTradeDurableGoods', 'WholesaleTradeNondurableGoods', 'FoodAndBeverageStores',
               'ClothingAndGeneralMerchandiseStores', 'PublishingIndustriesExceptInternet',
               'MotionPictureAndSoundRecordingIndustries: BroadcastingExceptInternet',
               'Telecommunications', 'AllOtherInformation', 'ComputerSystemsDesignAndRelatedServices',
               'ManagementAndTechnicalConsultingService', 'ScientificResearchAndDevelopmentServices',
               'AllOtherProfessionalAndTechnicalServicesExceptLegalServices', 'ApparelAndLeatherProducts',
               'AllMining', 'AllOtherRetailTrade']
    
    sector_dropdown = dbc.DropdownMenu(
        children=[return_dropdown_items(i, hyperlinkref='/sectors') for i in sectors],
        nav=True, in_navbar=True, label="Sectors")
    
    cx_health = dbc.DropdownMenu(
        children=[dbc.DropdownMenuItem('Consumer Health', href='/consumerhealth')],
        nav=True, in_navbar=True, label="Consumer Health", )
    trading_tools = dbc.DropdownMenu(
        children=[dbc.DropdownMenuItem('Option Spreads', href='/option_spreads')],
        nav=True, in_navbar=True, label="Option Spreads", )
    # here's how you can recreate the same thing using Navbar
    # (see also required callback at the end of the file)
    header = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Trading Tools", href="#"),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav([sector_dropdown, cx_health,trading_tools], className="ms-auto", navbar=True),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ), className="mb-5", )
    return header


app.layout = html.Div(id='main-parent',children=[build_header(),dash.page_container])
if __name__ == '__main__':
    app.run_server(debug=True)
